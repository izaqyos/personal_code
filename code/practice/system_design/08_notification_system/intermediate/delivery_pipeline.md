# Exercise: Notification Delivery Pipeline

## Objective
Design a reliable notification delivery pipeline.

## Requirements
- 10M notifications/day
- Multiple channels (push, email, SMS)
- Retry failed deliveries
- Rate limiting per user

## Tasks

### Task 1: Pipeline Architecture
Design the notification pipeline:
```
Event → ___ → ___ → ___ → Delivery
```

### Task 2: Retry Strategy
Design retry logic for failed notifications:
- Max retries: ___
- Backoff strategy: ___
- Dead letter handling: ___

### Task 3: Rate Limiting
How to prevent notification spam?
- Per-user limits: ___
- Aggregation strategy: ___

---

<details>
<summary>Solution</summary>

**Pipeline:** Event → Queue → Router (by channel) → Channel Workers → Delivery Status.

**Retry:** 3 retries, exponential backoff (1m, 5m, 30m), DLQ for manual review.

**Rate limiting:** Max 10 push/hour, aggregate similar notifications.

</details>
