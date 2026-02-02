# Real-Time Sync Patterns

## The Challenge

When multiple users interact with shared state:
- How do they see the same data?
- How do changes propagate?
- How do we handle conflicts?

## Sync Approaches

### 1. Polling (Used in This Project)

**How it works:**
- Client periodically requests latest state from server
- Simple HTTP GET requests at fixed intervals

```javascript
useEffect(() => {
  const fetchState = async () => {
    const res = await fetch('/api/game');
    const data = await res.json();
    setState(data);
  };

  fetchState(); // Initial fetch
  const interval = setInterval(fetchState, 1000); // Poll every second
  
  return () => clearInterval(interval);
}, []);
```

**Pros:**
- ✅ Simple implementation
- ✅ Works with any HTTP server
- ✅ No special infrastructure needed
- ✅ Reliable (HTTP is well-understood)

**Cons:**
- ❌ 1-second latency (or whatever interval)
- ❌ Wasted requests if nothing changed
- ❌ Higher server load at scale

**Best for:**
- Small to medium user counts
- Tolerance for slight delays
- Simple deployments

### 2. Long Polling

**How it works:**
- Client makes request, server holds it open
- Server responds when data changes or timeout
- Client immediately makes new request

```javascript
async function longPoll() {
  try {
    const res = await fetch('/api/game?wait=true', {
      signal: AbortSignal.timeout(30000)
    });
    const data = await res.json();
    setState(data);
  } finally {
    longPoll(); // Immediately reconnect
  }
}
```

**Pros:**
- ✅ Lower latency than polling
- ✅ Fewer wasted requests
- ✅ Works with most servers

**Cons:**
- ❌ Connection management complexity
- ❌ Server needs to support held connections
- ❌ Some proxies don't like long-held connections

### 3. WebSockets

**How it works:**
- Persistent bidirectional connection
- Server pushes updates instantly
- Client sends actions directly

```javascript
const socket = new WebSocket('wss://example.com/game');

socket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  setState(data);
};

const sendAction = (action) => {
  socket.send(JSON.stringify(action));
};
```

**Pros:**
- ✅ Instant updates (true real-time)
- ✅ Efficient (no request overhead)
- ✅ Bidirectional communication

**Cons:**
- ❌ Requires WebSocket server
- ❌ Connection state management
- ❌ Harder to scale (sticky sessions)
- ❌ Not all platforms support easily (e.g., basic serverless)

**Best for:**
- High-frequency updates
- Chat, games, collaboration tools
- When latency matters

### 4. Server-Sent Events (SSE)

**How it works:**
- Server pushes events over HTTP
- One-way: server to client only
- Client sends via regular HTTP POST

```javascript
const eventSource = new EventSource('/api/game/stream');

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  setState(data);
};

const sendAction = async (action) => {
  await fetch('/api/game', {
    method: 'POST',
    body: JSON.stringify(action)
  });
};
```

**Pros:**
- ✅ Simpler than WebSockets
- ✅ Works over HTTP (easier deployment)
- ✅ Auto-reconnect built-in

**Cons:**
- ❌ One-way only (server → client)
- ❌ Limited browser connections (6 per domain)
- ❌ Text-only (no binary)

## Optimistic Updates

**Pattern:** Update local state immediately, sync with server in background.

```javascript
const submitAnswer = async (answer) => {
  // 1. Optimistic update (instant feedback)
  setLocalAnswer(answer);
  
  try {
    // 2. Send to server
    await fetch('/api/game', {
      method: 'POST',
      body: JSON.stringify({ action: 'SUBMIT_ANSWER', payload: answer })
    });
  } catch (error) {
    // 3. Rollback on error
    setLocalAnswer(null);
    setError('Failed to submit');
  }
};
```

**Benefits:**
- Feels instant to user
- Works even with polling latency
- Graceful error handling

## Conflict Resolution

### Last Write Wins (Simple)
```javascript
// Server always uses latest value
gameState.scores[participantId] = newScore;
```

### Timestamps
```javascript
// Only accept if newer
if (incomingUpdate.timestamp > currentState.timestamp) {
  gameState = incomingUpdate;
}
```

### Version Numbers
```javascript
// Check version before accepting
if (incomingUpdate.version === currentState.version + 1) {
  gameState = incomingUpdate;
} else {
  // Conflict! Handle appropriately
}
```

### Merge Strategies
```javascript
// Quiz app example: merge responses, don't overwrite
const newResponses = [
  ...existingResponses.filter(r => 
    !incomingResponses.find(ir => 
      ir.participantId === r.participantId && 
      ir.questionIndex === r.questionIndex
    )
  ),
  ...incomingResponses
];
```

## This Project's Approach

### Architecture
```
┌─────────────┐   Poll (GET)   ┌─────────────┐
│   Client    │ ◄───────────── │   Vercel    │
│             │                │   KV Store  │
│             │ ──────────────►│             │
└─────────────┘  Action (POST) └─────────────┘
```

### Flow
1. Client polls `/api/game` every second
2. Server returns current state from KV
3. Client compares `lastUpdated` timestamp
4. Only updates if state changed
5. Actions POST to `/api/game`
6. Server updates KV, returns new state

### Code Pattern
```javascript
const lastUpdatedRef = useRef(0);

const fetchState = async () => {
  const res = await fetch('/api/game');
  const data = await res.json();
  
  // Only update if state actually changed
  if (data.lastUpdated !== lastUpdatedRef.current) {
    lastUpdatedRef.current = data.lastUpdated;
    setGameState(data);
  }
};
```

## Scaling Considerations

### Current Limits (Polling + KV)
- ~10-50 concurrent users comfortable
- 1 second sync delay acceptable
- No persistent connections to manage

### Scaling Up
1. **Increase poll interval** (2-5 seconds) for more users
2. **Add caching** (edge cache with short TTL)
3. **Switch to WebSockets** (for >100 users)
4. **Use dedicated real-time service** (Pusher, Ably, Firebase)

### Example: Adding Pusher
```javascript
import Pusher from 'pusher-js';

const pusher = new Pusher('APP_KEY', { cluster: 'us2' });
const channel = pusher.subscribe('quiz-game');

channel.bind('state-update', (data) => {
  setGameState(data);
});

// API triggers Pusher event after state change
// Clients receive instantly via WebSocket
```

## Resources

- [Polling vs WebSockets](https://ably.com/topic/websockets-vs-polling)
- [Server-Sent Events MDN](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
- [Optimistic Updates](https://tanstack.com/query/latest/docs/react/guides/optimistic-updates)
