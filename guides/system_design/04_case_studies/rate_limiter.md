# Rate Limiter Design

Design a distributed rate limiting service for an API platform.

## Requirements

### Functional Requirements
- Limit requests per user/API key
- Support different rate limits per endpoint
- Support different limits per pricing tier
- Return informative response when limit exceeded

### Non-Functional Requirements
- Low latency (< 1ms overhead)
- Highly available
- Accurate (no significant over-limiting)
- Distributed (works across multiple servers)
- Fault tolerant

## Capacity Estimation

### Traffic
```
Requests: 1 billion/day
        = 11,500 requests/second average
Peak:   = 50,000 requests/second

Users: 10 million active users
API keys: 1 million
```

### Storage
```
Per rate limit entry: ~100 bytes
Active entries: 10M users × 5 endpoints = 50M entries
Storage: 50M × 100 bytes = 5 GB

→ Fits in memory (Redis)
```

## High-Level Design

```
                    ┌─────────────────────────┐
                    │      API Gateway        │
                    │  ┌───────────────────┐  │
  Request ─────────>│  │   Rate Limiter    │  │
                    │  │   Middleware      │  │
                    │  └────────┬──────────┘  │
                    └───────────┼─────────────┘
                                │
                    ┌───────────┼───────────┐
                    ▼           ▼           ▼
              ┌──────────┐┌──────────┐┌──────────┐
              │  Redis   ││  Redis   ││  Redis   │
              │ Cluster  ││ Cluster  ││ Cluster  │
              └──────────┘└──────────┘└──────────┘
```

## Rate Limiting Rules

### Rule Structure

```yaml
rules:
  - name: free_tier
    limits:
      - endpoint: "*"
        requests: 100
        window: 60  # seconds
  
  - name: pro_tier
    limits:
      - endpoint: "*"
        requests: 1000
        window: 60
      - endpoint: "/api/search"
        requests: 100
        window: 60  # expensive endpoint
  
  - name: enterprise
    limits:
      - endpoint: "*"
        requests: 10000
        window: 60
```

### Rule Storage

```sql
CREATE TABLE rate_limit_rules (
    id SERIAL PRIMARY KEY,
    tier VARCHAR(50),
    endpoint_pattern VARCHAR(200),
    max_requests INT,
    window_seconds INT,
    created_at TIMESTAMP
);
```

Load rules into memory on startup, refresh periodically.

## Algorithm: Sliding Window Counter

Best balance of accuracy and efficiency.

```python
import redis
import time

class SlidingWindowCounter:
    def __init__(self, redis_client):
        self.redis = redis_client
    
    def is_allowed(self, key, limit, window):
        now = time.time()
        current_window = int(now // window) * window
        prev_window = current_window - window
        
        # Keys for current and previous windows
        curr_key = f"{key}:{current_window}"
        prev_key = f"{key}:{prev_window}"
        
        # Get counts
        pipe = self.redis.pipeline()
        pipe.get(curr_key)
        pipe.get(prev_key)
        curr_count, prev_count = pipe.execute()
        
        curr_count = int(curr_count or 0)
        prev_count = int(prev_count or 0)
        
        # Calculate weighted count
        elapsed = now - current_window
        weight = 1 - (elapsed / window)
        weighted_count = prev_count * weight + curr_count
        
        if weighted_count >= limit:
            return False, limit - int(weighted_count)
        
        # Increment current window
        pipe = self.redis.pipeline()
        pipe.incr(curr_key)
        pipe.expire(curr_key, window * 2)
        pipe.execute()
        
        remaining = limit - int(weighted_count) - 1
        return True, remaining
```

## Redis Lua Script (Atomic)

```lua
-- rate_limit.lua
local key = KEYS[1]
local limit = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local now = tonumber(ARGV[3])

local current_window = math.floor(now / window) * window
local prev_window = current_window - window

local curr_key = key .. ":" .. current_window
local prev_key = key .. ":" .. prev_window

local curr_count = tonumber(redis.call('GET', curr_key) or 0)
local prev_count = tonumber(redis.call('GET', prev_key) or 0)

local elapsed = now - current_window
local weight = 1 - (elapsed / window)
local weighted_count = prev_count * weight + curr_count

if weighted_count >= limit then
    return {0, math.floor(limit - weighted_count)}
end

redis.call('INCR', curr_key)
redis.call('EXPIRE', curr_key, window * 2)

return {1, math.floor(limit - weighted_count - 1)}
```

## API Response

### Rate Limit Headers

```http
HTTP/1.1 200 OK
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1640000000
```

### Rate Limit Exceeded

```http
HTTP/1.1 429 Too Many Requests
Content-Type: application/json
Retry-After: 30
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1640000030

{
  "error": {
    "code": "rate_limit_exceeded",
    "message": "Rate limit exceeded. Try again in 30 seconds.",
    "retry_after": 30
  }
}
```

## Distributed Architecture

### Redis Cluster

```
┌─────────────────────────────────────────────────────┐
│                  Redis Cluster                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │ Shard 1  │  │ Shard 2  │  │ Shard 3  │         │
│  │ Keys A-H │  │ Keys I-P │  │ Keys Q-Z │         │
│  └──────────┘  └──────────┘  └──────────┘         │
│       │             │             │               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ Replica  │  │ Replica  │  │ Replica  │        │
│  └──────────┘  └──────────┘  └──────────┘        │
└─────────────────────────────────────────────────────┘
```

### Key Distribution

```
rate_limit:user:123:/api/users → hash → Shard 2
rate_limit:user:456:/api/orders → hash → Shard 1
```

Consistent hashing ensures same user always hits same shard.

## Handling Failures

### Redis Unavailable

**Options:**

1. **Fail open**: Allow all requests
   ```python
   try:
       return rate_limiter.is_allowed(...)
   except RedisError:
       return True  # Fail open
   ```

2. **Fail closed**: Block all requests
   ```python
   try:
       return rate_limiter.is_allowed(...)
   except RedisError:
       return False  # Fail closed
   ```

3. **Local fallback**: Use in-memory rate limiting
   ```python
   try:
       return rate_limiter.is_allowed(...)
   except RedisError:
       return local_rate_limiter.is_allowed(...)
   ```

### Synchronization Issues

With multiple Redis nodes, counts may be slightly off.

**Mitigation:**
- Accept slight inaccuracy
- Use slightly lower limits
- Periodic synchronization

## Performance Optimization

### Local Cache for Rules

```python
class RateLimitService:
    def __init__(self):
        self.rules_cache = {}
        self.rules_ttl = 300  # 5 minutes
    
    def get_rule(self, tier, endpoint):
        cache_key = f"{tier}:{endpoint}"
        
        if cache_key not in self.rules_cache:
            rule = db.query_rule(tier, endpoint)
            self.rules_cache[cache_key] = rule
        
        return self.rules_cache[cache_key]
```

### Connection Pooling

```python
redis_pool = redis.ConnectionPool(
    host='redis-cluster',
    port=6379,
    max_connections=100
)
redis_client = redis.Redis(connection_pool=redis_pool)
```

### Batch Operations

```python
# Check multiple limits at once
def check_limits(user_id, endpoint, limits):
    pipe = redis.pipeline()
    
    for limit in limits:
        key = f"rate:{user_id}:{limit['scope']}"
        pipe.evalsha(RATE_LIMIT_SCRIPT, 1, key, limit['max'], limit['window'])
    
    results = pipe.execute()
    return all(r[0] for r in results)
```

## Advanced Features

### Burst Allowance

Allow short bursts above limit:

```python
# Token bucket with burst
token_bucket = {
    'capacity': 100,      # Max tokens (burst size)
    'refill_rate': 10,    # Tokens per second
}
```

### Adaptive Rate Limiting

Adjust limits based on system load:

```python
def get_dynamic_limit(base_limit):
    cpu_usage = get_cpu_usage()
    
    if cpu_usage > 80:
        return base_limit * 0.5  # Reduce limit
    elif cpu_usage > 60:
        return base_limit * 0.75
    else:
        return base_limit
```

### IP-Based Fallback

For unauthenticated requests:

```python
def get_rate_limit_key(request):
    if request.api_key:
        return f"key:{request.api_key}"
    elif request.user_id:
        return f"user:{request.user_id}"
    else:
        return f"ip:{request.ip}"
```

## Monitoring

### Metrics

```python
# Track rate limiting metrics
rate_limit_checks_total.inc()
rate_limit_allowed_total.inc()  # or rejected
rate_limit_latency.observe(duration)
```

### Dashboards

- Requests allowed vs rejected
- Rate limit hits by tier
- p99 latency
- Redis cluster health

## Interview Tips

1. Start with requirements (latency, accuracy)
2. Choose algorithm (sliding window counter)
3. Explain distributed challenges
4. Discuss failure handling (fail open vs closed)
5. Design for different limiting dimensions
6. Consider response format (headers, 429)

## Related Topics

- [Rate Limiting Pattern](../03_design_patterns/rate_limiting.md)
- [API Gateway](../02_building_blocks/api_gateway.md)
- [Caching](../02_building_blocks/caching.md)
