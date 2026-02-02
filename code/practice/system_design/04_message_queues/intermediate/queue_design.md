# Exercise: Message Queue Architecture Design

## Objective
Design message queue architecture for complex event-driven systems.

## Problem Statement
You're building an event-driven e-commerce system with these services:
- Order Service
- Inventory Service
- Payment Service
- Notification Service
- Analytics Service

When an order is placed, multiple services need to react.

## Tasks

### Task 1: Event Flow Design

Design the event flow for the "Order Placed" scenario:

1. List all events that should be published
2. List which services subscribe to which events
3. Draw the event flow diagram

```
Order Placed
    │
    ├──> Event: ___
    │         Subscribers: ___
    │
    ├──> Event: ___
    │         Subscribers: ___
    ...
```

### Task 2: Topic vs Queue Decision

For each event type, choose Topic (pub/sub) or Queue (point-to-point):

| Event | Topic or Queue | Reason |
|-------|---------------|--------|
| OrderPlaced | | |
| PaymentProcessed | | |
| InventoryReserved | | |
| ShipmentCreated | | |
| AnalyticsEvent | | |

### Task 3: Message Schema Design

Design the message schema for OrderPlaced event:

```json
{
  // Your schema here
}
```

Consider:
- What fields are required?
- How to version the schema?
- What metadata to include?

### Task 4: Consumer Group Design

For the Notification Service consuming OrderPlaced:
- 3 instances of Notification Service
- Each order should be notified exactly once

1. How do you ensure only one instance processes each message?

2. What happens if one instance crashes mid-processing?

3. Design the consumer group configuration:
```yaml
consumer_group:
  name: ___
  partition_assignment: ___
  auto_commit: ___
  commit_interval: ___
```

### Task 5: Dead Letter Queue Design

Design DLQ handling for failed order processing:

1. When should messages go to DLQ?

2. DLQ message schema (what additional info to capture):
```json
{
  "original_message": {},
  // What else?
}
```

3. DLQ processing workflow:
```
Message fails → ___ → ___ → ___ → Manual intervention
```

### Task 6: Ordering Guarantees

Orders from the same customer should be processed in order.

1. How do you ensure ordering?

2. What's the partition key?

3. What happens if you have 10 partitions and 1 customer places 100 orders?

---

<details>
<summary>Hints</summary>

- Topics for fan-out (multiple subscribers), queues for competing consumers
- Consumer groups ensure each message processed by one consumer
- Partition key ensures ordering within a partition
- DLQs need original message + failure context

</details>

<details>
<summary>Solution</summary>

### Task 1: Event Flow Design

```
Order Placed
    │
    ├──> Event: OrderCreated
    │         Subscribers: Inventory, Payment, Analytics, Notification
    │
    ├──> (after inventory) Event: InventoryReserved
    │         Subscribers: Order (update status)
    │
    ├──> (after payment) Event: PaymentProcessed
    │         Subscribers: Order, Shipping, Notification
    │
    └──> (after shipping) Event: ShipmentCreated
              Subscribers: Order, Notification, Analytics
```

### Task 2: Topic vs Queue Decision

| Event | Type | Reason |
|-------|------|--------|
| OrderPlaced | Topic | Multiple services need to react |
| PaymentProcessed | Topic | Order + Shipping + Notification need it |
| InventoryReserved | Queue | Only Order Service needs to know |
| ShipmentCreated | Topic | Multiple services interested |
| AnalyticsEvent | Topic | Analytics may have multiple consumers |

### Task 3: Message Schema

```json
{
  "specversion": "1.0",
  "id": "evt-123-456-789",
  "source": "order-service",
  "type": "com.ecommerce.order.created.v1",
  "time": "2024-01-15T10:30:00.000Z",
  "datacontenttype": "application/json",
  "data": {
    "orderId": "ord-123",
    "customerId": "cust-456",
    "items": [
      {"productId": "prod-789", "quantity": 2, "price": 29.99}
    ],
    "total": 59.98,
    "currency": "USD",
    "shippingAddress": {
      "street": "123 Main St",
      "city": "Seattle",
      "country": "US"
    }
  },
  "metadata": {
    "correlationId": "req-abc-123",
    "userId": "user-456"
  }
}
```

### Task 4: Consumer Group Design

1. **Ensure one instance processes:** Use consumer group with partition assignment

2. **Crash handling:** 
   - Don't auto-commit
   - Commit after processing
   - On crash, partition reassigned to another consumer

3. **Configuration:**
```yaml
consumer_group:
  name: notification-service
  partition_assignment: cooperative-sticky  # Minimize rebalancing
  auto_commit: false  # Manual commit after processing
  commit_interval: N/A  # Not used with manual commit
  max_poll_records: 100
  session_timeout: 30s
  heartbeat_interval: 10s
```

### Task 5: Dead Letter Queue Design

1. **DLQ triggers:**
   - Message fails processing 3 times
   - Message cannot be deserialized
   - Processing exceeds timeout

2. **DLQ schema:**
```json
{
  "original_message": { /* original message */ },
  "failure_info": {
    "error_type": "ProcessingException",
    "error_message": "Inventory service unavailable",
    "stack_trace": "...",
    "attempts": 3,
    "first_failure_at": "2024-01-15T10:30:00Z",
    "last_failure_at": "2024-01-15T10:35:00Z"
  },
  "consumer_info": {
    "consumer_group": "notification-service",
    "consumer_id": "consumer-1",
    "partition": 3,
    "offset": 12345
  }
}
```

3. **DLQ workflow:**
```
Message fails → Retry (3x with backoff) → DLQ → Alert ops team → 
Manual review → Fix issue → Replay to main queue
```

### Task 6: Ordering Guarantees

1. **Ensure ordering:** Use partition key = customer_id

2. **Partition key:** `customer_id` (all orders from same customer go to same partition)

3. **100 orders from 1 customer:**
   - All go to same partition (determined by hash(customer_id))
   - Processed in order by single consumer assigned to that partition
   - Other 9 partitions handle other customers in parallel

</details>
