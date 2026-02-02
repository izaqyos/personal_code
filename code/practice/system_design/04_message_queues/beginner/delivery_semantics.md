# Exercise: Message Delivery Semantics

## Objective
Understand and apply different message delivery guarantees.

## Delivery Semantics Review

| Semantic | Meaning | Trade-off |
|----------|---------|-----------|
| At-most-once | Message delivered 0 or 1 time | May lose messages |
| At-least-once | Message delivered 1+ times | May have duplicates |
| Exactly-once | Message delivered exactly 1 time | Complex, higher latency |

## Scenarios

For each scenario, choose the appropriate delivery semantic and explain how to implement it.

### Scenario 1: Click Tracking Analytics
**Context:** Track user clicks for analytics. Losing a few clicks is acceptable, but duplicates inflate metrics.

**Your choice:** ___

**Justification:** ___

**Implementation approach:** ___

### Scenario 2: Order Processing
**Context:** Process customer orders. Missing an order is unacceptable. Charging twice is also unacceptable.

**Your choice:** ___

**Justification:** ___

**Implementation approach:** ___

### Scenario 3: Email Notifications
**Context:** Send email notifications for events. Missing notifications is bad, but duplicates are annoying.

**Your choice:** ___

**Justification:** ___

**Implementation approach:** ___

### Scenario 4: Log Aggregation
**Context:** Aggregate logs from 1000 servers for monitoring. Volume is high (1M logs/second).

**Your choice:** ___

**Justification:** ___

**Implementation approach:** ___

## Task: Implement Idempotency

For at-least-once delivery, implement idempotent processing:

```python
# Message format
message = {
    "id": "msg-12345",  # Unique message ID
    "type": "order_created",
    "data": {"order_id": "ord-789", "amount": 99.99}
}

def process_order_message(message):
    # TODO: Implement idempotent processing
    # - Check if already processed
    # - Process if new
    # - Handle race conditions
    pass
```

---

<details>
<summary>Hints</summary>

- At-most-once: Don't retry, fire-and-forget
- At-least-once: Retry on failure, ack after processing
- Exactly-once: Use idempotency keys or transactions
- For idempotency, store processed message IDs

</details>

<details>
<summary>Solution</summary>

### Scenario 1: Click Tracking
- **Choice:** At-most-once
- **Justification:** High volume, losing a few clicks acceptable, duplicates would skew analytics
- **Implementation:** Fire and forget, no acks, no retries

### Scenario 2: Order Processing
- **Choice:** At-least-once with idempotency (effectively exactly-once)
- **Justification:** Can't lose orders, can't double-charge
- **Implementation:** Persist before ack, use order_id as idempotency key, check before processing

### Scenario 3: Email Notifications
- **Choice:** At-least-once with deduplication
- **Justification:** Missing notifications is worse than duplicates, but dedupe is easy
- **Implementation:** Retry on failure, dedupe at email service using notification ID

### Scenario 4: Log Aggregation
- **Choice:** At-most-once
- **Justification:** High volume, losing some logs acceptable, performance critical
- **Implementation:** UDP-like fire-and-forget, sample if overloaded

### Idempotent Processing Implementation

```python
import redis

redis_client = redis.Redis()
PROCESSED_TTL = 86400 * 7  # 7 days

def process_order_message(message):
    message_id = message["id"]
    
    # Check if already processed (atomic operation)
    if not redis_client.set(
        f"processed:{message_id}", 
        "1",
        nx=True,  # Only set if not exists
        ex=PROCESSED_TTL
    ):
        # Already processed - skip
        print(f"Skipping duplicate message: {message_id}")
        return
    
    try:
        # Process the order
        order_data = message["data"]
        create_order(order_data["order_id"], order_data["amount"])
        
    except Exception as e:
        # Failed - remove from processed set so it can be retried
        redis_client.delete(f"processed:{message_id}")
        raise

def create_order(order_id, amount):
    # Additional idempotency check at business level
    existing = db.query("SELECT id FROM orders WHERE id = ?", order_id)
    if existing:
        return existing  # Already created
    
    return db.insert("orders", {"id": order_id, "amount": amount})
```

</details>
