import React from 'react'
import NavBar from '../components/NavBar'
import MapButtons from '../components/MapButtons'
import MapView from '../components/MapView'
import SmallCard from '../components/SmallCard'

function FavoritesPage() {
  return (
    <div className>
        <NavBar />
        {/* <MapButtons /> */}
        <div className = "absolute w-72 p-5 bg-white h-screen border-r"
          style = {{'margin-top': '-72px', 'padding-top': '72px'}}>
          <p className = "mb-5">Favorited Stations</p>
          <SmallCard />
        </div>

        <div className = "absolute w-full h-40 left-72 bottom-0 bg-slate-100 border-l">
          <p>Times Square Station</p>
        </div>

        {/* <MapView /> */}
    </div>
  )
}

export default FavoritesPage