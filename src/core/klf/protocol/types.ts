/**
 * Kind Link Framework (KLF) Protocol Types
 * Core message types and interfaces for agent communication
 */

import { z } from 'zod';

// Core message type enumeration
export enum MessageType {
  // Basic communication
  PING = 'ping',
  PONG = 'pong',
  
  // Task coordination
  TASK_REQUEST = 'task_request',
  TASK_RESPONSE = 'task_response',
  TASK_ERROR = 'task_error',
  TASK_PROGRESS = 'task_progress',
  
  // Data operations
  DATA_QUERY = 'data_query',
  DATA_RESULT = 'data_result',
  DATA_STREAM = 'data_stream',
  
  // Node lifecycle
  NODE_REGISTER = 'node_register',
  NODE_UNREGISTER = 'node_unregister',
  NODE_STATUS = 'node_status',
  NODE_DISCOVERY = 'node_discovery',
  
  // Events and notifications
  EVENT = 'event',
  NOTIFICATION = 'notification',
  ALERT = 'alert',
  
  // Configuration and control
  CONFIG_UPDATE = 'config_update',
  CONTROL_COMMAND = 'control_command'
}

export enum Priority {
  LOW = 0,
  NORMAL = 1,
  HIGH = 2,
  CRITICAL = 3,
  EMERGENCY = 4
}

// Core message metadata
export interface MessageMetadata {
  priority: Priority;
  ttl?: number; // Time to live in milliseconds
  retryCount?: number;
  correlationId?: string;
  traceId?: string;
  replyTo?: string;
  encrypted?: boolean;
  compressed?: boolean;
  [key: string]: any; // Allow custom metadata
}

// Main KLF message interface
export interface KLFMessage {
  id: string; // UUID
  version: string; // Protocol version
  timestamp: string; // ISO 8601
  from: string; // Sender node ID
  to: string; // Recipient node ID or topic
  type: MessageType;
  payload: any;
  metadata: MessageMetadata;
  signature?: string; // Digital signature
}

// Zod schemas for runtime validation
export const MessageMetadataSchema = z.object({
  priority: z.nativeEnum(Priority),
  ttl: z.number().optional(),
  retryCount: z.number().optional(),
  correlationId: z.string().optional(),
  traceId: z.string().optional(),
  replyTo: z.string().optional(),
  encrypted: z.boolean().optional(),
  compressed: z.boolean().optional()
}).catchall(z.any());

export const KLFMessageSchema = z.object({
  id: z.string().uuid(),
  version: z.string(),
  timestamp: z.string().datetime(),
  from: z.string(),
  to: z.string(),
  type: z.nativeEnum(MessageType),
  payload: z.any(),
  metadata: MessageMetadataSchema,
  signature: z.string().optional()
});

// Capability definitions
export interface Capability {
  name: string;
  version: string;
  description: string;
  messageTypes: MessageType[];
  parameters?: Record<string, any>;
}

// Node information
export interface NodeInfo {
  id: string;
  type: string;
  version: string;
  capabilities: Capability[];
  endpoints: string[];
  metadata: Record<string, any>;
  status: 'starting' | 'running' | 'stopping' | 'stopped' | 'error';
  lastSeen: string;
}

// Transport configuration
export interface TransportConfig {
  type: 'websocket' | 'http' | 'ipc' | 'tcp';
  endpoint: string;
  options?: Record<string, any>;
}

// Security configuration
export interface SecurityConfig {
  enabled: boolean;
  keyPair?: {
    publicKey: string;
    privateKey: string;
  };
  trustedNodes?: string[];
  allowUnsigned?: boolean;
}

// Error types
export class KLFError extends Error {
  constructor(
    message: string,
    public code: string,
    public details?: any
  ) {
    super(message);
    this.name = 'KLFError';
  }
}

export class ValidationError extends KLFError {
  constructor(message: string, public validationErrors: any[]) {
    super(message, 'VALIDATION_ERROR', validationErrors);
    this.name = 'ValidationError';
  }
}

export class TransportError extends KLFError {
  constructor(message: string, details?: any) {
    super(message, 'TRANSPORT_ERROR', details);
    this.name = 'TransportError';
  }
}

export class SecurityError extends KLFError {
  constructor(message: string, details?: any) {
    super(message, 'SECURITY_ERROR', details);
    this.name = 'SecurityError';
  }
}

// Utility type guards
export function isKLFMessage(obj: any): obj is KLFMessage {
  try {
    KLFMessageSchema.parse(obj);
    return true;
  } catch {
    return false;
  }
}

export function validateKLFMessage(obj: any): KLFMessage {
  // TODO: Fix type validation
  // return KLFMessageSchema.parse(obj);
  return obj as KLFMessage;
}

// Message builder utility
export class MessageBuilder {
  private id: string = crypto.randomUUID();
  private version: string = '1.0.0';
  private timestamp: string = new Date().toISOString();
  private fromId?: string;
  private toId?: string;
  private messageType?: MessageType;
  private messagePayload: any = {};
  private messageMetadata: MessageMetadata = {
    priority: Priority.NORMAL
  };
  private messageSignature?: string;

  from(nodeId: string): this {
    this.fromId = nodeId;
    return this;
  }

  to(nodeId: string): this {
    this.toId = nodeId;
    return this;
  }

  type(messageType: MessageType): this {
    this.messageType = messageType;
    return this;
  }

  payload(data: any): this {
    this.messagePayload = data;
    return this;
  }

  priority(priority: Priority): this {
    this.messageMetadata.priority = priority;
    return this;
  }

  ttl(milliseconds: number): this {
    this.messageMetadata.ttl = milliseconds;
    return this;
  }

  correlationId(id: string): this {
    this.messageMetadata.correlationId = id;
    return this;
  }

  replyTo(nodeId: string): this {
    this.messageMetadata.replyTo = nodeId;
    return this;
  }

  build(): KLFMessage {
    // Ensure all required fields are set
    if (!this.fromId || !this.toId || !this.messageType) {
      throw new Error('Missing required fields: from, to, type');
    }
    
    // Build the complete message
    const completeMessage: KLFMessage = {
      id: this.id,
      version: this.version,
      timestamp: this.timestamp,
      from: this.fromId,
      to: this.toId,
      type: this.messageType,
      payload: this.messagePayload,
      metadata: this.messageMetadata,
      signature: this.messageSignature
    };
    
    return completeMessage;
  }
}

// Factory function for creating messages
export function createMessage(): MessageBuilder {
  return new MessageBuilder();
}

// Common message patterns
export function createPingMessage(from: string, to: string): KLFMessage {
  return createMessage()
    .from(from)
    .to(to)
    .type(MessageType.PING)
    .payload({ timestamp: Date.now() })
    .build();
}

export function createPongMessage(from: string, to: string, originalMessage: KLFMessage): KLFMessage {
  return createMessage()
    .from(from)
    .to(to)
    .type(MessageType.PONG)
    .payload({ originalTimestamp: originalMessage.payload?.timestamp, timestamp: Date.now() })
    .correlationId(originalMessage.id)
    .build();
}

export function createTaskRequest(
  from: string, 
  to: string, 
  taskType: string, 
  parameters: any
): KLFMessage {
  return createMessage()
    .from(from)
    .to(to)
    .type(MessageType.TASK_REQUEST)
    .payload({ taskType, parameters })
    .build();
}

export function createTaskResponse(
  from: string, 
  to: string, 
  result: any, 
  originalMessage: KLFMessage
): KLFMessage {
  return createMessage()
    .from(from)
    .to(to)
    .type(MessageType.TASK_RESPONSE)
    .payload({ result })
    .correlationId(originalMessage.id)
    .build();
}

export function createErrorMessage(
  from: string, 
  to: string, 
  error: Error, 
  originalMessage?: KLFMessage
): KLFMessage {
  const builder = createMessage()
    .from(from)
    .to(to)
    .type(MessageType.TASK_ERROR)
    .payload({ 
      error: error.message, 
      code: (error as any).code || 'UNKNOWN_ERROR',
      stack: error.stack 
    });

  if (originalMessage) {
    builder.correlationId(originalMessage.id);
  }

  return builder.build();
} 