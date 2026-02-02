# Exercise: WhatsApp-Scale Chat System

## Objective
Design a chat system handling 2 billion users and 100 billion messages/day.

## Requirements
- 2B registered users
- 100M concurrent connections
- 100B messages/day
- End-to-end encryption
- Offline message sync
- Group chats (up to 1000 members)
- 99.999% availability

## Tasks

### Task 1: Scale Calculations
- Messages/second: ___
- Storage/day: ___
- Bandwidth: ___
- WebSocket servers needed: ___

### Task 2: Architecture Design
Draw complete architecture including:
- Connection layer
- Message routing
- Storage layer
- Offline sync

### Task 3: Group Chat at Scale
How to handle a message to a 1000-member group?
- Fan-out strategy: ___
- Delivery tracking: ___

### Task 4: Multi-Device Sync
User has phone, tablet, and desktop. How to sync messages across all?

---

<details>
<summary>Solution</summary>

**Scale:** 1.15M messages/second, 100TB/day storage, 50TB bandwidth.

**Architecture:** Erlang/XMPP-based, sharded by user ID, Cassandra for messages.

**Group chat:** Fan-out on write for small groups, fan-out on read for large groups.

**Multi-device:** Message ID per device, sync using last-seen message ID.

</details>
