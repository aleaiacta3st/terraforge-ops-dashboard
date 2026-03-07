import { useState, useEffect } from 'react'
import api from '../api/client'

function Employees() {
  const [employees, setEmployees] = useState([])
  const [loading, setLoading] = useState(true)
  const [roleFilter, setRoleFilter] = useState('all')

  useEffect(() => {
    async function fetchEmployees() {
      try {
        const res = await api.get('/employees/')
        setEmployees(res.data)
      } catch (err) {
        console.error('Failed to fetch employees:', err)
      } finally {
        setLoading(false)
      }
    }
    fetchEmployees()
  }, [])

  if (loading) return <p className="p-8">Loading...</p>

  const roles = [...new Set(employees.map(e => e.role))].sort()
  const filtered = roleFilter === 'all' ? employees : employees.filter(e => e.role === roleFilter)

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-8">Employees</h1>

      <div className="flex items-center gap-4 mb-6">
        <label className="text-gray-400 text-sm">Filter by role:</label>
        <select
          value={roleFilter}
          onChange={e => setRoleFilter(e.target.value)}
          className="bg-gray-700 text-white px-3 py-2 rounded text-sm"
        >
          <option value="all">All Roles ({employees.length})</option>
          {roles.map(role => (
            <option key={role} value={role}>
              {role.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())} ({employees.filter(e => e.role === role).length})
            </option>
          ))}
        </select>
        <span className="text-gray-400 text-sm">Showing {filtered.length} employee{filtered.length !== 1 ? 's' : ''}</span>
      </div>

      <div className="bg-gray-800 rounded overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-gray-700">
            <tr>
              <th className="p-3">Code</th>
              <th className="p-3">Name</th>
              <th className="p-3">Role</th>
              <th className="p-3">Email</th>
              <th className="p-3">Phone</th>
              <th className="p-3">Hire Date</th>
              <th className="p-3">Status</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map(emp => (
              <tr key={emp.id} className="border-t border-gray-700">
                <td className="p-3 text-gray-400 text-sm">{emp.employee_code}</td>
                <td className="p-3 font-bold">{emp.full_name}</td>
                <td className="p-3">{emp.role.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}</td>
                <td className="p-3 text-sm">{emp.email}</td>
                <td className="p-3 text-sm">{emp.phone}</td>
                <td className="p-3 text-sm">{emp.hire_date}</td>
                <td className="p-3">
                  <span className={emp.is_active ? 'text-green-400' : 'text-red-400'}>
                    {emp.is_active ? 'Active' : 'Inactive'}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default Employees