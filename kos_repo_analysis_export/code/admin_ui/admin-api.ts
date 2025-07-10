const fetcher = async (path: string, method = 'GET', body?: any) => {
  const res = await fetch(`/admin/${path}`, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: body ? JSON.stringify(body) : undefined,
  })
  return res.json()
}

export const getAgents = () => fetcher('agents')
export const restartAgent = (id: string) => fetcher(`agents/${id}/restart`, 'POST')
export const toggleAgent = (id: string) => fetcher(`agents/${id}/toggle`, 'POST')

export const getIntentLog = () => fetcher('log')

export const getVaultKeys = () => fetcher('vault/keys')
export const getVaultValue = (k: string) => fetcher(`vault/${k}`)

export const getPlugins = () => fetcher('plugins')
export const togglePlugin = (id: string) => fetcher(`plugins/${id}/toggle`, 'POST')

export const getEnv = () => fetcher('env')
export const updateEnv = (env: Record<string, string>) => fetcher('env', 'POST', env)

export const getUsers = () => fetcher('users')
export const updateRole = (id: string, role: string) => fetcher(`users/${id}/role`, 'POST', { role }) 