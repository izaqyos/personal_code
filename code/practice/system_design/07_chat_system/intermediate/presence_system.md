# Exercise: Presence System Design

## Objective
Design online/offline presence tracking for a chat application.

## Requirements
- Show when users are online/offline
- Show "last seen" for offline users
- Handle 1M concurrent users
- Update presence in < 5 seconds

## Tasks

### Task 1: Heartbeat Design
Design the heartbeat mechanism:
- Interval: ___
- Protocol: ___
- Timeout to mark offline: ___

### Task 2: Storage Design
How to store presence status for 1M users?
- Data structure: ___
- Storage system: ___
- Key format: ___

### Task 3: Presence Updates
How to notify friends when someone goes online/offline?
- Option A: Push to all friends immediately
- Option B: Query on demand
- Option C: Hybrid

Choose and justify: ___

---

<details>
<summary>Solution</summary>

**Heartbeat:** 30-second interval, WebSocket ping, 60-second timeout.

**Storage:** Redis with `SET presence:{user_id} online EX 60`

**Updates:** Hybrid - push to close friends, query for others.

</details>
