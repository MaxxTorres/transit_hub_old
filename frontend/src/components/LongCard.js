import React from 'react'
import { FaTriangleExclamation } from "react-icons/fa6";

export default function LongCard() {
  return (
    <div className = "flex p-2 h-36 shadow-lg w-full border-2 border-mainOrange rounded-lg">
        <div className = "w-3/5">
            <p>Times Sq</p>
            <p> <span className = "text-4xl">10</span> min</p>
        </div>
        <div className = "w-2/5 border-l border-black p-1 pl-2">
            <div className = "text-2xl">
                <FaTriangleExclamation />
            </div>
        </div>
    </div>
  )
}
