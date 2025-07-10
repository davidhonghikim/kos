import React, { useEffect, useState } from 'react'
import { getEnv, updateEnv } from './admin-api'

export const EnvEditor = () => {
  const [env, setEnv] = useState<Record<string, string>>({})

  useEffect(() => {
    getEnv().then(setEnv)
  }, [])

  const handleChange = (k: string, v: string) => {
    setEnv({ ...env, [k]: v })
  }

  const handleSave = () => {
    updateEnv(env)
  }

  return (
    <div>
      <h2 className="text-lg font-semibold mb-2">Environment Variables</h2>
      <table className="table-auto w-full">
        <tbody>
          {Object.entries(env).map(([key, value]) => (
            <tr key={key}>
              <td className="p-2 font-mono text-sm">{key}</td>
              <td className="p-2">
                <input
                  value={value}
                  onChange={(e) => handleChange(key, e.target.value)}
                  className="w-full border rounded px-2 py-1 text-sm"
                />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <button onClick={handleSave} className="mt-4 px-4 py-2 bg-blue-600 text-white rounded">
        Save Changes
      </button>
    </div>
  )
} 