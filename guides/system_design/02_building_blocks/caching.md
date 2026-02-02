# Caching

Store frequently accessed data in fast storage to reduce latency and load.

## Why Cache?

- **Reduce latency**: Memory access ~100ns vs disk ~16μs
- **Reduce load**: Fewer database queries
- **Reduce cost**: Less compute/database usage
- **Improve availability**: Serve from cache if origin fails

## Cache Locations

### Multi-Level Caching

```
Client → Browser Cache → CDN → App Cache → DB Cache → Database
```

### Cache Levels

| Level | Location | Latency | Size |
|-------|----------|---------|------|
| L1 | Browser | 0 | 100s MB |
| L2 | CDN Edge | 10-50ms | 10s GB |
| L3 | Application | 1-5ms | 10s GB |
| L4 | Database | 0.1ms | GBs |
| L5 | Query Cache | 0.01ms | GBs |

## Caching Strategies

### Cache-Aside (Lazy Loading)

Application manages cache explicitly.

```python
def get_user(user_id):
    # 1. Check cache
    user = cache.get(f"user:{user_id}")
    if user:
        return user
    
    # 2. Cache miss - fetch from DB
    user = db.query("SELECT * FROM users WHERE id = ?", user_id)
    
    # 3. Populate cache
    cache.set(f"user:{user_id}", user, ttl=3600)
    return user
```

**Pros:**
- Only requested data is cached
- Cache failures don't break the app
- Simple to implement

**Cons:**
- Cache miss = 3 round trips
- Stale data possible

### Read-Through

Cache handles fetching on miss.

```
App → Cache → (miss) → Cache fetches from DB → returns to App
```

**Pros:**
- Simpler application code
- Consistent caching logic

**Cons:**
- Cache becomes critical path
- Less flexibility

### Write-Through

Write to cache and DB synchronously.

```
App → Cache → DB (synchronous)
          ↓
       returns
```

**Pros:**
- Cache always consistent with DB
- No stale data

**Cons:**
- Higher write latency
- Unused data may be cached

### Write-Behind (Write-Back)

Write to cache, async write to DB.

```
App → Cache → returns immediately
         ↓
    (async queue)
         ↓
        DB
```

**Pros:**
- Low write latency
- Batch writes to DB

**Cons:**
- Data loss risk if cache fails
- Complexity

### Write-Around

Write directly to DB, bypass cache.

```
Write: App → DB
Read:  App → Cache → (miss) → DB
```

**Pros:**
- Good for write-heavy, read-rare data
- No cache pollution

**Cons:**
- First read always misses

## Cache Invalidation

> "There are only two hard things in Computer Science: cache invalidation and naming things." - Phil Karlton

### TTL (Time-To-Live)

```python
cache.set("user:123", user_data, ttl=3600)  # Expires in 1 hour
```

**Pros:** Simple, automatic cleanup
**Cons:** Stale data until expiry

### Event-Based Invalidation

```python
def update_user(user_id, data):
    db.update(user_id, data)
    cache.delete(f"user:{user_id}")  # Invalidate
```

**Pros:** Immediate consistency
**Cons:** Requires coordination

### Version-Based Keys

```python
cache_key = f"user:{user_id}:v{version}"
```

**Pros:** Atomic updates
**Cons:** Key management complexity

## Cache Eviction Policies

When cache is full, what to remove?

| Policy | Description | Use Case |
|--------|-------------|----------|
| LRU | Least Recently Used | General purpose |
| LFU | Least Frequently Used | Popular items |
| FIFO | First In First Out | Simple |
| Random | Random eviction | When access pattern unknown |
| TTL | Expire by time | Time-sensitive data |

### LRU Implementation

```
Most Recent ← [A] ↔ [B] ↔ [C] ↔ [D] → Least Recent

Access B: Move to front
         [B] ↔ [A] ↔ [C] ↔ [D]

Add E (full): Evict D, add E to front
         [E] ↔ [B] ↔ [A] ↔ [C]
```

## Distributed Caching

### Partitioning

**Consistent Hashing:**
```
hash(key) → Virtual ring → Node
```

Minimizes redistribution when nodes change.

### Replication

```
       ┌──────────────────────────────┐
       │       Cache Cluster          │
       │  ┌────┐  ┌────┐  ┌────┐     │
Write ─┼─>│ N1 │──│ N2 │──│ N3 │     │
       │  └────┘  └────┘  └────┘     │
       └──────────────────────────────┘
```

**Primary-Replica:** Write to primary, replicate to replicas
**Multi-Master:** Write to any node

## Cache Patterns

### Cache Warming

Pre-populate cache before traffic.

```python
def warm_cache():
    popular_items = db.query("SELECT * FROM products ORDER BY views DESC LIMIT 1000")
    for item in popular_items:
        cache.set(f"product:{item.id}", item)
```

### Cache Stampede Prevention

Many requests hit cache miss simultaneously.

**Solution 1: Locking**
```python
def get_with_lock(key):
    value = cache.get(key)
    if value:
        return value
    
    if acquire_lock(key):
        value = fetch_from_db()
        cache.set(key, value)
        release_lock(key)
    else:
        wait_for_key(key)  # Wait for lock holder
    return cache.get(key)
```

**Solution 2: Probabilistic Early Expiration**
```python
def get_with_early_refresh(key):
    value, expiry = cache.get_with_expiry(key)
    ttl_remaining = expiry - now()
    
    # Probabilistically refresh before expiry
    if random() < (1 - ttl_remaining / original_ttl):
        async_refresh(key)
    
    return value
```

### Request Coalescing

Deduplicate identical in-flight requests.

```
Request 1 for key A ─┐
Request 2 for key A ──┼─> Single DB query ─> Both get result
Request 3 for key A ─┘
```

## Popular Caching Solutions

| Solution | Type | Use Case |
|----------|------|----------|
| Redis | In-memory KV | Sessions, caching, pub/sub |
| Memcached | In-memory KV | Simple caching |
| Varnish | HTTP cache | Web acceleration |
| Caffeine | Local cache | JVM applications |
| Guava Cache | Local cache | JVM applications |

## Cache Metrics

- **Hit Rate**: % of requests served from cache
- **Miss Rate**: % of requests that miss cache
- **Eviction Rate**: How often items are evicted
- **Latency**: p50, p99 for cache operations

**Target:** 90%+ hit rate for most applications

## Interview Tips

1. Identify what to cache (expensive operations, hot data)
2. Choose caching strategy based on read/write ratio
3. Plan cache invalidation carefully
4. Discuss cache consistency requirements
5. Address cache failure scenarios
6. Consider cache stampede prevention

## Related Topics

- [CDN](cdn.md)
- [Databases](databases.md)
- [Latency & Throughput](../01_fundamentals/latency_throughput.md)
