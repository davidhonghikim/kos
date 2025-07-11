export interface KLFEnvelope {
  id: string
  intent: string
  from: string
  to: string
  issued_at: number
  payload: any
  meta?: {
    auth?: {
      jwt?: string
      signature?: string
      publicKey?: string
    }
    trace?: string[]
    version?: string
    priority?: 'low' | 'normal' | 'high'
  }
}

export interface KLFResponse {
  status: 'ok' | 'error'
  result?: any
  error?: string
}

export interface KLFConfig {
  endpoint: string
  apiKey?: string
  authToken?: string
  reconnectAttempts?: number
  reconnectDelay?: number
} 