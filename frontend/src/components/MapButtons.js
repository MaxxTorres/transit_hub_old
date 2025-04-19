import React from 'react'
import { FaHeart } from 'react-icons/fa6'
import { FaPenToSquare } from 'react-icons/fa6'

export default function MapButtons(props) {
  const {label, toggleDetails} = props



  return (
    <div className = "flex items-center gap-2 h-12 m-5">
      <div className = "bg-white w-auto rounded-md shadow-lg border border-mainOrange p-2 px-5 text-center">
        {label}
      </div>
      <button className = "map-button"
        onClick = {toggleDetails}>
          <div className = "text-sm"> Details </div>
      </button>
      <button className = "map-button">
          <div className = "text-red-500 text-lg"> <FaHeart /> </div>
      </button>
      <button className = "map-button">
          <div className = "text-orange-500 text-lg"> <FaPenToSquare /> </div>
      </button>
    </div>
  )
}
