import type { KLFEnvelope, KLFResponse } from './klf-types'

export class KLFApi {
  private baseUrl: string
  private apiKey?: string

  constructor(baseUrl: string, apiKey?: string) {
    this.baseUrl = baseUrl
    this.apiKey = apiKey
  }

  async sendIntent(envelope: KLFEnvelope): Promise<KLFResponse> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    }

    if (this.apiKey) {
      headers['x-api-key'] = this.apiKey
    }

    const response = await fetch(`${this.baseUrl}/intent`, {
      method: 'POST',
      headers,
      body: JSON.stringify(envelope),
    })

    if (!response.ok) {
      throw new Error(`KLF API Error: ${response.status} ${response.statusText}`)
    }

    return await response.json()
  }

  async getHealth(): Promise<{ status: string }> {
    const response = await fetch(`${this.baseUrl}/health`)
    if (!response.ok) {
      throw new Error(`Health check failed: ${response.status}`)
    }
    return await response.json()
  }

  async getVaultValue(key: string): Promise<{ key: string; value: string }> {
    const headers: Record<string, string> = {}
    if (this.apiKey) {
      headers['x-api-key'] = this.apiKey
    }

    const response = await fetch(`${this.baseUrl}/vault/${key}`, {
      headers,
    })

    if (!response.ok) {
      throw new Error(`Vault read failed: ${response.status}`)
    }

    return await response.json()
  }
} 