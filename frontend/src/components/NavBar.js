import React from 'react'
import SearchBar from './SearchBar'
import {NavLink} from 'react-router-dom'
import Logo from '../assets/transit_hub_logo.png'

export default function NavBar() {
  const handleSearch = (query) => {
      console.log('User searched:', query);
  }

  return (
  <div className = "z-[5000] fixed flex items-center bg-mainOrange w-full top-0 drop-shadow-lg">
    <div className = "ml-5 h-11 w-32 bg-contain bg-center bg-no-repeat" style = {{backgroundImage: `url(${Logo})` }}></div>

    <SearchBar onSearch={handleSearch} />

    <div className = "flex items-center w-full">
      <NavLink 
        to = "/"
        className={({ isActive }) =>
            `nav-button ${isActive ? "underline" : " "}`}>
          Home
      </NavLink>

      <NavLink 
        to = "/stations"
        className={({ isActive }) =>
            `nav-button ${isActive ? "underline" : " "}`}>
          All Stations
      </NavLink>

      <NavLink 
        to = "/report"
        className={({ isActive }) =>
            `nav-button ${isActive ? "underline" : " "}`}>
          Make Report
      </NavLink>
    </div>
  </div>
  )
}
