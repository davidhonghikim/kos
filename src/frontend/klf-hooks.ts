import { useState, useEffect } from 'react'
import { KLFClient } from './klf-client'
import type { KLFEnvelope, KLFResponse } from './klf-types'

export function useIntent(client: KLFClient) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const sendIntent = async (envelope: KLFEnvelope): Promise<KLFResponse | null> => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await client.sendIntent(envelope)
      return response
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
      return null
    } finally {
      setLoading(false)
    }
  }

  return { sendIntent, loading, error }
}

export function useAgent(client: KLFClient, agentId: string) {
  const [status, setStatus] = useState<'idle' | 'connected' | 'disconnected'>('idle')

  useEffect(() => {
    // Monitor agent connection status
    const checkStatus = async () => {
      try {
        await client.sendIntent({
          id: crypto.randomUUID(),
          intent: 'agent.ping',
          from: 'ui.frontend',
          to: agentId,
          issued_at: Date.now(),
          payload: {}
        })
        setStatus('connected')
      } catch {
        setStatus('disconnected')
      }
    }

    checkStatus()
    const interval = setInterval(checkStatus, 30000) // Check every 30s
    return () => clearInterval(interval)
  }, [client, agentId])

  return { status }
} 