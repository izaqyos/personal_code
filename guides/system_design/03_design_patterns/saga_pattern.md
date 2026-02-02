# Saga Pattern

A pattern for managing distributed transactions across multiple services without using traditional two-phase commit.

## The Problem

### Distributed Transactions

In microservices, a single business operation may span multiple services.

```
Create Order:
  1. Order Service: Create order record
  2. Inventory Service: Reserve items
  3. Payment Service: Charge customer
  4. Shipping Service: Schedule delivery
```

**Challenge:** If step 3 fails, how do we undo steps 1 and 2?

### Why Not 2PC?

Two-Phase Commit (2PC) doesn't work well in microservices:
- High latency
- Reduced availability
- Resource locking
- Not supported by all databases

## Saga Solution

A saga is a sequence of local transactions where each transaction updates its own database and publishes an event to trigger the next transaction.

```
T1 → T2 → T3 → T4 (success path)
↓     ↓     ↓
C1    C2    C3    (compensating transactions if failure)
```

**Key insight:** Instead of ACID, use compensation to maintain consistency.

## Saga Types

### Choreography-Based Saga

Each service listens for events and decides what to do next.

```
Order Service                     Inventory Service
     │                                   │
     │ OrderCreated                      │
     │──────────────────────────────────>│
     │                                   │
     │                           InventoryReserved
     │<──────────────────────────────────│
     │                                   │
     │         Payment Service           │
     │                │                  │
     │────────────────│                  │
     │                │                  │
     │        PaymentProcessed           │
     │<───────────────│                  │
```

**Pros:**
- Loose coupling
- Simple for small sagas
- No single point of failure

**Cons:**
- Hard to track overall state
- Cyclic dependencies risk
- Testing complexity

### Orchestration-Based Saga

A central orchestrator coordinates the saga.

```
                  ┌─────────────────┐
                  │  Saga           │
                  │  Orchestrator   │
                  └────────┬────────┘
         ┌─────────────────┼─────────────────┐
         │                 │                 │
         ▼                 ▼                 ▼
   ┌──────────┐     ┌──────────┐     ┌──────────┐
   │ Order    │     │Inventory │     │ Payment  │
   │ Service  │     │ Service  │     │ Service  │
   └──────────┘     └──────────┘     └──────────┘
```

**Pros:**
- Clear workflow
- Easier to track and debug
- Centralized compensation logic

**Cons:**
- Orchestrator is a coupling point
- Single point of failure risk
- More complex implementation

## Implementation Example

### Order Saga (Orchestration)

```python
class OrderSaga:
    def __init__(self):
        self.steps = [
            SagaStep(
                action=self.create_order,
                compensation=self.cancel_order
            ),
            SagaStep(
                action=self.reserve_inventory,
                compensation=self.release_inventory
            ),
            SagaStep(
                action=self.process_payment,
                compensation=self.refund_payment
            ),
            SagaStep(
                action=self.schedule_shipping,
                compensation=self.cancel_shipping
            )
        ]
    
    def execute(self, order_data):
        completed_steps = []
        
        for step in self.steps:
            try:
                step.action(order_data)
                completed_steps.append(step)
            except Exception as e:
                # Rollback completed steps in reverse order
                for completed in reversed(completed_steps):
                    completed.compensation(order_data)
                raise SagaFailed(e)
        
        return Success()
```

### State Machine Representation

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  PENDING ──> INVENTORY_RESERVED ──> PAYMENT_PROCESSED      │
│     │               │                       │               │
│     │               │                       ▼               │
│     │               │              SHIPPING_SCHEDULED       │
│     │               │                       │               │
│     │               │                       ▼               │
│     │               │                   COMPLETED           │
│     │               │                                       │
│     ▼               ▼                                       │
│  CANCELLED    INVENTORY_FAILED ──> PAYMENT_REFUNDING       │
│                                            │                │
│                                            ▼                │
│                                        FAILED               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Compensating Transactions

### Design Principles

**Semantic Undo:** Undo the effect, not the exact transaction.

```
Original: Reserve 5 items
Compensation: Release 5 items (not "undo reserve")
```

**Idempotency:** Compensations may run multiple times.

```python
def release_inventory(order_id, items):
    # Check if already released
    if is_already_released(order_id):
        return
    
    for item in items:
        inventory.release(item.product_id, item.quantity)
    
    mark_released(order_id)
```

### Compensation Strategies

| Original Action | Compensation |
|-----------------|--------------|
| Create order | Cancel order |
| Reserve inventory | Release inventory |
| Charge payment | Refund payment |
| Send email | Send cancellation email |
| Create shipment | Cancel shipment |

## Error Handling

### Transient Failures

Retry with backoff before compensating.

```python
def execute_with_retry(action, max_retries=3):
    for attempt in range(max_retries):
        try:
            return action()
        except TransientError:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)
```

### Compensation Failures

What if compensation fails?

**Strategies:**
1. Retry compensation
2. Alert for manual intervention
3. Store in failed compensations table
4. Background job to retry

```python
def compensate_with_retry(compensation, max_retries=5):
    for attempt in range(max_retries):
        try:
            compensation()
            return
        except Exception:
            if attempt == max_retries - 1:
                store_failed_compensation(compensation)
                alert_operations_team()
```

### Saga State Persistence

Track saga state for recovery.

```sql
CREATE TABLE saga_instances (
    saga_id UUID PRIMARY KEY,
    saga_type VARCHAR(100),
    state VARCHAR(50),
    data JSONB,
    current_step INT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE saga_steps (
    id SERIAL PRIMARY KEY,
    saga_id UUID REFERENCES saga_instances,
    step_name VARCHAR(100),
    status VARCHAR(20),  -- PENDING, COMPLETED, COMPENSATED
    executed_at TIMESTAMP,
    compensated_at TIMESTAMP
);
```

## Saga Frameworks

| Framework | Language | Style |
|-----------|----------|-------|
| Axon Framework | Java | Both |
| Eventuate Tram | Java | Both |
| Temporal | Multi | Orchestration |
| AWS Step Functions | - | Orchestration |
| MassTransit | .NET | Both |

## Design Considerations

### Saga Timeout

What if a step takes too long?

```python
saga_config = {
    'timeout': timedelta(minutes=30),
    'step_timeout': timedelta(minutes=5)
}

# If timeout exceeded, start compensation
```

### Concurrent Sagas

Handle conflicts between sagas.

```python
# Optimistic locking
def reserve_inventory(product_id, quantity):
    inventory = get_inventory(product_id)
    
    if inventory.version != expected_version:
        raise ConcurrencyConflict()
    
    inventory.reserve(quantity)
    inventory.version += 1
    save(inventory)
```

### Saga Visibility

Track saga progress for debugging.

```
Saga: ORD-123
Status: FAILED
Steps:
  ✓ Create Order (completed in 50ms)
  ✓ Reserve Inventory (completed in 120ms)
  ✗ Process Payment (failed: insufficient funds)
  ← Cancel Order (compensated)
  ← Release Inventory (compensated)
```

## Choreography vs Orchestration

| Aspect | Choreography | Orchestration |
|--------|--------------|---------------|
| Coupling | Loose | Tighter |
| Visibility | Low | High |
| Complexity | Simple → Complex | Medium |
| Single Point of Failure | No | Yes (orchestrator) |
| Testing | Harder | Easier |
| Best for | Simple sagas | Complex workflows |

## Interview Tips

1. Explain why 2PC doesn't work for microservices
2. Describe saga as a sequence with compensations
3. Compare choreography vs orchestration
4. Discuss idempotency requirements
5. Address compensation failure handling
6. Consider saga state persistence and recovery

## Related Topics

- [Event-Driven Architecture](event_driven.md)
- [Microservices](microservices.md)
- [Message Queues](../02_building_blocks/message_queues.md)
