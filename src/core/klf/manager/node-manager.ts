/**
 * Node Manager
 * Handles node registration, lifecycle management, and message routing
 */

import EventEmitter from 'events';
import { BaseNode } from '../node/base-node.js';
import { KLFMessage, MessageType, NodeInfo } from '../protocol/types.js';
import { TransportManager } from '../transport/transport.js';
import { createLogger } from '../utils/logger.js';

const logger = createLogger('node-manager');

export interface NodeManagerEvents {
  'node-registered': (node: BaseNode) => void;
  'node-unregistered': (nodeId: string) => void;
  'node-started': (nodeId: string) => void;
  'node-stopped': (nodeId: string) => void;
  'node-error': (nodeId: string, error: Error) => void;
  'message-routed': (message: KLFMessage, targetNode: string) => void;
  'message-failed': (message: KLFMessage, error: Error) => void;
}

export class NodeManager extends EventEmitter {
  private nodes = new Map<string, BaseNode>();
  private transportManager?: TransportManager;
  private running = false;

  constructor(transportManager?: TransportManager) {
    super();
    this.transportManager = transportManager;
  }

  // Node registration and lifecycle
  async registerNode(node: BaseNode): Promise<void> {
    if (this.nodes.has(node.id)) {
      throw new Error(`Node with ID ${node.id} already registered`);
    }

    // Set up event listeners
    node.on('started', () => {
      logger.info(`Node ${node.id} started`);
      this.emit('node-started', node.id);
    });

    node.on('stopped', () => {
      logger.info(`Node ${node.id} stopped`);
      this.emit('node-stopped', node.id);
    });

    node.on('error', (error: Error) => {
      logger.error(`Node ${node.id} error:`, error);
      this.emit('node-error', node.id, error);
    });

    // Register the node
    this.nodes.set(node.id, node);
    
    // Configure message routing for specific node types
    if (node.type === 'http-api' && 'setMessageRouter' in node) {
      (node as any).setMessageRouter(this.routeMessage.bind(this));
    }

    logger.info(`Node registered: ${node.id} (${node.type})`);
    this.emit('node-registered', node);

    // Auto-start if manager is running
    if (this.running) {
      await this.startNode(node.id);
    }
  }

  async unregisterNode(nodeId: string): Promise<void> {
    const node = this.nodes.get(nodeId);
    if (!node) {
      throw new Error(`Node ${nodeId} not found`);
    }

    // Stop the node if it's running
    if (node.status === 'running') {
      await this.stopNode(nodeId);
    }

    // Remove event listeners
    node.removeAllListeners();

    // Unregister the node
    this.nodes.delete(nodeId);
    
    logger.info(`Node unregistered: ${nodeId}`);
    this.emit('node-unregistered', nodeId);
  }

  async startNode(nodeId: string): Promise<void> {
    const node = this.nodes.get(nodeId);
    if (!node) {
      throw new Error(`Node ${nodeId} not found`);
    }

    await node.start();
  }

  async stopNode(nodeId: string): Promise<void> {
    const node = this.nodes.get(nodeId);
    if (!node) {
      throw new Error(`Node ${nodeId} not found`);
    }

    await node.stop();
  }

  // Start/stop all nodes
  async startAll(): Promise<void> {
    this.running = true;
    
    const startPromises = Array.from(this.nodes.values())
      .filter(node => node.status === 'stopped')
      .map(node => this.startNode(node.id));

    await Promise.all(startPromises);
    logger.info('All nodes started');
  }

  async stopAll(): Promise<void> {
    this.running = false;
    
    const stopPromises = Array.from(this.nodes.values())
      .filter(node => node.status === 'running')
      .map(node => this.stopNode(node.id));

    await Promise.all(stopPromises);
    logger.info('All nodes stopped');
  }

  // Message routing
  async routeMessage(message: KLFMessage): Promise<KLFMessage | void> {
    logger.debug(`Routing message ${message.id}: ${message.type} from ${message.from} to ${message.to}`);

    try {
      // Handle broadcast messages
      if (message.to === 'broadcast') {
        return this.broadcastMessage(message);
      }

      // Find target node
      const targetNode = this.nodes.get(message.to);
      if (!targetNode) {
        // Try to route via transport if available
        if (this.transportManager) {
          await this.transportManager.send(message);
          this.emit('message-routed', message, message.to);
          return;
        }
        
        throw new Error(`Target node ${message.to} not found`);
      }

      // Route to local node
      const response = await targetNode.handleMessage(message);
      this.emit('message-routed', message, message.to);
      
      return response;

    } catch (error) {
      logger.error(`Failed to route message ${message.id}:`, error);
      this.emit('message-failed', message, error as Error);
      throw error;
    }
  }

  private async broadcastMessage(message: KLFMessage): Promise<void> {
    const promises = Array.from(this.nodes.values())
      .filter(node => node.id !== message.from && node.status === 'running')
      .map(async node => {
        try {
          await node.handleMessage({ ...message, to: node.id });
        } catch (error) {
          logger.error(`Failed to broadcast to node ${node.id}:`, error);
        }
      });

    await Promise.all(promises);
    
    // Also broadcast via transport if available
    if (this.transportManager) {
      await this.transportManager.broadcast(message);
    }
  }

  // Node queries
  getNode(nodeId: string): BaseNode | undefined {
    return this.nodes.get(nodeId);
  }

  getAllNodes(): BaseNode[] {
    return Array.from(this.nodes.values());
  }

  getNodesByType(type: string): BaseNode[] {
    return Array.from(this.nodes.values())
      .filter(node => node.type === type);
  }

  getRunningNodes(): BaseNode[] {
    return Array.from(this.nodes.values())
      .filter(node => node.status === 'running');
  }

  getNodeInfo(nodeId?: string): NodeInfo | NodeInfo[] {
    if (nodeId) {
      const node = this.nodes.get(nodeId);
      if (!node) {
        throw new Error(`Node ${nodeId} not found`);
      }
      return node.getNodeInfo();
    }

    return Array.from(this.nodes.values())
      .map(node => node.getNodeInfo());
  }

  // Health checks
  async pingNode(nodeId: string): Promise<boolean> {
    const node = this.nodes.get(nodeId);
    if (!node || node.status !== 'running') {
      return false;
    }

    try {
      const pingMessage: KLFMessage = {
        id: crypto.randomUUID(),
        version: '1.0.0',
        timestamp: new Date().toISOString(),
        from: 'node-manager',
        to: nodeId,
        type: MessageType.PING,
        payload: { timestamp: Date.now() },
        metadata: { priority: 0 }
      };

      const response = await node.handleMessage(pingMessage);
      return response ? response.type === MessageType.PONG : false;
    } catch {
      return false;
    }
  }

  async healthCheck(): Promise<Record<string, boolean>> {
    const results: Record<string, boolean> = {};
    
    for (const [nodeId, node] of this.nodes) {
      if (node.status === 'running') {
        results[nodeId] = await this.pingNode(nodeId);
      } else {
        results[nodeId] = false;
      }
    }
    
    return results;
  }

  // Statistics
  getStatistics() {
    const nodes = Array.from(this.nodes.values());
    const statusCounts = nodes.reduce((acc, node) => {
      acc[node.status] = (acc[node.status] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    const typeCounts = nodes.reduce((acc, node) => {
      acc[node.type] = (acc[node.type] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    return {
      totalNodes: nodes.length,
      statusCounts,
      typeCounts,
      runningNodes: nodes.filter(n => n.status === 'running').length
    };
  }

  // Transport integration
  setTransportManager(transportManager: TransportManager): void {
    this.transportManager = transportManager;

    // Set up transport message handling
    transportManager.getAllTransports().forEach(transport => {
      transport.on('message', async (message: KLFMessage) => {
        try {
          await this.routeMessage(message);
        } catch (error) {
          logger.error('Error routing transport message:', error);
        }
      });
    });
  }

  // Graceful shutdown
  async shutdown(): Promise<void> {
    logger.info('Starting graceful shutdown...');
    
    try {
      await this.stopAll();
      
      if (this.transportManager) {
        await this.transportManager.shutdown();
      }
      
      this.removeAllListeners();
      logger.info('Graceful shutdown completed');
    } catch (error) {
      logger.error('Error during shutdown:', error);
      throw error;
    }
  }

  // Event emitter with typed events
  on<K extends keyof NodeManagerEvents>(event: K, listener: NodeManagerEvents[K]): this {
    return super.on(event, listener);
  }

  emit<K extends keyof NodeManagerEvents>(event: K, ...args: Parameters<NodeManagerEvents[K]>): boolean {
    return super.emit(event, ...args);
  }
}

// Factory function
export function createNodeManager(transportManager?: TransportManager): NodeManager {
  return new NodeManager(transportManager);
} 