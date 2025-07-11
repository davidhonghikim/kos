# @kos/klf-client

Official KLF (Kind Link Framework) client for building kOS frontends.

## Quick Start

```bash
npm install @kos/klf-client
```

```typescript
import { KLFClient, createKLFClient } from '@kos/klf-client';

// Initialize client
const klf = await createKLFClient('http://localhost:30436');

// Discover services
const services = await klf.discoverServices();

// Make requests
const result = await klf.request('document.query', { 
  query: 'AI ethics research' 
});
```

## Available Services

- `document.upload` - Upload files for RAG processing
- `document.query` - Search documents using RAG
- `persona.chat` - Chat with AI personas  
- `vector.search` - Similarity search
- `auth.login` - User authentication
- `vault.store/retrieve` - Secret management
- `system.status` - System health

## React Hooks

```typescript
import { useKLFServices, useKLFRequest } from '@kos/klf-client';

function MyComponent() {
  const { services, loading } = useKLFServices(klfClient);
  const { request } = useKLFRequest(klfClient);
  
  const handleSearch = async () => {
    const results = await request('document.query', { 
      query: 'search term' 
    });
  };
}
```

## Backend Setup

Make sure the kOS backend is running:

```bash
cd griot-node/apps/persona-rag-bridge
npm run build
node dist-server/src/server.js
```

Backend will be available at `http://localhost:30436`
