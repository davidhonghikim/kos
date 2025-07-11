import { createContext, useContext, useState } from 'react'

type UserContextType = {
  userId: string
  agentId: string
  setUserId: (id: string) => void
  setAgentId: (id: string) => void
}

const UserContext = createContext<UserContextType | undefined>(undefined)

export function UserProvider({ children }: { children: React.ReactNode }) {
  const [userId, setUserId] = useState('')
  const [agentId, setAgentId] = useState('')

  return (
    <UserContext.Provider value={{ userId, agentId, setUserId, setAgentId }}>
      {children}
    </UserContext.Provider>
  )
}

export function useUser() {
  const context = useContext(UserContext)
  if (!context) {
    throw new Error('useUser must be used within UserProvider')
  }
  return context
} 