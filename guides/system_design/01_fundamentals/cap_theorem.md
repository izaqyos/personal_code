# CAP Theorem

In a distributed system, you can only guarantee two of three properties at any given time.

## The Three Properties

### Consistency (C)
Every read receives the most recent write or an error.

- All nodes see the same data at the same time
- Linearizability: operations appear atomic
- Strong consistency vs. eventual consistency

### Availability (A)
Every request receives a response (success or failure).

- System is always operational
- No timeouts or errors due to system state
- Degraded responses still count as available

### Partition Tolerance (P)
System continues operating despite network partitions.

- Messages between nodes can be lost or delayed
- Network can split into isolated segments
- **In real systems, P is not optional**

## The CAP Triangle

```
            Consistency
               /\
              /  \
             /    \
            /  CP  \
           /________\
          /\        /\
         /  \  CA  /  \
        / AP \    /    \
       /______\  /______\
    Availability      Partition
                      Tolerance
```

## Why You Must Choose

### During a Network Partition

```
┌─────────┐         X         ┌─────────┐
│ Node A  │─────────X─────────│ Node B  │
│ Data: 1 │         X         │ Data: 1 │
└─────────┘         X         └─────────┘
     │                              │
  Write(2)                       Read(?)
     │                              │
     ▼                              ▼
┌─────────┐                   ┌─────────┐
│ Node A  │                   │ Node B  │
│ Data: 2 │                   │ Data: 1 │
└─────────┘                   └─────────┘
```

**Choice 1 (CP)**: Node B returns error (consistency over availability)

**Choice 2 (AP)**: Node B returns stale data (availability over consistency)

## System Classifications

### CP Systems (Consistency + Partition Tolerance)

**Behavior**: Refuse to respond if cannot guarantee consistency

**Examples:**
- MongoDB (with majority writes)
- HBase
- Redis Cluster
- Zookeeper
- etcd

**Use When:**
- Financial transactions
- Inventory management
- Booking systems
- Leader election

### AP Systems (Availability + Partition Tolerance)

**Behavior**: Always respond, even with potentially stale data

**Examples:**
- Cassandra
- DynamoDB
- CouchDB
- Riak

**Use When:**
- Shopping carts
- Social media feeds
- DNS
- Session stores

### CA Systems (Consistency + Availability)

**Behavior**: Works only when there's no partition

**Examples:**
- Single-node RDBMS
- Theoretically impossible in distributed systems

**Reality**: Not practical because partitions always happen

## Consistency Spectrum

CAP's "C" is about strong consistency, but there's a spectrum:

```
Strong ◄───────────────────────────► Eventual

Linearizable → Sequential → Causal → Eventual
    │              │           │         │
 Strictest    Total order   Happens   Converges
              per client    before    eventually
```

### Eventual Consistency

**Properties:**
- If no new updates, all replicas converge
- Replicas may be temporarily inconsistent
- Conflict resolution needed

**Conflict Resolution:**
- Last-write-wins (LWW)
- Vector clocks
- CRDTs (Conflict-free Replicated Data Types)

## Real-World Trade-offs

### Example: Shopping Cart

**Strong Consistency:**
- User always sees accurate cart
- Operations may fail during partitions
- Risk: Frustrated users can't checkout

**Eventual Consistency:**
- Cart always available
- Items might temporarily disappear/reappear
- Risk: User might see stale cart

**Practical Solution:**
- AP for cart operations
- CP for checkout/payment

### Example: Social Media

```
Write Post → Eventually replicate → Followers see post

Acceptable: 5-second delay before post appears
Unacceptable: Payment processes twice
```

## Common Misconceptions

1. **"CAP means choose 2 of 3"**
   - Reality: P is required; choose between C and A during partitions

2. **"Systems are either CP or AP"**
   - Reality: Systems can be tuned; different operations can have different guarantees

3. **"Eventual consistency means inconsistent"**
   - Reality: It means temporarily inconsistent, eventually converges

## Interview Tips

1. Understand that P is not optional in distributed systems
2. Explain the trade-off specific to the use case
3. Discuss what happens during network partitions
4. Consider hybrid approaches (CP for some ops, AP for others)
5. Mention PACELC as an extension

## Related Topics

- [PACELC Theorem](pacelc.md)
- [Databases](../02_building_blocks/databases.md)
- [Availability & Reliability](availability_reliability.md)
