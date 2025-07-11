import { useState, useEffect } from 'react'
import { fetchAgentState } from './agent-api'

export const AgentInspector = ({ agentId }: { agentId: string }) => {
  const [state, setState] = useState<any>(null)

  useEffect(() => {
    fetchAgentState(agentId).then(setState)
  }, [agentId])

  return (
    <div className="p-4 bg-white shadow-md rounded">
      <h2 className="text-lg font-semibold">Agent State: {agentId}</h2>
      <pre className="overflow-auto text-sm bg-gray-100 p-2 mt-2">
        {JSON.stringify(state, null, 2)}
      </pre>
    </div>
  )
} 