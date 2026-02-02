# Network Performance Basics - Beginner

Understanding network latency and bandwidth fundamentals.

## Learning Objectives
- Calculate network transfer times
- Understand latency vs bandwidth trade-offs
- Estimate API call performance

## Background

### Network Latency Reference
| Path | Round-Trip Time |
|------|-----------------|
| Same machine (loopback) | 0.1 ms |
| Same datacenter | 0.5-1 ms |
| Same region (AWS availability zones) | 1-2 ms |
| Cross-country (US East to West) | 60-80 ms |
| Trans-Atlantic (US to Europe) | 80-120 ms |
| Trans-Pacific (US to Asia) | 150-200 ms |

### Bandwidth Reference
| Connection | Speed | Real Throughput |
|------------|-------|-----------------|
| 4G LTE | 20-50 Mbps | 2-5 MB/s |
| Home broadband | 100-1000 Mbps | 10-100 MB/s |
| Datacenter | 10-100 Gbps | 1-10 GB/s |

---

## Exercise 1: API Call Latency

**Question:** A web page makes 5 sequential API calls.
- Server location: Different region (50 ms RTT)
- Server processing: 10 ms per call
- Data returned: 10 KB per call (negligible transfer time)

Calculate total time for all calls.

**Your Answer:**
```
Per-call time = ?
Total time = ?
```

<details>
<summary>Solution</summary>

```
Per-Call Time:
  Network RTT: 50 ms
  Server processing: 10 ms
  Data transfer: 10 KB / 100 Mbps = 0.8 ms (negligible)
  Total: ~60 ms per call

Total Time (Sequential):
  5 calls × 60 ms = 300 ms

Optimization - Parallel Calls:
  If calls are independent:
  Time = 60 ms (all 5 in parallel)
  
  Speedup: 5x faster with parallelization!
```
</details>

---

## Exercise 2: Bandwidth vs Latency

**Question:** Download a 100 MB file from:
1. Local server (1 ms RTT, 1 Gbps)
2. Cross-country CDN (50 ms RTT, 1 Gbps)
3. International server (150 ms RTT, 100 Mbps)

**Your Answer:**
```
Local = ?
Cross-country CDN = ?
International = ?
```

<details>
<summary>Solution</summary>

```
Local Server:
  Transfer: 100 MB / 125 MB/s = 0.8 seconds
  Latency overhead: negligible (few ms)
  Total: ~0.8 seconds

Cross-Country CDN:
  Transfer: 100 MB / 125 MB/s = 0.8 seconds
  TCP slow-start overhead: ~1-2 seconds (need to ramp up)
  Total: ~2 seconds

International Server:
  Transfer: 100 MB / 12.5 MB/s = 8 seconds
  TCP slow-start: ~2-3 seconds
  Total: ~10 seconds

Key insight: For large files, bandwidth dominates.
For small requests, latency dominates.
```
</details>

---

## Exercise 3: Small vs Large Requests

**Question:** Compare these API designs:
1. REST: 100 separate calls, 1 KB each
2. GraphQL: 1 call, 100 KB response

Network: 50 ms RTT, 100 Mbps

**Your Answer:**
```
REST (100 calls) = ?
GraphQL (1 call) = ?
Improvement = ?
```

<details>
<summary>Solution</summary>

```
REST (100 Sequential Calls):
  Per call: 50 ms RTT + 0.08 ms transfer = 50 ms
  Total: 100 × 50 ms = 5,000 ms = 5 seconds

REST (100 Parallel Calls):
  Assuming connection reuse (HTTP/2):
  Time: ~50-100 ms (parallel on single connection)
  
  With connection limits (HTTP/1.1, 6 connections):
  Time: 100 / 6 × 50 ms = 833 ms

GraphQL (1 Call):
  Transfer: 100 KB / 12.5 MB/s = 8 ms
  RTT: 50 ms
  Total: ~60 ms

Improvement: 
  GraphQL vs Sequential REST: 83x faster
  GraphQL vs Parallel REST: 10-15x faster

Lesson: Reduce round trips, especially over high-latency links.
```
</details>

---

## Exercise 4: Connection Overhead

**Question:** First request to a new HTTPS server:
1. DNS lookup: 20 ms
2. TCP handshake: 1.5 × RTT
3. TLS handshake: 2 × RTT (TLS 1.2) or 1 × RTT (TLS 1.3)
4. HTTP request/response: 1 × RTT

Calculate first vs subsequent request times.
RTT = 50 ms

**Your Answer:**
```
First request (TLS 1.2) = ?
First request (TLS 1.3) = ?
Subsequent request (keep-alive) = ?
```

<details>
<summary>Solution</summary>

```
First Request (TLS 1.2):
  DNS: 20 ms
  TCP: 1.5 × 50 ms = 75 ms
  TLS: 2 × 50 ms = 100 ms
  HTTP: 1 × 50 ms = 50 ms
  Total: 245 ms

First Request (TLS 1.3):
  DNS: 20 ms
  TCP: 1.5 × 50 ms = 75 ms
  TLS: 1 × 50 ms = 50 ms
  HTTP: 1 × 50 ms = 50 ms
  Total: 195 ms

Subsequent Request (Keep-Alive):
  Just HTTP: 50 ms
  
  DNS: Cached
  TCP: Reused connection
  TLS: Session resumed

Speedup: First request 4-5x slower than subsequent!

This is why:
- Connection pooling is important
- HTTP/2 multiplexing helps
- Preconnect hints in HTML
```
</details>

---

## Exercise 5: Global Latency Impact

**Question:** Your servers are in US-East. Calculate user experience:

1. User in US-East: 10 ms RTT
2. User in US-West: 70 ms RTT  
3. User in Europe: 100 ms RTT
4. User in Asia: 200 ms RTT

Each page load requires 10 sequential API calls.

**Your Answer:**
```
US-East total = ?
US-West total = ?
Europe total = ?
Asia total = ?
```

<details>
<summary>Solution</summary>

```
US-East (10 ms RTT):
  10 calls × 10 ms = 100 ms
  User experience: Fast, responsive

US-West (70 ms RTT):
  10 calls × 70 ms = 700 ms
  User experience: Noticeable delay

Europe (100 ms RTT):
  10 calls × 100 ms = 1,000 ms = 1 second
  User experience: Slow

Asia (200 ms RTT):
  10 calls × 200 ms = 2,000 ms = 2 seconds
  User experience: Very slow, frustrating

Solutions:
1. CDN for static assets
2. Edge computing (Cloudflare Workers, Lambda@Edge)
3. Regional backend deployments
4. Reduce sequential calls (batch, GraphQL)
5. Prefetch likely-needed data
```
</details>

---

## Exercise 6: Bandwidth Estimation

**Question:** Video streaming service:
- SD quality: 3 Mbps
- HD quality: 8 Mbps
- 4K quality: 25 Mbps

User has 50 Mbps connection. Calculate:
1. Maximum quality supportable
2. Buffering time for 1 minute of 4K video
3. How many simultaneous HD streams?

**Your Answer:**
```
Max quality = ?
Buffer time for 1 min 4K = ?
Simultaneous HD streams = ?
```

<details>
<summary>Solution</summary>

```
Maximum Quality:
  50 Mbps connection > 25 Mbps 4K requirement
  4K is supportable (with some margin)
  
  Note: Need ~20% headroom for reliability
  Safe choice: HD (8 Mbps uses 16% of bandwidth)

Buffer 1 Minute of 4K:
  Data: 25 Mbps × 60 sec = 1,500 Mb = 187.5 MB
  Download at 50 Mbps: 30 seconds to buffer 1 minute
  
  Ratio: Can download 2x faster than playback
  Result: Minimal buffering after initial 30-second buffer

Simultaneous HD Streams:
  50 Mbps / 8 Mbps = 6.25 streams
  Safely: 5-6 simultaneous HD streams
  
  Common scenario: 
    Family streaming (3 devices): 24 Mbps
    Remaining for browsing: 26 Mbps
    Works fine!
```
</details>

---

## Key Takeaways

1. **Latency dominates for small requests**, bandwidth for large transfers
2. **Reduce round trips**: Batch calls, use GraphQL, prefetch
3. **Connection reuse** saves 4-5x on subsequent requests
4. **Geographic distance** means higher latency - use CDN/edge
5. **Parallel requests** when possible, but respect connection limits

## Quick Reference
```
Cross-country round trip: 60-80 ms
International round trip: 100-200 ms

First HTTPS request: 200-400 ms overhead
Subsequent request: Just RTT

100 Mbps = 12.5 MB/s actual throughput
```

## Next Steps
- Try [Intermediate: TCP Optimization](../intermediate/tcp_optimization.md)
- Learn about [Cache Effects](../../05_cache_effects/beginner/cache_basics.md)
