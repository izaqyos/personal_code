# Exercise: Distributed Cache Design

## Objective
Design a distributed caching layer for a high-scale application.

## Problem Statement
You're designing the caching infrastructure for a global social network:

**Scale:**
- 500M daily active users
- 10M requests/second
- 50TB of frequently accessed data
- 99.99% cache availability required
- < 5ms p99 latency for cache operations

**Current pain points:**
- Single Redis instance running out of memory
- Cache failures cause cascading database overload
- Inconsistent data across regions

## Tasks

### Task 1: Cluster Architecture

Design a Redis Cluster architecture:

1. How many nodes do you need? Show your calculations.

2. How would you partition data across nodes?

3. Draw the cluster topology including:
   - Master nodes
   - Replica nodes
   - Sentinel/coordination

### Task 2: Consistent Hashing Implementation

Explain how consistent hashing would work for your cache cluster:

1. How do you map keys to nodes?

2. What happens when you add a node?

3. What happens when a node fails?

Include the distribution of these example keys across 5 nodes:
- `user:1001`
- `user:5000000`
- `post:abc123`
- `feed:user:1001`

### Task 3: Multi-Region Strategy

Design caching for 3 regions (US, EU, Asia):

1. **Replication strategy**: How do you sync cache across regions?
   - Option A: Active-Active with eventual consistency
   - Option B: Active-Passive with read replicas
   - Option C: Independent caches per region
   
   Choose one and justify.

2. **Conflict resolution**: For Option A, how do you handle:
   - Two regions updating the same key?
   - Clock skew between regions?

3. **Read/Write patterns**: Where do reads and writes go?

### Task 4: Failure Handling

Design for these failure scenarios:

1. **Single node failure**
   - Detection time: ___
   - Failover process: ___
   - Data loss potential: ___

2. **Region failure**
   - Traffic rerouting: ___
   - Cache warming strategy: ___
   - Stale data handling: ___

3. **Split brain**
   - Detection: ___
   - Resolution: ___

### Task 5: Capacity Planning

Given:
- 50TB data, 3x replication = 150TB storage
- 10M requests/second

Calculate:
1. Nodes needed (assuming 64GB RAM per node)
2. Network bandwidth requirements
3. Cost estimate (use $X/GB/month for cloud)

### Task 6: Monitoring & Observability

Define key metrics to monitor:

| Metric | Threshold | Action if Exceeded |
|--------|-----------|-------------------|
| Hit rate | | |
| Latency p99 | | |
| Memory usage | | |
| Connection count | | |
| Eviction rate | | |

---

<details>
<summary>Hints</summary>

- Redis Cluster uses 16384 hash slots
- Typical replication factor is 2-3
- Consider data locality for multi-region
- Sentinel requires 3+ instances for quorum
- Network bandwidth often overlooked in cache design

</details>

<details>
<summary>Solution</summary>

### Task 1: Cluster Architecture

**Node calculation:**
- 50TB data with 3x replication = 150TB storage
- Per node: 64GB RAM, ~50GB usable
- Nodes needed: 150TB / 50GB = 3000 nodes for storage
- For 10M ops/sec: ~100K ops/sec per node = 100 nodes minimum
- **Answer: ~3000 master nodes + 6000 replicas = 9000 total**

**Partitioning:** Redis Cluster's 16384 hash slots distributed evenly.

```
                    ┌─────────────────────────────────────┐
                    │          Cluster Proxy              │
                    └─────────────────┬───────────────────┘
                                      │
    ┌─────────────┬───────────────────┼───────────────────┬─────────────┐
    ▼             ▼                   ▼                   ▼             ▼
┌───────┐    ┌───────┐           ┌───────┐          ┌───────┐    ┌───────┐
│Master1│    │Master2│           │Master3│          │Master4│    │MasterN│
│0-3276 │    │3277-  │           │ ...   │          │ ...   │    │-16383 │
└───┬───┘    └───┬───┘           └───┬───┘          └───┬───┘    └───┬───┘
    │            │                   │                  │            │
┌───┴───┐    ┌───┴───┐           ┌───┴───┐          ┌───┴───┐    ┌───┴───┐
│Replica│    │Replica│           │Replica│          │Replica│    │Replica│
│Replica│    │Replica│           │Replica│          │Replica│    │Replica│
└───────┘    └───────┘           └───────┘          └───────┘    └───────┘
```

### Task 2: Consistent Hashing

**Key to node mapping:**
```
slot = CRC16(key) mod 16384
node = slot_to_node[slot]
```

**Adding a node:**
- Reassign slots from existing nodes
- Only ~1/N of keys move
- Migration happens in background

**Node failure:**
- Replica promoted to master
- Cluster redirects requests
- Minimal data loss (last few seconds)

**Key distribution example (5 nodes, ~3277 slots each):**
```
user:1001     → CRC16 = 8234 → Slot 8234 → Node 3
user:5000000  → CRC16 = 1456 → Slot 1456 → Node 1
post:abc123   → CRC16 = 12789 → Slot 12789 → Node 4
feed:user:1001 → CRC16 = 5621 → Slot 5621 → Node 2
```

### Task 3: Multi-Region Strategy

**Choice: Option C - Independent caches per region** (with smart invalidation)

**Justification:**
- Simplest to operate
- Lowest cross-region latency
- Cache misses go to local read replica

**Write pattern:**
```
Write → Primary Region DB → Async replicate → Other regions
                         → Invalidation event → All cache regions
```

**Read pattern:**
```
Read → Local cache → Local DB replica → Primary DB (fallback)
```

### Task 4: Failure Handling

**Single node failure:**
- Detection: 5-10 seconds (heartbeat timeout)
- Failover: Replica promotion (automatic)
- Data loss: Seconds of async replication lag

**Region failure:**
- Traffic: DNS/GLB reroutes to nearest healthy region
- Cache warming: Gradual (accept higher DB load initially)
- Stale data: Accept during failover, TTL handles cleanup

**Split brain:**
- Detection: Quorum-based (majority of Sentinels)
- Resolution: Minority partition becomes read-only, rejects writes

### Task 5: Capacity Planning

**Nodes:**
- 150TB / 50GB per node = 3000 master nodes
- 2 replicas each = 6000 replica nodes
- Total: 9000 nodes

**Network:**
- 10M ops/sec × 1KB avg = 10 GB/s
- Cross-node: ~30 GB/s (replication + redirects)

**Cost estimate:**
- 9000 nodes × 64GB = 576TB RAM
- Cloud: ~$0.10/GB/hour = $576K/month for RAM
- Plus compute, network, storage

### Task 6: Monitoring

| Metric | Threshold | Action if Exceeded |
|--------|-----------|-------------------|
| Hit rate | < 95% | Investigate access patterns, increase cache size |
| Latency p99 | > 10ms | Check network, add nodes, optimize keys |
| Memory usage | > 80% | Scale out, review eviction policy |
| Connection count | > 80% limit | Scale out, optimize connection pooling |
| Eviction rate | > 100/sec | Increase memory, review TTLs |

</details>
