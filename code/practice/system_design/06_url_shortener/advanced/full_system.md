# Exercise: Complete URL Shortener System Design

## Objective
Design a production-ready URL shortening service.

## Problem Statement
Design a URL shortening service like bit.ly with:

**Scale:**
- 500M URLs created per month
- 50B redirects per month
- 99.99% availability
- < 50ms p99 redirect latency
- Global presence (serve users worldwide)

**Features:**
- URL shortening
- Custom aliases
- Link expiration
- Analytics (clicks, geo, referrer)
- User accounts and dashboards
- API access

## Tasks

### Task 1: Requirements Analysis

1. **Capacity estimation:**
   - URLs/second (write): ___
   - Redirects/second (read): ___
   - Read:Write ratio: ___
   - Storage per year: ___

2. **Identify critical vs nice-to-have:**

| Feature | Critical | Nice-to-have |
|---------|----------|--------------|
| Redirect | | |
| Create short URL | | |
| Analytics (real-time) | | |
| Analytics (historical) | | |
| Custom alias | | |
| User dashboard | | |

### Task 2: System Architecture

Design the complete system:

1. Draw architecture diagram including:
   - Load balancing layer
   - Application services
   - Data stores
   - CDN
   - Analytics pipeline

2. Explain the request flow for:
   - Creating a short URL
   - Redirect request
   - Viewing analytics

### Task 3: Data Model Design

Design schemas for all data stores:

1. **URL Store (primary database):**
   ```sql
   -- Your schema
   ```

2. **Analytics Store (time-series):**
   ```sql
   -- Your schema
   ```

3. **User/Account Store:**
   ```sql
   -- Your schema
   ```

4. **Cache structure:**
   ```
   -- Your Redis data structures
   ```

### Task 4: Analytics Pipeline

Design the analytics system:

1. **Real-time analytics:**
   - What data to capture per click?
   - How to process in real-time?
   - What to show on dashboard?

2. **Batch analytics:**
   - What aggregations to compute?
   - How often to run?
   - Where to store results?

3. **Data pipeline:**
   ```
   Click Event → ___ → ___ → ___ → Dashboard
   ```

### Task 5: Global Distribution

Design for global presence:

1. **CDN strategy:**
   - What to cache at edge?
   - Cache TTL?
   - Origin shield?

2. **Multi-region data:**
   - How to sync URLs across regions?
   - Where do writes go?
   - Consistency model?

3. **Geographic routing:**
   - How to route users to nearest region?
   - Failover strategy?

### Task 6: Production Considerations

1. **Security:**
   - Malicious URL detection?
   - Spam prevention?
   - Privacy (don't log sensitive data)?

2. **Monitoring:**
   - Key metrics to track?
   - Alerting thresholds?
   - On-call runbooks?

3. **Cost optimization:**
   - Most expensive components?
   - Optimization strategies?
   - Cost per 1M redirects estimate?

---

<details>
<summary>Hints</summary>

- 500M URLs/month = 200 URLs/second average
- 50B redirects/month = 20K redirects/second average
- CDN can cache popular redirects at edge
- Analytics can be eventually consistent
- Consider ClickHouse or similar for analytics

</details>

<details>
<summary>Solution</summary>

### Task 1: Requirements Analysis

**Capacity:**
- Writes: 500M/month = 200/second (peak: 2000/second)
- Reads: 50B/month = 20,000/second (peak: 200,000/second)
- Ratio: 100:1 read-heavy
- Storage: 500M × 500 bytes × 12 months = 3 TB/year

**Priority:**

| Feature | Priority | Reason |
|---------|----------|--------|
| Redirect | Critical | Core functionality |
| Create short URL | Critical | Core functionality |
| Analytics (real-time) | Nice-to-have | Can lag slightly |
| Analytics (historical) | Nice-to-have | Batch is fine |
| Custom alias | Nice-to-have | Premium feature |
| User dashboard | Nice-to-have | Not in critical path |

### Task 2: System Architecture

```
                              ┌─────────────────────────────────────┐
                              │            Global DNS               │
                              │         (Geo-routing)               │
                              └─────────────────┬───────────────────┘
                                                │
                    ┌───────────────────────────┼───────────────────────────┐
                    ▼                           ▼                           ▼
            ┌───────────────┐           ┌───────────────┐           ┌───────────────┐
            │   CDN Edge    │           │   CDN Edge    │           │   CDN Edge    │
            │   (US-East)   │           │   (EU-West)   │           │  (Asia-Pac)   │
            └───────┬───────┘           └───────┬───────┘           └───────┬───────┘
                    │                           │                           │
            ┌───────▼───────┐           ┌───────▼───────┐           ┌───────▼───────┐
            │ Regional LB   │           │ Regional LB   │           │ Regional LB   │
            └───────┬───────┘           └───────┬───────┘           └───────┬───────┘
                    │                           │                           │
        ┌───────────┼───────────┐               │                           │
        ▼           ▼           ▼               ▼                           ▼
   ┌─────────┐ ┌─────────┐ ┌─────────┐    ┌─────────┐                 ┌─────────┐
   │ API Svc │ │ API Svc │ │ API Svc │    │ API Svc │                 │ API Svc │
   └────┬────┘ └────┬────┘ └────┬────┘    └────┬────┘                 └────┬────┘
        │           │           │              │                           │
        └───────────┼───────────┘              │                           │
                    ▼                          ▼                           ▼
            ┌───────────────┐           ┌───────────────┐           ┌───────────────┐
            │ Redis Cluster │           │ Redis Cluster │           │ Redis Cluster │
            └───────────────┘           └───────────────┘           └───────────────┘
                    │                           │                           │
                    └───────────────────────────┼───────────────────────────┘
                                                │
                                        ┌───────▼───────┐
                                        │  PostgreSQL   │
                                        │  (Primary)    │◄──── Writes
                                        │  + Replicas   │
                                        └───────┬───────┘
                                                │
                                        ┌───────▼───────┐
                                        │    Kafka      │
                                        │  (Analytics)  │
                                        └───────┬───────┘
                                                │
                                        ┌───────▼───────┐
                                        │  ClickHouse   │
                                        │  (Analytics)  │
                                        └───────────────┘
```

### Task 3: Data Model

**URL Store:**
```sql
CREATE TABLE urls (
    id BIGSERIAL,
    short_code VARCHAR(10) PRIMARY KEY,
    original_url TEXT NOT NULL,
    user_id BIGINT,
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP,
    custom_alias BOOLEAN DEFAULT FALSE,
    status VARCHAR(20) DEFAULT 'active'
);

CREATE INDEX idx_user_urls ON urls(user_id, created_at);
```

**Analytics Store (ClickHouse):**
```sql
CREATE TABLE clicks (
    short_code String,
    timestamp DateTime,
    country_code String,
    referrer String,
    user_agent String,
    ip_hash String
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (short_code, timestamp);
```

**Cache:**
```
url:{short_code} → original_url (String, TTL 24h)
user:{user_id}:urls → [short_codes] (List, TTL 1h)
rate:{user_id} → count (String with INCR, TTL 60s)
```

### Task 4: Analytics Pipeline

**Real-time:**
```
Click → Kafka → Flink → Redis (real-time counters) → Dashboard
                   └───→ ClickHouse (raw events)
```

Capture: timestamp, short_code, country, referrer, device

**Batch (hourly):**
```sql
-- Aggregate clicks per hour
INSERT INTO clicks_hourly
SELECT 
    short_code,
    toStartOfHour(timestamp) as hour,
    country_code,
    count() as clicks
FROM clicks
WHERE timestamp > now() - INTERVAL 2 HOUR
GROUP BY short_code, hour, country_code;
```

### Task 5: Global Distribution

**CDN:**
- Cache: Popular redirects (top 10% gets 90% traffic)
- TTL: 1 hour (balance freshness vs hit rate)
- Origin shield: Yes, one per region

**Multi-region data:**
- URLs sync via async replication
- Writes to primary region, read from local
- Eventual consistency OK (seconds of lag)

**Routing:**
- GeoDNS routes to nearest region
- Failover: Automated via health checks

### Task 6: Production Considerations

**Security:**
- URL scanning via Google Safe Browsing API
- Rate limiting: 100 URLs/hour for free tier
- No IP logging, hash for analytics

**Monitoring:**
- Redirect latency (p50, p99)
- Error rate (4xx, 5xx)
- Cache hit rate
- Database connection pool

**Cost estimate:**
- CDN: ~$0.02/GB = $0.02 per 1M redirects (1KB each)
- Compute: $0.05 per 1M redirects
- Storage: $0.01 per 1M redirects
- **Total: ~$0.10 per 1M redirects**

</details>
