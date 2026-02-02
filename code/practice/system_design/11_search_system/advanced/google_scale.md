# Exercise: Web-Scale Search Engine

## Objective
Design a search engine for the web.

## Requirements
- 100B+ web pages indexed
- 10B queries/day
- < 200ms query latency
- Freshness (hours for news, days for general)
- Spam detection

## Tasks

### Task 1: Crawling
Design web crawler:
- Politeness: ___
- Prioritization: ___
- Deduplication: ___

### Task 2: Index Partitioning
How to partition 100B documents?
- Sharding strategy: ___
- Shard count: ___
- Replica placement: ___

### Task 3: Query Processing
Design query execution:
- Query parsing: ___
- Shard fan-out: ___
- Result merging: ___

### Task 4: Ranking
High-level ranking design:
- Signals used: ___
- Real-time vs offline: ___

---

<details>
<summary>Solution</summary>

**Crawling:** Respect robots.txt, prioritize by PageRank, SimHash for dedup.

**Partitioning:** Term-based sharding, 10K+ shards, 3 replicas per shard.

**Ranking:** 200+ signals including PageRank, freshness, user signals, ML ranking.

</details>
