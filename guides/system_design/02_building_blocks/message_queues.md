# Message Queues

Asynchronous communication between services via message passing.

## Why Message Queues?

- **Decoupling**: Services don't need to know about each other
- **Async processing**: Don't block on slow operations
- **Load leveling**: Buffer traffic spikes
- **Reliability**: Persist messages until processed
- **Scalability**: Add consumers independently

## Core Concepts

### Producer-Consumer Pattern

```
Producer → Queue → Consumer
```

### Pub/Sub Pattern

```
Publisher → Topic → Subscriber 1
                 → Subscriber 2
                 → Subscriber 3
```

### Key Terms

| Term | Definition |
|------|------------|
| Message | Unit of data sent through the queue |
| Queue | FIFO buffer holding messages |
| Topic | Named channel for pub/sub |
| Producer | Service that sends messages |
| Consumer | Service that receives messages |
| Broker | Server managing queues/topics |

## Delivery Guarantees

### At-Most-Once
Message delivered 0 or 1 time.

```
Producer → Broker (no ack) → Consumer
```

**Trade-off:** Fastest, but may lose messages
**Use case:** Metrics, logs (loss acceptable)

### At-Least-Once
Message delivered 1+ times.

```
Producer → Broker → Consumer → ACK
                        ↓
              (if no ACK, redeliver)
```

**Trade-off:** No loss, but duplicates possible
**Use case:** Most applications (with idempotency)

### Exactly-Once
Message delivered exactly 1 time.

**Implementation:**
- Idempotency keys
- Transactional outbox
- Deduplication at consumer

**Trade-off:** Complex, higher latency
**Use case:** Financial transactions

## Message Ordering

### FIFO (Strict Order)

```
Send: A, B, C
Receive: A, B, C (guaranteed)
```

**Requirement:** Single partition/queue
**Trade-off:** Limited throughput

### Best-Effort Order

```
Send: A, B, C
Receive: A, C, B (possible)
```

**Trade-off:** Higher throughput, no ordering guarantee

### Partition-Based Ordering

```
Key: user_123 → Partition 3 → Ordered within partition
```

Messages with same key always go to same partition.

## Pull vs Push

### Pull (Polling)

```
Consumer ──(poll every N seconds)──> Broker
```

**Pros:** Consumer controls rate
**Cons:** Latency, wasted polls

### Push (Long Polling)

```
Consumer ──(wait for message)──> Broker
         <──(message arrives)──
```

**Pros:** Lower latency, efficient
**Cons:** Consumer must handle backpressure

## Acknowledgment Patterns

### Auto-ACK
```
Broker → Consumer (message deleted immediately)
```

Fast but risky if consumer crashes.

### Manual ACK
```
Broker → Consumer → Process → ACK → Broker (delete)
```

Safe but slower.

### Negative ACK (NACK)
```
Consumer → NACK → Broker (redeliver or dead-letter)
```

## Dead Letter Queues (DLQ)

Handle messages that fail repeatedly.

```
Queue → Consumer ──(fail)──> Retry
              ↓ (max retries)
         Dead Letter Queue → Manual inspection
```

**Use for:**
- Poison messages
- Debugging
- Audit trail

## Backpressure

When consumers can't keep up:

**Producer-side:**
- Block (synchronous)
- Drop messages
- Return error

**Consumer-side:**
- Rate limiting
- Scaling consumers
- Message TTL

## Common Patterns

### Work Queue (Competing Consumers)

```
Producer → Queue → Consumer 1
                → Consumer 2
                → Consumer 3
```

Each message processed by one consumer.

### Fanout

```
Producer → Exchange → Queue A → Consumer A
                   → Queue B → Consumer B
```

Each message goes to all consumers.

### Request-Reply

```
Request Queue:  Client → Server
Reply Queue:    Server → Client (correlation ID)
```

### Saga Pattern

Coordinate distributed transactions.

```
Order → Payment → Inventory → Shipping
          ↓          ↓           ↓
    (compensate) (compensate) (compensate)
```

## Popular Message Brokers

### Apache Kafka

**Architecture:**
```
Producer → Broker Cluster → Consumer Group
              ↓
         Partitioned Topics
              ↓
           Log Storage
```

**Strengths:**
- High throughput (100K+ msg/sec)
- Persistent log
- Replay capability
- Partitioning for scale

**Use cases:**
- Event streaming
- Log aggregation
- Real-time analytics

### RabbitMQ

**Architecture:**
```
Producer → Exchange → Queue → Consumer
                ↓
         Routing Rules
```

**Strengths:**
- Flexible routing
- Multiple protocols (AMQP, MQTT)
- Priority queues
- Plugin ecosystem

**Use cases:**
- Task queues
- RPC
- Complex routing

### Amazon SQS

**Types:**
- Standard: High throughput, best-effort ordering
- FIFO: Exactly-once, strict ordering

**Strengths:**
- Fully managed
- Scales automatically
- Pay per message

### Comparison

| Feature | Kafka | RabbitMQ | SQS |
|---------|-------|----------|-----|
| Throughput | Very High | High | High |
| Ordering | Partition | Queue | FIFO only |
| Persistence | Log | Optional | Managed |
| Replay | Yes | No | No |
| Complexity | High | Medium | Low |
| Managed | No* | No* | Yes |

*Cloud-managed versions available

## Design Considerations

### Idempotency

Messages may be delivered multiple times. Design consumers to handle duplicates.

```python
def process_payment(message):
    idempotency_key = message['idempotency_key']
    if already_processed(idempotency_key):
        return  # Skip duplicate
    
    process(message)
    mark_processed(idempotency_key)
```

### Message Size

- Keep messages small (< 1MB typically)
- Store large data elsewhere, pass reference
- Consider compression

### Monitoring

- Queue depth (messages waiting)
- Processing latency
- Error rates
- Consumer lag (Kafka)

## Interview Tips

1. Explain why async processing is needed
2. Choose appropriate delivery guarantee
3. Discuss ordering requirements
4. Plan for failure scenarios
5. Address idempotency
6. Choose broker based on requirements

## Related Topics

- [Event-Driven Architecture](../03_design_patterns/event_driven.md)
- [Saga Pattern](../03_design_patterns/saga_pattern.md)
- [Availability & Reliability](../01_fundamentals/availability_reliability.md)
