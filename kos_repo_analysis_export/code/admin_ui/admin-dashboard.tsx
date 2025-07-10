import React, { useState } from 'react'
import { AgentManager } from './agent-manager'
import { IntentLog } from './intent-log'
import { VaultAdmin } from './vault-admin'
import { PluginControl } from './plugin-control'
import { EnvEditor } from './env-editor'
import { AuthUsers } from './auth-users'

type Tab = 'agents' | 'intents' | 'vault' | 'plugins' | 'env' | 'users'

export const AdminDashboard = () => {
  const [tab, setTab] = useState<Tab>('agents')

  return (
    <div className="w-full min-h-screen bg-gray-50">
      <header className="flex justify-between items-center p-4 shadow bg-white">
        <h1 className="text-xl font-bold">KOS Admin Console</h1>
        <nav className="space-x-4">
          {(['agents', 'intents', 'vault', 'plugins', 'env', 'users'] as Tab[]).map((t) => (
            <button key={t} onClick={() => setTab(t)} className="text-blue-600 hover:underline capitalize">
              {t}
            </button>
          ))}
        </nav>
      </header>
      <main className="p-4">
        {tab === 'agents' && <AgentManager />}
        {tab === 'intents' && <IntentLog />}
        {tab === 'vault' && <VaultAdmin />}
        {tab === 'plugins' && <PluginControl />}
        {tab === 'env' && <EnvEditor />}
        {tab === 'users' && <AuthUsers />}
      </main>
    </div>
  )
} 