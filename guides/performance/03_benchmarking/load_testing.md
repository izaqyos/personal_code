# Load Testing

Testing system performance under realistic and stress conditions.

## Key Metrics

### Latency
```
p50 (median): 50% of requests faster than this
p95: 95% of requests faster than this
p99: 99% of requests faster than this
p99.9: 99.9% of requests faster than this (tail latency)
```

### Throughput
```
RPS: Requests per second
TPS: Transactions per second
QPS: Queries per second
```

### Error Rate
```
Error rate = Failed requests / Total requests
Target: Usually < 0.1% under normal load
```

### Saturation
```
CPU utilization
Memory usage
Connection pool usage
Queue depths
```

## Load Testing Types

### Smoke Test
Quick sanity check with minimal load.
```
Duration: 1-5 minutes
Load: 1-5 users
Goal: Verify system works
```

### Load Test
Normal expected load.
```
Duration: 10-60 minutes
Load: Expected peak users
Goal: Baseline performance metrics
```

### Stress Test
Find the breaking point.
```
Duration: Until failure
Load: Gradually increasing
Goal: Maximum capacity
```

### Soak Test
Extended duration for leak detection.
```
Duration: 4-24 hours
Load: Normal load
Goal: Find memory leaks, resource exhaustion
```

### Spike Test
Sudden traffic burst.
```
Duration: 15-30 minutes
Load: 2-10x normal, sudden
Goal: Recovery behavior
```

## Tools

### k6 (JavaScript)
```javascript
// script.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
    stages: [
        { duration: '1m', target: 100 },  // Ramp up
        { duration: '5m', target: 100 },  // Stay
        { duration: '1m', target: 0 },    // Ramp down
    ],
};

export default function() {
    const res = http.get('http://api.example.com/endpoint');
    
    check(res, {
        'status is 200': (r) => r.status === 200,
        'response time < 500ms': (r) => r.timings.duration < 500,
    });
    
    sleep(1);
}
```

```bash
k6 run script.js
```

### Locust (Python)
```python
# locustfile.py
from locust import HttpUser, task, between

class WebUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(3)  # Weight: 3x more likely
    def view_item(self):
        self.client.get("/item/1")
    
    @task(1)
    def create_order(self):
        self.client.post("/order", json={"item_id": 1})
```

```bash
locust -f locustfile.py --host=http://localhost:8080
# Opens web UI at localhost:8089
```

### wrk (C)
```bash
# Simple benchmark
wrk -t12 -c400 -d30s http://localhost:8080/api

# With Lua script
wrk -t12 -c400 -d30s -s script.lua http://localhost:8080/api
```

### Apache Bench (ab)
```bash
# 1000 requests, 100 concurrent
ab -n 1000 -c 100 http://localhost:8080/api

# With POST data
ab -n 1000 -c 100 -p data.json -T application/json http://localhost:8080/api
```

### hey
```bash
# 200 requests, 50 concurrent
hey -n 200 -c 50 http://localhost:8080/api

# Duration-based
hey -z 30s -c 50 http://localhost:8080/api
```

## Designing Load Tests

### Realistic Workload
```
1. Analyze production traffic patterns
2. Mix of read/write operations
3. Realistic think time between requests
4. Representative data sizes
```

### User Journey Simulation
```python
# Locust example
class ShoppingUser(HttpUser):
    @task
    def shopping_flow(self):
        # Browse products
        self.client.get("/products")
        sleep(random.uniform(2, 5))
        
        # View product detail
        self.client.get("/product/123")
        sleep(random.uniform(1, 3))
        
        # Add to cart
        self.client.post("/cart", json={"product_id": 123})
        sleep(random.uniform(0.5, 1))
        
        # Checkout
        self.client.post("/checkout", json={"cart_id": "..."})
```

### Parameterization
```python
# Use different data for each request
import random

class ApiUser(HttpUser):
    user_ids = list(range(1, 10000))
    
    @task
    def get_user(self):
        user_id = random.choice(self.user_ids)
        self.client.get(f"/user/{user_id}")
```

## Analyzing Results

### Key Questions
```
1. What is p95/p99 latency?
2. At what load does latency spike?
3. What is max sustainable throughput?
4. What fails first (CPU, memory, connections)?
5. Are there error spikes?
```

### Example Analysis
```
Load Test Results:
  Duration: 30 minutes
  Users: 500 concurrent

Latency (ms):
  p50:  45
  p95:  120
  p99:  450
  p99.9: 2100

Throughput:
  Avg: 2,340 RPS
  Peak: 2,890 RPS

Errors:
  Total: 127 (0.03%)
  Types: 95 timeout, 32 connection refused

Resources at peak:
  CPU: 78%
  Memory: 62%
  Connections: 450/500

Conclusion: System handles 500 users well.
Recommend: Test 1000 users to find limit.
```

## Common Bottlenecks

### Connection Pool Exhaustion
```
Symptoms:
  - Timeout errors increase
  - Latency spikes
  - CPU/memory normal

Fix:
  - Increase pool size
  - Reduce connection hold time
  - Add connection timeout
```

### Database Bottleneck
```
Symptoms:
  - Slow queries in logs
  - DB CPU/IO high
  - App server resources OK

Fix:
  - Add indexes
  - Query optimization
  - Read replicas
  - Caching
```

### Memory Leak
```
Symptoms:
  - Memory grows over time
  - Eventually OOM or GC pauses
  - Found in soak tests

Fix:
  - Profile memory usage
  - Fix leaking references
  - Add memory limits
```

### Thread Pool Starvation
```
Symptoms:
  - Requests queue up
  - Latency grows linearly
  - CPU underutilized

Fix:
  - Increase thread pool
  - Use async I/O
  - Reduce blocking calls
```

## Capacity Planning

### Little's Law
```
L = λW

Where:
  L = Average number of items in system
  λ = Average arrival rate
  W = Average time in system

Example:
  100 RPS, 50ms avg response time
  L = 100 × 0.05 = 5 concurrent requests
```

### Capacity Estimation
```
Max RPS = (Concurrent connections × 1000) / Avg response time (ms)

Example:
  500 connections, 50ms response
  Max RPS = (500 × 1000) / 50 = 10,000 RPS
```

## Quick Reference

### Tool Selection

| Tool | Best For | Language |
|------|----------|----------|
| k6 | CI/CD integration | JavaScript |
| Locust | Complex scenarios | Python |
| wrk | Max throughput | Lua |
| ab | Quick tests | CLI |
| hey | Simple HTTP | CLI |
| Gatling | Enterprise | Scala |

### Load Test Checklist
```
□ Define success criteria (latency, error rate)
□ Use realistic workload mix
□ Include think time
□ Test with production-like data
□ Monitor server resources
□ Run from separate machine/network
□ Document environment
□ Save raw results
```

### Percentile Guidelines
```
p50: User experience for most requests
p95: Good indicator of overall health
p99: Important for SLAs
p99.9: Tail latency, affects heavy users
```

## Related Topics
- [Profiling Tools](profiling_tools.md)
- [Microbenchmarks](microbenchmarks.md)
