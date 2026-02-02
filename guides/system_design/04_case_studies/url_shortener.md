# URL Shortener Design

Design a URL shortening service like TinyURL or bit.ly.

## Requirements

### Functional Requirements
- Shorten a long URL to a short URL
- Redirect short URL to original URL
- Custom aliases (optional)
- Expiration time (optional)
- Analytics (click count, optional)

### Non-Functional Requirements
- High availability
- Low latency redirects
- Short URLs should be unpredictable
- Scale: 100M URLs/month created, 10:1 read:write ratio

## Capacity Estimation

### Traffic
```
Writes: 100M URLs/month
      = 100M / (30 × 24 × 3600) ≈ 40 URLs/second

Reads: 40 × 10 = 400 redirects/second
Peak: 400 × 5 = 2000 redirects/second
```

### Storage
```
Per URL: ~500 bytes (short URL, long URL, metadata)
Monthly: 100M × 500 bytes = 50 GB/month
5 years: 50 GB × 60 = 3 TB
```

### Short URL Length
```
Characters: a-z, A-Z, 0-9 = 62 characters
6 characters: 62^6 = 56.8 billion combinations
7 characters: 62^7 = 3.5 trillion combinations

For 100M URLs/month × 60 months = 6B URLs
→ 7 characters is sufficient
```

## High-Level Design

```
           ┌─────────────────────────────────────────┐
           │              Load Balancer              │
           └─────────────────────────────────────────┘
                              │
           ┌──────────────────┼──────────────────┐
           ▼                  ▼                  ▼
    ┌────────────┐     ┌────────────┐     ┌────────────┐
    │ App Server │     │ App Server │     │ App Server │
    └────────────┘     └────────────┘     └────────────┘
           │                  │                  │
           └──────────────────┼──────────────────┘
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
              ┌──────────┐       ┌──────────┐
              │  Cache   │       │ Database │
              │ (Redis)  │       │          │
              └──────────┘       └──────────┘
```

## Short URL Generation

### Approach 1: Hash and Encode

```python
import hashlib
import base64

def generate_short_url(long_url):
    # MD5 hash of URL
    hash_bytes = hashlib.md5(long_url.encode()).digest()
    
    # Base64 encode and take first 7 characters
    encoded = base64.urlsafe_b64encode(hash_bytes).decode()
    short_code = encoded[:7]
    
    return short_code
```

**Pros:** Deterministic, same URL → same short code
**Cons:** Collisions possible

### Approach 2: Counter-Based

```python
class Counter:
    def __init__(self, start=0):
        self.value = start
    
    def next(self):
        self.value += 1
        return base62_encode(self.value)

def base62_encode(num):
    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = []
    while num > 0:
        result.append(chars[num % 62])
        num //= 62
    return ''.join(reversed(result))
```

**Pros:** No collisions
**Cons:** Predictable, requires distributed counter

### Approach 3: Pre-Generated Keys

```
Key Generation Service → Key Database
                              │
                        Pre-generated keys
                              │
                        App Server (fetch keys in batch)
```

```python
class KeyService:
    def __init__(self):
        self.unused_keys = []
        self.used_keys = set()
    
    def get_keys(self, count=1000):
        # Fetch batch from key DB
        keys = key_db.fetch_unused(count)
        key_db.mark_used(keys)
        return keys
```

**Pros:** Fast, no collisions, unpredictable
**Cons:** Key management complexity

## Database Schema

### URL Table
```sql
CREATE TABLE urls (
    id BIGINT PRIMARY KEY,
    short_code VARCHAR(10) UNIQUE NOT NULL,
    long_url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP,
    user_id BIGINT,
    click_count INT DEFAULT 0
);

CREATE INDEX idx_short_code ON urls(short_code);
CREATE INDEX idx_expires_at ON urls(expires_at);
```

### Database Choice

**SQL (PostgreSQL):**
- ACID compliance
- Familiar queries
- Good for moderate scale

**NoSQL (DynamoDB, Cassandra):**
- Better horizontal scaling
- Simple key-value lookups
- Higher write throughput

## Caching Strategy

### Cache Redirect Mappings

```
Redis:
  short_code → long_url

Cache-aside pattern:
  1. Check cache
  2. If miss, query DB
  3. Populate cache
  4. Return
```

```python
def get_long_url(short_code):
    # Check cache
    long_url = cache.get(short_code)
    if long_url:
        return long_url
    
    # Query database
    url_record = db.query(
        "SELECT long_url FROM urls WHERE short_code = ?", 
        short_code
    )
    
    if url_record:
        # Populate cache
        cache.set(short_code, url_record.long_url, ttl=3600)
        return url_record.long_url
    
    return None
```

### Cache Hit Ratio Target: 80%+

Popular URLs accessed frequently → high cache efficiency.

## API Design

### Shorten URL
```
POST /api/shorten
Content-Type: application/json

{
  "long_url": "https://example.com/very/long/path",
  "custom_alias": "my-link",  // optional
  "expires_at": "2024-12-31"  // optional
}

Response:
{
  "short_url": "https://tiny.url/abc123d",
  "expires_at": "2024-12-31"
}
```

### Redirect
```
GET /abc123d

Response:
HTTP/1.1 301 Moved Permanently
Location: https://example.com/very/long/path
```

**301 vs 302:**
- 301: Permanent redirect (cached by browser)
- 302: Temporary redirect (not cached, enables analytics)

## Scaling Considerations

### Read-Heavy Optimization
- CDN for static redirects
- Read replicas
- Aggressive caching

### Write Scaling
- Database sharding by short_code
- Pre-generated key batches
- Async analytics updates

### Geographic Distribution
```
User (Asia) → CDN Edge → Regional App Server → Regional Cache
                                  │
                           Global Database
```

## Additional Features

### Analytics
```
Separate analytics service:
  - Click tracking
  - Geo data
  - Referrer
  - Device info
```

Use async processing (queue) to not block redirects.

### Custom Aliases
```sql
-- Check availability
SELECT 1 FROM urls WHERE short_code = 'custom-alias';

-- If available, insert
INSERT INTO urls (short_code, long_url) VALUES ('custom-alias', '...');
```

### Expiration
```python
# Background job
def cleanup_expired():
    while True:
        db.execute(
            "DELETE FROM urls WHERE expires_at < NOW()"
        )
        cache.delete_expired()
        time.sleep(3600)  # Run hourly
```

## Trade-offs

| Decision | Trade-off |
|----------|-----------|
| 301 vs 302 | SEO + caching vs analytics |
| Random vs sequential | Unpredictable vs simple |
| Cache TTL | Memory vs latency |
| SQL vs NoSQL | Consistency vs scale |

## Interview Tips

1. Start with requirements and estimates
2. Calculate short URL length needed
3. Discuss URL generation approaches
4. Design for read-heavy workload
5. Address caching strategy
6. Consider analytics as separate concern

## Related Topics

- [Caching](../02_building_blocks/caching.md)
- [Databases](../02_building_blocks/databases.md)
- [Consistent Hashing](../02_building_blocks/consistent_hashing.md)
