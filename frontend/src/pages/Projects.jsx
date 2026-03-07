import { useState, useEffect } from 'react'
import api from '../api/client'

function Projects() {
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchProjects() {
      try {
        const res = await api.get('/projects/')
        setProjects(res.data)
      } catch (err) {
        console.error('Failed to fetch projects:', err)
      } finally {
        setLoading(false)
      }
    }
    fetchProjects()
  }, [])

  if (loading) return <p className="p-8">Loading...</p>

  const statusColor = {
    active: 'text-green-400',
    planning: 'text-blue-400',
    delayed: 'text-orange-400',
    on_hold: 'text-red-400',
    completed: 'text-gray-400',
  }

  function formatBudget(value) {
    const num = Number(value)
    if (num >= 10000000) return `₹${(num / 10000000).toFixed(1)} Cr`
    if (num >= 100000) return `₹${(num / 100000).toFixed(1)} L`
    return `₹${num.toLocaleString()}`
  }

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-8">Projects</h1>

      <div className="bg-gray-800 rounded overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-gray-700">
            <tr>
              <th className="p-3">Project</th>
              <th className="p-3">Client</th>
              <th className="p-3">Location</th>
              <th className="p-3">Type</th>
              <th className="p-3">Status</th>
              <th className="p-3">Budget</th>
            </tr>
          </thead>
          <tbody>
            {projects.map(project => {
              const spent = Number(project.spent)
              const budget = Number(project.budget)
              const percent = budget > 0 ? (spent / budget) * 100 : 0
              const overBudget = percent > 100

              return (
                <tr key={project.id} className="border-t border-gray-700">
                  <td className="p-3">
                    <p className="font-bold">{project.name}</p>
                    <p className="text-gray-400 text-sm">{project.project_code}</p>
                  </td>
                  <td className="p-3">{project.client_name}</td>
                  <td className="p-3">{project.site_location}</td>
                  <td className="p-3">{project.project_type}</td>
                  <td className={`p-3 ${statusColor[project.status]}`}>{project.status}</td>
                  <td className="p-3 w-48">
                    <div className="flex justify-between text-sm mb-1">
                      <span>{formatBudget(spent)}</span>
                      <span className="text-gray-400">{formatBudget(budget)}</span>
                    </div>
                    <div className="bg-gray-600 rounded h-2 overflow-hidden">
                      <div
                        className={`h-2 rounded ${overBudget ? 'bg-red-400' : 'bg-green-400'}`}
                        style={{ width: `${Math.min(percent, 100)}%` }}
                      />
                    </div>
                    {overBudget && (
                      <p className="text-red-400 text-sm mt-1">{Math.round(percent - 100)}% over budget</p>
                    )}
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default Projects