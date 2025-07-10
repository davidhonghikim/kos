import { useEffect, useState } from 'react'
import { fetchFunctionCalls } from './agent-api'

export const FunctionCallViewer = ({ agentId }: { agentId: string }) => {
  const [calls, setCalls] = useState<any[]>([])

  useEffect(() => {
    fetchFunctionCalls(agentId).then(setCalls)
  }, [agentId])

  return (
    <div className="p-4 bg-white border rounded">
      <h2 className="font-semibold">LLM Function Calls</h2>
      <ul className="text-sm mt-2">
        {calls.map((c, i) => (
          <li key={i} className="border-b py-1">
            {c.tool}({JSON.stringify(c.args)})
          </li>
        ))}
      </ul>
    </div>
  )
} 