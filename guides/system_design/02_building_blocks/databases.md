# Databases

Choosing and scaling databases for distributed systems.

## SQL vs NoSQL

### SQL (Relational)

**Characteristics:**
- Structured schema (tables, rows, columns)
- ACID transactions
- SQL query language
- Relationships via foreign keys

**Examples:** PostgreSQL, MySQL, Oracle, SQL Server

**Use when:**
- Complex queries and joins
- ACID compliance required
- Data integrity critical
- Well-defined schema

### NoSQL

**Types:**

| Type | Examples | Use Case |
|------|----------|----------|
| Key-Value | Redis, DynamoDB | Caching, sessions |
| Document | MongoDB, Couchbase | Flexible schema, JSON |
| Wide-Column | Cassandra, HBase | Time series, analytics |
| Graph | Neo4j, Neptune | Relationships, social |

**Use when:**
- Flexible schema needed
- Horizontal scaling required
- High write throughput
- Simple queries (key lookups)

## ACID vs BASE

### ACID (SQL)

- **Atomicity**: All or nothing transactions
- **Consistency**: Valid state to valid state
- **Isolation**: Concurrent transactions don't interfere
- **Durability**: Committed data survives failures

### BASE (NoSQL)

- **Basically Available**: System always responds
- **Soft state**: State may change over time
- **Eventually consistent**: Converges to consistency

## Database Scaling

### Vertical Scaling
Add more resources to single server.

**Limits:**
- Hardware ceiling
- Downtime for upgrades
- Cost increases exponentially

### Horizontal Scaling

#### Read Replicas

```
         ┌──────────┐
Writes ──│ Primary  │
         └────┬─────┘
              │ replication
     ┌────────┼────────┐
     ▼        ▼        ▼
┌────────┐ ┌────────┐ ┌────────┐
│Replica1│ │Replica2│ │Replica3│ ← Reads
└────────┘ └────────┘ └────────┘
```

**Benefits:**
- Scale read capacity
- Geographic distribution
- Failover capability

**Trade-offs:**
- Replication lag (eventual consistency)
- Write scaling unchanged

#### Sharding (Partitioning)

Distribute data across multiple databases.

```
         ┌─────────────────────────────────┐
         │         Shard Router            │
         └─────────────────────────────────┘
                 /         |         \
         ┌──────┐    ┌──────┐    ┌──────┐
         │Shard1│    │Shard2│    │Shard3│
         │ A-H  │    │ I-P  │    │ Q-Z  │
         └──────┘    └──────┘    └──────┘
```

**Sharding Strategies:**

| Strategy | Method | Pros | Cons |
|----------|--------|------|------|
| Range | user_id 1-1M | Simple queries | Hot spots |
| Hash | hash(key) % N | Even distribution | Range queries hard |
| Directory | Lookup table | Flexible | Extra hop |
| Geographic | By region | Low latency | Uneven sizes |

**Challenges:**
- Cross-shard queries
- Rebalancing data
- Transaction complexity
- Operational overhead

## Replication Strategies

### Synchronous

```
Client → Primary → Replica (wait) → ACK → Client
```

**Pros:** Strong consistency
**Cons:** Higher latency, reduced availability

### Asynchronous

```
Client → Primary → ACK → Client
              ↓
          Replica (later)
```

**Pros:** Low latency
**Cons:** Potential data loss, stale reads

### Semi-Synchronous

```
Client → Primary → At least 1 replica → ACK → Client
```

Balance between consistency and performance.

## Indexing

### B-Tree Index
Balanced tree structure for range queries.

```
                    [M]
                   /   \
              [D,H]     [R,W]
             / | \      / | \
          [A-C][E-G][I-L][N-Q][S-V][X-Z]
```

**Good for:** Range queries, sorted data
**Cost:** Write overhead, storage

### Hash Index
Direct lookup by key.

**Good for:** Equality queries
**Bad for:** Range queries

### Composite Index
Multiple columns.

```sql
CREATE INDEX idx_user_date ON orders(user_id, order_date);
```

**Order matters:** (A, B) works for A alone, but not B alone.

### Full-Text Index
Search within text content.

```sql
CREATE INDEX idx_content ON articles USING gin(to_tsvector(content));
```

## Query Optimization

### Explain Plans
```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';
```

### Common Optimizations

| Problem | Solution |
|---------|----------|
| Full table scan | Add index |
| N+1 queries | Use JOINs or batch |
| Large result sets | Pagination |
| Complex joins | Denormalize |
| Slow aggregations | Materialized views |

## Database Patterns

### Connection Pooling

```
App ─┬─ Connection 1 ─┐
     ├─ Connection 2 ─┼─── Database
     └─ Connection 3 ─┘
```

Reuse connections instead of creating per request.

### CQRS (Command Query Responsibility Segregation)

```
Commands (Write) ─→ Write Model ─→ Write DB
                                      │
                                  sync/async
                                      ↓
Queries (Read) ←── Read Model ←── Read DB
```

Separate read and write paths for optimization.

### Event Sourcing

Store events, not current state.

```
Events: [UserCreated] → [EmailChanged] → [NameChanged]
                                              ↓
                                         Rebuild State
```

**Benefits:** Audit trail, temporal queries
**Challenges:** Event schema evolution, storage

## Popular Databases

### Relational
| Database | Strength |
|----------|----------|
| PostgreSQL | Features, extensions |
| MySQL | Widespread, simple |
| CockroachDB | Distributed SQL |
| Vitess | MySQL sharding |

### NoSQL
| Database | Type | Strength |
|----------|------|----------|
| MongoDB | Document | Flexibility |
| Cassandra | Wide-column | Write scale |
| DynamoDB | Key-value | Managed, scalable |
| Redis | Key-value | Speed, data structures |
| Elasticsearch | Search | Full-text search |

## Interview Considerations

### Choosing a Database

```
Need ACID?
├── Yes → SQL (PostgreSQL, MySQL)
└── No
    ├── Simple key-value? → Redis, DynamoDB
    ├── Flexible schema? → MongoDB
    ├── High write throughput? → Cassandra
    ├── Search? → Elasticsearch
    └── Graph relationships? → Neo4j
```

### Capacity Estimation

```
Users: 10M
Writes: 100 writes/user/day = 1B writes/day
        = 11,500 writes/second

Storage: 1KB/write × 1B/day = 1TB/day
         = 365TB/year
```

## Interview Tips

1. Clarify data model and access patterns
2. Estimate scale (reads, writes, storage)
3. Choose SQL vs NoSQL with reasoning
4. Discuss scaling strategy (replicas, sharding)
5. Address consistency requirements
6. Plan for failure scenarios

## Related Topics

- [CAP Theorem](../01_fundamentals/cap_theorem.md)
- [Caching](caching.md)
- [Consistent Hashing](consistent_hashing.md)
