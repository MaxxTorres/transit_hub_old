import React, { useState } from 'react';
import { FaMagnifyingGlass } from "react-icons/fa6"

function SearchBar({ onSearch }) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(query); // send the query to parent or do something
  };

  return (
    <form onSubmit={handleSubmit} className="m-3 mx-8 flex items-center gap-2">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="search for a station"
        className="py-1 px-3 border border-gray-300 rounded-2xl focus:outline-none focus:ring-2 focus:ring-sky-600"
      />
      <button
        type="submit"
        className="p-2 bg-white rounded-xl hover:bg-gray-200"
      >
        <FaMagnifyingGlass />
      </button>
    </form>
  );
}

export default SearchBar;
