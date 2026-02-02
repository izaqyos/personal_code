# Network Performance

Understanding network latency and bandwidth for distributed systems.

## Key Metrics

### Latency
Time for a packet to travel one way.

```
Same machine (loopback): ~50 μs
Same datacenter: 0.5 ms
Same region (cross-AZ): 1-2 ms
Cross-country (US): 30-50 ms
Cross-Atlantic: 80-100 ms
Cross-Pacific: 150-200 ms
```

### RTT (Round-Trip Time)
```
RTT ≈ 2 × One-way latency + Processing time

Same datacenter: ~1 ms
Cross-country: ~70 ms
International: ~200-400 ms
```

### Bandwidth
```
1 Gbps = 125 MB/s
10 Gbps = 1.25 GB/s
25 Gbps = 3.125 GB/s
100 Gbps = 12.5 GB/s
```

## Bandwidth-Delay Product

How much data can be "in flight":
```
BDP = Bandwidth × RTT

Example: 1 Gbps link, 100 ms RTT
BDP = 125 MB/s × 0.1 s = 12.5 MB

Need 12.5 MB buffer to fully utilize the link
```

## TCP Characteristics

### Connection Overhead
```
TCP handshake: 1.5 RTT
TLS handshake: +2 RTT (TLS 1.2) or +1 RTT (TLS 1.3)

Total for HTTPS: 2.5-3.5 RTT before first byte
```

### TCP Slow Start
New connections start slow:
```
Initial window: ~10 segments (14 KB)
Doubles each RTT until congestion/limit

Time to reach 1 MB/s on 100ms RTT:
  14 KB → 28 → 56 → 112 → 224 → 448 → 896 KB
  = 6 RTTs = 600 ms
```

### Keep-Alive
Reuse connections to avoid handshake:
```
First request: 3 RTT (connect + request)
Subsequent: 1 RTT (request only)
```

## Protocol Comparison

| Protocol | Overhead | Latency | Use Case |
|----------|----------|---------|----------|
| TCP | Connection, reliability | Higher | Most apps |
| UDP | Minimal | Lower | Gaming, video |
| QUIC | Built-in TLS, mux | Medium | HTTP/3 |
| gRPC | HTTP/2, protobuf | Low | Microservices |

## Datacenter Networking

### Typical Topology
```
       ┌─────────────────────────────────┐
       │          Spine Switches         │
       │  (100 Gbps between pods)        │
       └──────────────┬──────────────────┘
                      │
    ┌─────────────────┼─────────────────┐
    │                 │                 │
┌───▼───┐         ┌───▼───┐         ┌───▼───┐
│ Leaf  │         │ Leaf  │         │ Leaf  │
│Switch │         │Switch │         │Switch │
└───┬───┘         └───┬───┘         └───┬───┘
    │                 │                 │
 Servers           Servers           Servers
```

### Within-Datacenter Latency
```
Same rack: 100-200 μs
Different rack: 200-500 μs
Different pod: 500-1000 μs
```

## Calculation Examples

### Example 1: API Call Latency
```
Cross-country API call:
  Network RTT: 70 ms
  Server processing: 10 ms
  DNS (cached): 0 ms
  TLS (reused): 0 ms
  
  Total: ~80 ms per call
```

### Example 2: Data Transfer
```
Transfer 10 GB cross-country:

Bandwidth-limited:
  1 Gbps link: 10 GB / 125 MB/s = 80 seconds
  
Latency not significant for bulk transfer
(amortized over large data)
```

### Example 3: Many Small Requests
```
1000 sequential API calls, 70 ms RTT each:
  Time: 1000 × 70 ms = 70 seconds

Parallel (10 concurrent):
  Time: 100 × 70 ms = 7 seconds

Batched (1 request with all data):
  Time: 70 ms + processing
```

## Optimization Strategies

### Reduce Round Trips
```
Bad: 10 sequential API calls
Good: 1 batch API call

Savings: 9 × RTT
```

### Connection Pooling
```python
# Bad: new connection per request
response = requests.get(url)

# Good: reuse connections
session = requests.Session()
response = session.get(url)
```

### Compression
```
1 MB JSON response:
  Uncompressed: 8 ms transfer (1 Gbps)
  gzip (~10:1): 0.8 ms transfer + 1 ms decompress
  Savings: 6.2 ms (on slow networks, much more)
```

### CDN/Edge Caching
```
Without CDN: 100 ms (cross-country)
With CDN: 10 ms (edge cache)
Savings: 90 ms per request
```

## DNS Resolution

```
DNS lookup: 10-100 ms (first time)
Cached: 0 ms

TTL typically: 60-3600 seconds
```

## Quick Reference

### Latency Table

| Path | Latency | RTT |
|------|---------|-----|
| Loopback | 50 μs | 100 μs |
| Same DC | 0.5 ms | 1 ms |
| Same region | 1-2 ms | 2-4 ms |
| Cross-US | 30-50 ms | 60-100 ms |
| US → Europe | 80-100 ms | 160-200 ms |
| US → Asia | 150-200 ms | 300-400 ms |

### Bandwidth Translation

| Rate | Per Second | Per Minute | Per Hour |
|------|------------|------------|----------|
| 1 Mbps | 125 KB | 7.5 MB | 450 MB |
| 10 Mbps | 1.25 MB | 75 MB | 4.5 GB |
| 100 Mbps | 12.5 MB | 750 MB | 45 GB |
| 1 Gbps | 125 MB | 7.5 GB | 450 GB |
| 10 Gbps | 1.25 GB | 75 GB | 4.5 TB |

## Related Topics
- [Storage](storage.md)
- [Memory](memory.md)
