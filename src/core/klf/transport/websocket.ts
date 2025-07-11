/**
 * WebSocket Transport Implementation
 * Real-time bidirectional communication using WebSockets
 */

import WebSocket, { WebSocketServer as WSServer } from 'ws';
import { Transport } from './transport.js';
import { KLFMessage, TransportConfig, TransportError, validateKLFMessage } from '../protocol/types.js';
import { createLogger } from '../utils/logger.js';

const logger = createLogger('websocket-transport');

export interface WebSocketTransportConfig extends TransportConfig {
  type: 'websocket';
  options?: {
    reconnectInterval?: number;
    maxReconnectAttempts?: number;
    pingInterval?: number;
    pongTimeout?: number;
    compression?: boolean;
  };
}

export class WebSocketTransport extends Transport {
  private ws?: WebSocket;
  private reconnectTimer?: NodeJS.Timeout;
  private pingTimer?: NodeJS.Timeout;
  private reconnectAttempts = 0;
  private readonly maxReconnectAttempts: number;
  private readonly reconnectInterval: number;
  private readonly pingInterval: number;
  private readonly pongTimeout: number;

  constructor(config: WebSocketTransportConfig) {
    super(config);
    
    this.maxReconnectAttempts = config.options?.maxReconnectAttempts ?? 5;
    this.reconnectInterval = config.options?.reconnectInterval ?? 5000;
    this.pingInterval = config.options?.pingInterval ?? 30000;
    this.pongTimeout = config.options?.pongTimeout ?? 5000;
  }

  async connect(): Promise<void> {
    if (this.connected) {
      return;
    }

    return new Promise((resolve, reject) => {
      try {
        this.ws = new WebSocket(this.config.endpoint, {
          perMessageDeflate: this.config.options?.compression ?? true
        });

        this.ws.on('open', () => {
          logger.info(`Connected to ${this.config.endpoint}`);
          this.reconnectAttempts = 0;
          this.handleConnect();
          this.startPingTimer();
          resolve();
        });

        this.ws.on('message', (data: WebSocket.Data) => {
          try {
            const rawMessage = data.toString();
            const messageData = JSON.parse(rawMessage);
            const message = validateKLFMessage(messageData);
            this.handleMessage(message);
          } catch (error) {
            logger.error('Failed to parse message:', error);
            this.handleError(new TransportError('Invalid message format', error));
          }
        });

        this.ws.on('close', (code: number, reason: Buffer) => {
          logger.warn(`Connection closed: ${code} ${reason.toString()}`);
          this.cleanup();
          this.handleDisconnect();
          this.attemptReconnect();
        });

        this.ws.on('error', (error: Error) => {
          logger.error('WebSocket error:', error);
          this.handleError(new TransportError('WebSocket error', error));
          reject(error);
        });

        this.ws.on('pong', () => {
          logger.debug('Received pong');
        });

      } catch (error) {
        reject(new TransportError('Failed to create WebSocket connection', error));
      }
    });
  }

  async disconnect(): Promise<void> {
    if (!this.ws) {
      return;
    }

    this.clearTimers();
    
    if (this.ws.readyState === WebSocket.OPEN) {
      this.ws.close(1000, 'Normal closure');
    }

    this.cleanup();
  }

  async send(message: KLFMessage): Promise<void> {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      throw new TransportError('WebSocket is not connected');
    }

    try {
      const serialized = JSON.stringify(message);
      
      return new Promise((resolve, reject) => {
        this.ws!.send(serialized, (error) => {
          if (error) {
            reject(new TransportError('Failed to send message', error));
          } else {
            logger.debug(`Sent message: ${message.type} from ${message.from} to ${message.to}`);
            resolve();
          }
        });
      });
    } catch (error) {
      throw new TransportError('Failed to serialize message', error);
    }
  }

  private cleanup(): void {
    this.connected = false;
    this.clearTimers();
    
    if (this.ws) {
      this.ws.removeAllListeners();
      this.ws = undefined;
    }
  }

  private clearTimers(): void {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = undefined;
    }

    if (this.pingTimer) {
      clearInterval(this.pingTimer);
      this.pingTimer = undefined;
    }
  }

  private startPingTimer(): void {
    this.pingTimer = setInterval(() => {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        logger.debug('Sending ping');
        this.ws.ping();
      }
    }, this.pingInterval);
  }

  private attemptReconnect(): void {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      logger.error(`Max reconnection attempts (${this.maxReconnectAttempts}) reached`);
      return;
    }

    this.reconnectAttempts++;
    logger.info(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts}) in ${this.reconnectInterval}ms`);

    this.reconnectTimer = setTimeout(() => {
      this.connect().catch((error) => {
        logger.error('Reconnection failed:', error);
      });
    }, this.reconnectInterval);
  }
}

// WebSocket Server for accepting incoming connections
export class WebSocketServer {
  private wss?: WSServer;
  private transports = new Map<string, WebSocketTransport>();

  constructor(private port: number, private options?: WebSocket.ServerOptions) {}

  async start(): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        this.wss = new WSServer({ 
          port: this.port,
          ...this.options 
        });

        this.wss.on('connection', (ws: WebSocket, request) => {
          const clientId = `client-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
          logger.info(`New client connected: ${clientId} from ${request.socket.remoteAddress}`);

          // Create a transport wrapper for this connection
          const transport = this.createClientTransport(ws, clientId);
          this.transports.set(clientId, transport);

          ws.on('close', () => {
            logger.info(`Client disconnected: ${clientId}`);
            this.transports.delete(clientId);
          });

          ws.on('error', (error) => {
            logger.error(`Client error ${clientId}:`, error);
            this.transports.delete(clientId);
          });
        });

        this.wss.on('listening', () => {
          logger.info(`WebSocket server listening on port ${this.port}`);
          resolve();
        });

        this.wss.on('error', (error) => {
          logger.error('WebSocket server error:', error);
          reject(error);
        });

      } catch (error) {
        reject(error);
      }
    });
  }

  async stop(): Promise<void> {
    if (!this.wss) {
      return;
    }

    return new Promise((resolve) => {
      this.wss!.close(() => {
        logger.info('WebSocket server stopped');
        resolve();
      });
    });
  }

  getConnectedClients(): string[] {
    return Array.from(this.transports.keys());
  }

  getClientTransport(clientId: string): WebSocketTransport | undefined {
    return this.transports.get(clientId);
  }

  async broadcast(message: KLFMessage): Promise<void> {
    const promises = Array.from(this.transports.values())
      .map(transport => transport.send(message).catch(error => {
        logger.error('Failed to send broadcast message:', error);
      }));

    await Promise.allSettled(promises);
  }

  private createClientTransport(ws: WebSocket, clientId: string): WebSocketTransport {
    // Create a transport that wraps the existing WebSocket connection
    const config: WebSocketTransportConfig = {
      type: 'websocket',
      endpoint: `ws://client-${clientId}`
    };

    const transport = new WebSocketTransport(config);
    
    // Override the connection methods since we already have a connection
    (transport as any).ws = ws;
    (transport as any).connected = true;

    // Set up message handling
    ws.on('message', (data: WebSocket.Data) => {
      try {
        const rawMessage = data.toString();
        const messageData = JSON.parse(rawMessage);
        const message = validateKLFMessage(messageData);
        transport.emit('message', message);
      } catch (error) {
        logger.error('Failed to parse client message:', error);
        transport.emit('error', new TransportError('Invalid message format', error));
      }
    });

    return transport;
  }
}

export function createWebSocketTransport(config: WebSocketTransportConfig): WebSocketTransport {
  return new WebSocketTransport(config);
}

export function createWebSocketServer(port: number, options?: WebSocket.ServerOptions): WebSocketServer {
  return new WebSocketServer(port, options);
} 