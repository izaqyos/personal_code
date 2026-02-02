# Exercise: Payment Transaction Handling

## Objective
Design reliable payment transaction processing.

## Requirements
- 1M transactions/day
- Multiple payment methods
- Refund support
- Audit trail

## Tasks

### Task 1: State Machine
Design payment states:
```
CREATED → ___ → ___ → COMPLETED
    ↓         ↓
   FAILED   REFUNDED
```

### Task 2: Database Schema
Design payment tables:
```sql
CREATE TABLE payments (
    -- TODO
);

CREATE TABLE payment_events (
    -- TODO
);
```

### Task 3: Failure Handling
How to handle:
- Gateway timeout: ___
- Partial success: ___
- Double submission: ___

---

<details>
<summary>Solution</summary>

**States:** CREATED → AUTHORIZED → CAPTURED → SETTLED → COMPLETED.

**Failure:** Timeout → async status check, Partial → rollback, Double → idempotency check.

</details>
