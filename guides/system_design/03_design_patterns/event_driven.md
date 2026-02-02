# Event-Driven Architecture

A design pattern where the flow of the program is determined by events - significant changes in state.

## Core Concepts

### What is an Event?

A record of something that happened.

```json
{
  "eventId": "evt-123",
  "eventType": "OrderCreated",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "orderId": "ord-456",
    "userId": "user-789",
    "total": 99.99
  }
}
```

**Characteristics:**
- Immutable (can't change the past)
- Past tense naming (OrderCreated, not CreateOrder)
- Contains all relevant data

### Event vs Command vs Query

| Type | Intent | Example |
|------|--------|---------|
| Command | Request action | CreateOrder |
| Event | Notify something happened | OrderCreated |
| Query | Request data | GetOrder |

## Architecture Patterns

### Event Notification

Services notify others about state changes.

```
Order Service ──OrderCreated──> Email Service
                            ──> Inventory Service
                            ──> Analytics Service
```

**Characteristics:**
- Loose coupling
- Publishers don't know subscribers
- Subscribers react independently

### Event-Carried State Transfer

Events carry full state, reducing callbacks.

```json
// Instead of just ID
{ "eventType": "CustomerUpdated", "customerId": "123" }

// Carry the data
{
  "eventType": "CustomerUpdated",
  "customerId": "123",
  "data": {
    "name": "John Doe",
    "email": "john@example.com",
    "address": "..."
  }
}
```

**Benefits:**
- Subscribers don't need to call back
- Works with stale source
- Decouples availability

### Event Sourcing

Store events as the source of truth, not current state.

```
Event Store:
  [OrderCreated] → [ItemAdded] → [ItemRemoved] → [OrderConfirmed]
                                                        │
                                                  Rebuild State
                                                        ↓
                                            Current Order Object
```

**Benefits:**
- Complete audit trail
- Time travel (reconstruct past states)
- Debug by replaying events

**Challenges:**
- Event schema evolution
- Storage growth
- Query complexity

### CQRS (Command Query Responsibility Segregation)

Separate read and write models.

```
Commands (Write) ──> Write Model ──> Event Store
                                         │
                                   (project events)
                                         ↓
Queries (Read) <── Read Model <── Read Database
```

**Why separate?**
- Different optimization needs
- Scale reads/writes independently
- Simpler models for each purpose

## Event Flow Patterns

### Choreography

Services react to events independently.

```
Order Created
     │
     ├──> Inventory: Reserve Stock
     │         │
     │    Stock Reserved
     │         │
     ├──> Payment: Process Payment
     │         │
     │    Payment Processed
     │         │
     └──> Shipping: Schedule Delivery
```

**Pros:**
- Loose coupling
- Simple to add new services

**Cons:**
- Hard to track overall flow
- Distributed logic

### Orchestration

Central coordinator manages the flow.

```
           ┌────────────────┐
           │  Orchestrator  │
           └───────┬────────┘
    ┌──────────────┼──────────────┐
    ↓              ↓              ↓
Inventory      Payment       Shipping
```

**Pros:**
- Clear workflow visibility
- Centralized logic

**Cons:**
- Orchestrator is a coupling point
- Can become complex

## Message Brokers

### Apache Kafka

Log-based, high throughput.

```
Producer → Topic (Partitioned Log) → Consumer Group
                    │
              Retained for days
                    │
              Replay possible
```

**Best for:**
- High volume event streaming
- Replay requirements
- Log aggregation

### RabbitMQ

Traditional message broker.

```
Producer → Exchange → Queue → Consumer
                ↓
         Routing Rules
```

**Best for:**
- Complex routing
- Priority queues
- Request-reply patterns

### AWS EventBridge

Serverless event bus.

```
Event Source → Event Bus → Rules → Targets (Lambda, SQS, etc.)
```

**Best for:**
- AWS-native applications
- Cross-account events
- SaaS integrations

## Event Design

### Schema Design

```json
{
  "specversion": "1.0",
  "type": "com.example.order.created",
  "source": "/orders/service",
  "id": "A234-1234-1234",
  "time": "2024-01-15T10:30:00Z",
  "datacontenttype": "application/json",
  "data": {
    "orderId": "123",
    "customerId": "456"
  }
}
```

Consider CloudEvents specification for standardization.

### Schema Evolution

How to handle schema changes?

**Strategies:**
1. **Additive only**: Only add fields
2. **Version in type**: `OrderCreatedV2`
3. **Schema registry**: Enforce compatibility

```
// Compatible change (add field)
v1: { orderId, customerId }
v2: { orderId, customerId, priority }  // new field

// Breaking change (remove/rename field)
v1: { orderId, customerId }
v2: { orderId, userId }  // renamed - breaks consumers
```

### Idempotency

Ensure events can be processed multiple times safely.

```python
def handle_order_created(event):
    event_id = event['eventId']
    
    if already_processed(event_id):
        return  # Idempotent - skip duplicate
    
    process_order(event)
    mark_processed(event_id)
```

## Error Handling

### Dead Letter Queue

Events that fail repeatedly go to DLQ.

```
Main Queue → Consumer ──(fail)──> Retry Queue
                                      │
                              (max retries exceeded)
                                      ↓
                               Dead Letter Queue
                                      │
                              Manual inspection
```

### Compensating Events

Undo effects of previous events.

```
Event: PaymentProcessed
Compensation: PaymentRefunded

Event: InventoryReserved
Compensation: InventoryReleased
```

### Retry Strategies

```python
retry_delays = [1, 5, 25, 125]  # seconds (exponential)

for attempt, delay in enumerate(retry_delays):
    try:
        process(event)
        break
    except TransientError:
        sleep(delay + random_jitter())
```

## Event-Driven vs Request-Response

| Aspect | Event-Driven | Request-Response |
|--------|--------------|------------------|
| Coupling | Loose | Tighter |
| Latency | Higher | Lower |
| Debugging | Harder | Easier |
| Scalability | Better | Depends |
| Consistency | Eventual | Immediate possible |

## Use Cases

### Good Fit
- Audit/compliance requirements
- Complex workflows
- Integration with external systems
- Analytics and reporting
- Decoupled microservices

### Not a Good Fit
- Simple CRUD
- Immediate consistency required
- Small applications
- Team unfamiliar with pattern

## Interview Tips

1. Explain difference between events and commands
2. Discuss choreography vs orchestration trade-offs
3. Address eventual consistency implications
4. Plan for failure (DLQ, retries, idempotency)
5. Consider event schema evolution
6. Choose appropriate message broker

## Related Topics

- [Message Queues](../02_building_blocks/message_queues.md)
- [Saga Pattern](saga_pattern.md)
- [Microservices](microservices.md)
