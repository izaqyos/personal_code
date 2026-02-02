# Exercise: Notification System Basics

## Objective
Understand different notification channels and their trade-offs.

## Tasks

### Task 1: Channel Comparison
Compare notification channels:

| Channel | Latency | Reliability | Cost | Use Case |
|---------|---------|-------------|------|----------|
| Push (Mobile) | | | | |
| Email | | | | |
| SMS | | | | |
| In-App | | | | |
| WebSocket | | | | |

### Task 2: Priority Design
Design notification priority levels:
- Critical: ___
- High: ___
- Medium: ___
- Low: ___

### Task 3: User Preferences Schema
```json
{
  "user_id": "123",
  "preferences": {
    // TODO: Design preference structure
  }
}
```

---

<details>
<summary>Solution</summary>

**Channels:** Push (low latency, unreliable), Email (high latency, reliable), SMS (medium, expensive).

**Priorities:** Critical=security alerts, High=transactions, Medium=social, Low=marketing.

</details>
