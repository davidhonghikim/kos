import React, { useEffect, useState } from 'react'
import { getPlugins, togglePlugin } from './admin-api'

export const PluginControl = () => {
  const [plugins, setPlugins] = useState([])

  useEffect(() => {
    getPlugins().then(setPlugins)
  }, [])

  return (
    <div>
      <h2 className="text-lg font-semibold mb-2">Plugin Control</h2>
      <ul>
        {plugins.map((p: any) => (
          <li key={p.name} className="flex justify-between border-b py-1">
            <span>{p.name}</span>
            <button
              onClick={() => togglePlugin(p.name)}
              className={`text-sm px-2 py-1 rounded ${
                p.enabled ? 'bg-red-200' : 'bg-green-200'
              }`}
            >
              {p.enabled ? 'Disable' : 'Enable'}
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
} 