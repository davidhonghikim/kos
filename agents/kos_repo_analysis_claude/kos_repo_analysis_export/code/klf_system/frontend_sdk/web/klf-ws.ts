type Callback = (msg: any) => void

export class KLFWebSocket {
  private socket: WebSocket
  private listeners: Callback[] = []

  constructor(topic: string, baseUrl: string = 'ws://localhost:8000') {
    this.socket = new WebSocket(`${baseUrl}/${topic}`)
    this.socket.onmessage = (event) => {
      const msg = JSON.parse(event.data)
      this.listeners.forEach((cb) => cb(msg))
    }
  }

  onMessage(callback: Callback) {
    this.listeners.push(callback)
  }

  close() {
    this.socket.close()
  }
} 