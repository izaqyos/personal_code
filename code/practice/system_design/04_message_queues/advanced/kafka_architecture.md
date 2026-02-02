# Exercise: Kafka Architecture Design

## Objective
Design a production Kafka deployment for high-scale event streaming.

## Problem Statement
You're designing Kafka infrastructure for a ride-sharing platform:

**Scale:**
- 10M rides/day
- 1M driver location updates/minute
- 100K concurrent users
- 50 microservices consuming events

**Requirements:**
- < 100ms end-to-end latency for ride matching
- 7 days retention for most topics
- 30 days retention for analytics
- 99.99% availability
- No message loss

## Tasks

### Task 1: Cluster Sizing

Calculate the Kafka cluster requirements:

1. **Message volume:**
   - Rides: 10M/day = ___ messages/second
   - Location updates: 1M/minute = ___ messages/second
   - Estimated other events: ___
   - Total: ___ messages/second

2. **Storage calculation:**
   - Average message size: ___ bytes
   - Daily volume: ___ GB
   - With replication factor 3: ___ GB
   - 7-day retention: ___ TB
   - 30-day analytics: ___ TB

3. **Broker sizing:**
   - Messages/sec per broker: ~100K (typical)
   - Brokers needed for throughput: ___
   - Brokers needed for storage: ___
   - Total brokers (with overhead): ___

### Task 2: Topic Design

Design topics for the platform:

| Topic Name | Partitions | Retention | Replication | Key |
|------------|------------|-----------|-------------|-----|
| rides | | | | |
| driver-locations | | | | |
| ride-requests | | | | |
| payments | | | | |
| analytics-events | | | | |

Justify your partition count for `driver-locations`:
___

### Task 3: Consumer Group Architecture

Design consumer groups for ride matching service:

1. How many instances of ride-matching service?

2. How many partitions in ride-requests topic?

3. What happens if:
   - 10 partitions, 15 consumers?
   - 10 partitions, 5 consumers?

4. Design rebalancing strategy:
```yaml
consumer_config:
  partition_assignment_strategy: ___
  session_timeout_ms: ___
  max_poll_interval_ms: ___
  max_poll_records: ___
```

### Task 4: High Availability Design

Design for 99.99% availability:

1. **Broker distribution:**
   - How many racks/availability zones?
   - Min ISR (In-Sync Replicas) setting?
   - `unclean.leader.election.enable` setting?

2. **ZooKeeper/KRaft design:**
   - Number of nodes?
   - Quorum configuration?

3. **Failure scenarios:**

| Failure | Impact | Recovery |
|---------|--------|----------|
| 1 broker down | | |
| 1 AZ down | | |
| ZK node down | | |
| Network partition | | |

### Task 5: Performance Optimization

Optimize for < 100ms latency:

1. **Producer settings:**
```properties
acks=___
batch.size=___
linger.ms=___
compression.type=___
```

2. **Consumer settings:**
```properties
fetch.min.bytes=___
fetch.max.wait.ms=___
max.partition.fetch.bytes=___
```

3. **Broker settings:**
```properties
num.io.threads=___
num.network.threads=___
socket.send.buffer.bytes=___
socket.receive.buffer.bytes=___
```

### Task 6: Monitoring & Operations

Design monitoring for the cluster:

1. **Key metrics to track:**

| Metric | Warning | Critical | Action |
|--------|---------|----------|--------|
| Under-replicated partitions | | | |
| Consumer lag | | | |
| Request latency p99 | | | |
| Disk usage | | | |
| Network throughput | | | |

2. **Alerting priorities:**
   - P1 (page immediately): ___
   - P2 (page during hours): ___
   - P3 (ticket): ___

3. **Operational runbooks needed:**
   - ___
   - ___
   - ___

---

<details>
<summary>Hints</summary>

- Partitions = parallelism, but more isn't always better
- Replication factor 3 is standard for production
- min.insync.replicas = 2 with RF=3 is common
- Consumer lag is the key metric for real-time systems
- ISR = In-Sync Replicas must be >= min.insync.replicas for writes

</details>

<details>
<summary>Solution</summary>

### Task 1: Cluster Sizing

**Message volume:**
- Rides: 10M/day = 116 messages/second
- Location updates: 1M/minute = 16,667 messages/second
- Other events (notifications, analytics): ~5,000 messages/second
- Total: ~22,000 messages/second

**Storage:**
- Average message size: 1 KB
- Daily volume: 22K × 86400 × 1KB = 1.9 TB/day
- With RF=3: 5.7 TB/day
- 7-day retention: 40 TB
- 30-day analytics (assuming 30% of events): 17 TB
- Total: ~60 TB

**Brokers:**
- For throughput: 22K/100K per broker = 1 (but need headroom)
- For storage: 60TB / 2TB per broker = 30 brokers
- With 30% headroom: **40 brokers**

### Task 2: Topic Design

| Topic | Partitions | Retention | RF | Key |
|-------|------------|-----------|-----|-----|
| rides | 50 | 7d | 3 | ride_id |
| driver-locations | 100 | 1h | 3 | driver_id |
| ride-requests | 50 | 7d | 3 | rider_id |
| payments | 20 | 30d | 3 | payment_id |
| analytics-events | 100 | 30d | 3 | event_type |

**driver-locations partitions justification:**
- 1M updates/minute = 16K/second
- Need high parallelism for consumers
- Driver ID as key ensures location ordering per driver
- 100 partitions allows 100 parallel consumers

### Task 3: Consumer Group Architecture

1. **Ride-matching instances:** 10-20 (based on partitions)

2. **ride-requests partitions:** 50 (allows up to 50 parallel consumers)

3. **Consumer vs Partition mismatch:**
   - 10 partitions, 15 consumers: 5 consumers idle
   - 10 partitions, 5 consumers: Each consumer handles 2 partitions

4. **Configuration:**
```yaml
consumer_config:
  partition_assignment_strategy: CooperativeStickyAssignor
  session_timeout_ms: 30000
  max_poll_interval_ms: 300000  # 5 minutes for processing
  max_poll_records: 500
```

### Task 4: High Availability

**Broker distribution:**
- 3 availability zones (AZs)
- Distribute 40 brokers: ~13-14 per AZ
- min.insync.replicas = 2
- unclean.leader.election.enable = false

**ZooKeeper (or KRaft):**
- 5 nodes (across 3 AZs)
- Quorum = 3 (majority)

**Failure scenarios:**

| Failure | Impact | Recovery |
|---------|--------|----------|
| 1 broker | Minimal, replicas take over | Auto-recovery |
| 1 AZ | Degraded (2 AZs remain) | Manual failover |
| ZK node | None if quorum maintained | Auto-recovery |
| Network partition | Minority side read-only | Resolve partition |

### Task 5: Performance Optimization

**Producer:**
```properties
acks=1  # or "all" if no loss allowed
batch.size=32768  # 32KB
linger.ms=5  # Wait up to 5ms for batching
compression.type=lz4  # Fast compression
```

**Consumer:**
```properties
fetch.min.bytes=1  # Return immediately
fetch.max.wait.ms=100  # Max wait 100ms
max.partition.fetch.bytes=1048576  # 1MB
```

**Broker:**
```properties
num.io.threads=16
num.network.threads=8
socket.send.buffer.bytes=1048576
socket.receive.buffer.bytes=1048576
```

### Task 6: Monitoring

| Metric | Warning | Critical | Action |
|--------|---------|----------|--------|
| Under-replicated | > 0 for 5m | > 0 for 15m | Check broker health |
| Consumer lag | > 10K | > 100K | Scale consumers |
| Request latency p99 | > 50ms | > 200ms | Check broker load |
| Disk usage | > 70% | > 85% | Add brokers or reduce retention |
| Network throughput | > 70% capacity | > 90% | Add brokers |

**Alerting priorities:**
- P1: Under-replicated partitions, broker down, disk > 90%
- P2: Consumer lag > 100K, latency > 200ms
- P3: Disk > 70%, network > 70%

**Runbooks:**
- Broker replacement procedure
- Partition reassignment
- Consumer lag investigation
- Cluster expansion
- Disaster recovery

</details>
