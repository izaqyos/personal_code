# Exercise: Enterprise Notification System

## Objective
Design a notification system for 100M users.

## Requirements
- 1B notifications/day
- Multi-channel (push, email, SMS, in-app)
- Template management
- A/B testing
- Analytics
- 99.9% delivery rate

## Tasks

### Task 1: Scale Calculations
- Notifications/second: ___
- Storage for templates: ___
- Queue depth: ___

### Task 2: System Architecture
Design complete system with:
- Ingestion layer
- Processing layer
- Delivery layer
- Analytics pipeline

### Task 3: Template Engine
Design dynamic template system:
- Variable substitution
- Localization
- Channel-specific rendering

### Task 4: Delivery Tracking
How to track delivery status across all channels?

---

<details>
<summary>Solution</summary>

**Scale:** 11,500/second peak, 10GB templates, 100K queue depth.

**Architecture:** Kafka ingestion → Worker pools per channel → Status tracking in Cassandra.

**Templates:** Handlebars-style with locale fallback.

</details>
