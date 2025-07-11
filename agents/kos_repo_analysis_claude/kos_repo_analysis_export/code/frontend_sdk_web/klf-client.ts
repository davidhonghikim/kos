import type { KLFEnvelope, KLFResponse } from './klf-types'

export class KLFClient {
  private endpoint: string
  private apiKey?: string
  private authToken?: string

  constructor(config: { endpoint: string; apiKey?: string; authToken?: string }) {
    this.endpoint = config.endpoint
    this.apiKey = config.apiKey
    this.authToken = config.authToken
  }

  setAuthToken(token: string) {
    this.authToken = token
  }

  async sendIntent(envelope: KLFEnvelope): Promise<KLFResponse> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    }

    if (this.apiKey) headers['x-api-key'] = this.apiKey
    if (this.authToken) headers['Authorization'] = `Bearer ${this.authToken}`

    const res = await fetch(`${this.endpoint}/intent`, {
      method: 'POST',
      headers,
      body: JSON.stringify(envelope),
    })

    if (!res.ok) {
      throw new Error(`KLF Error ${res.status}: ${res.statusText}`)
    }

    return await res.json()
  }
} 