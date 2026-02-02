# Exercise: Rate Limiter Service Design

## Objective
Design a complete rate limiting service for a large-scale platform.

## Problem Statement
Design a rate limiting service for a platform with:

**Scale:**
- 100M API requests/day
- 1M unique users
- 100 different rate limit rules
- 50 API servers consuming the service

**Requirements:**
- < 5ms p99 latency overhead
- 99.99% availability
- Support multiple limiting strategies (per user, per IP, per API key)
- Real-time rule updates without restart
- Analytics on rate limit hits

## Tasks

### Task 1: System Architecture

Design the high-level architecture:

1. Draw the system components:
   - Rate limiter service
   - Data stores
   - Configuration management
   - Analytics pipeline

2. How do API servers communicate with rate limiter?
   - Sync vs async?
   - Protocol?

3. What happens if rate limiter service is unavailable?

### Task 2: Rule Engine Design

Design the rule configuration system:

```yaml
# Example rule configuration
rules:
  - name: ___
    scope: ___  # user, ip, api_key, endpoint
    limit: ___
    window: ___
    action: ___  # reject, throttle, log
```

Design rules for:
1. Free tier users: 100 req/min globally
2. Pro tier: 1000 req/min globally, 100 req/sec per endpoint
3. Enterprise: Custom limits per customer
4. All users: 10 req/sec for expensive `/search` endpoint

### Task 3: Data Store Design

Design the data storage layer:

1. **For counters (real-time):**
   - Store: ___
   - Schema: ___
   - Replication: ___

2. **For rules (configuration):**
   - Store: ___
   - How to propagate updates?
   - Caching strategy?

3. **For analytics:**
   - Store: ___
   - What data to capture?
   - Retention policy?

### Task 4: API Design

Design the rate limiter API:

```protobuf
// gRPC or REST - your choice
// Design the request/response for:

// 1. Check if request is allowed
message CheckRequest {
    // TODO
}

message CheckResponse {
    // TODO
}

// 2. Get current usage
message UsageRequest {
    // TODO
}

// 3. Update rules (admin)
message UpdateRuleRequest {
    // TODO
}
```

### Task 5: Performance Optimization

Design for < 5ms p99 latency:

1. **Caching strategy:**
   - What to cache locally?
   - Cache invalidation?
   - Accuracy vs performance trade-off?

2. **Connection management:**
   - How to minimize network overhead?
   - Connection pooling design?

3. **Batch operations:**
   - When to batch?
   - Trade-offs?

### Task 6: Observability

Design monitoring and debugging:

1. **Key metrics:**
   | Metric | Purpose |
   |--------|---------|
   | | |
   | | |
   | | |

2. **Dashboards needed:**
   - ___
   - ___
   - ___

3. **Alerting rules:**
   | Alert | Condition | Priority |
   |-------|-----------|----------|
   | | | |
   | | | |

---

<details>
<summary>Hints</summary>

- Consider sidecar vs centralized service pattern
- gRPC for low-latency inter-service communication
- Local caching is crucial for latency
- Rule updates can use pub/sub for propagation

</details>

<details>
<summary>Solution</summary>

### Task 1: System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        API Servers (50)                             │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Rate Limit SDK (embedded)                                   │  │
│  │  - Local cache (rules + recent decisions)                    │  │
│  │  - Async sync with central service                           │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │ gRPC
                    ┌─────────────▼─────────────┐
                    │   Rate Limiter Service    │
                    │   (3+ instances, LB)      │
                    └─────────────┬─────────────┘
                                  │
           ┌──────────────────────┼──────────────────────┐
           ▼                      ▼                      ▼
    ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
    │    Redis     │      │   Postgres   │      │    Kafka     │
    │  (counters)  │      │   (rules)    │      │  (analytics) │
    └──────────────┘      └──────────────┘      └──────────────┘
```

**Communication:** gRPC for low latency, async for analytics.

**Service unavailable:** Fail-open with local cache fallback.

### Task 2: Rule Engine Design

```yaml
rules:
  - name: free_tier_global
    scope: user
    tier_match: free
    limit: 100
    window: 60
    action: reject
    
  - name: pro_tier_global
    scope: user
    tier_match: pro
    limit: 1000
    window: 60
    action: reject
    
  - name: pro_tier_per_endpoint
    scope: user_endpoint
    tier_match: pro
    limit: 100
    window: 1
    action: reject
    
  - name: enterprise_custom
    scope: user
    tier_match: enterprise
    limit: "${customer.custom_limit}"  # From customer config
    window: 60
    action: reject
    
  - name: search_all_users
    scope: user_endpoint
    endpoint: /search
    limit: 10
    window: 1
    action: reject
    priority: 10  # Higher priority, checked first
```

### Task 3: Data Store Design

1. **Counters (Redis Cluster):**
   ```
   Key: rl:{scope}:{identifier}:{window}
   Value: count (integer)
   TTL: window + buffer
   
   Replication: 3 replicas, 2 AZs
   ```

2. **Rules (PostgreSQL + cache):**
   ```sql
   CREATE TABLE rate_limit_rules (
       id UUID PRIMARY KEY,
       name VARCHAR(100),
       scope VARCHAR(50),
       tier_match VARCHAR(50),
       limit_value INT,
       window_seconds INT,
       action VARCHAR(20),
       priority INT DEFAULT 0,
       enabled BOOLEAN DEFAULT true,
       updated_at TIMESTAMP
   );
   ```
   
   Propagation: Redis Pub/Sub on rule change → SDK invalidates cache.

3. **Analytics (Kafka → ClickHouse):**
   ```json
   {
     "timestamp": "...",
     "user_id": "...",
     "endpoint": "...",
     "rule_name": "...",
     "decision": "allowed|rejected",
     "current_count": 45,
     "limit": 100
   }
   ```
   
   Retention: 30 days raw, 1 year aggregated.

### Task 4: API Design

```protobuf
service RateLimiter {
    rpc Check(CheckRequest) returns (CheckResponse);
    rpc GetUsage(UsageRequest) returns (UsageResponse);
    rpc UpdateRule(UpdateRuleRequest) returns (UpdateRuleResponse);
}

message CheckRequest {
    string user_id = 1;
    string api_key = 2;
    string ip_address = 3;
    string endpoint = 4;
    string tier = 5;
    int32 cost = 6;  // For weighted limiting
}

message CheckResponse {
    bool allowed = 1;
    int32 remaining = 2;
    int64 reset_at = 3;
    string rule_matched = 4;
    map<string, string> headers = 5;  // X-RateLimit-*
}

message UsageRequest {
    string user_id = 1;
    repeated string scopes = 2;
}

message UsageResponse {
    repeated ScopeUsage usage = 1;
}

message ScopeUsage {
    string scope = 1;
    int32 current = 2;
    int32 limit = 3;
    int64 reset_at = 4;
}
```

### Task 5: Performance Optimization

1. **Caching:**
   - Rules cached locally (5-minute TTL, pub/sub invalidation)
   - Recent decisions cached (100ms TTL for identical requests)
   - "Known good" users cached locally
   - Accuracy: ±10% acceptable for non-critical limits

2. **Connection management:**
   - gRPC connection pooling (10 connections per client)
   - HTTP/2 multiplexing
   - Keep-alive enabled

3. **Batch operations:**
   - Batch check for multiple endpoints in single request
   - Async counter updates (eventual consistency mode)
   - Trade-off: Slight over-limit in exchange for speed

### Task 6: Observability

**Key metrics:**
| Metric | Purpose |
|--------|---------|
| Check latency (p50, p99) | Performance |
| Rejection rate by rule | Rule effectiveness |
| Redis latency | Backend health |
| Cache hit rate | Optimization effectiveness |
| Requests per second | Capacity planning |

**Dashboards:**
- Service health (latency, errors, throughput)
- Rate limit effectiveness (rejections by rule, user, endpoint)
- Customer usage (usage vs limits)

**Alerting:**
| Alert | Condition | Priority |
|-------|-----------|----------|
| High latency | p99 > 10ms for 5min | P1 |
| Redis down | Connection failures | P1 |
| High rejection rate | > 10% rejections | P2 |
| Rule update failure | Update errors | P2 |

</details>
