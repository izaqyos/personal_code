# Latency & Throughput

Two fundamental performance metrics for system design.

## Definitions

### Latency
Time taken to complete a single operation.

- Measured in milliseconds (ms), microseconds (μs), or nanoseconds (ns)
- Time from request sent to response received
- Often reported as percentiles (p50, p95, p99)

### Throughput
Number of operations completed per unit time.

- Measured in requests per second (RPS), transactions per second (TPS)
- Also: bytes per second for data transfer
- Indicates system capacity

## Relationship

Latency and throughput are related but not inversely proportional:

```
Throughput = Concurrent Requests / Average Latency

Example: 100 concurrent requests, 100ms latency
Throughput = 100 / 0.1s = 1000 RPS
```

### Little's Law
```
L = λ × W

L = Average number of items in system
λ = Arrival rate (throughput)
W = Average time in system (latency)
```

## Latency Percentiles

### Why Percentiles Matter

Average latency hides outliers:
```
Requests: 10ms, 10ms, 10ms, 10ms, 10ms, 10ms, 10ms, 10ms, 10ms, 1000ms
Average: 109ms (misleading!)
p50: 10ms (half are faster)
p99: 1000ms (1% experience this)
```

### Common Percentiles

| Percentile | Meaning |
|------------|---------|
| p50 (median) | Half of requests are faster |
| p90 | 90% of requests are faster |
| p95 | 95% of requests are faster |
| p99 | 99% of requests are faster |
| p99.9 | 99.9% of requests are faster |

### Tail Latency
High percentiles (p99, p99.9) are "tail latency."

**Why it matters:**
- Users making multiple requests likely hit the tail
- A page loading 10 resources: probability of hitting p99 ≈ 10%
- Poor tail latency degrades user experience

## Latency Numbers Every Programmer Should Know

### CPU & Memory
| Operation | Latency |
|-----------|---------|
| L1 cache reference | 1 ns |
| L2 cache reference | 4 ns |
| L3 cache reference | 12 ns |
| Main memory reference | 100 ns |
| Branch mispredict | 5 ns |

### Storage
| Operation | Latency |
|-----------|---------|
| SSD random read | 16 μs |
| SSD sequential read (1 MB) | 250 μs |
| HDD seek | 4 ms |
| HDD sequential read (1 MB) | 5 ms |

### Network
| Operation | Latency |
|-----------|---------|
| Same datacenter RTT | 0.5 ms |
| Cross-country RTT (US) | 40 ms |
| Cross-continent RTT | 150 ms |
| Packet round trip (1 Gbps) | 10 μs |

### Comparison Visualization
```
L1 cache ●
L2 cache ●●●●
Main memory ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●

SSD random ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
           ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
           ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
           ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●

HDD seek   [imagine 4,000,000 dots]
```

## Throughput Considerations

### Bottleneck Identification

```
Request → Load Balancer → App Server → Database
            [10K RPS]       [5K RPS]    [1K RPS]
                                            ↑
                                       Bottleneck
```

System throughput = throughput of slowest component

### Scaling Throughput

**Horizontal Scaling:**
```
1 server:  1,000 RPS
5 servers: 5,000 RPS (linear if stateless)
```

**Vertical Scaling:**
```
4 cores:  1,000 RPS
8 cores:  ~1,800 RPS (diminishing returns)
```

### Amdahl's Law
```
Speedup = 1 / (S + P/N)

S = Serial fraction
P = Parallel fraction (1 - S)
N = Number of processors
```

If 10% is serial, max speedup = 10x regardless of processors.

## Latency vs Throughput Trade-offs

### Batching
```
Without batching: 1 item/request, 1ms each
  → 1000 RPS, 1ms latency

With batching: 100 items/request, 10ms each
  → 100 requests/s × 100 items = 10,000 items/s
  → Higher throughput, higher latency
```

### Caching
```
Cache Hit:  1ms  → Low latency
Cache Miss: 100ms + cache write

High cache hit rate = low average latency + high throughput
```

### Connection Pooling
```
Without pool: New connection per request (50ms overhead)
With pool: Reuse connections (0ms overhead)

→ Dramatically improves both latency and throughput
```

## Measuring Performance

### Latency Measurement
```python
start = time.monotonic()
response = make_request()
latency = time.monotonic() - start
```

### Throughput Measurement
```python
# Count requests over time window
requests_in_window / window_duration
```

### Tools
- **wrk**: HTTP benchmarking
- **Apache JMeter**: Load testing
- **k6**: Modern load testing
- **Prometheus + Grafana**: Monitoring

## Capacity Estimation

### Example: Design a URL shortener

**Requirements:**
- 100M URLs/month created
- 10:1 read:write ratio

**Calculations:**
```
Writes: 100M / (30 × 24 × 3600) ≈ 40 writes/sec
Reads:  40 × 10 = 400 reads/sec

Storage: 100M × 100 bytes = 10 GB/month
Bandwidth: 400 × 100 bytes = 40 KB/s
```

## Interview Tips

1. Always clarify latency requirements (p99 target?)
2. Estimate throughput from user numbers
3. Identify the bottleneck first
4. Use the reference latency numbers
5. Consider tail latency for user-facing services

## Related Topics

- [Scalability](scalability.md)
- [Caching](../02_building_blocks/caching.md)
- [Load Balancers](../02_building_blocks/load_balancers.md)
