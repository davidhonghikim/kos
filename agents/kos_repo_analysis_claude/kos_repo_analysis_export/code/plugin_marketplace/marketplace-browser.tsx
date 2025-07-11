import React, { useEffect, useState } from 'react';
import { fetchPluginList, installPlugin } from './plugin-api';
import type { PluginMeta } from './plugin-types';

export default function MarketplaceBrowser() {
  const [plugins, setPlugins] = useState<PluginMeta[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchPluginList()
      .then(setPlugins)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const handleInstall = async (pluginId: string) => {
    try {
      await installPlugin(pluginId);
      alert('Plugin installed successfully');
    } catch (e) {
      alert('Install failed: ' + (e as Error).message);
    }
  };

  if (loading) return <div>Loading plugins…</div>;
  if (error) return <div className="text-red-500">Error: {error}</div>;

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Plugin Marketplace</h1>
      {plugins.map(plugin => (
        <div key={plugin.id} className="border p-4 rounded shadow">
          <h2 className="font-semibold text-lg">{plugin.name}</h2>
          <p className="text-sm text-gray-600">{plugin.description}</p>
          <button
            className="mt-2 bg-blue-600 text-white px-3 py-1 rounded"
            onClick={() => handleInstall(plugin.id)}
          >
            Install
          </button>
        </div>
      ))}
    </div>
  );
} 