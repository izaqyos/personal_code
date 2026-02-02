# Exercise: Payment System Basics

## Objective
Understand payment processing fundamentals.

## Tasks

### Task 1: Payment Flow
Describe the flow for a credit card payment:
```
Customer → ___ → ___ → ___ → Merchant
```

### Task 2: Key Concepts
Define:
- Authorization: ___
- Capture: ___
- Settlement: ___
- Chargeback: ___

### Task 3: Idempotency
Why is idempotency critical for payments?
Design an idempotency key strategy:
```
Key format: ___
Storage: ___
TTL: ___
```

---

<details>
<summary>Solution</summary>

**Flow:** Customer → Merchant → Payment Gateway → Card Network → Issuing Bank.

**Idempotency:** Prevents double-charging. Key: `{merchant_id}:{order_id}`, stored in Redis with 24h TTL.

</details>
