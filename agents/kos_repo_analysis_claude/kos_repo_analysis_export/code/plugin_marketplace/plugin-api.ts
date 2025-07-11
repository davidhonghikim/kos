import type { PluginMeta } from './plugin-types';

export async function fetchPluginList(): Promise<PluginMeta[]> {
  const res = await fetch('/plugin_marketplace/plugin-registry.json');
  if (!res.ok) throw new Error('Failed to load plugin registry');
  return res.json();
}

export async function installPlugin(pluginId: string): Promise<void> {
  const res = await fetch('/api/plugin/install', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ pluginId }),
  });

  if (!res.ok) throw new Error(`Install failed: ${res.statusText}`);
} 