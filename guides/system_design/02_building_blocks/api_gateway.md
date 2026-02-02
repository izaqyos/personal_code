# API Gateway

A single entry point for all client requests to backend services.

## Why API Gateway?

- **Single entry point**: Clients access one endpoint
- **Cross-cutting concerns**: Authentication, rate limiting, logging
- **Protocol translation**: REST to gRPC, etc.
- **Request routing**: Direct to appropriate service
- **Response aggregation**: Combine multiple service responses

## Architecture

```
                    ┌──────────────────┐
Mobile ────────────>│                  │───> User Service
                    │                  │
Web ───────────────>│   API Gateway    │───> Order Service
                    │                  │
Partner ───────────>│                  │───> Payment Service
                    └──────────────────┘
                            │
                    Logging, Metrics
```

## Core Functions

### Request Routing

```yaml
routes:
  - path: /api/users/*
    service: user-service
    port: 8080
  
  - path: /api/orders/*
    service: order-service
    port: 8081
  
  - path: /api/payments/*
    service: payment-service
    port: 8082
```

### Authentication & Authorization

```
Client → Gateway → Auth Service
           ↓ (verified)
       Backend Service
```

**Methods:**
- API Keys
- JWT validation
- OAuth 2.0
- mTLS

### Rate Limiting

```
Client A: 100 requests/minute
Client B: 1000 requests/minute (premium)

Exceeded? → 429 Too Many Requests
```

**Algorithms:**
- Token bucket
- Sliding window
- Fixed window

### Request/Response Transformation

```
Client Request (JSON) → Gateway → Backend (gRPC)
                          ↓
              Transform request/response
```

### Response Aggregation

```
Client: GET /api/dashboard
          ↓
Gateway: Call user-service
         Call order-service
         Call analytics-service
          ↓
         Combine responses
          ↓
Client: Single aggregated response
```

## API Gateway Patterns

### Gateway per Client Type (BFF)

Backend for Frontend pattern.

```
Mobile App ───> Mobile BFF ───┐
                              ├───> Microservices
Web App ──────> Web BFF ──────┘
```

**Benefits:**
- Optimized for each client
- Different payload sizes
- Client-specific logic

### Gateway Routing

```
/api/v1/* ───> Legacy Service
/api/v2/* ───> New Service

Header: X-Version: beta ───> Beta Service
```

### Gateway Offloading

Move cross-cutting concerns from services to gateway.

```
Before: Each service handles SSL, auth, logging
After:  Gateway handles, services focus on business logic
```

## Features

### SSL/TLS Termination

```
Client ─[HTTPS]─> Gateway ─[HTTP]─> Services
```

Centralize certificate management.

### Caching

```
GET /api/products/123
  ↓
Gateway Cache ─[hit]─> Return cached
             ─[miss]─> Fetch from service
```

### Load Balancing

Gateway distributes requests across service instances.

```
Gateway ───> Service Instance 1
        ├──> Service Instance 2
        └──> Service Instance 3
```

### Circuit Breaking

Protect services from cascading failures.

```
Service unhealthy → Circuit OPEN → Return fallback
                         ↓ (timeout)
                  → Circuit HALF-OPEN → Test request
                         ↓ (success)
                  → Circuit CLOSED → Normal traffic
```

### Request Validation

```yaml
validation:
  /api/users:
    POST:
      required: [name, email]
      schema: user-schema.json
```

### Logging & Metrics

```
Every request:
  - Request ID
  - Timestamp
  - Duration
  - Status code
  - Client info
```

## Popular Solutions

### Cloud-Native

| Solution | Provider | Strengths |
|----------|----------|-----------|
| AWS API Gateway | AWS | Lambda integration, managed |
| Azure API Management | Azure | Enterprise features |
| Google Cloud Endpoints | GCP | gRPC support |
| Kong | Multi-cloud | Plugin ecosystem |

### Self-Hosted

| Solution | Language | Strengths |
|----------|----------|-----------|
| Kong | Lua/Go | Plugins, performance |
| NGINX | C | High performance |
| Envoy | C++ | Service mesh, gRPC |
| Express Gateway | Node.js | Developer-friendly |
| Spring Cloud Gateway | Java | Spring ecosystem |

## Configuration Example (Kong)

```yaml
services:
  - name: user-service
    url: http://user-service:8080
    routes:
      - name: user-route
        paths:
          - /api/users
        methods:
          - GET
          - POST
    plugins:
      - name: rate-limiting
        config:
          minute: 100
      - name: jwt
        config:
          secret_is_base64: false
```

## API Gateway vs Service Mesh

| Aspect | API Gateway | Service Mesh |
|--------|-------------|--------------|
| Scope | North-South traffic | East-West traffic |
| Position | Edge of system | Between services |
| Auth | Client authentication | Service-to-service |
| Examples | Kong, AWS API GW | Istio, Linkerd |

```
     API Gateway (N-S)
          │
    ┌─────┴─────┐
    │           │
Service A ←──→ Service B
         (E-W)
    Service Mesh
```

## Design Considerations

### Single Point of Failure

**Mitigation:**
- Multiple gateway instances
- Load balancer in front
- Health checks
- Auto-scaling

### Latency Overhead

```
Without gateway: Client → Service (10ms)
With gateway:    Client → Gateway → Service (12ms)
```

**Mitigation:**
- Keep gateway lightweight
- Colocate with services
- Use efficient protocols

### Coupling

Gateway knows about all services.

**Mitigation:**
- Service discovery
- Dynamic configuration
- Avoid business logic in gateway

## Interview Tips

1. Explain why centralized entry point is valuable
2. List key functions (auth, rate limiting, routing)
3. Discuss BFF pattern for different clients
4. Address single point of failure
5. Compare with service mesh
6. Choose appropriate solution for scale

## Related Topics

- [Load Balancers](load_balancers.md)
- [Rate Limiting](../03_design_patterns/rate_limiting.md)
- [Microservices](../03_design_patterns/microservices.md)
