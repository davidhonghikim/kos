export class KLFClient {
  private endpoint: string
  private apiKey?: string
  private bearerToken?: string

  constructor(endpoint: string = 'http://localhost:8000', apiKey?: string, bearerToken?: string) {
    this.endpoint = endpoint
    this.apiKey = apiKey
    this.bearerToken = bearerToken
  }

  async sendIntent(envelope: KLFEnvelope): Promise<KLFResponse> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    }

    if (this.apiKey) headers['X-API-Key'] = this.apiKey
    if (this.bearerToken) headers['Authorization'] = `Bearer ${this.bearerToken}`

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