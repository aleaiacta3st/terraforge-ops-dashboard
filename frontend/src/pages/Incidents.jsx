import { useState, useEffect } from 'react'
import api from '../api/client'

function Incidents() {
  const [incidents, setIncidents] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedIncident, setSelectedIncident] = useState(null)
  const [analysis, setAnalysis] = useState(null)
  const [analysisLoading, setAnalysisLoading] = useState(false)
  const [similar, setSimilar] = useState([])
  const [similarLoading, setSimilarLoading] = useState(false)
  const [token, setToken] = useState(localStorage.getItem('token'))
  const [loginError, setLoginError] = useState('')

  useEffect(() => {
    async function fetchIncidents() {
      try {
        const res = await api.get('/incidents/')
        setIncidents(res.data)
      } catch (err) {
        console.error('Failed to fetch incidents:', err)
      } finally {
        setLoading(false)
      }
    }
    fetchIncidents()
  }, [])

  async function handleLogin(e) {
    e.preventDefault()
    const form = e.target
    const username = form.username.value
    const password = form.password.value

    try {
      const res = await api.post('/auth/login', new URLSearchParams({ username, password }))
      localStorage.setItem('token', res.data.access_token)
      setToken(res.data.access_token)
      setLoginError('')
    } catch {
      setLoginError('Invalid username or password')
    }
  }

  async function triggerAnalysis(incidentId) {
    setAnalysisLoading(true)
    setAnalysis(null)
    try {
      await api.post(`/incidents/${incidentId}/analyse`)
      let attempts = 0
      while (attempts < 10) {
        await new Promise(r => setTimeout(r, 2000))
        try {
          const res = await api.get(`/incidents/${incidentId}/analyse`)
          setAnalysis(res.data)
          break
        } catch {
          attempts++
        }
      }
    } catch (err) {
      console.error('Analysis failed:', err)
    } finally {
      setAnalysisLoading(false)
    }
  }

  async function fetchAnalysis(incidentId) {
    setAnalysisLoading(true)
    setAnalysis(null)
    try {
      const res = await api.get(`/incidents/${incidentId}/analyse`)
      setAnalysis(res.data)
    } catch {
      setAnalysis(null)
    } finally {
      setAnalysisLoading(false)
    }
  }

  async function fetchSimilar(incidentId) {
    setSimilarLoading(true)
    setSimilar([])
    try {
      const res = await api.get(`/incidents/${incidentId}/similar`)
      setSimilar(res.data)
    } catch {
      setSimilar([])
    } finally {
      setSimilarLoading(false)
    }
  }

  function selectIncident(incident) {
    setSelectedIncident(incident)
    setAnalysis(null)
    setSimilar([])
    fetchAnalysis(incident.id)
    fetchSimilar(incident.id)
  }

  if (loading) return <p className="p-8">Loading...</p>

  const severityColor = {
    low: 'text-green-400',
    medium: 'text-yellow-400',
    high: 'text-orange-400',
    critical: 'text-red-400',
  }

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-8">Safety Incidents</h1>

      {!token && (
        <div className="bg-gray-800 rounded p-4 mb-8 max-w-md">
          <p className="mb-3 text-yellow-400">Log in to trigger AI analysis</p>
          <form onSubmit={handleLogin} className="flex flex-col gap-3">
            <input name="username" placeholder="Username" className="bg-gray-700 p-2 rounded" />
            <input name="password" type="password" placeholder="Password" className="bg-gray-700 p-2 rounded" />
            <button type="submit" className="bg-blue-600 hover:bg-blue-500 p-2 rounded">Log In</button>
            {loginError && <p className="text-red-400 text-sm">{loginError}</p>}
          </form>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
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
                {incidents.map(incident => (
                  <tr
                    key={incident.id}
                    onClick={() => selectIncident(incident)}
                    className={`border-t border-gray-700 cursor-pointer hover:bg-gray-700 ${selectedIncident?.id === incident.id ? 'bg-gray-600' : ''}`}
                  >
                    <td className="p-3">{incident.title}</td>
                    <td className="p-3">{incident.incident_type}</td>
                    <td className={`p-3 ${severityColor[incident.severity]}`}>{incident.severity}</td>
                    <td className="p-3">{incident.status}</td>
                    <td className="p-3">{incident.date_occurred}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div>
          {selectedIncident ? (
            <div className="bg-gray-800 rounded p-4">
              <h2 className="text-xl font-bold mb-4">{selectedIncident.title}</h2>
              <div className="space-y-2 text-sm mb-6">
                <p><span className="text-gray-400">Type:</span> {selectedIncident.incident_type}</p>
                <p><span className="text-gray-400">Severity:</span> <span className={severityColor[selectedIncident.severity]}>{selectedIncident.severity}</span></p>
                <p><span className="text-gray-400">Status:</span> {selectedIncident.status}</p>
                <p><span className="text-gray-400">Date:</span> {selectedIncident.date_occurred}</p>
                <p><span className="text-gray-400">Description:</span> {selectedIncident.description}</p>
              </div>

              {similarLoading && <p className="text-gray-400 text-sm mb-4">Finding similar incidents...</p>}
              {similar.length > 0 && (
                <div className="mb-6 border-t border-gray-700 pt-4">
                  <h3 className="font-bold text-yellow-400 mb-3">Similar Past Incidents</h3>
                  <div className="space-y-2">
                    {similar.map(s => (
                      <div key={s.id} className="bg-gray-700 rounded p-3 text-sm">
                        <p className="font-bold">{s.title}</p>
                        <p className="text-gray-400">
                          <span className={severityColor[s.severity]}>{s.severity}</span> · {s.incident_type} · {s.date_occurred}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {token && (
                <button
                  onClick={() => triggerAnalysis(selectedIncident.id)}
                  disabled={analysisLoading}
                  className="bg-blue-600 hover:bg-blue-500 disabled:bg-gray-600 px-4 py-2 rounded mb-4 w-full"
                >
                  {analysisLoading ? 'Analysing...' : analysis ? 'Redo AI Analysis' : 'Run AI Analysis'}
                </button>
              )}

              {analysisLoading && <p className="text-gray-400">Waiting for AI analysis...</p>}

              {analysis && (
                <div className="space-y-3 mt-4 border-t border-gray-700 pt-4">
                  <h3 className="font-bold text-blue-400">AI Analysis (RAG-Enhanced)</h3>
                  <p className="text-gray-400 text-sm">Analysed: {new Date(analysis.created_at).toLocaleString()}</p>
                  <p><span className="text-gray-400">Risk Level:</span> <span className={severityColor[analysis.risk_level?.toLowerCase()] || 'text-white'}> {analysis.risk_level}</span></p>
                  <p><span className="text-gray-400">Contributing Factors:</span> {analysis.contributing_factors}</p>
                  <p><span className="text-gray-400">Recommendations:</span> {analysis.recommendations}</p>
                </div>
              )}
            </div>
          ) : (
            <div className="bg-gray-800 rounded p-4 text-gray-400">
              Click an incident to view details and run AI analysis
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Incidents