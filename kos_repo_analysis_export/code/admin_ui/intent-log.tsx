import React, { useEffect, useState } from 'react'
import { getIntentLog } from './admin-api'

export const IntentLog = () => {
  const [log, setLog] = useState([])

  useEffect(() => {
    getIntentLog().then(setLog)
  }, [])

  return (
    <div>
      <h2 className="text-lg font-semibold mb-2">Intent Log</h2>
      <ul className="bg-white border p-4 max-h-[400px] overflow-auto space-y-2">
        {log.map((entry: any, i: number) => (
          <li key={i} className="text-xs bg-gray-50 p-2 rounded shadow">
            <code>{JSON.stringify(entry)}</code>
          </li>
        ))}
      </ul>
    </div>
  )
} 