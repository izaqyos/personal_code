# Exercise: Replication and Consistency Design

## Objective
Design database replication for various consistency requirements.

## Problem Statement
You're designing the database layer for a global financial trading platform:

**Requirements:**
- 3 regions: New York (primary), London, Tokyo
- Trade execution requires strong consistency
- Portfolio viewing can tolerate slight staleness
- Audit logs must be immutable and consistent
- 100K trades/day, 10M portfolio views/day

## Tasks

### Task 1: Replication Topology

Design the replication topology:

1. Draw the replication flow between regions

2. For each link, specify:
   - Synchronous or asynchronous?
   - Replication lag acceptable?
   - Conflict resolution needed?

3. What happens if New York goes down?

### Task 2: Consistency Levels per Operation

For each operation, specify the consistency level and justification:

| Operation | Consistency Level | Why |
|-----------|------------------|-----|
| Execute trade | | |
| View portfolio | | |
| Check account balance | | |
| View trade history | | |
| Write audit log | | |
| Generate daily report | | |

Consistency levels: Strong, Eventual, Read-your-writes, Causal

### Task 3: Conflict Resolution

Scenario: Network partition causes split-brain. Both New York and London process trades.

1. How do you detect the conflict?

2. Design a conflict resolution strategy for trades:
   ```
   Trade in NY: BUY 100 AAPL at $150 (timestamp: 10:00:00.100)
   Trade in London: SELL 50 AAPL at $151 (timestamp: 10:00:00.095)
   ```

3. How do you handle:
   - Both trades valid (sufficient shares)?
   - One trade invalid (insufficient shares)?
   - Both trades invalid?

### Task 4: Read-Your-Writes Consistency

User submits a trade in New York, then immediately views portfolio from London.

1. Problem: Replication lag means London doesn't have the trade yet

2. Design a solution that guarantees read-your-writes:
   - Approach: ___
   - Implementation: ___
   - Trade-offs: ___

### Task 5: Quorum Configuration

Given 5 replicas (2 in NY, 2 in London, 1 in Tokyo):

1. What W and R values ensure strong consistency?
   - W = ___
   - R = ___
   - Why? ___

2. What W and R values optimize for:
   - Low write latency: W=___, R=___
   - Low read latency: W=___, R=___
   - Balanced: W=___, R=___

3. If Tokyo replica fails, does each configuration still work?

### Task 6: Handling Replication Lag

Design monitoring and mitigation for replication lag:

1. **Metrics to track:**
   ```
   - ___
   - ___
   - ___
   ```

2. **Alerting thresholds:**
   | Lag | Action |
   |-----|--------|
   | > 1s | |
   | > 5s | |
   | > 30s | |

3. **Automatic mitigation:**
   - How to route reads when lag is high?
   - When to stop accepting writes?

---

<details>
<summary>Hints</summary>

- Synchronous replication guarantees consistency but adds latency
- Read-your-writes can use session tokens or routing
- Quorum: W + R > N for strong consistency
- Consider time-based conflict resolution for financial data

</details>

<details>
<summary>Solution</summary>

### Task 1: Replication Topology

```
              ┌────────────────┐
              │  New York (P)  │
              │   Primary      │
              └───────┬────────┘
                      │
        ┌─────────────┼─────────────┐
        │ sync        │ async       │
        ▼             ▼             
┌───────────────┐ ┌───────────────┐
│    London     │ │    Tokyo      │
│  (sync replica)│ │ (async replica)│
└───────────────┘ └───────────────┘
```

**Links:**
- NY → London: Synchronous (strong consistency for trades)
- NY → Tokyo: Asynchronous (latency too high for sync)

**Failover:**
- London promoted to primary (already sync)
- Tokyo continues as async replica
- Automatic with < 1 second downtime

### Task 2: Consistency Levels

| Operation | Consistency Level | Why |
|-----------|------------------|-----|
| Execute trade | Strong | Financial accuracy required |
| View portfolio | Read-your-writes | User's trades visible, slight lag OK |
| Check account balance | Strong | Must be accurate for trade validation |
| View trade history | Eventual | Historical, lag OK |
| Write audit log | Strong | Compliance requires consistency |
| Generate daily report | Eventual | Batch job, lag OK |

### Task 3: Conflict Resolution

1. **Detection:** 
   - Sequence numbers per region
   - Conflict when merging: same resource, different regions, overlapping time

2. **Resolution strategy:**
   ```
   1. Order by global timestamp (using synchronized clocks)
   2. Apply in order: SELL at 10:00:00.095 first
   3. Then BUY at 10:00:00.100
   4. If either fails validation, mark as PENDING_REVIEW
   ```

3. **Handling invalid trades:**
   - Both valid: Apply both in timestamp order
   - One invalid: Apply valid one, reject invalid with notification
   - Both invalid: Reject both, alert compliance team

### Task 4: Read-Your-Writes Consistency

**Problem:** User trades in NY, reads from London before replication.

**Solution - Session token approach:**
```python
def execute_trade(user_id, trade):
    result = primary_db.execute(trade)
    
    # Return position token (log sequence number)
    return {
        "trade_id": result.id,
        "position": primary_db.get_position()  # e.g., "NY:1234567"
    }

def get_portfolio(user_id, min_position=None):
    if min_position:
        # Wait for replica to catch up to position
        wait_for_position(replica_db, min_position, timeout=5s)
    
    return replica_db.get_portfolio(user_id)
```

**Trade-offs:** 
- Adds latency when read follows write
- Requires position tracking
- May timeout if lag too high

### Task 5: Quorum Configuration

With N=5 replicas:

1. **Strong consistency:** W=3, R=3 (W+R=6 > 5)

2. **Optimizations:**
   - Low write latency: W=1, R=5 (accept on one, read all)
   - Low read latency: W=5, R=1 (write to all, read any)
   - Balanced: W=3, R=3

3. **Tokyo failure (N=4):**
   - W=3, R=3: Still works (3 available >= W and R)
   - W=1, R=5: Fails (only 4 available for reads)
   - W=5, R=1: Fails (only 4 available for writes)

### Task 6: Handling Replication Lag

**Metrics:**
- Replication lag (seconds behind primary)
- Bytes pending replication
- Last applied transaction timestamp

**Alerting:**

| Lag | Action |
|-----|--------|
| > 1s | Warning, monitor closely |
| > 5s | Critical, route reads to primary |
| > 30s | Emergency, stop non-critical writes, investigate |

**Automatic mitigation:**
```python
def route_read(user_id, consistency_required):
    lag = get_replica_lag()
    
    if consistency_required == "strong" or lag > 5:
        return primary_db
    else:
        return replica_db

def can_accept_write(priority):
    lag = get_replica_lag()
    
    if priority == "critical":
        return True  # Trades always accepted
    elif lag > 30:
        return False  # Non-critical writes blocked
    else:
        return True
```

</details>
