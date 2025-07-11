/**
 * @kos/klf-client - Kind Link Framework Client for kOS frontends
 * 
 * This is the official KLF client library that enables frontends to communicate
 * with kOS backend services through the Kind Link Framework protocol.
 */

export interface KLFMessage {
  klf: {
    version: string;
    timestamp: string;
  };
  sender: {
    did: string;
    signature?: string;
  };
  recipient: {
    did: string;
  };
  payload: {
    type: 'service_request' | 'service_response' | 'event' | 'error';
    service?: string;
    action?: string;
    body: any;
  };
}

export interface KLFService {
  id: string;
  name: string;
  description: string;
  version: string;
  type: string;
  capabilities: string[];
  endpoints: Array<{
    name: string;
    url: string;
    method: string;
    description: string;
    parameters: Array<{
      name: string;
      type: string;
      required: boolean;
      description: string;
    }>;
  }>;
  status: 'active' | 'inactive' | 'error';
  health: {
    status: 'healthy' | 'degraded' | 'unhealthy';
    lastCheck: string;
    metrics?: Record<string, number>;
  };
}

export interface KLFClientConfig {
  baseUrl?: string;
  clientId?: string;
  timeout?: number;
}

export class KLFClient {
  private baseUrl: string;
  private clientId: string;
  private timeout: number;
  private websocket?: WebSocket;
  private eventListeners: Map<string, Function[]> = new Map();

  constructor(config: KLFClientConfig = {}) {
    this.baseUrl = (config.baseUrl || 'http://localhost:30436').replace(/\/$/, '');
    this.clientId = config.clientId || `client-${Date.now()}`;
    this.timeout = config.timeout || 30000;
  }

  /**
   * Health check - verify KLF backend is running
   */
  async ping(): Promise<{ status: string; timestamp: string; version: string }> {
    const response = await this.fetch('/klf/v1/health');
    return response.json();
  }

  /**
   * Get node identity and basic info
   */
  async getIdentity(): Promise<{
    did: string;
    name: string;
    version: string;
    capabilities: string[];
  }> {
    const response = await this.fetch('/klf/v1/identity');
    return response.json();
  }

  /**
   * Discover all available services
   */
  async discoverServices(): Promise<KLFService[]> {
    const response = await this.fetch('/klf/v1/capabilities');
    const data = await response.json();
    return data.services || [];
  }

  /**
   * Send a service request
   */
  async request(service: string, params: any = {}): Promise<any> {
    const message: KLFMessage = {
      klf: {
        version: '1.0.0',
        timestamp: new Date().toISOString()
      },
      sender: {
        did: `did:kos:client:${this.clientId}`
      },
      recipient: {
        did: 'did:kos:backend:main'
      },
      payload: {
        type: 'service_request',
        service: service,
        body: params
      }
    };

    const response = await this.fetch('/klf/v1/request', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(message)
    });

    const result = await response.json();
    
    // Handle error responses
    if (result.payload?.type === 'error') {
      throw new Error(result.payload.body.message || 'KLF service error');
    }

    return result.payload?.body || result;
  }

  /**
   * Connect to real-time events via WebSocket
   */
  async connectWebSocket(): Promise<void> {
    const wsUrl = this.baseUrl.replace('http', 'ws') + '/klf/v1/events';
    
    this.websocket = new WebSocket(wsUrl);
    
    return new Promise((resolve, reject) => {
      this.websocket!.onopen = () => {
        console.log('KLF WebSocket connected');
        resolve();
      };
      
      this.websocket!.onerror = (error) => {
        console.error('KLF WebSocket error:', error);
        reject(error);
      };
      
      this.websocket!.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          this.handleWebSocketMessage(message);
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error);
        }
      };
      
      this.websocket!.onclose = () => {
        console.log('KLF WebSocket disconnected');
      };
    });
  }

  /**
   * Subscribe to real-time events
   */
  onEvent(eventType: string, callback: (data: any) => void): void {
    if (!this.eventListeners.has(eventType)) {
      this.eventListeners.set(eventType, []);
    }
    this.eventListeners.get(eventType)!.push(callback);
  }

  /**
   * Remove event listener
   */
  offEvent(eventType: string, callback: Function): void {
    const listeners = this.eventListeners.get(eventType);
    if (listeners) {
      const index = listeners.indexOf(callback);
      if (index > -1) {
        listeners.splice(index, 1);
      }
    }
  }

  /**
   * Disconnect WebSocket
   */
  disconnect(): void {
    if (this.websocket) {
      this.websocket.close();
      this.websocket = undefined;
    }
  }

  private handleWebSocketMessage(message: any): void {
    const eventType = message.payload?.type || 'unknown';
    const listeners = this.eventListeners.get(eventType);
    
    if (listeners) {
      listeners.forEach(callback => {
        try {
          callback(message.payload?.body || message);
        } catch (error) {
          console.error('Error in event listener:', error);
        }
      });
    }
  }

  private async fetch(path: string, options?: RequestInit): Promise<Response> {
    const url = `${this.baseUrl}${path}`;
    
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);
    
    try {
      const response = await fetch(url, {
        ...options,
        signal: controller.signal
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      return response;
    } catch (error) {
      if (error.name === 'AbortError') {
        throw new Error(`Request timeout after ${this.timeout}ms`);
      }
      throw error;
    } finally {
      clearTimeout(timeoutId);
    }
  }
}

/**
 * Convenience function to create and test KLF client connection
 */
export async function createKLFClient(baseUrl = 'http://localhost:30436'): Promise<KLFClient> {
  const client = new KLFClient({ baseUrl });
  
  try {
    await client.ping();
    console.log('✅ KLF client connected successfully');
    return client;
  } catch (error) {
    console.error('❌ Failed to connect to KLF backend:', error);
    throw new Error(`KLF connection failed: ${error.message}`);
  }
}

// React hooks (if React is available)
declare const React: any;

if (typeof React !== 'undefined') {
  const { useState, useEffect } = React;
  
  /**
   * React hook for KLF service discovery
   */
  export function useKLFServices(client: KLFClient) {
    const [services, setServices] = useState<KLFService[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
      const loadServices = async () => {
        try {
          setLoading(true);
          const discoveredServices = await client.discoverServices();
          setServices(discoveredServices);
          setError(null);
        } catch (err) {
          setError(err instanceof Error ? err.message : 'Failed to load services');
        } finally {
          setLoading(false);
        }
      };

      loadServices();
    }, [client]);

    return { services, loading, error };
  }

  /**
   * React hook for KLF service requests
   */
  export function useKLFRequest(client: KLFClient) {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const request = async (service: string, params: any = {}) => {
      setLoading(true);
      setError(null);
      
      try {
        const result = await client.request(service, params);
        return result;
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'Request failed';
        setError(errorMessage);
        throw err;
      } finally {
        setLoading(false);
      }
    };

    return { request, loading, error };
  }
}

// Export all types and utilities
export * from './types';
