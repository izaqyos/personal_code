# Microservices Architecture

An architectural style that structures an application as a collection of loosely coupled, independently deployable services.

## Monolith vs Microservices

### Monolithic Architecture

```
┌─────────────────────────────────────┐
│           Single Application        │
│  ┌─────┐  ┌─────┐  ┌─────────────┐ │
│  │Users│  │Order│  │   Payment   │ │
│  └─────┘  └─────┘  └─────────────┘ │
│  ┌───────────────────────────────┐ │
│  │         Shared Database       │ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
```

**Pros:**
- Simple to develop, test, deploy
- Easy debugging
- No distributed system complexity

**Cons:**
- Hard to scale specific components
- Technology lock-in
- Large codebase becomes unwieldy
- Long deployment cycles

### Microservices Architecture

```
┌──────────┐   ┌──────────┐   ┌──────────┐
│User Svc  │   │Order Svc │   │Payment   │
│   ┌───┐  │   │   ┌───┐  │   │   ┌───┐  │
│   │DB │  │   │   │DB │  │   │   │DB │  │
│   └───┘  │   │   └───┘  │   │   └───┘  │
└──────────┘   └──────────┘   └──────────┘
      ↕              ↕              ↕
┌─────────────────────────────────────────┐
│           API Gateway / Mesh            │
└─────────────────────────────────────────┘
```

**Pros:**
- Independent deployment
- Technology flexibility
- Scale services independently
- Smaller, focused teams

**Cons:**
- Distributed system complexity
- Network latency
- Data consistency challenges
- Operational overhead

## Key Principles

### Single Responsibility
Each service does one thing well.

```
❌ User Service: handles users, orders, payments
✓ User Service: handles user management only
```

### Loose Coupling
Services should be independent.

```
❌ Order Service calls User DB directly
✓ Order Service calls User API
```

### High Cohesion
Related functionality stays together.

```
❌ User address in one service, user profile in another
✓ All user data in User Service
```

### Database per Service
Each service owns its data.

```
❌ Shared database across services
✓ User Service → User DB
  Order Service → Order DB
```

## Service Boundaries

### Domain-Driven Design (DDD)

**Bounded Context**: Logical boundary where a domain model applies.

```
┌─────────────────────────────────────────────┐
│ E-Commerce Domain                           │
│                                             │
│ ┌─────────────┐  ┌─────────────┐           │
│ │   Catalog   │  │  Ordering   │           │
│ │  Context    │  │  Context    │           │
│ │             │  │             │           │
│ │ Product     │  │ Order       │           │
│ │ Category    │  │ LineItem    │           │
│ └─────────────┘  └─────────────┘           │
│                                             │
│ ┌─────────────┐  ┌─────────────┐           │
│ │  Shipping   │  │  Payment    │           │
│ │  Context    │  │  Context    │           │
│ └─────────────┘  └─────────────┘           │
└─────────────────────────────────────────────┘
```

### Anti-Corruption Layer
Translate between different contexts.

```
Order Context ──> ACL ──> Legacy Inventory System
                  │
           (translation)
```

## Communication Patterns

### Synchronous (Request-Response)

```
Service A ──HTTP/gRPC──> Service B
         <────────────────
```

**Use when:**
- Immediate response needed
- Simple queries
- Low latency required

### Asynchronous (Event-Driven)

```
Service A ──publish──> Message Queue ──consume──> Service B
```

**Use when:**
- Fire and forget
- Long-running operations
- Loose coupling preferred

### API Styles

| Style | Use Case | Example |
|-------|----------|---------|
| REST | CRUD operations | GET /users/123 |
| GraphQL | Flexible queries | Query multiple resources |
| gRPC | High performance | Internal services |
| Events | Decoupling | Order created event |

## Service Discovery

How services find each other.

### Client-Side Discovery

```
Client → Service Registry → Get Service Location
   ↓
Call Service Directly
```

### Server-Side Discovery

```
Client → Load Balancer → Service Registry
                ↓
         Route to Service
```

**Tools:** Consul, etcd, Kubernetes DNS

## Data Management

### Database per Service

**Challenge:** How to query across services?

**Solutions:**

1. **API Composition**
   ```
   API Gateway calls multiple services, combines results
   ```

2. **CQRS**
   ```
   Separate read models aggregating data from multiple services
   ```

3. **Event Sourcing**
   ```
   Subscribe to events, build local read-optimized views
   ```

### Saga Pattern

Manage distributed transactions.

```
Order Saga:
  1. Create Order (Order Service)
  2. Reserve Inventory (Inventory Service)
  3. Process Payment (Payment Service)
  4. Ship Order (Shipping Service)
  
Compensation (if step 3 fails):
  2'. Release Inventory
  1'. Cancel Order
```

## Deployment Patterns

### One Service per Host

```
VM 1: User Service
VM 2: Order Service
VM 3: Payment Service
```

### Containerization

```
Docker:
  user-service:latest
  order-service:latest
  payment-service:latest
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: user-service
        image: user-service:latest
```

## Observability

### Logging
Centralized logging with correlation IDs.

```
Request ID: abc-123
  User Service: Processing user lookup
  Order Service: Fetching orders for user
  Payment Service: Checking payment status
```

### Metrics
Monitor service health.

- Request rate
- Error rate
- Latency (p50, p95, p99)
- Resource usage

### Distributed Tracing
Track requests across services.

```
Trace: abc-123
  └── User Service (10ms)
      └── Order Service (25ms)
          └── Payment Service (15ms)
```

**Tools:** Jaeger, Zipkin, AWS X-Ray

## Challenges

### Network Reliability
Networks fail; plan for it.

**Solutions:**
- Retries with backoff
- Circuit breakers
- Timeouts
- Bulkheads

### Data Consistency
No ACID across services.

**Solutions:**
- Eventual consistency
- Saga pattern
- Event sourcing

### Testing
Complex integration testing.

**Approaches:**
- Contract testing (Pact)
- Consumer-driven contracts
- End-to-end tests (sparingly)

### Operational Complexity
Many services to manage.

**Solutions:**
- Kubernetes
- Service mesh
- Infrastructure as code
- Platform teams

## When to Use Microservices

### Good Fit
- Large teams working in parallel
- Different scaling needs per service
- Polyglot requirements
- Rapid, independent deployments needed

### Not a Good Fit
- Small team / early startup
- Simple domain
- No clear service boundaries
- Limited DevOps maturity

## Interview Tips

1. Explain trade-offs vs monolith
2. Discuss service boundary definition (DDD)
3. Address data consistency (sagas, eventual consistency)
4. Plan for failure (circuit breakers, retries)
5. Discuss observability (logging, tracing, metrics)
6. Consider team structure (Conway's Law)

## Related Topics

- [Event-Driven Architecture](event_driven.md)
- [Saga Pattern](saga_pattern.md)
- [API Gateway](../02_building_blocks/api_gateway.md)
