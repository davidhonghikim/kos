import { useState } from 'react'
import { runSandboxTool } from './agent-api'

export const SandboxRunner = () => {
  const [tool, setTool] = useState('')
  const [output, setOutput] = useState('')

  const runTool = async () => {
    const result = await runSandboxTool(tool)
    setOutput(result)
  }

  return (
    <div className="bg-gray-100 p-4 rounded">
      <input
        className="w-full p-2 border"
        placeholder="Tool name or recipe ID"
        value={tool}
        onChange={(e) => setTool(e.target.value)}
      />
      <button onClick={runTool} className="mt-2 bg-blue-600 text-white px-4 py-2">Run</button>
      <pre className="mt-4 text-sm">{output}</pre>
    </div>
  )
} 