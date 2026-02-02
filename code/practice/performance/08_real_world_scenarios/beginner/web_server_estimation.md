# Web Server Performance Estimation - Beginner

Estimating real-world web application performance.

## Learning Objectives
- Calculate request throughput
- Understand latency breakdown
- Estimate capacity requirements

## Background

### Typical Web Request Breakdown
```
DNS lookup: 0-50 ms (cached: 0)
TCP connect: 1× RTT
TLS handshake: 1-2× RTT
Request to server: 1× RTT
Server processing: 5-200 ms
Response transfer: Data/Bandwidth
```

### Common Processing Times
| Operation | Time |
|-----------|------|
| JSON parse (1 KB) | 0.1 ms |
| Database query (indexed) | 1-5 ms |
| Database query (scan) | 50-500 ms |
| Cache lookup (Redis) | 0.5-2 ms |
| API call (same DC) | 5-20 ms |
| External API | 100-500 ms |

---

## Exercise 1: Simple API Endpoint

**Question:** API endpoint that returns user profile:
- Read from cache: 2 ms
- Serialize JSON: 0.5 ms
- Response size: 2 KB
- Network (same region): 10 ms RTT

Calculate:
1. Total latency
2. Requests per second (single worker)

**Your Answer:**
```
Total latency = ?
RPS (single worker) = ?
```

<details>
<summary>Solution</summary>

```
Total Latency:
  Network RTT: 10 ms
  Cache read: 2 ms
  Serialize: 0.5 ms
  Response transfer: ~0.1 ms (2 KB over broadband)
  Total: ~12.6 ms

RPS (Single Worker):
  Time per request: 12.6 ms
  But network and processing overlap...
  
  Server-side only: 2.5 ms
  RPS = 1000 / 2.5 = 400 RPS per worker

With 8 workers:
  RPS = 400 × 8 = 3,200 RPS

Note: This assumes CPU-bound. If I/O-bound (async),
can handle many more concurrent requests.
```
</details>

---

## Exercise 2: Database-Backed Endpoint

**Question:** List products with filters:
- Parse request: 0.1 ms
- Database query: 20 ms
- Process results (100 items): 2 ms
- Serialize response: 1 ms
- Response: 50 KB

Calculate throughput for:
1. Synchronous server (1 worker)
2. Async server (handles I/O overlap)

**Your Answer:**
```
Sync server RPS = ?
Async server RPS = ?
Bottleneck = ?
```

<details>
<summary>Solution</summary>

```
Synchronous Server:
  Total time: 0.1 + 20 + 2 + 1 = 23.1 ms
  RPS = 1000 / 23.1 = 43 RPS per worker
  
  8 workers: 344 RPS

Async Server:
  Worker during DB wait can handle other requests
  CPU time: 0.1 + 2 + 1 = 3.1 ms per request
  Max RPS (CPU-bound): 1000 / 3.1 = 322 RPS per core
  
  8 cores: 2,576 RPS
  
  But database becomes bottleneck:
  DB can handle: ~50 concurrent queries
  50 queries × 50 RPS each = 2,500 RPS max

Bottleneck: Database (async helps CPU utilization)
```
</details>

---

## Exercise 3: Cache Hit Rate Impact

**Question:** Product page with caching:
- Cache hit: 2 ms response
- Cache miss: 100 ms (DB + compute)

Calculate response times for:
1. 50% cache hit rate
2. 90% cache hit rate
3. 99% cache hit rate

**Your Answer:**
```
50% hit rate: Average = ?
90% hit rate: Average = ?
99% hit rate: Average = ?
```

<details>
<summary>Solution</summary>

```
Average Response Time = (hit_rate × hit_time) + (miss_rate × miss_time)

50% Hit Rate:
  Average = (0.5 × 2) + (0.5 × 100) = 1 + 50 = 51 ms
  
90% Hit Rate:
  Average = (0.9 × 2) + (0.1 × 100) = 1.8 + 10 = 11.8 ms

99% Hit Rate:
  Average = (0.99 × 2) + (0.01 × 100) = 1.98 + 1 = 2.98 ms

Impact:
  50% → 90%: 4.3x faster
  90% → 99%: 4x faster
  
Each percentage point of cache hit rate matters
significantly when miss penalty is high!
```
</details>

---

## Exercise 4: External API Dependency

**Question:** E-commerce checkout calls:
1. Inventory check: 15 ms
2. Payment gateway: 200 ms
3. Shipping rates: 100 ms
4. Notification service: 50 ms

Calculate:
1. Sequential total
2. Parallel (where possible)
3. Strategies to improve

**Your Answer:**
```
Sequential total = ?
Parallel optimization = ?
Further improvements = ?
```

<details>
<summary>Solution</summary>

```
Sequential Total:
  15 + 200 + 100 + 50 = 365 ms

Parallel Optimization:
  Required order: Inventory first, then payment
  Can parallelize: Shipping + Notification during payment
  
  Timeline:
    T=0: Inventory (15 ms)
    T=15: Start Payment + Shipping + Notification in parallel
    T=215: Payment completes (longest)
    
  Total: 15 + 200 = 215 ms
  Savings: 150 ms (41% faster)

Further Improvements:
  1. Async notification (return before it completes)
     - Reduces user-visible time by 50 ms
  
  2. Cache shipping rates (if location-based)
     - Reduces to 1-2 ms cache hit
  
  3. Pre-validate payment (tokenization)
     - Reduce 200 ms to 50 ms for returning users
  
  Best case: 15 + 50 = 65 ms (82% improvement!)
```
</details>

---

## Exercise 5: Server Capacity Planning

**Question:** Web application with:
- Peak traffic: 10,000 requests/minute
- Average response time: 50 ms
- Server: 8 cores, async framework

Can one server handle it? How many requests in queue?

**Your Answer:**
```
RPS needed = ?
Server capacity = ?
Queue depth = ?
```

<details>
<summary>Solution</summary>

```
RPS Needed:
  10,000 / 60 = 167 RPS

Server Capacity:
  Processing time: 50 ms (includes I/O waits)
  CPU time (async): ~10 ms per request
  
  Per core: 1000 / 10 = 100 RPS
  8 cores: 800 RPS theoretical
  
  With overhead: ~600 RPS practical

Can Handle: Yes! 600 RPS > 167 RPS needed

Utilization: 167 / 600 = 28%

Queue Depth (Little's Law):
  L = λ × W
  λ = 167 RPS = 2.78 requests/second
  W = 0.05 seconds
  L = 167 × 0.05 = 8.35 concurrent requests
  
  Very manageable - server is underutilized.

For 50,000 requests/minute (833 RPS):
  Need 2 servers (with headroom)
```
</details>

---

## Exercise 6: End-to-End Latency Budget

**Question:** Design a page load with 200 ms latency budget:
- User in: US-West
- Server in: US-East
- Network RTT: 60 ms

Allocate time for:
1. DNS + Connection
2. Server processing
3. Data transfer
4. Client rendering

**Your Answer:**
```
DNS + Connection = ?
Server processing budget = ?
Data transfer budget = ?
Client rendering = ?
```

<details>
<summary>Solution</summary>

```
Total Budget: 200 ms
Network RTT: 60 ms (fixed)

Allocation:

1. DNS + Connection (first visit):
   DNS: 20 ms (or 0 if cached)
   TCP: 60 ms (1 RTT)
   TLS: 60 ms (1 RTT with TLS 1.3)
   Total: 140 ms (First visit!)
   
   That's 70% of budget just for connection!
   Solution: Keep-alive, preconnect hints

2. Server Processing:
   Request RTT: 60 ms (included above)
   Processing budget: 50 ms
   
3. Data Transfer:
   Remaining: 200 - 140 - 50 = 10 ms
   At 10 Mbps: 10 ms × 1.25 MB/s = 12.5 KB
   
   That's very small! Need CDN.

4. Client Rendering:
   Borrowed from response time
   Target: Start rendering in first 100 ms of data

Optimized Strategy:
  - Use CDN (reduces RTT to 10-20 ms)
  - Keep-alive connections (eliminate TCP/TLS)
  - Server processing: 30 ms
  - Streaming response (start render early)
  
  CDN path: 20 ms RTT + 30 ms server + 50 ms transfer = 100 ms
  That's 100 ms under budget!
```
</details>

---

## Key Takeaways

1. **Network often dominates** latency for web apps
2. **Cache hit rate is crucial**: 90% vs 99% = 4x difference
3. **Parallelize independent calls**: Often 30-50% savings
4. **Async servers scale better**: I/O overlap increases throughput
5. **CDNs transform latency**: Move content close to users

## Quick Reference
```
Simple API: 200-500 RPS per core
DB-backed: 50-200 RPS per core
External API dependent: 5-50 RPS per core

Cache hit: 1-5 ms
DB query: 5-50 ms
External API: 100-500 ms
```

## Next Steps
- Try [Intermediate: Database Performance](../intermediate/database_estimation.md)
- Complete the [Performance Practice Summary](../../README.md)
