import {Routes, Route} from 'react-router-dom'
import HomePage from './pages/HomePage'
import StationsPage from './pages/StationsPage'
import ReportPage from './pages/ReportPage'
import "./index.css";

function App() {
  return (
    <div style = {{'margin-top': '56px'}}>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="stations" element={<StationsPage />} />
        <Route path="report" element={<ReportPage />} />
      </Routes>
    </div>
  );
}

export default App;
