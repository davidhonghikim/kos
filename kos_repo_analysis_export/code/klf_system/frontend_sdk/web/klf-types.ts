export type KLFEnvelope = {
  from: string
  to: string
  intent: string
  payload: Record<string, any>
  meta?: Record<string, any>
}

export type KLFResponse = {
  status: 'ok' | 'error'
  result?: any
  error?: { message: string; code?: number }
} 