import React, { useState, useRef, useEffect } from 'react';
import {FaCaretDown} from 'react-icons/fa6'

export default function Dropdown({ label = "Select", items = [], onSelect }) {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(e) {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div ref={dropdownRef} className="relative inline-block text-left">
      <button
        onClick={() => setIsOpen(prev => !prev)}
        className="flex items-center gap-2 bg-white border border-gray-300 rounded-sm px-4 py-2 shadow hover:bg-gray-50 focus:outline-none"
      >
        {label}
        <FaCaretDown />
      </button>

      {isOpen && (
        <ul className="absolute z-50 mt-2 w-full bg-white border border-gray-200 rounded shadow-lg">
          {items.map((item, index) => (
            <li
              key={index}
              className="px-4 py-2 hover:bg-gray-100 cursor-pointer"
              onClick={() => {
                onSelect(item);
                setIsOpen(false);
              }}
            >
              {item.label || item}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
