# Exercise: URL Shortener Scaling

## Objective
Scale a URL shortener to handle high traffic.

## Problem Statement
Your URL shortener has grown:
- 100M URLs stored
- 10K URLs created/second (peak)
- 100K redirects/second (peak)
- 99.9% availability required

Current issues:
- Database is becoming a bottleneck
- Single point of failure
- Latency increasing during peak hours

## Tasks

### Task 1: Caching Strategy

Design the caching layer:

1. What to cache?
   - ___
   - ___

2. Cache key structure:
   ```
   Key: ___
   Value: ___
   TTL: ___
   ```

3. Cache invalidation strategy:
   - When URL is deleted: ___
   - When URL expires: ___

4. Calculate cache size:
   - 100M URLs × ___% hot = ___ URLs cached
   - Average entry size: ___ bytes
   - Total cache size: ___ GB

### Task 2: Database Scaling

Design the database scaling strategy:

1. **Read scaling:**
   - Approach: ___
   - Number of read replicas: ___
   - Read/write split logic: ___

2. **Write scaling:**
   - When to shard? (What metric triggers?)
   - Shard key: ___
   - Number of shards for 100M URLs: ___

3. Draw the database architecture:
   ```
   [Your diagram here]
   ```

### Task 3: Short Code Generation at Scale

With 10K URLs/second, how do you generate unique codes?

**Option A: Distributed Counter**
- How to implement?
- Pros/cons?

**Option B: UUID-based**
- How to implement?
- Pros/cons?

**Option C: Pre-generated Keys**
- How to implement?
- Pros/cons?

Recommend one and justify:
___

### Task 4: High Availability

Design for 99.9% availability:

1. **Multi-region deployment:**
   - How many regions?
   - Active-active or active-passive?
   - Data replication strategy?

2. **Failure scenarios:**

| Component Failure | Impact | Mitigation |
|------------------|--------|------------|
| One app server | | |
| Cache (Redis) | | |
| Primary database | | |
| Entire region | | |

### Task 5: Traffic Spike Handling

Black Friday causes 10x traffic spike. Design your approach:

1. **Auto-scaling policies:**
   ```yaml
   scaling:
     min_instances: ___
     max_instances: ___
     scale_up_threshold: ___
     scale_down_threshold: ___
   ```

2. **Graceful degradation:**
   - What features to disable under load?
   - How to prioritize traffic?

3. **Rate limiting:**
   - Per-user limits?
   - Global limits?

---

<details>
<summary>Hints</summary>

- 80/20 rule: 20% of URLs get 80% of traffic
- Read replicas can handle 100K reads/second easily
- Pre-generated keys avoid runtime generation bottleneck
- Redis cluster can handle millions of ops/second

</details>

<details>
<summary>Solution</summary>

### Task 1: Caching Strategy

1. **What to cache:**
   - Short code → original URL mappings
   - User rate limit counters

2. **Cache key structure:**
   ```
   Key: url:{short_code}
   Value: original_url (string)
   TTL: 24 hours (or until expiry)
   ```

3. **Invalidation:**
   - Deletion: Explicitly delete cache key
   - Expiry: Let TTL handle it, or set cache TTL = URL TTL

4. **Cache size:**
   - 100M × 10% hot = 10M URLs cached
   - Entry: ~500 bytes (code + URL + overhead)
   - Total: 10M × 500 = 5 GB

### Task 2: Database Scaling

1. **Read scaling:**
   - 3 read replicas (handles 100K reads/sec easily)
   - Reads go to replicas, writes to primary
   - Use connection pooling (PgBouncer)

2. **Write scaling:**
   - Shard when primary CPU > 70% sustained
   - Shard key: short_code (hash-based distribution)
   - 4 shards for 100M URLs (25M each, room to grow)

3. **Architecture:**
   ```
   Load Balancer
        │
   ┌────┴────┐
   │  Cache  │ (Redis Cluster)
   └────┬────┘
        │ (miss)
   ┌────┴────┬────────────┬────────────┐
   │ Primary │  Replica1  │  Replica2  │
   │ (Write) │  (Read)    │  (Read)    │
   └─────────┴────────────┴────────────┘
   ```

### Task 3: Short Code Generation at Scale

**Recommendation: Pre-generated Keys**

Implementation:
1. Key Generation Service generates batches of unique codes
2. Store in `available_keys` table
3. App servers fetch batches (1000 keys at a time)
4. Mark as used atomically

```sql
-- Fetch batch atomically
UPDATE available_keys 
SET status = 'used', assigned_to = 'server-1'
WHERE id IN (SELECT id FROM available_keys WHERE status = 'available' LIMIT 1000)
RETURNING short_code;
```

Pros:
- No collision checking at write time
- Predictable performance
- Works with sharding

Cons:
- Need to pre-generate keys
- Slightly more complex

### Task 4: High Availability

1. **Multi-region:**
   - 2 regions (US-East, US-West)
   - Active-active for reads
   - Single primary for writes (async replication)

2. **Failure handling:**

| Component | Impact | Mitigation |
|-----------|--------|------------|
| App server | None | Auto-scaling replaces |
| Cache | Higher latency | DB handles load, cache rebuilds |
| Primary DB | Writes fail | Promote replica, queue writes |
| Region | 50% capacity | Route to other region |

### Task 5: Traffic Spike

1. **Auto-scaling:**
   ```yaml
   scaling:
     min_instances: 10
     max_instances: 100
     scale_up_threshold: 70% CPU for 2 minutes
     scale_down_threshold: 30% CPU for 10 minutes
   ```

2. **Graceful degradation:**
   - Disable: Analytics, custom alias creation
   - Priority: Redirects over URL creation
   - Queue: Non-critical operations

3. **Rate limiting:**
   - Per-user: 10 creates/minute, 1000 redirects/minute
   - Global: 50K creates/second max
   - Burst: Allow 2x rate for 30 seconds

</details>
