type PluginEvent = {
  pluginId: string;
  event: string;
  payload?: any;
};

const subscribers: Record<string, ((payload: any) => void)[]> = {};

export function subscribe(event: string, cb: (payload: any) => void) {
  if (!subscribers[event]) subscribers[event] = [];
  subscribers[event].push(cb);
}

export function emit(event: string, payload: PluginEvent) {
  const subs = subscribers[event] || [];
  subs.forEach(cb => cb(payload));
} 