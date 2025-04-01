import firebase_admin
from firebase_admin import credentials, firestore
import requests
import csv
import time
from google.transit import gtfs_realtime_pb2
import os
import json

# --- GTFS Feed URLs ---
MTA_FEEDS = {
    '123': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs',
    'ACE': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace',
    'NQRW': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw',
    'BDFM': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm',
    'G': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-g',
    'JZ': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-jz',
    'L': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l',
    'SI': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-si'
}

# MTA API endpoints
TRIP_UPDATE_URL = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs'

# File paths
STOPS_FILE = "stops.txt"
ROUTES_FILE = "routes.txt"

# --- Helper Functions ---
def get_borough_from_stop_id(stop_id):
    """Infer borough from stop_id based on MTA conventions"""
    if stop_id.startswith(('1', '2', '3', '4', '5', '6', 'A', 'B', 'C', 'D')):
        if int(stop_id[1:]) < 200:
            return "Manhattan"
        elif int(stop_id[1:]) < 400:
            return "Bronx"
        else:
            return "Brooklyn"
    elif stop_id.startswith('N'):
        return "Queens"
    elif stop_id.startswith('S'):
        return "Staten Island"
    elif stop_id.startswith('G'):
        return "Brooklyn"
    else:
        # Default case - try to determine from station name or coordinates
        return "Unknown"

# --- Firebase Init ---
def initialize_firebase():
    cred = credentials.Certificate("./firebase-credentials.json")
    firebase_admin.initialize_app(cred)
    return firestore.client()

# --- Load Stations from GTFS CSV ---
def fetch_stations_from_csv(filepath=STOPS_FILE):
    stations = {}
    try:
        with open(filepath, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Only process parent stations (not individual entrances)
                if row.get("location_type") == "1":
                    stop_id = row["stop_id"]
                    stop_name = row["stop_name"]
                    
                    # Extract latitude and longitude
                    lat = float(row.get("stop_lat", 0))
                    lon = float(row.get("stop_lon", 0))
                    
                    # Determine accessibility - in stops.txt this might be in parent_station
                    # For simplicity, we'll check related entries later
                    
                    # Create a unique station ID for the Firebase database
                    station_id = f"{stop_name}_{stop_id}".lower().replace(" ", "_").replace("-", "_").replace("/", "_")
                    
                    # Try to determine borough
                    borough = get_borough_from_stop_id(stop_id)
                    
                    stations[station_id] = {
                        "station_code": stop_id,
                        "station_name": stop_name,
                        "station_type": "subway",
                        "is_accessible": False,  # Default value, will update later
                        "borough": borough,
                        "location": {
                            "latitude": lat,
                            "longitude": lon
                        }
                    }
        
        # Second pass to determine accessibility
        with open(filepath, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("parent_station"):
                    parent_id = row.get("parent_station")
                    # Find the station with this parent in our stations dict
                    for station_id, station_data in stations.items():
                        if station_data["station_code"] == parent_id:
                            # If any entrance is accessible, mark the station as accessible
                            if row.get("wheelchair_boarding") == "1":
                                stations[station_id]["is_accessible"] = True
        
        return stations
    except Exception as e:
        print(f"Failed to load station CSV: {e}")
        return {}

# --- Load Routes from GTFS CSV ---
def fetch_routes_from_csv(filepath=ROUTES_FILE):
    routes = {}
    try:
        with open(filepath, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                route_id = row["route_id"]
                route_name = row["route_short_name"]
                route_desc = row.get("route_desc", "")
                route_color = row.get("route_color", "")
                
                routes[route_id] = {
                    "route_id": route_id,
                    "route_name": route_name,
                    "route_description": route_desc,
                    "route_color": f"#{route_color}" if route_color else "#000000",
                    "active": True,
                    "created_at": firestore.SERVER_TIMESTAMP
                }
        return routes
    except Exception as e:
        print(f"Failed to load routes CSV: {e}")
        return {}

# --- GTFS Alerts ---
def fetch_gtfs_alerts(api_key=None):
    headers = {"x-api-key": api_key} if api_key else {}
    all_alerts = []

    for feed_name, feed_url in MTA_FEEDS.items():
        try:
            print(f"Fetching {feed_name} alerts...")
            response = requests.get(feed_url, headers=headers)
            if response.status_code != 200:
                print(f"Failed to fetch alerts for {feed_name}: Status {response.status_code}")
                continue

            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(response.content)

            for entity in feed.entity:
                if entity.HasField('alert'):
                    alert = entity.alert
                    alert_type = "Service Change"
                    alert_header = ""
                    alert_description = ""
                    
                    if alert.header_text.translation:
                        alert_header = alert.header_text.translation[0].text
                        alert_type = alert_header.split(':')[0] if ':' in alert_header else alert_header
                    
                    if alert.description_text.translation:
                        alert_description = alert.description_text.translation[0].text
                    
                    affected_routes = []
                    for informed_entity in alert.informed_entity:
                        if informed_entity.HasField('route_id') and informed_entity.route_id:
                            affected_routes.append(informed_entity.route_id)
                    
                    affected_stops = set()
                    for informed_entity in alert.informed_entity:
                        if informed_entity.HasField('stop_id'):
                            affected_stops.add(informed_entity.stop_id)

                    if not affected_stops:
                        # System-wide alert
                        all_alerts.append({
                            'station_id': 'system_wide',
                            'alert_type': alert_type,
                            'alert_header': alert_header,
                            'alert_description': alert_description,
                            'affected_routes': affected_routes,
                            'active': True,
                            'created_at': firestore.SERVER_TIMESTAMP
                        })
                    else:
                        # Station-specific alerts
                        for stop_id in affected_stops:
                            station_id = f"stop_{stop_id}"
                            all_alerts.append({
                                'station_id': station_id,
                                'alert_type': alert_type,
                                'alert_header': alert_header, 
                                'alert_description': alert_description,
                                'affected_routes': affected_routes,
                                'active': True,
                                'created_at': firestore.SERVER_TIMESTAMP
                            })
        except Exception as e:
            print(f"Error fetching alerts for {feed_name}: {e}")
            continue

    if not all_alerts:
        print("Fallback: using sample alerts.")
        all_alerts = [
            {
                'station_id': 'times_square_127',
                'alert_type': 'Delays',
                'alert_header': 'Delays on 1,2,3 lines',
                'alert_description': 'Expect delays due to signal problems.',
                'affected_routes': ['1', '2', '3'],
                'active': True,
                'created_at': firestore.SERVER_TIMESTAMP
            }
        ]
    return all_alerts

# --- GTFS Trip Updates: Real-time Arrivals ---
def fetch_realtime_arrivals(api_key=None, stop_id_filter=None):
    print("Fetching real-time arrivals...")
    headers = {"x-api-key": api_key} if api_key else {}
    
    arrivals = []
    try:
        response = requests.get(TRIP_UPDATE_URL, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch trip updates: Status {response.status_code}")
            return arrivals
        
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)

        for entity in feed.entity:
            if not entity.HasField('trip_update'):
                continue
            
            route = entity.trip_update.trip.route_id
            trip_id = entity.trip_update.trip.trip_id
            direction = entity.trip_update.trip.direction_id if entity.trip_update.trip.HasField('direction_id') else None
            
            for stu in entity.trip_update.stop_time_update:
                stop_id = stu.stop_id
                
                if stop_id_filter and stop_id != stop_id_filter:
                    continue
                
                if stu.HasField('arrival'):
                    arrival_time = stu.arrival.time
                    arrival_data = {
                        'route': route,
                        'trip_id': trip_id,
                        'stop_id': stop_id,
                        'direction': "Northbound" if direction == 0 else "Southbound" if direction == 1 else "Unknown",
                        'arrival_time': time.strftime('%H:%M:%S', time.localtime(arrival_time)),
                        'timestamp': arrival_time,
                        'updated_at': firestore.SERVER_TIMESTAMP
                    }
                    arrivals.append(arrival_data)

        # Sort by timestamp
        arrivals.sort(key=lambda x: x['timestamp'])
        return arrivals
        
    except Exception as e:
        print(f"Error fetching real-time arrivals: {e}")
        return []

# --- Store Next Arrivals ---
def store_arrivals(db, arrivals):
    print(f"Storing {len(arrivals)} arrivals...")
    batch = db.batch()
    count = 0
    
    # Group arrivals by stop_id
    arrivals_by_stop = {}
    for arrival in arrivals:
        stop_id = arrival['stop_id']
        if stop_id not in arrivals_by_stop:
            arrivals_by_stop[stop_id] = []
        arrivals_by_stop[stop_id].append(arrival)
    
    # For each stop, store the next few arrivals by route
    for stop_id, stop_arrivals in arrivals_by_stop.items():
        # Group by route
        arrivals_by_route = {}
        for arrival in stop_arrivals:
            route = arrival['route']
            if route not in arrivals_by_route:
                arrivals_by_route[route] = []
            arrivals_by_route[route].append(arrival)
        
        # Store the next few arrivals for each route
        for route, route_arrivals in arrivals_by_route.items():
            # Sort by timestamp
            route_arrivals.sort(key=lambda x: x['timestamp'])
            
            # Only keep the next few arrivals per route
            for i, arrival in enumerate(route_arrivals[:3]):
                doc_id = f"{stop_id}_{route}_{i}"
                batch.set(db.collection('next_arrivals').document(doc_id), arrival)
                count += 1
                
                # Firebase limits batches to 500 operations
                if count >= 450:
                    batch.commit()
                    batch = db.batch()
                    count = 0
    
    # Commit any remaining operations
    if count > 0:
        batch.commit()

# --- Integrate with Station Routes ---
def match_stations_with_routes(stations, routes, arrivals):
    """Match stations with the routes that serve them based on real-time arrivals"""
    station_routes = {}
    
    for arrival in arrivals:
        stop_id = arrival['stop_id']
        route_id = arrival['route']
        
        # Find the station in our stations dict
        for station_id, station_data in stations.items():
            if station_data["station_code"] == stop_id:
                if station_id not in station_routes:
                    station_routes[station_id] = set()
                
                # Add the route to this station
                station_routes[station_id].add(route_id)
    
    # Update stations with their routes
    for station_id, route_set in station_routes.items():
        if station_id in stations:
            stations[station_id]["routes"] = list(route_set)
    
    return stations

# --- Upload to Firestore ---
def update_firebase(db, stations, routes, alerts, arrivals):
    batch = db.batch()
    count = 0
    
    print("Uploading stations...")
    for station_id, station_data in stations.items():
        batch.set(db.collection('stations').document(station_id), station_data)
        count += 1
        
        if count >= 450:
            batch.commit()
            batch = db.batch()
            count = 0
    
    print("Uploading routes...")
    for route_id, route_data in routes.items():
        batch.set(db.collection('routes').document(route_id), route_data)
        count += 1
        
        if count >= 450:
            batch.commit()
            batch = db.batch()
            count = 0
    
    print("Resetting existing alerts...")
    existing_alerts = db.collection('alerts').where('active', '==', True).stream()
    for alert in existing_alerts:
        batch.update(db.collection('alerts').document(alert.id), {'active': False})
        count += 1
        
        if count >= 450:
            batch.commit()
            batch = db.batch()
            count = 0
    
    print("Adding new alerts...")
    for alert in alerts:
        alert_ref = db.collection('alerts').document()
        batch.set(alert_ref, alert)
        count += 1
        
        if count >= 450:
            batch.commit()
            batch = db.batch()
            count = 0
    
    # Commit remaining operations
    if count > 0:
        batch.commit()
    
    # Handle arrivals separately since they need special processing
    print("Adding arrivals...")
    store_arrivals(db, arrivals)

    # No sample user data - will be created when users interact with the website
    print("Schema for users, favorites, and reports is ready but no data will be created")

# --- MAIN ---
def main():
    # API key for MTA data (optional)
    api_key = os.environ.get('MTA_API_KEY', None)
    
    # Initialize Firebase
    db = initialize_firebase()
    
    # Load static data from CSV files
    stations = fetch_stations_from_csv(STOPS_FILE)
    print(f"Loaded {len(stations)} stations.")
    
    routes = fetch_routes_from_csv(ROUTES_FILE)
    print(f"Loaded {len(routes)} routes.")
    
    # Fetch real-time data from MTA API
    alerts = fetch_gtfs_alerts(api_key)
    print(f"Loaded {len(alerts)} alerts.")
    
    arrivals = fetch_realtime_arrivals(api_key)
    print(f"Loaded {len(arrivals)} arrivals.")
    
    # Match stations with routes based on arrivals
    stations = match_stations_with_routes(stations, routes, arrivals)
    
    # Upload everything to Firebase
    update_firebase(db, stations, routes, alerts, arrivals)
    print("✅ Done.")

if __name__ == "__main__":
    main()