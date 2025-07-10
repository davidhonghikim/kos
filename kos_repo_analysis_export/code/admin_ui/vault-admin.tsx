import React, { useEffect, useState } from 'react'
import { getVaultKeys, getVaultValue } from './admin-api'

export const VaultAdmin = () => {
  const [keys, setKeys] = useState<string[]>([])
  const [selected, setSelected] = useState<string | null>(null)
  const [value, setValue] = useState<any>()

  useEffect(() => {
    getVaultKeys().then(setKeys)
  }, [])

  useEffect(() => {
    if (selected) getVaultValue(selected).then(setValue)
  }, [selected])

  return (
    <div className="grid grid-cols-2 gap-4">
      <div>
        <h3 className="font-medium mb-2">Vault Keys</h3>
        <ul className="space-y-1">
          {keys.map((k) => (
            <li key={k}>
              <button onClick={() => setSelected(k)} className="text-blue-600 hover:underline">
                {k}
              </button>
            </li>
          ))}
        </ul>
      </div>
      <div>
        {selected && (
          <>
            <h3 className="font-medium mb-2">Value for: {selected}</h3>
            <pre className="bg-gray-100 p-4 rounded text-sm overflow-auto max-h-[300px]">
              {JSON.stringify(value, null, 2)}
            </pre>
          </>
        )}
      </div>
    </div>
  )
} 