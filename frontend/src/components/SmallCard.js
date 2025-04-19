import React from 'react'
import { FaTriangleExclamation } from "react-icons/fa6";

export default function SmallCard(props) {
  const {label} = props

  return (
    <div className = "flex hover:scale-105 transition bg-white p-2 h-36 shadow-lg w-full border-2 border-mainOrange rounded-lg">
        <div className = "w-3/5">
            <p className = "font-semibold">{label}</p>
            <p> <span className = "text-4xl">10</span> min</p>
            <p></p>
        </div>
        <div className = "w-2/5 border-l border-black p-1 pl-2">
            <div className = "text-2xl">
                <FaTriangleExclamation />
            </div>
        </div>
    </div>
  )
}
