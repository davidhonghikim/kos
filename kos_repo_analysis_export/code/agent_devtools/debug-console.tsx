import { useState } from 'react'
import { sendAgentCommand } from './agent-api'

export const DebugConsole = ({ agentId }: { agentId: string }) => {
  const [input, setInput] = useState('')
  const [output, setOutput] = useState('')

  const handleRun = async () => {
    const result = await sendAgentCommand(agentId, input)
    setOutput(result)
  }

  return (
    <div className="p-4 bg-black text-green-400 font-mono rounded">
      <textarea
        className="w-full bg-black text-green-400"
        rows={4}
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />
      <button onClick={handleRun} className="bg-green-700 px-4 py-2 mt-2">Run</button>
      <pre className="mt-4">{output}</pre>
    </div>
  )
} 