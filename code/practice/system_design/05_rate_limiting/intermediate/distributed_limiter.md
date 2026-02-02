# Exercise: Distributed Rate Limiter

## Objective
Design a rate limiter that works across multiple servers.

## Problem Statement
You have 10 API servers behind a load balancer. Users can hit any server. You need to enforce a global rate limit of 100 requests/minute per user.

## Tasks

### Task 1: Problem Analysis

Why doesn't a local rate limiter work here?

```
User sends 100 requests:
  - Server 1 sees 10 requests → Allows all
  - Server 2 sees 10 requests → Allows all
  - ...
  - Server 10 sees 10 requests → Allows all
  
Result: ___
```

### Task 2: Centralized Counter Design

Design using Redis as centralized store:

1. **Key structure:**
   ```
   Key: ___
   Value: ___
   TTL: ___
   ```

2. **Implementation:**
   ```python
   def is_allowed(user_id, limit=100, window=60):
       # TODO: Implement using Redis
       pass
   ```

3. **Race condition handling:**
   How do you handle two servers checking simultaneously?

### Task 3: Redis Lua Script

Write a Lua script for atomic rate limiting:

```lua
-- KEYS[1] = rate limit key
-- ARGV[1] = limit
-- ARGV[2] = window (seconds)
-- ARGV[3] = current timestamp

-- TODO: Implement atomic rate limiting
-- Return: 1 if allowed, 0 if rejected
```

### Task 4: Failure Handling

Design for Redis failure scenarios:

1. **Redis unavailable for 5 seconds**
   - Behavior: ___
   - Trade-off: ___

2. **Redis latency spike (100ms → 500ms)**
   - Behavior: ___
   - Mitigation: ___

3. **Redis data loss (restart)**
   - Behavior: ___
   - Recovery: ___

### Task 5: Optimization Strategies

Design optimizations for:

1. **Local caching:**
   ```python
   class HybridRateLimiter:
       def __init__(self):
           self.local_cache = {}
           # TODO: Design local + Redis hybrid
   ```

2. **Batch updates:**
   Instead of checking Redis for every request, batch updates.
   - Trade-offs: ___

3. **Sticky sessions:**
   Route same user to same server.
   - Pros: ___
   - Cons: ___

---

<details>
<summary>Hints</summary>

- Redis INCR is atomic
- Lua scripts execute atomically in Redis
- Consider fail-open vs fail-closed
- Local caching can reduce Redis calls but adds inaccuracy

</details>

<details>
<summary>Solution</summary>

### Task 1: Problem Analysis

Result: 100 requests allowed (10 per server × 10 servers)

Problem: Each server has isolated view, no global coordination.

### Task 2: Centralized Counter Design

1. **Key structure:**
   ```
   Key: ratelimit:{user_id}:{window_start}
   Value: request count (integer)
   TTL: 60 seconds
   ```

2. **Implementation:**
   ```python
   import redis
   import time
   
   r = redis.Redis()
   
   def is_allowed(user_id, limit=100, window=60):
       now = int(time.time())
       window_start = (now // window) * window
       key = f"ratelimit:{user_id}:{window_start}"
       
       # Atomic increment
       count = r.incr(key)
       
       # Set expiry on first request
       if count == 1:
           r.expire(key, window)
       
       return count <= limit
   ```

3. **Race condition:** INCR is atomic, so no race condition for the counter itself. The expire race is benign (might extend TTL slightly).

### Task 3: Redis Lua Script

```lua
local key = KEYS[1]
local limit = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local now = tonumber(ARGV[3])

local window_start = math.floor(now / window) * window
local actual_key = key .. ":" .. window_start

local current = redis.call('INCR', actual_key)

if current == 1 then
    redis.call('EXPIRE', actual_key, window)
end

if current > limit then
    return 0
else
    return 1
end
```

### Task 4: Failure Handling

1. **Redis unavailable (5s):**
   - Fail-open: Allow all requests (risk abuse)
   - Fail-closed: Reject all (risk user impact)
   - Recommended: Fail-open with circuit breaker

2. **Latency spike:**
   - Add timeout (50ms) to Redis calls
   - Fall back to local limiting if timeout
   - Alert on sustained latency

3. **Redis data loss:**
   - All counters reset → temporary over-limit
   - Recovery: natural (counters rebuild)
   - Mitigation: Redis persistence (RDB/AOF)

### Task 5: Optimization

1. **Local caching:**
   ```python
   class HybridRateLimiter:
       def __init__(self, local_limit=10):
           self.local_counts = {}  # user_id → count
           self.local_limit = local_limit
       
       def is_allowed(self, user_id):
           # Fast local check first
           local_count = self.local_counts.get(user_id, 0)
           
           if local_count < self.local_limit:
               self.local_counts[user_id] = local_count + 1
               return True
           
           # Check Redis when local limit reached
           return self.check_redis(user_id)
   ```

2. **Batch updates:**
   - Aggregate locally, sync to Redis every N requests or M seconds
   - Trade-off: Less accurate (can over-limit by batch size)

3. **Sticky sessions:**
   - Pros: Local limiter works, less Redis calls
   - Cons: Uneven load, failover resets user's counter

</details>
