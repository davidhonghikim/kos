export const callAgentDK = async (agentId: string, tool: string, args: any) => {
  const res = await fetch(`/api/agent/${agentId}/call`, {
    method: 'POST',
    body: JSON.stringify({ tool, args }),
    headers: { 'Content-Type': 'application/json' },
  })
  return await res.json()
} 