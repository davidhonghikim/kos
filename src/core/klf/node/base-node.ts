/**
 * Base Node Implementation
 * Foundation class that all Griot nodes extend
 */

import EventEmitter from 'events';
import { nanoid } from 'nanoid';
import { 
  KLFMessage, 
  MessageType, 
  Capability, 
  NodeInfo,
  createMessage,
  createPongMessage,
  createErrorMessage,
  Priority
} from '../protocol/types.js';
import { createLogger } from '../utils/logger.js';

const logger = createLogger('base-node');

export interface NodeConfig {
  id?: string;
  type: string;
  version?: string;
  capabilities?: Capability[];
  metadata?: Record<string, any>;
}

export interface NodeEvents {
  'message': (message: KLFMessage) => void;
  'started': () => void;
  'stopped': () => void;
  'error': (error: Error) => void;
  'status-change': (status: NodeStatus) => void;
}

export type NodeStatus = 'starting' | 'running' | 'stopping' | 'stopped' | 'error';

export abstract class BaseNode extends EventEmitter {
  public readonly id: string;
  public readonly type: string;
  public readonly version: string;
  public readonly capabilities: Capability[];
  public readonly metadata: Record<string, any>;
  
  private _status: NodeStatus = 'stopped';
  private startTime?: Date;
  private messageHandlers = new Map<MessageType, (message: KLFMessage) => Promise<KLFMessage | void>>();

  constructor(config: NodeConfig) {
    super();
    
    this.id = config.id || `${config.type}-${nanoid(8)}`;
    this.type = config.type;
    this.version = config.version || '1.0.0';
    this.capabilities = config.capabilities || [];
    this.metadata = config.metadata || {};

    // Register default message handlers
    this.registerMessageHandler(MessageType.PING, this.handlePing.bind(this));
    this.registerMessageHandler(MessageType.NODE_STATUS, this.handleStatusRequest.bind(this));

    logger.info(`Node created: ${this.id} (${this.type})`);
  }

  // Abstract methods that concrete nodes must implement
  abstract initialize(): Promise<void>;
  abstract cleanup(): Promise<void>;

  // Node lifecycle methods
  async start(): Promise<void> {
    if (this._status === 'running') {
      logger.warn(`Node ${this.id} is already running`);
      return;
    }

    try {
      this.setStatus('starting');
      this.startTime = new Date();
      
      await this.initialize();
      
      this.setStatus('running');
      this.emit('started');
      
      logger.info(`Node ${this.id} started successfully`);
    } catch (error) {
      this.setStatus('error');
      this.emit('error', error as Error);
      throw error;
    }
  }

  async stop(): Promise<void> {
    if (this._status === 'stopped') {
      logger.warn(`Node ${this.id} is already stopped`);
      return;
    }

    try {
      this.setStatus('stopping');
      
      await this.cleanup();
      
      this.setStatus('stopped');
      this.emit('stopped');
      
      logger.info(`Node ${this.id} stopped successfully`);
    } catch (error) {
      this.setStatus('error');
      this.emit('error', error as Error);
      throw error;
    }
  }

  // Message handling
  async handleMessage(message: KLFMessage): Promise<KLFMessage | void> {
    logger.debug(`Node ${this.id} received message: ${message.type} from ${message.from}`);

    try {
      // Check if message is addressed to this node
      if (message.to !== this.id && message.to !== 'broadcast') {
        logger.warn(`Message ${message.id} not addressed to this node (${this.id})`);
        return;
      }

      // Find and execute handler
      const handler = this.messageHandlers.get(message.type);
      if (handler) {
        const response = await handler(message);
        if (response) {
          logger.debug(`Node ${this.id} sending response: ${response.type} to ${response.to}`);
        }
        return response;
      } else {
        // No handler found, call the default handler
        return this.handleUnknownMessage(message);
      }
    } catch (error) {
      logger.error(`Error handling message ${message.id}:`, error);
      
      // Send error response if the message expects a reply
      if (message.metadata.replyTo) {
        return createErrorMessage(this.id, message.metadata.replyTo, error as Error, message);
      }
      
      this.emit('error', error as Error);
    }
  }

  // Message handler registration
  protected registerMessageHandler(
    type: MessageType, 
    handler: (message: KLFMessage) => Promise<KLFMessage | void>
  ): void {
    this.messageHandlers.set(type, handler);
    logger.debug(`Registered handler for message type: ${type}`);
  }

  // Utility methods for sending messages
  protected createResponse(originalMessage: KLFMessage, payload: any, type: MessageType = MessageType.TASK_RESPONSE): KLFMessage {
    return createMessage()
      .from(this.id)
      .to(originalMessage.from)
      .type(type)
      .payload(payload)
      .correlationId(originalMessage.id)
      .build();
  }

  protected createNotification(to: string, payload: any): KLFMessage {
    return createMessage()
      .from(this.id)
      .to(to)
      .type(MessageType.NOTIFICATION)
      .payload(payload)
      .build();
  }

  protected createTaskRequest(to: string, taskType: string, parameters: any): KLFMessage {
    return createMessage()
      .from(this.id)
      .to(to)
      .type(MessageType.TASK_REQUEST)
      .payload({ taskType, parameters })
      .build();
  }

  // Default message handlers
  private async handlePing(message: KLFMessage): Promise<KLFMessage> {
    logger.debug(`Received ping from ${message.from}`);
    return createPongMessage(this.id, message.from, message);
  }

  private async handleStatusRequest(message: KLFMessage): Promise<KLFMessage> {
    const status = this.getNodeInfo();
    return this.createResponse(message, status);
  }

  // Override this to handle unknown message types
  protected async handleUnknownMessage(message: KLFMessage): Promise<KLFMessage | void> {
    logger.warn(`No handler for message type: ${message.type}`);
    
    if (message.metadata.replyTo) {
      const error = new Error(`Unknown message type: ${message.type}`);
      return createErrorMessage(this.id, message.metadata.replyTo, error, message);
    }
  }

  // Status management
  get status(): NodeStatus {
    return this._status;
  }

  private setStatus(status: NodeStatus): void {
    if (this._status !== status) {
      const oldStatus = this._status;
      this._status = status;
      
      logger.info(`Node ${this.id} status changed: ${oldStatus} -> ${status}`);
      this.emit('status-change', status);
    }
  }

  // Node information
  getNodeInfo(): NodeInfo {
    return {
      id: this.id,
      type: this.type,
      version: this.version,
      capabilities: this.capabilities,
      endpoints: [], // Override in concrete implementations
      metadata: {
        ...this.metadata,
        startTime: this.startTime?.toISOString(),
        uptime: this.startTime ? Date.now() - this.startTime.getTime() : 0
      },
      status: this._status,
      lastSeen: new Date().toISOString()
    };
  }

  // Capability management
  hasCapability(name: string): boolean {
    return this.capabilities.some(cap => cap.name === name);
  }

  getCapability(name: string): Capability | undefined {
    return this.capabilities.find(cap => cap.name === name);
  }

  // Event emitter with typed events
  on<K extends keyof NodeEvents>(event: K, listener: NodeEvents[K]): this {
    return super.on(event, listener);
  }

  emit<K extends keyof NodeEvents>(event: K, ...args: Parameters<NodeEvents[K]>): boolean {
    return super.emit(event, ...args);
  }

  // Graceful shutdown handling
  protected setupGracefulShutdown(): void {
    const signals: NodeJS.Signals[] = ['SIGINT', 'SIGTERM'];
    
    signals.forEach(signal => {
      process.on(signal, async () => {
        logger.info(`Received ${signal}, shutting down node ${this.id}`);
        try {
          await this.stop();
          process.exit(0);
        } catch (error) {
          logger.error('Error during shutdown:', error);
          process.exit(1);
        }
      });
    });
  }
}

// Utility function to create a simple node
export function createSimpleNode(
  type: string, 
  handlers: Partial<Record<MessageType, (message: KLFMessage) => Promise<KLFMessage | void>>>
): BaseNode {
  class SimpleNode extends BaseNode {
    async initialize(): Promise<void> {
      // Register provided handlers
      Object.entries(handlers).forEach(([messageType, handler]) => {
        if (handler) {
          this.registerMessageHandler(messageType as MessageType, handler);
        }
      });
    }

    async cleanup(): Promise<void> {
      // No cleanup needed for simple nodes
    }
  }

  return new SimpleNode({ type });
} 