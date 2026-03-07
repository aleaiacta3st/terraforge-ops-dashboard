import { useState } from 'react'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import api from './api/client'
import Dashboard from './pages/Dashboard'
import Incidents from './pages/Incidents'
import Projects from './pages/Projects'
import Employees from './pages/Employees'
import Equipment from './pages/Equipment'

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'))
  const [username, setUsername] = useState(localStorage.getItem('username') || '')
  const [loginError, setLoginError] = useState('')

  async function handleLogin(e) {
    e.preventDefault()
    const form = e.target
    const usernameVal = form.username.value
    const password = form.password.value

    try {
      const res = await api.post('/auth/login', new URLSearchParams({ username: usernameVal, password }))
      localStorage.setItem('token', res.data.access_token)
      localStorage.setItem('username', usernameVal)
      setToken(res.data.access_token)
      setUsername(usernameVal)
      setLoginError('')
    } catch {
      setLoginError('Invalid credentials')
    }
  }

  function handleLogout() {
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    setToken(null)
    setUsername('')
  }

  return (
    <BrowserRouter>
      <div className="bg-gray-900 text-white min-h-screen">
        <nav className="bg-gray-800 p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-6">
              <img src="/logo.svg" alt="Terraforge" className="h-10" />
              <Link to="/" className="hover:text-blue-400">Dashboard</Link>
              <Link to="/incidents" className="hover:text-blue-400">Incidents</Link>
              <Link to="/projects" className="hover:text-blue-400">Projects</Link>
              <Link to="/employees" className="hover:text-blue-400">Employees</Link>
              <Link to="/equipment" className="hover:text-blue-400">Equipment</Link>
            </div>

            <div>
              {token ? (
                <div className="flex items-center gap-4">
                  <span className="text-gray-400 text-sm">{username}</span>
                  <button
                    onClick={handleLogout}
                    className="bg-gray-700 hover:bg-gray-600 px-3 py-1 rounded text-sm"
                  >
                    Log Out
                  </button>
                </div>
              ) : (
                <form onSubmit={handleLogin} className="flex items-center gap-2">
                  <input
                    name="username"
                    placeholder="Username"
                    className="bg-gray-700 px-2 py-1 rounded text-sm w-28"
                  />
                  <input
                    name="password"
                    type="password"
                    placeholder="Password"
                    className="bg-gray-700 px-2 py-1 rounded text-sm w-28"
                  />
                  <button
                    type="submit"
                    className="bg-blue-600 hover:bg-blue-500 px-3 py-1 rounded text-sm"
                  >
                    Log In
                  </button>
                  {loginError && <span className="text-red-400 text-sm">{loginError}</span>}
                </form>
              )}
            </div>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/incidents" element={<Incidents />} />
          <Route path="/projects" element={<Projects />} />
          <Route path="/employees" element={<Employees />} />
          <Route path="/equipment" element={<Equipment />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App