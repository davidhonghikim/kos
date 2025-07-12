import React, { useState } from 'react'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState('dashboard')

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <h1 className="logo">kOS</h1>
          <nav className="nav">
            <button 
              className={`nav-item ${activeTab === 'dashboard' ? 'active' : ''}`}
              onClick={() => setActiveTab('dashboard')}
            >
              Dashboard
            </button>
            <button 
              className={`nav-item ${activeTab === 'chat' ? 'active' : ''}`}
              onClick={() => setActiveTab('chat')}
            >
              Chat
            </button>
            <button 
              className={`nav-item ${activeTab === 'services' ? 'active' : ''}`}
              onClick={() => setActiveTab('services')}
            >
              Services
            </button>
            <button 
              className={`nav-item ${activeTab === 'agents' ? 'active' : ''}`}
              onClick={() => setActiveTab('agents')}
            >
              Agents
            </button>
          </nav>
        </div>
      </header>

      <main className="main">
        {activeTab === 'dashboard' && (
          <div className="dashboard">
            <h2>kOS Dashboard</h2>
            <div className="dashboard-grid">
              <div className="card">
                <h3>System Status</h3>
                <p>All systems operational</p>
              </div>
              <div className="card">
                <h3>Active Agents</h3>
                <p>3 agents running</p>
              </div>
              <div className="card">
                <h3>Services</h3>
                <p>12 services active</p>
              </div>
              <div className="card">
                <h3>Kitchen</h3>
                <p>Kitchen system ready</p>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'chat' && (
          <div className="chat">
            <h2>Multi-Agent Chat</h2>
            <div className="chat-container">
              <div className="chat-messages">
                <div className="message">
                  <span className="agent">System:</span> Welcome to kOS chat interface
                </div>
              </div>
              <div className="chat-input">
                <input type="text" placeholder="Type your message..." />
                <button>Send</button>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'services' && (
          <div className="services">
            <h2>Service Management</h2>
            <div className="services-grid">
              <div className="service-card">
                <h3>Backend API</h3>
                <p>Status: Running</p>
                <p>Port: 8000</p>
              </div>
              <div className="service-card">
                <h3>Frontend</h3>
                <p>Status: Running</p>
                <p>Port: 3000</p>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'agents' && (
          <div className="agents">
            <h2>Agent Management</h2>
            <div className="agents-list">
              <div className="agent-item">
                <h3>KLF Agent</h3>
                <p>Status: Active</p>
              </div>
              <div className="agent-item">
                <h3>Kitchen Agent</h3>
                <p>Status: Active</p>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App 