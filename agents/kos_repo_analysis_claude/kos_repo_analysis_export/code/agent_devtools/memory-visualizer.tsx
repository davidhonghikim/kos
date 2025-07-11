import { useEffect, useState } from 'react'
import { fetchMemory } from './agent-api'

export const MemoryVisualizer = ({ agentId }: { agentId: string }) => {
  const [mem, setMem] = useState<any>([])

  useEffect(() => {
    fetchMemory(agentId).then(setMem)
  }, [agentId])

  return (
    <div className="p-4 bg-white shadow rounded">
      <h2 className="text-lg font-semibold">Vector Memory (Top 10)</h2>
      <ul className="list-disc ml-5 text-sm mt-2">
        {mem.slice(0, 10).map((entry, i) => (
          <li key={i}>{entry.text} — score: {entry.score}</li>
        ))}
      </ul>
    </div>
  )
} 