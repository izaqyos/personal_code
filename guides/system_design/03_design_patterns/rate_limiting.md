# Rate Limiting

Control the rate of requests to protect systems from overload and abuse.

## Why Rate Limiting?

- **Prevent abuse**: Stop malicious users from overwhelming the system
- **Ensure fairness**: Share resources among users
- **Control costs**: Limit expensive operations
- **Maintain stability**: Prevent cascading failures
- **Meet SLAs**: Ensure quality for paying customers

## Rate Limiting Strategies

### User-Based

```
User A: 100 requests/minute
User B: 100 requests/minute
```

### IP-Based

```
IP 1.2.3.4: 60 requests/minute
```

**Caution:** Multiple users behind NAT share an IP.

### API Key-Based

```
API Key abc123: 1000 requests/hour
API Key xyz789: 10000 requests/hour (premium)
```

### Endpoint-Based

```
GET /api/users: 1000/min
POST /api/orders: 100/min (more expensive)
```

## Rate Limiting Algorithms

### Token Bucket

Tokens added at fixed rate; requests consume tokens.

```
Bucket Capacity: 10 tokens
Refill Rate: 2 tokens/second

Time 0: 10 tokens
  Request (1 token) → 9 tokens ✓
  Request (1 token) → 8 tokens ✓

Time 1: 8 + 2 = 10 tokens (capped at capacity)
  5 Requests → 5 tokens ✓

Time 2: 5 + 2 = 7 tokens
```

**Characteristics:**
- Allows burst up to bucket size
- Smooth rate limiting over time
- Memory: O(1) per key

```python
class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.refill_rate = refill_rate  # tokens per second
        self.tokens = capacity
        self.last_refill = time.time()
    
    def allow(self, tokens=1):
        self._refill()
        
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False
    
    def _refill(self):
        now = time.time()
        elapsed = now - self.last_refill
        refill = elapsed * self.refill_rate
        
        self.tokens = min(self.capacity, self.tokens + refill)
        self.last_refill = now
```

### Leaky Bucket

Requests processed at fixed rate; excess queued or dropped.

```
            ┌──────────┐
Requests ───>│  Queue   │───> Processed at fixed rate
            └──────────┘
                  │
            (overflow dropped)
```

**Characteristics:**
- Smooth output rate
- Queue provides buffering
- Memory: O(queue size)

### Fixed Window

Count requests in fixed time windows.

```
Window: 1 minute
Limit: 100 requests

00:00 - 01:00: [|||||||||||] 45 requests ✓
01:00 - 02:00: [|||||||||||||||||] 78 requests ✓
02:00 - 03:00: [||||||||||||||||||||||||] 120 requests → 100 ✓, 20 rejected
```

**Characteristics:**
- Simple to implement
- Memory efficient
- Problem: burst at window boundary

**Edge case:**
```
00:59: 90 requests
01:01: 90 requests
→ 180 requests in 2 seconds! (at window boundary)
```

### Sliding Window Log

Track exact timestamp of each request.

```python
class SlidingWindowLog:
    def __init__(self, limit, window_size):
        self.limit = limit
        self.window_size = window_size
        self.requests = []  # list of timestamps
    
    def allow(self):
        now = time.time()
        cutoff = now - self.window_size
        
        # Remove old requests
        self.requests = [r for r in self.requests if r > cutoff]
        
        if len(self.requests) < self.limit:
            self.requests.append(now)
            return True
        return False
```

**Characteristics:**
- Accurate
- No boundary issues
- Memory: O(requests in window)

### Sliding Window Counter

Hybrid: weighted count from current and previous windows.

```
Previous Window (60% elapsed): 80 requests
Current Window (40% elapsed): 30 requests

Weighted count = 80 × 0.6 + 30 = 78 requests
Limit: 100
→ Request allowed
```

```python
class SlidingWindowCounter:
    def __init__(self, limit, window_size):
        self.limit = limit
        self.window_size = window_size
        self.prev_count = 0
        self.curr_count = 0
        self.window_start = time.time()
    
    def allow(self):
        now = time.time()
        window_progress = (now - self.window_start) / self.window_size
        
        # New window?
        if window_progress >= 1:
            self.prev_count = self.curr_count
            self.curr_count = 0
            self.window_start = now
            window_progress = 0
        
        # Weighted count
        count = (
            self.prev_count * (1 - window_progress) + 
            self.curr_count
        )
        
        if count < self.limit:
            self.curr_count += 1
            return True
        return False
```

**Characteristics:**
- Good approximation
- Memory efficient: O(2) per key
- Smooth across boundaries

## Algorithm Comparison

| Algorithm | Memory | Accuracy | Burst Handling |
|-----------|--------|----------|----------------|
| Token Bucket | O(1) | Good | Allows burst |
| Leaky Bucket | O(queue) | Exact | Smooths burst |
| Fixed Window | O(1) | Approximate | Boundary burst |
| Sliding Log | O(n) | Exact | No burst |
| Sliding Counter | O(1) | Good | Smooths burst |

## Distributed Rate Limiting

### Centralized Store

```
Service 1 ─┐
Service 2 ──┼──> Redis ──> Rate Limit State
Service 3 ─┘
```

**Redis Implementation:**

```python
def check_rate_limit(user_id, limit, window):
    key = f"ratelimit:{user_id}"
    
    # Atomic increment with expiry
    pipe = redis.pipeline()
    pipe.incr(key)
    pipe.expire(key, window)
    count, _ = pipe.execute()
    
    return count <= limit
```

**Lua Script (atomic):**

```lua
local key = KEYS[1]
local limit = tonumber(ARGV[1])
local window = tonumber(ARGV[2])

local current = redis.call('INCR', key)
if current == 1 then
    redis.call('EXPIRE', key, window)
end

if current > limit then
    return 0
else
    return 1
end
```

### Local + Sync

Each node has local counter, synced periodically.

```
Node 1: Local count = 30
Node 2: Local count = 25
Node 3: Local count = 20
        ↓ sync ↓
Central: Total = 75 (distributed among nodes)
```

**Trade-off:** Less accurate but lower latency.

## Response Headers

Communicate limits to clients:

```http
HTTP/1.1 200 OK
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1640000000

HTTP/1.1 429 Too Many Requests
Retry-After: 30
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1640000030
```

## Rate Limiting Levels

### API Gateway

```
Client → API Gateway (rate limit) → Services
```

Centralized, protects all services.

### Application Level

```
Client → Service (rate limit in code)
```

Fine-grained, per-endpoint control.

### Load Balancer

```
Client → Load Balancer (rate limit) → Services
```

Network-level protection.

## Design Considerations

### Handling Exceeded Limits

**Return 429:**
```json
{
  "error": "rate_limit_exceeded",
  "retry_after": 30
}
```

**Queue request:**
```
Request → Queue → Process when capacity available
```

**Degrade gracefully:**
```
Serve cached response instead of real-time
```

### Race Conditions

Concurrent requests may exceed limit.

**Solution:** Atomic operations (Redis INCR, Lua scripts)

### Clock Skew

Distributed nodes may have different times.

**Solution:** Use centralized time source or logical clocks

## Popular Solutions

| Solution | Type | Notes |
|----------|------|-------|
| nginx | Server | `limit_req` module |
| Kong | Gateway | Plugin-based |
| AWS API Gateway | Cloud | Built-in throttling |
| Cloudflare | CDN | Edge rate limiting |
| Redis | Store | Lua scripts |

## Interview Tips

1. Explain why rate limiting is needed
2. Compare algorithms (token bucket vs sliding window)
3. Discuss distributed challenges
4. Plan for response handling (429, headers)
5. Consider different limiting dimensions (user, IP, endpoint)
6. Address edge cases (race conditions, clock skew)

## Related Topics

- [API Gateway](../02_building_blocks/api_gateway.md)
- [Load Balancers](../02_building_blocks/load_balancers.md)
- [Caching](../02_building_blocks/caching.md)
