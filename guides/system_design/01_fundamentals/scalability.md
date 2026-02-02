# Scalability

The ability of a system to handle increased load by adding resources.

## Types of Scaling

### Vertical Scaling (Scale Up)
Adding more power to existing machines.

**Pros:**
- Simple to implement
- No code changes required
- No distributed system complexity

**Cons:**
- Hardware limits (can't scale infinitely)
- Single point of failure
- Expensive at high end
- Downtime during upgrade

**Use When:**
- Early stage startups
- Database scaling (initially)
- Stateful applications

### Horizontal Scaling (Scale Out)
Adding more machines to the pool.

**Pros:**
- Theoretically unlimited scaling
- Better fault tolerance
- Can use commodity hardware
- No downtime for scaling

**Cons:**
- Application must support distribution
- Data consistency challenges
- Network overhead
- More complex operations

**Use When:**
- Web servers (stateless)
- Microservices
- High availability requirements

## Scaling Strategies

### Stateless Services
- Store no session data locally
- Any instance can handle any request
- Easy to scale horizontally
- Use external stores for state (Redis, DB)

### Database Scaling

```
Read Replicas → Read-heavy workloads
Sharding → Write-heavy workloads
Caching → Reduce database load
```

**Read Replicas:**
- Primary handles writes
- Replicas handle reads
- Eventual consistency tradeoff

**Sharding:**
- Partition data across databases
- Shard key determines placement
- Complex queries across shards

### Caching Layers
```
Client → CDN → App Cache → Database Cache → Database
```

Each layer reduces load on the next.

## Measuring Scalability

### Key Metrics
- **Throughput**: Requests per second (RPS)
- **Latency**: Response time (p50, p95, p99)
- **Concurrency**: Simultaneous connections

### Load Testing
```
Baseline → Stress Test → Find Bottleneck → Optimize → Repeat
```

## Common Bottlenecks

| Layer | Bottleneck | Solution |
|-------|-----------|----------|
| Web | CPU | Horizontal scaling |
| Database | Connections | Connection pooling |
| Database | Reads | Read replicas, caching |
| Database | Writes | Sharding |
| Network | Bandwidth | CDN, compression |
| Storage | I/O | SSD, distributed storage |

## Scalability Patterns

### Load Balancer + App Servers
```
           ┌─────────────┐
           │Load Balancer│
           └─────────────┘
          /       |       \
    ┌─────┐   ┌─────┐   ┌─────┐
    │App 1│   │App 2│   │App 3│
    └─────┘   └─────┘   └─────┘
```

### Database with Read Replicas
```
    ┌─────────┐
    │ Primary │ ← Writes
    └─────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌────────┐
│Replica1│ │Replica2│ ← Reads
└────────┘ └────────┘
```

## Real-World Example

**Twitter-like Feed:**

1. **1K users**: Single server, single DB
2. **100K users**: Add read replicas, cache popular tweets
3. **10M users**: Shard by user, fan-out on read/write
4. **100M users**: Multiple data centers, eventual consistency

## Interview Tips

1. Always clarify scale requirements first
2. Start simple, then scale as needed
3. Identify the bottleneck before solving
4. Consider cost vs. complexity tradeoffs
5. Discuss monitoring and auto-scaling

## Related Topics

- [Availability & Reliability](availability_reliability.md)
- [Load Balancers](../02_building_blocks/load_balancers.md)
- [Databases](../02_building_blocks/databases.md)
- [Caching](../02_building_blocks/caching.md)
