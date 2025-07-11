/**
 * Transport Abstraction Layer
 * Provides a unified interface for different transport mechanisms
 */

import EventEmitter from 'events';
import { KLFMessage, TransportConfig, TransportError } from '../protocol/types.js';

export interface TransportEvents {
  'message': (message: KLFMessage) => void;
  'connect': () => void;
  'disconnect': () => void;
  'error': (error: Error) => void;
}

export abstract class Transport extends EventEmitter {
  protected config: TransportConfig;
  protected connected: boolean = false;

  constructor(config: TransportConfig) {
    super();
    this.config = config;
  }

  abstract connect(): Promise<void>;
  abstract disconnect(): Promise<void>;
  abstract send(message: KLFMessage): Promise<void>;

  get isConnected(): boolean {
    return this.connected;
  }

  get endpoint(): string {
    return this.config.endpoint;
  }

  protected handleMessage(message: KLFMessage): void {
    this.emit('message', message);
  }

  protected handleConnect(): void {
    this.connected = true;
    this.emit('connect');
  }

  protected handleDisconnect(): void {
    this.connected = false;
    this.emit('disconnect');
  }

  protected handleError(error: Error): void {
    this.emit('error', error);
  }

  // Add typed event methods
  on<K extends keyof TransportEvents>(event: K, listener: TransportEvents[K]): this {
    return super.on(event, listener);
  }

  emit<K extends keyof TransportEvents>(event: K, ...args: Parameters<TransportEvents[K]>): boolean {
    return super.emit(event, ...args);
  }
}

export class TransportManager {
  private transports = new Map<string, Transport>();
  private defaultTransport?: Transport;

  async addTransport(name: string, transport: Transport): Promise<void> {
    if (this.transports.has(name)) {
      throw new TransportError(`Transport ${name} already exists`);
    }

    this.transports.set(name, transport);
    
    // Set first transport as default
    if (!this.defaultTransport) {
      this.defaultTransport = transport;
    }

    // Connect the transport
    await transport.connect();
  }

  async removeTransport(name: string): Promise<void> {
    const transport = this.transports.get(name);
    if (!transport) {
      throw new TransportError(`Transport ${name} not found`);
    }

    await transport.disconnect();
    this.transports.delete(name);

    if (this.defaultTransport === transport) {
      this.defaultTransport = this.transports.values().next().value;
    }
  }

  getTransport(name: string): Transport | undefined {
    return this.transports.get(name);
  }

  getDefaultTransport(): Transport | undefined {
    return this.defaultTransport;
  }

  getAllTransports(): Transport[] {
    return Array.from(this.transports.values());
  }

  async send(message: KLFMessage, transportName?: string): Promise<void> {
    let transport: Transport | undefined;

    if (transportName) {
      transport = this.getTransport(transportName);
      if (!transport) {
        throw new TransportError(`Transport ${transportName} not found`);
      }
    } else {
      transport = this.getDefaultTransport();
      if (!transport) {
        throw new TransportError('No transport available');
      }
    }

    if (!transport.isConnected) {
      throw new TransportError(`Transport ${transportName || 'default'} is not connected`);
    }

    await transport.send(message);
  }

  async broadcast(message: KLFMessage): Promise<void> {
    const transports = this.getAllTransports();
    const promises = transports
      .filter(t => t.isConnected)
      .map(t => t.send(message));

    await Promise.all(promises);
  }

  async shutdown(): Promise<void> {
    const promises = Array.from(this.transports.values())
      .map(transport => transport.disconnect());

    await Promise.all(promises);
    this.transports.clear();
    this.defaultTransport = undefined;
  }
}

export function createTransportManager(): TransportManager {
  return new TransportManager();
} 