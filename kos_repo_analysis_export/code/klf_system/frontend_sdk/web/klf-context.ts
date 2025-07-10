import { createContext, useContext, useState } from 'react'

type UserContextType = {
  userId: string
  agentId: string
  setUserId: (id: string) => void
  setAgentId: (id: string) => void
}

const KLFContext = createContext<UserContextType | undefined>(undefined)

export const KLFProvider = ({ children }: { children: React.ReactNode }) => {
  const [userId, setUserId] = useState('anon')
  const [agentId, setAgentId] = useState('default-agent')

  return (
    <KLFContext.Provider value={{ userId, agentId, setUserId, setAgentId }}>
      {children}
    </KLFContext.Provider>
  )
}

export const useKLFContext = (): UserContextType => {
  const ctx = useContext(KLFContext)
  if (!ctx) throw new Error('useKLFContext must be used inside <KLFProvider>')
  return ctx
} 