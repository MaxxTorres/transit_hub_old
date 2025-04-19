import React, {useState} from 'react'
import NavBar from '../components/NavBar'
import MapButtons from '../components/MapButtons'
import { MapWithHeader } from '../components/MapView'
import MapView from '../components/MapView'
import SmallCard from '../components/SmallCard'
import LongCard from '../components/LongCard'


function HomePage() {
  const [showFavorites, setShowFavorites] = useState(false)
  const [showDetails, setShowDetails] = useState(false)

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
      <div className = {`z-[3000] absolute w-72 p-5 bg-white h-screen border-r-2"
        transform transition-transform duration-300
        ${showFavorites ? 'translate-x-0' : '-translate-x-full'}`}
        style = {{'margin-top': '-58px', 'padding-top': '80px'}}>
        <p className = "mb-3">Liked Stations</p>
        <SmallCard />
      </div>

      {/* Favorites More Details Bottom Bar */}
      <div className = {`z-[4000] rounded-t-3xl absolute w-full h-40 left-0 bottom-0 bg-slate-100 border-t-2
        transform transition-transform duration-300 border-t
        ${showDetails ? 'translate-x-0' : 'translate-y-full'}`}>
        <p className = "m-5 ml-10">Times Square Station</p>
      </div>

      {/* Map with Buttons */}
      <div className="z-[2000] relative h-screen w-full">
        <div className={`absolute top-0 left-20 z-[1000] transform transition-transform duration-300
          ${showFavorites ? 'translate-x-52' : ''}`}>
          <MapButtons toggleDetails={toggleDetails}/>
        </div>
        
        <MapView />
      </div>
    </div>
  )
}

export default HomePage