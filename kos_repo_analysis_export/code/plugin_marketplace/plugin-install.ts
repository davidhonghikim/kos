import { downloadAndVerifyPlugin } from './plugin-loader';

export async function installPlugin(pluginId: string): Promise<void> {
  const registry = await fetch('/plugin_marketplace/plugin-registry.json').then(r => r.json());
  const plugin = registry.find((p: any) => p.id === pluginId);

  if (!plugin) throw new Error(`Plugin ${pluginId} not found in registry`);

  await downloadAndVerifyPlugin(plugin.url, plugin.id);
} 