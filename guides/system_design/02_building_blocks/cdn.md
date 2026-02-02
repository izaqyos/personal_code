# Content Delivery Network (CDN)

Distributed network of servers that deliver content to users from nearby locations.

## Why CDN?

- **Reduce latency**: Content served from edge locations near users
- **Reduce origin load**: Cache absorbs traffic
- **Handle traffic spikes**: Distributed capacity
- **Improve availability**: Failover between edge locations
- **DDoS protection**: Absorb attacks at edge

## How CDN Works

```
User (Tokyo) → CDN Edge (Tokyo) → [Cache Hit] → Response
                      ↓
               [Cache Miss]
                      ↓
               Origin Server (US)
```

### Request Flow

1. User requests content (e.g., image.jpg)
2. DNS resolves to nearest CDN edge
3. Edge checks local cache
4. **Hit**: Return cached content
5. **Miss**: Fetch from origin, cache, return

## CDN Architecture

### Edge Locations (PoPs)

```
                    ┌─────────┐
                    │ Origin  │
                    └────┬────┘
         ┌───────────────┼───────────────┐
         ↓               ↓               ↓
    ┌─────────┐    ┌─────────┐    ┌─────────┐
    │ Edge US │    │ Edge EU │    │Edge Asia│
    └─────────┘    └─────────┘    └─────────┘
         ↑               ↑               ↑
      Users           Users           Users
```

### Tiered Architecture

```
User → Edge → Regional → Shield → Origin
       (L1)     (L2)      (L3)
```

- **Edge**: Many locations, small cache
- **Regional**: Fewer locations, larger cache
- **Shield**: Single layer before origin

## Content Types

### Static Content
Pre-built, doesn't change per request.

- Images, videos, CSS, JavaScript
- Font files
- PDF documents
- **Cache TTL**: Hours to days

### Dynamic Content
Generated per request.

- API responses
- Personalized pages
- **Cache TTL**: Seconds or no cache

### Streaming Media
Video/audio delivery.

- Adaptive bitrate (HLS, DASH)
- Edge transcoding
- Live vs VOD

## Caching Strategies

### Cache-Control Headers

```http
Cache-Control: max-age=86400, public
Cache-Control: no-cache
Cache-Control: private, max-age=3600
```

| Directive | Meaning |
|-----------|---------|
| max-age=N | Cache for N seconds |
| public | Can be cached by CDN |
| private | Only browser cache |
| no-cache | Revalidate before use |
| no-store | Never cache |

### Cache Keys

What makes a cached item unique:

```
Default: URL + Host
Custom:  URL + Host + Query Params + Headers + Cookies
```

**Example:**
```
https://example.com/api/user?lang=en
https://example.com/api/user?lang=es
→ Different cache entries
```

### Cache Invalidation

**Time-based (TTL):**
```
Set-Cookie: max-age=3600  # Expires in 1 hour
```

**Purge:**
```bash
# Invalidate specific URL
curl -X PURGE https://cdn.example.com/image.jpg
```

**Versioning:**
```
/assets/app.v2.js  # New version = new URL
```

## CDN Features

### SSL/TLS Termination
CDN handles HTTPS, optionally HTTP to origin.

```
User ─[HTTPS]─> CDN Edge ─[HTTP]─> Origin
```

### Compression
```
Origin → CDN (compress) → User
   or
Origin (pre-compressed) → CDN → User
```

Formats: gzip, brotli

### Image Optimization
```
/image.jpg?width=400&format=webp
```

- Resize
- Format conversion
- Quality adjustment
- Lazy loading

### Edge Computing
Run code at edge locations.

**Examples:**
- Cloudflare Workers
- AWS Lambda@Edge
- Fastly Compute@Edge

**Use cases:**
- A/B testing
- Authentication
- Geolocation redirects
- Request/response modification

## Performance Metrics

### Cache Hit Ratio
```
Hit Ratio = Cache Hits / Total Requests

Target: 90%+ for static content
```

### Time to First Byte (TTFB)
```
User Request → First Byte Received

CDN TTFB: 10-50ms (from edge)
Origin TTFB: 100-500ms (without CDN)
```

### Bandwidth Savings
```
Savings = (1 - Origin Bandwidth / Total Bandwidth) × 100%
```

## CDN Selection Criteria

| Factor | Consideration |
|--------|---------------|
| Coverage | PoP locations for your users |
| Features | Edge compute, image optimization |
| Performance | Latency, throughput |
| Pricing | Bandwidth, requests, features |
| Security | DDoS, WAF, bot protection |
| Integration | API, IaC support |

## Popular CDN Providers

| Provider | Strengths |
|----------|-----------|
| Cloudflare | Security, workers, free tier |
| AWS CloudFront | AWS integration |
| Akamai | Enterprise, coverage |
| Fastly | Edge compute, real-time |
| Google Cloud CDN | GCP integration |

## CDN Patterns

### Multi-CDN

```
DNS (Route 53) ─┬─> CDN A (70%)
                └─> CDN B (30%)
```

**Benefits:**
- Redundancy
- Performance optimization
- Vendor negotiation

### Origin Shield

```
Edge 1 ─┐
Edge 2 ──┼─> Shield ─> Origin
Edge 3 ─┘
```

Reduces origin load by consolidating cache fills.

### Failover

```
CDN → Origin A (primary)
         ↓ (failure)
      Origin B (backup)
```

## Security

### DDoS Protection
CDN absorbs volumetric attacks at edge.

### Web Application Firewall (WAF)
Filter malicious requests.

```
Rules: SQL injection, XSS, bot detection
```

### Bot Management
Distinguish good bots (Googlebot) from bad.

### Rate Limiting
```
Limit: 100 requests/second per IP
```

## Interview Tips

1. Explain CDN purpose (latency, load reduction)
2. Discuss cache strategies and invalidation
3. Consider content types (static vs dynamic)
4. Address cache warming for new content
5. Plan for cache misses and origin protection
6. Discuss security features

## Related Topics

- [Caching](caching.md)
- [Load Balancers](load_balancers.md)
- [Latency & Throughput](../01_fundamentals/latency_throughput.md)
