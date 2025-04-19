import {Routes, Route} from 'react-router-dom'
import 'leaflet/dist/leaflet.css';
import HomePage from './pages/HomePage'
import FavoritesPage from './pages/FavoritesPage'
import StationsPage from './pages/StationsPage'
import ReportPage from './pages/ReportPage'
import "./index.css";

function App() {
  return (
    <div style = {{'margin-top': '57px'}}>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="favorites" element={<FavoritesPage />} />
        <Route path="stations" element={<StationsPage />} />
        <Route path="report" element={<ReportPage />} />
      </Routes>
    </div>
  );
}

export default App;
