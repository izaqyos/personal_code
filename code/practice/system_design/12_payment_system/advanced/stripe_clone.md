# Exercise: Stripe-like Payment Platform

## Objective
Design a payment platform for merchants.

## Requirements
- 10B transactions/year
- Global (multi-currency)
- PCI DSS compliant
- 99.999% availability
- Real-time fraud detection
- Instant payouts

## Tasks

### Task 1: Architecture
Design complete system:
- API layer
- Payment processor
- Fraud engine
- Settlement system
- Payout system

### Task 2: PCI Compliance
How to handle sensitive card data?
- Tokenization: ___
- Encryption: ___
- Data isolation: ___

### Task 3: Fraud Detection
Design real-time fraud detection:
- Signals: ___
- ML model: ___
- Decision latency: ___

### Task 4: Reconciliation
Design daily reconciliation:
- What to reconcile: ___
- Discrepancy handling: ___

---

<details>
<summary>Solution</summary>

**PCI:** Tokenize at edge, never store PAN, isolated cardholder data environment.

**Fraud:** Device fingerprint, velocity checks, ML model with < 100ms decision.

**Reconciliation:** Match gateway records with bank settlements, auto-resolve small discrepancies, escalate large ones.

</details>
