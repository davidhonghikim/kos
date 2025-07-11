import { useEffect, useState } from 'react'
import { useKLFContext } from './klf-context'
import { KLFClient } from './klf-client'
import type { KLFEnvelope, KLFResponse } from './klf-types'

export const useIntent = (client: KLFClient, intent: string, payload: any) => {
  const { userId, agentId } = useKLFContext()
  const [data, setData] = useState<KLFResponse | null>(null)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    const run = async () => {
      try {
        const envelope: KLFEnvelope = {
          from: agentId,
          to: 'backend',
          intent,
          payload,
          meta: { user: userId },
        }
        const res = await client.sendIntent(envelope)
        setData(res)
      } catch (err: any) {
        setError(err)
      }
    }

    run()
  }, [intent, JSON.stringify(payload)])

  return { data, error }
} 