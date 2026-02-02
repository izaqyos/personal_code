# PACELC Theorem

An extension of CAP that addresses system behavior when there is **no** partition.

## The Limitation of CAP

CAP only describes behavior during network partitions. But what about normal operation?

**Key insight**: Even without partitions, there's a trade-off between consistency and latency.

## PACELC Explained

```
If Partition (P):
    Choose Availability (A) or Consistency (C)
Else (E):
    Choose Latency (L) or Consistency (C)
```

### Full Form
**P**artition → **A**vailability vs **C**onsistency, **E**lse **L**atency vs **C**onsistency

## The Four Categories

### PA/EL (Availability + Low Latency)
Prioritize availability and speed over consistency.

**Examples:**
- Cassandra (default)
- DynamoDB
- Riak

**Trade-offs:**
- Always available
- Low latency reads/writes
- Eventually consistent
- May read stale data

**Use Cases:**
- Social media feeds
- Shopping carts
- Session data
- Analytics

### PC/EC (Consistency Always)
Prioritize consistency regardless of conditions.

**Examples:**
- Traditional RDBMS with synchronous replication
- VoltDB
- ACID-compliant distributed databases

**Trade-offs:**
- Always consistent
- Higher latency (wait for replicas)
- Lower availability during partitions

**Use Cases:**
- Banking transactions
- Inventory management
- Reservation systems

### PA/EC (Availability during partition, Consistency otherwise)
Best of both worlds when possible.

**Examples:**
- MongoDB (with specific configurations)
- Cosmos DB (with strong consistency)

**Trade-offs:**
- Consistent during normal operation
- Falls back to available during partitions
- Moderate latency

**Use Cases:**
- E-commerce (normal: consistent, partition: accept orders)
- User profiles

### PC/EL (Consistent during partition, Low latency otherwise)
Rare combination - hard to achieve.

**Examples:**
- PNUTS (Yahoo's system)

**Trade-offs:**
- Low latency normally
- Sacrifices availability during partitions
- Complex to implement

## System Examples

| System | Partition | Normal | Classification |
|--------|-----------|--------|----------------|
| Cassandra | PA | EL | PA/EL |
| DynamoDB | PA | EL | PA/EL |
| MongoDB (default) | PC | EC | PC/EC |
| MySQL (single node) | - | EC | EC only |
| Cosmos DB (strong) | PC | EC | PC/EC |
| Cosmos DB (eventual) | PA | EL | PA/EL |
| CockroachDB | PC | EC | PC/EC |

## Why Latency Matters

### Synchronous Replication
```
Client → Primary → Replica₁ → Replica₂ → ACK → Client
         [10ms]    [50ms]      [50ms]    [10ms]
                                          
Total: 120ms per write
```

### Asynchronous Replication
```
Client → Primary → ACK → Client
         [10ms]    [10ms]

Total: 20ms per write
(Replicas updated in background)
```

### The Consistency-Latency Trade-off

```
Latency ◄───────────────────────────► Consistency

Async     Quorum      Read-your-    Strong
Repl.     Writes      own-writes    Consistency
 │           │            │             │
Fast      Medium      Moderate       Slow
Stale     Majority    Session       Always
          Consistent  Consistent    Current
```

## Tunable Consistency

Many modern databases allow tuning:

### Cassandra Example
```
Write: ANY → ONE → QUORUM → ALL
        │     │       │       │
     Fastest  │       │    Strongest
              │       │
           Balance    │
                   Consistent
```

### Read/Write Quorums
```
W + R > N → Strong consistency
W = N, R = 1 → Fast reads, slow writes
W = 1, R = N → Fast writes, slow reads

W = Write replicas required
R = Read replicas required  
N = Total replicas
```

## Decision Framework

```
┌─────────────────────────────────────┐
│ What's more important?              │
│                                     │
│ Data always correct?                │
│   ├── Yes → PC/EC systems           │
│   │         (MongoDB, CockroachDB)  │
│   │                                 │
│   └── No, availability/speed first? │
│         ├── Yes → PA/EL systems     │
│         │         (Cassandra, Dynamo)│
│         │                           │
│         └── Depends on operation?   │
│               → Use tunable systems │
│                 (Configure per-op)  │
└─────────────────────────────────────┘
```

## Interview Tips

1. Mention PACELC when discussing CAP trade-offs
2. Explain that latency is always a factor, not just during partitions
3. Discuss how systems can be tuned for different guarantees
4. Use specific examples (Cassandra vs MongoDB)
5. Connect to business requirements

## Related Topics

- [CAP Theorem](cap_theorem.md)
- [Databases](../02_building_blocks/databases.md)
- [Latency & Throughput](latency_throughput.md)
