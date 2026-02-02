# Load Balancers

Distribute incoming traffic across multiple servers to ensure high availability and reliability.

## Why Load Balancing?

- **Distribute load**: Prevent any single server from being overwhelmed
- **High availability**: Route around failed servers
- **Horizontal scaling**: Add/remove servers dynamically
- **Maintenance**: Take servers offline without downtime

## Types of Load Balancers

### Layer 4 (Transport Layer)
Operates at TCP/UDP level.

**How it works:**
- Routes based on IP address and port
- No inspection of packet content
- Fast and efficient

**Use cases:**
- High-performance routing
- TCP/UDP traffic
- When content inspection not needed

### Layer 7 (Application Layer)
Operates at HTTP/HTTPS level.

**How it works:**
- Inspects HTTP headers, URLs, cookies
- Content-based routing
- SSL termination

**Use cases:**
- Web applications
- API routing
- A/B testing
- Authentication

### Comparison

| Feature | L4 | L7 |
|---------|----|----|
| Speed | Faster | Slower |
| Inspection | IP/Port only | Full content |
| SSL Termination | No | Yes |
| Routing flexibility | Limited | High |
| Cost | Lower | Higher |

## Load Balancing Algorithms

### Round Robin
Distribute requests sequentially.

```
Request 1 → Server A
Request 2 → Server B
Request 3 → Server C
Request 4 → Server A
...
```

**Pros:** Simple, even distribution
**Cons:** Ignores server capacity/load

### Weighted Round Robin
Distribute based on server capacity.

```
Weights: A=3, B=2, C=1
Requests: A, A, A, B, B, C, A, A, A, B, B, C, ...
```

**Pros:** Accounts for different server capabilities
**Cons:** Static weights, manual configuration

### Least Connections
Route to server with fewest active connections.

```
Server A: 10 connections
Server B: 5 connections ← Next request
Server C: 8 connections
```

**Pros:** Adapts to actual load
**Cons:** Doesn't account for connection duration

### Weighted Least Connections
Combines weights with connection count.

```
Score = connections / weight
Route to lowest score
```

### IP Hash
Route based on client IP.

```
hash(client_ip) % num_servers → Server
```

**Pros:** Same client → same server (session affinity)
**Cons:** Uneven distribution if IP range is skewed

### Least Response Time
Route to server with fastest response.

**Pros:** Optimizes for user experience
**Cons:** Requires health monitoring

## Health Checks

### Types

**Active (Synthetic):**
```
Load Balancer → /health → Server
                         ↓
                    200 OK or 503
```

**Passive (Real Traffic):**
```
Monitor actual request success/failure rates
```

### Health Check Configuration

```yaml
health_check:
  interval: 30s        # How often to check
  timeout: 5s          # Max wait time
  healthy_threshold: 2    # Consecutive successes to mark healthy
  unhealthy_threshold: 3  # Consecutive failures to mark unhealthy
  path: /health
```

### Graceful Degradation
```
Healthy → Unhealthy (stop new connections)
                   → Drain existing connections
                   → Remove from pool
```

## Session Affinity (Sticky Sessions)

Ensure same client routes to same server.

### Methods

**Cookie-based:**
```
Response: Set-Cookie: SERVERID=server_a
Request:  Cookie: SERVERID=server_a → Route to server_a
```

**IP-based:**
```
hash(client_ip) → Always same server
```

### When to Use

**Use sticky sessions:**
- In-memory session storage
- WebSocket connections
- Caching at server level

**Avoid sticky sessions:**
- Stateless applications
- External session store (Redis)
- Want even distribution

## SSL/TLS Termination

### At Load Balancer
```
Client ─[HTTPS]─> Load Balancer ─[HTTP]─> Servers
```

**Pros:**
- Centralized certificate management
- Offload crypto from app servers
- Inspect L7 traffic

**Cons:**
- Internal traffic unencrypted
- Load balancer must handle crypto

### End-to-End
```
Client ─[HTTPS]─> Load Balancer ─[HTTPS]─> Servers
```

**Pros:**
- Full encryption
- Defense in depth

**Cons:**
- Certificate per server
- L4 load balancing only (unless re-encryption)

## Architecture Patterns

### Single Load Balancer
```
        ┌────────────┐
        │    LB      │
        └────────────┘
         /    |    \
   ┌────┐  ┌────┐  ┌────┐
   │ S1 │  │ S2 │  │ S3 │
   └────┘  └────┘  └────┘
```
**Risk:** Single point of failure

### Active-Passive LB
```
   ┌────────────┐
   │  Primary   │←── Active
   └────────────┘
        ↕ heartbeat
   ┌────────────┐
   │  Standby   │←── Passive
   └────────────┘
```
**Failover:** Standby takes over on primary failure

### Active-Active LB
```
   ┌────────────┐   ┌────────────┐
   │    LB1     │   │    LB2     │
   └────────────┘   └────────────┘
         \              /
          \            /
           ┌──────────┐
           │  Servers │
           └──────────┘
```
**DNS:** Returns both LB IPs

## Global Load Balancing

### DNS-Based
```
User (US) → DNS → US datacenter IP
User (EU) → DNS → EU datacenter IP
```

**Methods:**
- GeoDNS: Route by user location
- Latency-based: Route to lowest latency
- Weighted: Percentage to each DC

### Anycast
Same IP announced from multiple locations.
Network routes to nearest announcement.

## Popular Solutions

| Solution | Type | Use Case |
|----------|------|----------|
| AWS ALB | L7 | HTTP/HTTPS apps |
| AWS NLB | L4 | TCP/UDP, low latency |
| HAProxy | L4/L7 | High performance |
| nginx | L7 | Web apps, reverse proxy |
| Envoy | L7 | Service mesh, gRPC |
| Cloudflare | L7 | CDN, DDoS protection |

## Interview Tips

1. Start with why you need load balancing
2. Choose L4 vs L7 based on requirements
3. Discuss algorithm choice
4. Address health checks and failover
5. Consider SSL termination strategy
6. Plan for load balancer redundancy

## Related Topics

- [Scalability](../01_fundamentals/scalability.md)
- [Availability & Reliability](../01_fundamentals/availability_reliability.md)
- [API Gateway](api_gateway.md)
