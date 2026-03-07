import { useState, useEffect } from 'react'
import api from '../api/client'

function Equipment() {
  const [equipment, setEquipment] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchEquipment() {
      try {
        const res = await api.get('/equipment/')
        setEquipment(res.data)
      } catch (err) {
        console.error('Failed to fetch equipment:', err)
      } finally {
        setLoading(false)
      }
    }
    fetchEquipment()
  }, [])

  if (loading) return <p className="p-8">Loading...</p>

  const statusBadge = {
    operational: 'bg-green-400/20 text-green-400',
    maintenance: 'bg-yellow-400/20 text-yellow-400',
    broken: 'bg-red-400/20 text-red-400',
    decommissioned: 'bg-gray-400/20 text-gray-400',
  }

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-8">Equipment</h1>

      <div className="bg-gray-800 rounded overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-gray-700">
            <tr>
              <th className="p-3">Name</th>
              <th className="p-3">Type</th>
              <th className="p-3">Serial Number</th>
              <th className="p-3">Status</th>
              <th className="p-3">Last Maintenance</th>
              <th className="p-3">Next Due</th>
            </tr>
          </thead>
          <tbody>
            {equipment.map(item => (
              <tr key={item.id} className="border-t border-gray-700">
                <td className="p-3 font-bold">{item.name}</td>
                <td className="p-3">{item.equipment_type.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}</td>
                <td className="p-3 text-gray-400 text-sm">{item.serial_number}</td>
                <td className="p-3">
                  <span className={`px-2 py-1 rounded text-sm ${statusBadge[item.status]}`}>
                    {item.status.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}
                  </span>
                </td>
                <td className="p-3 text-sm">{item.last_maintenance_date || '—'}</td>
                <td className="p-3 text-sm">{item.next_maintenance_due || '—'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default Equipment