# Vercel KV (Redis)

## What is Vercel KV?

Vercel KV is a serverless Redis database optimized for Vercel deployments.

**Key Features:**
- Key-value storage (like Redis)
- Serverless (no connection management)
- Global distribution
- REST API interface

## Basic Operations

### Setup

```javascript
import { kv } from '@vercel/kv'
```

### Get/Set

```javascript
// Set a value
await kv.set('key', 'value')

// Set with expiration (in seconds)
await kv.set('key', 'value', { ex: 3600 })  // Expires in 1 hour

// Get a value
const value = await kv.get('key')

// Get with type
const data = await kv.get<GameState>('game_state')
```

### Delete

```javascript
await kv.del('key')
await kv.del('key1', 'key2', 'key3')  // Multiple keys
```

### Check Existence

```javascript
const exists = await kv.exists('key')  // Returns 0 or 1
```

## Data Types

### Strings

```javascript
await kv.set('name', 'Alice')
const name = await kv.get('name')  // 'Alice'

// Increment number stored as string
await kv.incr('counter')   // 1
await kv.incr('counter')   // 2
await kv.incrby('counter', 5)  // 7
```

### JSON Objects

```javascript
// Automatically serialized/deserialized
const gameState = {
  participants: [{ id: '1', name: 'Alice' }],
  scores: { '1': 25 },
  screen: 'quiz'
}

await kv.set('game_state', gameState)

const state = await kv.get('game_state')
// { participants: [...], scores: {...}, screen: 'quiz' }
```

### Lists

```javascript
// Push to list
await kv.lpush('messages', 'Hello')
await kv.rpush('messages', 'World')

// Get all items
const messages = await kv.lrange('messages', 0, -1)

// Pop items
const first = await kv.lpop('messages')
const last = await kv.rpop('messages')
```

### Hashes (Object fields)

```javascript
// Set hash field
await kv.hset('user:1', { name: 'Alice', score: 100 })

// Get specific field
const name = await kv.hget('user:1', 'name')

// Get all fields
const user = await kv.hgetall('user:1')
// { name: 'Alice', score: 100 }

// Increment field
await kv.hincrby('user:1', 'score', 10)
```

### Sets (Unique values)

```javascript
// Add to set
await kv.sadd('participants', 'alice', 'bob')

// Check membership
const isMember = await kv.sismember('participants', 'alice')

// Get all members
const members = await kv.smembers('participants')

// Remove from set
await kv.srem('participants', 'alice')
```

## In This Project

### Game State Storage

```javascript
const GAME_KEY = 'quiz_game_state'

const defaultState = {
  participants: [],
  scores: {},
  responses: [],
  screen: 'join',
  currentQuestionIndex: 0,
  activeQuestions: null,
  quizStarted: false,
  lastUpdated: Date.now()
}

// Get current state
async function getGameState() {
  try {
    const state = await kv.get(GAME_KEY)
    return state || { ...defaultState }
  } catch (error) {
    console.error('KV get error:', error)
    return { ...defaultState }
  }
}

// Save state
async function setGameState(state) {
  try {
    await kv.set(GAME_KEY, state)
    return true
  } catch (error) {
    console.error('KV set error:', error)
    return false
  }
}
```

### Usage in API

```javascript
export default async function handler(req, res) {
  if (req.method === 'GET') {
    const gameState = await getGameState()
    return res.status(200).json(gameState)
  }

  if (req.method === 'POST') {
    const { action, payload } = req.body
    let gameState = await getGameState()

    // Modify state based on action
    switch (action) {
      case 'JOIN':
        gameState.participants.push(payload.participant)
        break
      // ... other actions
    }

    gameState.lastUpdated = Date.now()
    await setGameState(gameState)
    return res.status(200).json(gameState)
  }
}
```

## Patterns

### Atomic Updates

**Problem:** Multiple clients updating same key

```javascript
// ❌ Race condition
const state = await kv.get('counter')
await kv.set('counter', state + 1)

// ✅ Atomic operation
await kv.incr('counter')
```

### Optimistic Locking

```javascript
// Use lastUpdated as version
async function updateIfNotStale(newState, expectedVersion) {
  const current = await kv.get('game_state')
  
  if (current.lastUpdated !== expectedVersion) {
    throw new Error('State changed, please retry')
  }
  
  await kv.set('game_state', newState)
}
```

### TTL (Time to Live)

```javascript
// Session that expires
await kv.set('session:abc', userData, { ex: 3600 })  // 1 hour

// Game that auto-resets after 24 hours
await kv.set('game_state', state, { ex: 86400 })
```

### Multiple Games (Namespacing)

```javascript
const getGameKey = (gameId) => `game:${gameId}:state`

// Each game has its own state
await kv.set(getGameKey('game123'), gameState)
await kv.get(getGameKey('game123'))
```

## Error Handling

```javascript
async function safeGet(key, defaultValue) {
  try {
    const value = await kv.get(key)
    return value ?? defaultValue
  } catch (error) {
    console.error(`KV error getting ${key}:`, error)
    return defaultValue
  }
}

async function safeSet(key, value) {
  try {
    await kv.set(key, value)
    return true
  } catch (error) {
    console.error(`KV error setting ${key}:`, error)
    return false
  }
}
```

## Limits (Hobby)

| Resource | Limit |
|----------|-------|
| Storage | 256 MB |
| Daily Commands | 30,000 |
| Max Key Size | 512 B |
| Max Value Size | 100 KB (1 MB with chunks) |
| Connections | Serverless (pooled) |

## Best Practices

1. **Use meaningful keys**
   ```javascript
   // Good
   'game:abc123:state'
   'user:12345:preferences'
   
   // Bad
   'data1'
   'x'
   ```

2. **Set TTL on temporary data**
   ```javascript
   await kv.set('temp_code', code, { ex: 300 })  // 5 min
   ```

3. **Handle missing keys gracefully**
   ```javascript
   const value = await kv.get('key')
   if (!value) {
     // Key doesn't exist
   }
   ```

4. **Minimize round trips**
   ```javascript
   // Instead of multiple gets
   const a = await kv.get('a')
   const b = await kv.get('b')
   
   // Use batch operations
   const [a, b] = await Promise.all([
     kv.get('a'),
     kv.get('b')
   ])
   ```

## Resources

- [Vercel KV Docs](https://vercel.com/docs/storage/vercel-kv)
- [Redis Commands Reference](https://redis.io/commands/)
- [KV Quickstart](https://vercel.com/docs/storage/vercel-kv/quickstart)
