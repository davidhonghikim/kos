import { useState } from 'react'
import { probeLLM } from './agent-api'

export const LLMProbe = () => {
  const [input, setInput] = useState('')
  const [result, setResult] = useState('')

  const handleSend = async () => {
    const res = await probeLLM(input)
    setResult(res)
  }

  return (
    <div className="bg-white p-4 rounded shadow">
      <textarea
        className="w-full p-2 border"
        rows={3}
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Enter test prompt"
      />
      <button onClick={handleSend} className="mt-2 bg-purple-600 text-white px-4 py-2">Send</button>
      <pre className="mt-3 text-sm">{result}</pre>
    </div>
  )
} 