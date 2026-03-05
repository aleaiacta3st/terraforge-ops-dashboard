import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Incidents from './pages/Incidents'

function App() {
  return (
    <BrowserRouter>
      <div className="bg-gray-900 text-white min-h-screen">
        <nav className="bg-gray-800 p-4">
          <div className="flex items-center gap-6">
            <img src="/logo.svg" alt="Terraforge" className="h-10" />
            <Link to="/" className="hover:text-blue-400">Dashboard</Link>
            <Link to="/incidents" className="hover:text-blue-400">Incidents</Link>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/incidents" element={<Incidents />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App