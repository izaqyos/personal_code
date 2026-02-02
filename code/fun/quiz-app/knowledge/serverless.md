# Serverless Functions

## What are Serverless Functions?

Serverless functions are small, single-purpose pieces of code that run on-demand without managing servers.

```
Traditional Server         Serverless Function
┌────────────────┐        ┌────────────────┐
│ Always running │        │ Run on request │
│ Pay for uptime │        │ Pay per invoke │
│ You manage     │        │ Platform manages│
│ Scale manually │        │ Auto-scales    │
└────────────────┘        └────────────────┘
```

## Vercel Serverless Functions

### How It Works

1. Create file in `/api` directory
2. Export default function
3. Vercel deploys as serverless endpoint

```javascript
// api/hello.js
export default function handler(req, res) {
  res.status(200).json({ message: 'Hello World' });
}
```

**Becomes:** `https://your-app.vercel.app/api/hello`

### Request Object (req)

```javascript
export default function handler(req, res) {
  req.method    // 'GET', 'POST', 'PUT', 'DELETE'
  req.query     // URL params: /api/user?id=123 → { id: '123' }
  req.body      // POST body (auto-parsed if JSON)
  req.headers   // Request headers
  req.cookies   // Cookies
}
```

### Response Object (res)

```javascript
export default function handler(req, res) {
  // Set status
  res.status(200)
  res.status(404)
  
  // Send JSON
  res.json({ data: 'value' })
  
  // Send text
  res.send('Hello')
  
  // Set headers
  res.setHeader('Content-Type', 'application/json')
  
  // Redirect
  res.redirect('/other-page')
  
  // Chain
  res.status(201).json({ created: true })
}
```

## This Project's API

### File: `api/game.js`

```javascript
import { kv } from '@vercel/kv'

export default async function handler(req, res) {
  // CORS headers for cross-origin requests
  res.setHeader('Access-Control-Allow-Origin', '*')
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type')

  // Handle preflight
  if (req.method === 'OPTIONS') {
    return res.status(200).end()
  }

  // GET - Fetch state
  if (req.method === 'GET') {
    const state = await kv.get('quiz_game_state')
    return res.status(200).json(state || defaultState)
  }

  // POST - Process action
  if (req.method === 'POST') {
    const { action, payload } = req.body
    // ... process action
    await kv.set('quiz_game_state', newState)
    return res.status(200).json(newState)
  }

  return res.status(405).json({ error: 'Method not allowed' })
}
```

## Request/Response Flow

```
┌─────────────────────────────────────────────────────────────┐
│                      Browser                                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ fetch('/api/game', { method: 'POST', body: ... })    │   │
│  └───────────────────────────┬──────────────────────────┘   │
└──────────────────────────────┼──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                   Vercel Edge Network                         │
│  1. Route to nearest region                                  │
│  2. Cold start function if not warm                          │
│  3. Execute handler                                          │
│  4. Return response                                          │
└───────────────────────────┬─────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                   api/game.js (Serverless)                    │
│  ┌────────────────────────────────────────────────────┐     │
│  │ handler(req, res) {                                │     │
│  │   const state = await kv.get('key')                │     │
│  │   // process                                       │     │
│  │   await kv.set('key', newState)                    │     │
│  │   res.json(newState)                               │     │
│  │ }                                                  │     │
│  └────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## Cold Starts

### What is a Cold Start?

When a function hasn't run recently, Vercel needs to:
1. Provision execution environment
2. Load your code
3. Initialize dependencies

**Duration:** 100ms - 1s (depending on code size)

### Mitigating Cold Starts

1. **Keep functions small**
   ```javascript
   // Good: Single purpose
   // api/game.js - game state only
   // api/quiz.js - quiz data only
   
   // Bad: Everything in one function
   // api/all-endpoints.js
   ```

2. **Minimize dependencies**
   ```javascript
   // Import only what you need
   import { kv } from '@vercel/kv'
   // Not: import * as vercel from '@vercel/*'
   ```

3. **Use Edge Functions** (when possible)
   ```javascript
   // api/fast.js
   export const config = {
     runtime: 'edge'
   }
   
   export default async function handler(request) {
     return new Response('Fast!')
   }
   ```

## Error Handling

```javascript
export default async function handler(req, res) {
  try {
    const data = await riskyOperation()
    return res.status(200).json(data)
  } catch (error) {
    console.error('API Error:', error)
    
    // Don't expose internal errors
    return res.status(500).json({ 
      error: 'Internal server error',
      // Only in dev:
      ...(process.env.NODE_ENV === 'development' && { 
        details: error.message 
      })
    })
  }
}
```

## CORS Handling

**Why CORS?** Browser security prevents requests to different origins.

```javascript
export default function handler(req, res) {
  // Allow requests from any origin
  res.setHeader('Access-Control-Allow-Origin', '*')
  
  // Or specific origins
  res.setHeader('Access-Control-Allow-Origin', 'https://mysite.com')
  
  // Allow specific methods
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
  
  // Allow specific headers
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization')
  
  // Handle preflight
  if (req.method === 'OPTIONS') {
    return res.status(200).end()
  }
  
  // Your logic
}
```

## Environment Variables

### Setting in Vercel

1. Dashboard → Project → Settings → Environment Variables
2. Or via CLI: `vercel env add`

### Accessing in Code

```javascript
export default function handler(req, res) {
  const apiKey = process.env.API_KEY
  const dbUrl = process.env.DATABASE_URL
}
```

### Local Development

Create `.env.local`:
```
API_KEY=your-key-here
DATABASE_URL=postgres://...
```

Pull from Vercel:
```bash
vercel env pull .env.local
```

## Limits (Hobby Plan)

| Resource | Limit |
|----------|-------|
| Execution Time | 10 seconds |
| Memory | 1024 MB |
| Payload Size | 4.5 MB |
| Concurrent Executions | 1000 |

## Best Practices

1. **Keep functions focused**
   - One endpoint = one file
   - Single responsibility

2. **Return quickly**
   - Long operations → background jobs
   - Set timeouts on external calls

3. **Log appropriately**
   ```javascript
   console.log('Info:', data)     // Informational
   console.error('Error:', err)   // Errors
   // Vercel captures both
   ```

4. **Validate input**
   ```javascript
   if (!req.body?.action) {
     return res.status(400).json({ error: 'Action required' })
   }
   ```

5. **Use proper HTTP status codes**
   - 200: Success
   - 201: Created
   - 400: Bad request
   - 401: Unauthorized
   - 404: Not found
   - 500: Server error

## Resources

- [Vercel Serverless Docs](https://vercel.com/docs/functions/serverless-functions)
- [Edge Functions](https://vercel.com/docs/functions/edge-functions)
- [API Routes Guide](https://vercel.com/guides/getting-started-with-vercel-apis)
