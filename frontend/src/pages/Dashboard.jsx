import { useState, useEffect } from 'react'
import api from '../api/client'

function Dashboard() {
  const [projects, setProjects] = useState([])
  const [incidents, setIncidents] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchData() {
      try {
        const [projectsRes, incidentsRes] = await Promise.all([
          api.get('/projects/'),
          api.get('/incidents/'),
        ])
        setProjects(projectsRes.data)
        setIncidents(incidentsRes.data)
      } catch (err) {
        console.error('Failed to fetch data:', err)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  if (loading) return <p className="p-8">Loading...</p>

  const activeProjects = projects.filter(p => p.status === 'active')
  const openIncidents = incidents.filter(i => i.status === 'open' || i.status === 'investigating')
  const criticalIncidents = incidents.filter(i => i.severity === 'critical' || i.severity === 'high')

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-8">Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-gray-800 rounded p-4">
          <p className="text-gray-400 text-sm">Total Projects</p>
          <p className="text-2xl font-bold">{projects.length}</p>
        </div>
        <div className="bg-gray-800 rounded p-4">
          <p className="text-gray-400 text-sm">Active Projects</p>
          <p className="text-2xl font-bold text-green-400">{activeProjects.length}</p>
        </div>
        <div className="bg-gray-800 rounded p-4">
          <p className="text-gray-400 text-sm">Open Incidents</p>
          <p className="text-2xl font-bold text-yellow-400">{openIncidents.length}</p>
        </div>
        <div className="bg-gray-800 rounded p-4">
          <p className="text-gray-400 text-sm">Critical/High Severity</p>
          <p className="text-2xl font-bold text-red-400">{criticalIncidents.length}</p>
        </div>
      </div>

      <h2 className="text-xl font-bold mb-4">Recent Incidents</h2>
      <div className="bg-gray-800 rounded overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-gray-700">
            <tr>
              <th className="p-3">Title</th>
              <th className="p-3">Type</th>
              <th className="p-3">Severity</th>
              <th className="p-3">Status</th>
              <th className="p-3">Date</th>
            </tr>
          </thead>
          <tbody>
            {incidents.slice(0, 5).map(incident => (
              <tr key={incident.id} className="border-t border-gray-700">
                <td className="p-3">{incident.title}</td>
                <td className="p-3">{incident.incident_type}</td>
                <td className="p-3">{incident.severity}</td>
                <td className="p-3">{incident.status}</td>
                <td className="p-3">{incident.date_occurred}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default Dashboard