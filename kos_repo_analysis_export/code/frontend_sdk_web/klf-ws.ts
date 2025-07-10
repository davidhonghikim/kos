import type { KLFEnvelope } from './klf-types'

export class KLFWebSocket {
  private ws: WebSocket | null = null
  private reconnectAttempts = 0
  private maxReconnectAttempts = 5
  private reconnectDelay = 1000

  constructor(
    private url: string,
    private onMessage?: (envelope: KLFEnvelope) => void,
    private onError?: (error: Event) => void
  ) {}

  connect() {
    try {
      this.ws = new WebSocket(this.url)
      this.ws.onopen = () => {
        console.log('KLF WebSocket connected')
        this.reconnectAttempts = 0
      }
      
      this.ws.onmessage = (event) => {
        try {
          const envelope: KLFEnvelope = JSON.parse(event.data)
          this.onMessage?.(envelope)
        } catch (err) {
          console.error('Failed to parse WebSocket message:', err)
        }
      }
      
      this.ws.onerror = (error) => {
        console.error('KLF WebSocket error:', error)
        this.onError?.(error)
      }
      
      this.ws.onclose = () => {
        console.log('KLF WebSocket disconnected')
        this.attemptReconnect()
      }
    } catch (err) {
      console.error('Failed to create WebSocket connection:', err)
    }
  }

  private attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++
      setTimeout(() => {
        console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})`)
        this.connect()
      }, this.reconnectDelay * this.reconnectAttempts)
    }
  }

  send(envelope: KLFEnvelope) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(envelope))
    } else {
      throw new Error('WebSocket is not connected')
    }
  }

  disconnect() {
    this.ws?.close()
    this.ws = null
  }
} 