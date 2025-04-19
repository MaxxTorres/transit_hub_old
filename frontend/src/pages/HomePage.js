import React, {useState, useEffect} from 'react'
import NavBar from '../components/NavBar'
import MapButtons from '../components/MapButtons'
import { MapWithHeader } from '../components/MapView'
import MapView from '../components/MapView'
import SmallCard from '../components/SmallCard'
import LongCard from '../components/LongCard'
import { useLocation } from 'react-router-dom';


function HomePage() {
  const [showFavorites, setShowFavorites] = useState(false)
  const [showDetails, setShowDetails] = useState(false)
  
  const allStationsSelect = useLocation();
  const {selectedStation = {station: "Times Square"}} = allStationsSelect.state || {}
  
  const [focusedStation, setFocusedStation] = useState(selectedStation.station)
  const sampleFavorites = ["Times Square", "Jay St", "8th St NYU"]
  
  useEffect(() => {
    if (allStationsSelect.state?.showDetails) {
      setShowDetails(true);
    }
  }, [allStationsSelect.state]);
  
  const renderedFavorites = sampleFavorites.map((station) => {
    return(<SmallCard label={station} />)
  })
  
  const toggleFavorites = () => {
    setShowFavorites(!showFavorites)
  }

  const toggleDetails = () => {
    setShowDetails(!showDetails)
  }

  return (
    <div>
      <NavBar />

      <button className = "z-[3000] absolute right-5 top-20 !h-16 map-button"
        onClick = {toggleFavorites}>
        Show Favorites
      </button>
      
      {/* Favorites Side Bar */}
      <div className = {`z-[3000] flex flex-col gap-5 absolute w-72 p-5 bg-white h-screen border-r-2"
        transform transition-transform duration-300
        ${showFavorites ? 'translate-x-0' : '-translate-x-full'}`}
        style = {{'padding-top': '20px'}}>
        <p>Liked Stations</p>
        {renderedFavorites}
      </div>

      {/* Favorites More Details Bottom Bar */}
      <div className = {`z-[4000] shadow-inner rounded-t-3xl fixed w-full h-40 left-0 bottom-0 bg-slate-100 border-t-2
        transform transition-transform duration-300 border-t
        ${showDetails ? 'translate-y-0' : 'translate-y-full'}`}>
        <p className = "m-5 ml-10">{focusedStation}</p>
      </div>

      {/* Map with Buttons */}
      <div className="z-[2000] relative h-screen w-full">
        <div className={`absolute top-0 left-20 z-[1000] transform transition-transform duration-300
          ${showFavorites ? 'translate-x-52' : ''}`}>
          <MapButtons label={focusedStation} toggleDetails={toggleDetails}/>
        </div>
        
        <MapView />
      </div>
    </div>
  )
}

export default HomePage