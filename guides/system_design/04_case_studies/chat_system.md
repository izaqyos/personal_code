# Chat System Design

Design a real-time messaging system like WhatsApp, Slack, or Discord.

## Requirements

### Functional Requirements
- 1-on-1 messaging
- Group chat (up to 500 members)
- Online/offline status (presence)
- Message delivery status (sent, delivered, read)
- Message history
- Push notifications (offline users)

### Non-Functional Requirements
- Real-time messaging (< 100ms latency)
- High availability
- Message ordering
- Message persistence
- Scale: 100M daily active users, 50B messages/day

## Capacity Estimation

### Traffic
```
DAU: 100M users
Messages: 50B/day = 500K messages/second

Connections: 100M concurrent WebSocket connections
```

### Storage
```
Message size: 1KB average (including metadata)
Daily: 50B × 1KB = 50 TB/day
1 year: 50 TB × 365 = 18 PB

With replication (3x): 54 PB
```

### Bandwidth
```
Incoming: 500K msg/s × 1KB = 500 MB/s
Outgoing: 500K msg/s × 3 recipients avg = 1.5 GB/s
```

## High-Level Design

```
                      ┌─────────────────────────┐
                      │     Load Balancer       │
                      └───────────┬─────────────┘
                                  │
          ┌───────────────────────┼───────────────────────┐
          ▼                       ▼                       ▼
   ┌──────────────┐       ┌──────────────┐       ┌──────────────┐
   │   WebSocket  │       │   WebSocket  │       │   WebSocket  │
   │    Server    │       │    Server    │       │    Server    │
   └──────────────┘       └──────────────┘       └──────────────┘
          │                       │                       │
          └───────────────────────┼───────────────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    ▼                           ▼
            ┌──────────────┐           ┌──────────────┐
            │    Redis     │           │   Message    │
            │   (Pub/Sub)  │           │    Queue     │
            └──────────────┘           └──────────────┘
                                              │
                                              ▼
                                       ┌──────────────┐
                                       │   Message    │
                                       │   Storage    │
                                       └──────────────┘
```

## Connection Management

### WebSocket Connections

```python
class WebSocketServer:
    def __init__(self):
        self.connections = {}  # user_id → WebSocket
        self.redis = Redis()
    
    async def on_connect(self, websocket, user_id):
        self.connections[user_id] = websocket
        
        # Register connection location
        server_id = os.environ['SERVER_ID']
        self.redis.set(f"user_location:{user_id}", server_id)
        
        # Publish presence update
        self.redis.publish("presence", json.dumps({
            "user_id": user_id,
            "status": "online"
        }))
    
    async def on_disconnect(self, user_id):
        del self.connections[user_id]
        self.redis.delete(f"user_location:{user_id}")
```

### Connection Routing

How to find which server a user is connected to?

```
User A (Server 1) → Message to User B
    │
    ▼
Redis: user_location:B = "Server 3"
    │
    ▼
Pub/Sub → Server 3 → User B
```

## Message Flow

### Sending a Message

```
1. Client A → WebSocket Server 1 (send message)
2. Server 1 → Message Queue (persist & process)
3. Message Service → Database (store message)
4. Message Service → Check User B location
5. If online: Pub/Sub → Server 3 → User B
   If offline: Push Notification Service
6. Server 1 → Client A (delivery confirmation)
```

### Message Structure

```json
{
  "message_id": "msg-uuid-123",
  "conversation_id": "conv-456",
  "sender_id": "user-789",
  "content": "Hello!",
  "type": "text",
  "timestamp": 1640000000000,
  "status": "sent"
}
```

## Database Design

### Messages Table (Cassandra)

```sql
CREATE TABLE messages (
    conversation_id UUID,
    message_id TIMEUUID,
    sender_id UUID,
    content TEXT,
    type VARCHAR,
    created_at TIMESTAMP,
    PRIMARY KEY (conversation_id, message_id)
) WITH CLUSTERING ORDER BY (message_id DESC);
```

**Why Cassandra?**
- High write throughput
- Time-series friendly (message ordering)
- Horizontal scaling

### Conversations Table

```sql
CREATE TABLE conversations (
    conversation_id UUID PRIMARY KEY,
    type VARCHAR,  -- 'direct' or 'group'
    participant_ids SET<UUID>,
    created_at TIMESTAMP,
    last_message_at TIMESTAMP
);
```

### User Conversations (Inbox)

```sql
CREATE TABLE user_conversations (
    user_id UUID,
    last_message_at TIMESTAMP,
    conversation_id UUID,
    unread_count INT,
    PRIMARY KEY (user_id, last_message_at, conversation_id)
) WITH CLUSTERING ORDER BY (last_message_at DESC);
```

## Presence System

### Heartbeat Approach

```python
class PresenceService:
    def __init__(self):
        self.redis = Redis()
        self.heartbeat_interval = 30  # seconds
    
    def update_presence(self, user_id):
        # Set with TTL
        self.redis.setex(
            f"presence:{user_id}",
            self.heartbeat_interval * 2,
            "online"
        )
    
    def get_presence(self, user_id):
        status = self.redis.get(f"presence:{user_id}")
        return "online" if status else "offline"
    
    def get_bulk_presence(self, user_ids):
        keys = [f"presence:{uid}" for uid in user_ids]
        statuses = self.redis.mget(keys)
        return {
            uid: "online" if status else "offline"
            for uid, status in zip(user_ids, statuses)
        }
```

### Presence Updates

Don't broadcast to everyone - fan out on read:

```
User opens chat:
  1. Fetch friend list
  2. Batch query presence for friends
  3. Subscribe to presence channel for friends
```

## Message Delivery Status

### Status Tracking

```
SENT → DELIVERED → READ
  │        │         │
Server   Recipient  Recipient
stored   received   opened chat
```

```python
class MessageStatus:
    def update_delivered(self, message_id, user_id):
        # Update message status
        db.execute("""
            UPDATE messages 
            SET delivered_at = NOW(), status = 'delivered'
            WHERE message_id = ? AND status = 'sent'
        """, message_id)
        
        # Notify sender
        sender_id = get_sender(message_id)
        notify_user(sender_id, {
            "type": "delivery_receipt",
            "message_id": message_id,
            "status": "delivered"
        })
    
    def update_read(self, conversation_id, user_id, up_to_message_id):
        # Mark all messages as read up to this point
        db.execute("""
            UPDATE messages 
            SET read_at = NOW(), status = 'read'
            WHERE conversation_id = ? 
            AND message_id <= ? 
            AND status != 'read'
        """, conversation_id, up_to_message_id)
```

## Group Chat

### Fan-out Strategies

**Fan-out on Write:**
```
Sender → Queue → Write to each recipient's inbox

Pros: Fast reads
Cons: Slow writes for large groups, storage duplication
```

**Fan-out on Read:**
```
Sender → Queue → Single write
Reader → Query group messages

Pros: Fast writes, less storage
Cons: Slower reads
```

**Hybrid:**
- Small groups (< 100): Fan-out on write
- Large groups (100+): Fan-out on read

### Group Message Delivery

```python
def send_group_message(group_id, sender_id, message):
    # Get group members
    members = get_group_members(group_id)
    
    # Store message once
    message_id = store_message(group_id, sender_id, message)
    
    # Notify online members
    for member_id in members:
        if member_id == sender_id:
            continue
        
        server_id = redis.get(f"user_location:{member_id}")
        
        if server_id:
            # Online - send via pub/sub
            redis.publish(f"user_messages:{server_id}", {
                "user_id": member_id,
                "message": message
            })
        else:
            # Offline - queue notification
            queue_push_notification(member_id, message)
```

## Offline Support

### Message Sync

```python
def sync_messages(user_id, last_sync_timestamp):
    # Get all conversations
    conversations = get_user_conversations(user_id)
    
    new_messages = []
    for conv in conversations:
        messages = db.query("""
            SELECT * FROM messages
            WHERE conversation_id = ?
            AND created_at > ?
            ORDER BY created_at
        """, conv.id, last_sync_timestamp)
        
        new_messages.extend(messages)
    
    return new_messages
```

### Push Notifications

```python
def queue_push_notification(user_id, message):
    notification = {
        "user_id": user_id,
        "title": message.sender_name,
        "body": message.content[:100],
        "data": {
            "conversation_id": message.conversation_id,
            "message_id": message.id
        }
    }
    
    push_queue.publish(notification)
```

## Scaling Considerations

### WebSocket Server Scaling

```
100M concurrent connections
Per server: 50K connections (limited by file descriptors)
Servers needed: 2000 WebSocket servers
```

### Database Sharding

```
Shard by conversation_id:
  - Messages for same conversation on same shard
  - Enables efficient queries

Shard by user_id for inbox:
  - User's conversations on same shard
```

### Message Queue Partitioning

```
Kafka topics:
  - messages (partitioned by conversation_id)
  - presence (partitioned by user_id)
  - notifications (partitioned by user_id)
```

## Trade-offs

| Decision | Trade-off |
|----------|-----------|
| Cassandra vs SQL | Scale vs queries |
| Fan-out on write/read | Write speed vs read speed |
| Heartbeat interval | Accuracy vs overhead |
| Message storage duration | Cost vs history access |

## Interview Tips

1. Start with scale estimation
2. Design WebSocket connection management
3. Explain message routing between servers
4. Discuss presence system (heartbeat + TTL)
5. Address offline users (sync + push)
6. Consider group chat optimizations

## Related Topics

- [Message Queues](../02_building_blocks/message_queues.md)
- [Load Balancers](../02_building_blocks/load_balancers.md)
- [Databases](../02_building_blocks/databases.md)
