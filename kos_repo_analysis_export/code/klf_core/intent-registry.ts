type HandlerFn = (payload: any, meta: any) => Promise<any>;

const registry: Record<string, HandlerFn> = {};

export function registerIntent(intent: string, handler: HandlerFn) {
  if (registry[intent]) {
    throw new Error(`Intent "${intent}" already registered`);
  }
  registry[intent] = handler;
}

export function getHandler(intent: string): HandlerFn | undefined {
  return registry[intent];
}

export function getAllIntents(): string[] {
  return Object.keys(registry);
} 