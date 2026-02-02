# Availability & Reliability

## Definitions

**Availability**: The percentage of time a system is operational and accessible.

**Reliability**: The probability that a system will perform correctly over a given time period.

**Fault Tolerance**: The ability to continue operating despite component failures.

## Availability Metrics

### The Nines

| Availability | Downtime/Year | Downtime/Month | Downtime/Week |
|-------------|---------------|----------------|---------------|
| 99% (2 nines) | 3.65 days | 7.31 hours | 1.68 hours |
| 99.9% (3 nines) | 8.77 hours | 43.83 min | 10.08 min |
| 99.99% (4 nines) | 52.60 min | 4.38 min | 1.01 min |
| 99.999% (5 nines) | 5.26 min | 26.30 sec | 6.05 sec |

### SLA, SLO, SLI

- **SLI (Service Level Indicator)**: Metric that measures service health
  - Example: Response time, error rate, throughput

- **SLO (Service Level Objective)**: Target value for an SLI
  - Example: "99.9% of requests complete in < 200ms"

- **SLA (Service Level Agreement)**: Contract with consequences
  - Example: "If uptime < 99.9%, customer gets credits"

## Calculating Availability

### Single Component
```
Availability = MTTF / (MTTF + MTTR)

MTTF = Mean Time To Failure
MTTR = Mean Time To Recovery
```

### Serial Components (all must work)
```
A_total = A₁ × A₂ × A₃ × ...

Example: 99.9% × 99.9% × 99.9% = 99.7%
```

### Parallel Components (any one works)
```
A_total = 1 - (1 - A₁) × (1 - A₂) × ...

Example: 1 - (0.001 × 0.001) = 99.9999%
```

## Fault Tolerance Strategies

### Redundancy

**Active-Active:**
- All replicas handle traffic
- Load balanced
- Immediate failover
- More complex state sync

**Active-Passive:**
- Standby takes over on failure
- Simpler state management
- Brief failover time
- Wasted idle resources

### Replication Patterns

**Synchronous Replication:**
```
Client → Primary → Replica → ACK → Client
```
- Strong consistency
- Higher latency
- Availability depends on replica

**Asynchronous Replication:**
```
Client → Primary → ACK → Client
              ↓
          Replica (later)
```
- Lower latency
- Eventual consistency
- Potential data loss on failure

### Geographic Distribution

```
┌─────────────────┐     ┌─────────────────┐
│   US-EAST       │     │   US-WEST       │
│  ┌──────────┐   │     │  ┌──────────┐   │
│  │ Service  │◄──┼─────┼──┤ Service  │   │
│  └──────────┘   │     │  └──────────┘   │
│  ┌──────────┐   │     │  ┌──────────┐   │
│  │ Database │◄──┼─────┼──┤ Database │   │
│  └──────────┘   │     │  └──────────┘   │
└─────────────────┘     └─────────────────┘
```

## Failure Modes

### Fail-Safe
System fails in a safe state
- Example: Traffic light shows red on failure

### Fail-Fast
Detect and report failure immediately
- Example: Return error instead of hanging

### Fail-Over
Switch to backup system
- Example: Database failover to replica

### Graceful Degradation
Reduce functionality but stay operational
- Example: Show cached data when DB is down

## Design Patterns

### Health Checks
```
Load Balancer → /health → 200 OK
                       → 503 (remove from pool)
```

### Circuit Breaker
Prevent cascading failures by stopping calls to failing services.

```
CLOSED → Failures exceed threshold → OPEN
                                       ↓
                                   (timeout)
                                       ↓
                                   HALF-OPEN
                                       ↓
                          Success → CLOSED
                          Failure → OPEN
```

### Bulkhead
Isolate components to prevent failure propagation.

```
┌─────────────────────────────────┐
│ Service                         │
│ ┌─────────┐ ┌─────────────────┐ │
│ │Pool: DB │ │Pool: External API│ │
│ │ 10 conn │ │ 5 connections   │ │
│ └─────────┘ └─────────────────┘ │
└─────────────────────────────────┘
```

If external API hangs, DB pool is unaffected.

### Retry with Backoff
```python
def retry_with_backoff(operation, max_retries=3):
    for attempt in range(max_retries):
        try:
            return operation()
        except TransientError:
            wait = (2 ** attempt) + random.uniform(0, 1)
            time.sleep(wait)
    raise MaxRetriesExceeded
```

## Chaos Engineering

Intentionally inject failures to test resilience.

**Principles:**
1. Define steady state (normal behavior)
2. Hypothesize that steady state continues during failure
3. Introduce real-world failures
4. Try to disprove the hypothesis

**Tools:**
- Netflix Chaos Monkey
- Gremlin
- AWS Fault Injection Simulator

## Interview Tips

1. State availability requirements upfront (e.g., "four nines")
2. Calculate availability of your design
3. Identify single points of failure
4. Discuss failover mechanisms
5. Consider blast radius of failures

## Related Topics

- [Scalability](scalability.md)
- [Circuit Breaker](../03_design_patterns/circuit_breaker.md)
- [Load Balancers](../02_building_blocks/load_balancers.md)
