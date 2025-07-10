import { useEffect, useState } from 'react'
import { getTaskTrace } from './agent-api'

export const TaskTrace = ({ agentId }: { agentId: string }) => {
  const [trace, setTrace] = useState<any[]>([])

  useEffect(() => {
    getTaskTrace(agentId).then(setTrace)
  }, [agentId])

  return (
    <div className="p-4 bg-white shadow rounded">
      <h2 className="text-lg font-bold">Task Trace</h2>
      <ul className="text-sm list-disc ml-5 mt-2">
        {trace.map((step, i) => (
          <li key={i}>{JSON.stringify(step)}</li>
        ))}
      </ul>
    </div>
  )
} 