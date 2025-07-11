export const fetchAgentState = async (id: string) => {
  const res = await fetch(`/api/agent/${id}/state`)
  return await res.json()
}

export const getTaskTrace = async (id: string) => {
  const res = await fetch(`/api/agent/${id}/trace`)
  return await res.json()
}

export const sendAgentCommand = async (id: string, input: string) => {
  const res = await fetch(`/api/agent/${id}/cmd`, {
    method: 'POST',
    body: JSON.stringify({ input }),
    headers: { 'Content-Type': 'application/json' },
  })
  return await res.text()
}

export const fetchMemory = async (id: string) => {
  const res = await fetch(`/api/agent/${id}/memory`)
  return await res.json()
}

export const runSandboxTool = async (tool: string) => {
  const res = await fetch(`/api/sandbox/run`, {
    method: 'POST',
    body: JSON.stringify({ tool }),
    headers: { 'Content-Type': 'application/json' },
  })
  return await res.text()
}

export const fetchFunctionCalls = async (id: string) => {
  const res = await fetch(`/api/agent/${id}/calls`)
  return await res.json()
}

export const probeLLM = async (prompt: string) => {
  const res = await fetch(`/api/probe`, {
    method: 'POST',
    body: JSON.stringify({ prompt }),
    headers: { 'Content-Type': 'application/json' },
  })
  return await res.text()
} 