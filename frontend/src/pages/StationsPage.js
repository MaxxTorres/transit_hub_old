import React from 'react'
import NavBar from '../components/NavBar'
import LongCard from '../components/LongCard'
import Dropdown from '../components/Dropdown'
import {NavLink} from 'react-router-dom'

function StationsPage() {
  const sampleStations = ["Times Square", "Jay St", "8th St NYU"]

  const renderedStations = sampleStations.map((station) => {
    return(
      <NavLink
        to = "/"
        state = {{showDetails: true, selectedStation: {station}}}>
        <LongCard label={station} />
      </NavLink>
    )
  })

  return (
    <div>
        <NavBar />

        <div className = "m-10 mt-20 flex gap-2 items-center">
          <div>Filter by</div>
          <Dropdown label = "Line" />
          <Dropdown label = "Location" />
          <Dropdown label = "Status" />
        </div>

        <div className = "flex flex-col gap-5 w-auto m-10">
          {renderedStations}
        </div>
    </div>
  )
}

export default StationsPage