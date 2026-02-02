# Exercise: Basic Chat System Design

## Objective
Design the core components of a real-time chat system.

## Tasks

### Task 1: Choose Communication Protocol
Compare protocols for real-time messaging:

| Protocol | Latency | Complexity | Browser Support |
|----------|---------|------------|-----------------|
| HTTP Polling | | | |
| Long Polling | | | |
| WebSocket | | | |
| Server-Sent Events | | | |

Which would you choose for chat? ___

### Task 2: Message Data Model
Design the message schema:
```json
{
  // TODO: Define message structure
}
```

### Task 3: Basic Flow
Describe what happens when User A sends a message to User B.

---

<details>
<summary>Solution</summary>

**Protocol choice:** WebSocket - bidirectional, low latency, persistent connection.

**Message schema:**
```json
{
  "id": "msg-123",
  "conversation_id": "conv-456",
  "sender_id": "user-789",
  "content": "Hello!",
  "type": "text",
  "timestamp": 1640000000000
}
```

**Flow:** User A → WebSocket → Server → Lookup User B connection → WebSocket → User B

</details>
