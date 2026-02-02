# Exercise: SQL vs NoSQL Decision

## Objective
Learn when to choose SQL vs NoSQL databases for different use cases.

## Scenarios

For each scenario, recommend SQL or NoSQL, specify which database, and justify your choice.

### Scenario 1: Banking Transaction System
**Requirements:**
- Strong consistency required
- Complex queries joining accounts, transactions, users
- ACID transactions for money transfers
- ~10,000 transactions/day

**Your recommendation:**
- Database type: ___
- Specific database: ___
- Justification: ___

### Scenario 2: Social Media Posts
**Requirements:**
- Flexible schema (posts can have text, images, videos, polls)
- High write throughput (1M posts/hour)
- Each post is mostly standalone
- Eventual consistency acceptable

**Your recommendation:**
- Database type: ___
- Specific database: ___
- Justification: ___

### Scenario 3: Real-Time Gaming Leaderboard
**Requirements:**
- Sorted rankings for millions of players
- Update scores in real-time
- Sub-millisecond read latency
- Simple key-value with sorting

**Your recommendation:**
- Database type: ___
- Specific database: ___
- Justification: ___

### Scenario 4: E-commerce Product Catalog
**Requirements:**
- Products have varying attributes (clothing has size/color, electronics have specs)
- Full-text search needed
- Hierarchical categories
- ~100K products, moderate traffic

**Your recommendation:**
- Database type: ___
- Specific database: ___
- Justification: ___

### Scenario 5: IoT Sensor Data
**Requirements:**
- 1 million sensors reporting every second
- Time-series data (timestamp + value)
- Query patterns: recent data, aggregations over time
- Data expires after 30 days

**Your recommendation:**
- Database type: ___
- Specific database: ___
- Justification: ___

## Summary Table

| Scenario | Type | Database | Key Reason |
|----------|------|----------|------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |

---

<details>
<summary>Hints</summary>

- ACID = SQL, flexible schema = Document DB
- High write = Cassandra, Sorted data = Redis
- Time-series has specialized databases
- Consider if you need joins

</details>

<details>
<summary>Solution</summary>

### Scenario 1: Banking Transaction System
- **Database type:** SQL
- **Specific database:** PostgreSQL
- **Justification:** ACID transactions critical for money transfers, need joins for account/user queries, strong consistency required

### Scenario 2: Social Media Posts
- **Database type:** NoSQL (Document)
- **Specific database:** MongoDB
- **Justification:** Flexible schema for varying post types, high write throughput, eventual consistency OK, no complex joins needed

### Scenario 3: Real-Time Gaming Leaderboard
- **Database type:** NoSQL (Key-Value/Sorted Set)
- **Specific database:** Redis
- **Justification:** Sorted sets provide O(log N) ranking, sub-millisecond latency, perfect for leaderboards

### Scenario 4: E-commerce Product Catalog
- **Database type:** Hybrid - Document + Search
- **Specific database:** MongoDB + Elasticsearch
- **Justification:** MongoDB for flexible product attributes, Elasticsearch for full-text search and faceted navigation

### Scenario 5: IoT Sensor Data
- **Database type:** Time-Series Database
- **Specific database:** InfluxDB or TimescaleDB
- **Justification:** Optimized for time-series writes, built-in retention policies, efficient time-based aggregations

### Summary Table

| Scenario | Type | Database | Key Reason |
|----------|------|----------|------------|
| 1 | SQL | PostgreSQL | ACID, joins, consistency |
| 2 | Document | MongoDB | Flexible schema, write throughput |
| 3 | Key-Value | Redis | Sorted sets, low latency |
| 4 | Document+Search | MongoDB + ES | Flexibility + search |
| 5 | Time-Series | InfluxDB | Optimized for time-series |

</details>
