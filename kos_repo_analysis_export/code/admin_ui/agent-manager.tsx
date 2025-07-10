import React, { useEffect, useState } from 'react'
import { getAgents, restartAgent, toggleAgent } from './admin-api'

export const AgentManager = () => {
  const [agents, setAgents] = useState([])

  useEffect(() => {
    getAgents().then(setAgents)
  }, [])

  return (
    <div>
      <h2 className="text-lg font-semibold mb-2">Agents</h2>
      <table className="table-auto w-full border">
        <thead>
          <tr className="bg-gray-100">
            <th>Name</th><th>Status</th><th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {agents.map((a: any) => (
            <tr key={a.name} className="border-t">
              <td>{a.name}</td>
              <td>{a.status}</td>
              <td className="space-x-2">
                <button onClick={() => restartAgent(a.name)} className="text-yellow-600">Restart</button>
                <button onClick={() => toggleAgent(a.name)} className="text-red-600">Toggle</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
} 