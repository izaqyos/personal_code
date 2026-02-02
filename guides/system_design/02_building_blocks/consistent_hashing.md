# Consistent Hashing

A technique for distributing data across nodes while minimizing redistribution when nodes change.

## The Problem

### Naive Hashing

```
node = hash(key) % num_nodes
```

**Issue:** When nodes change, almost all keys need redistribution.

```
Before: 3 nodes
  key_a: hash(a) % 3 = 1 → Node 1
  key_b: hash(b) % 3 = 2 → Node 2
  key_c: hash(c) % 3 = 0 → Node 0

After: 4 nodes (added one)
  key_a: hash(a) % 4 = 2 → Node 2 (moved!)
  key_b: hash(b) % 4 = 3 → Node 3 (moved!)
  key_c: hash(c) % 4 = 1 → Node 1 (moved!)
```

**Problem:** ~N/N+1 keys move when adding 1 node to N nodes.

## Consistent Hashing Solution

### Hash Ring Concept

Map both keys and nodes to a circular hash space.

```
           0
           │
     Node A├───────────┐
           │           │
   270 ────┼──── 90    │
           │           │
     Node B├───────────┤
           │     Node C│
          180
```

### Key Assignment

Each key is assigned to the first node clockwise from its hash position.

```
        key_x
          ↓
    ┌─────●─────────────┐
    │                   │
Node A                 Node B
    │                   │
    └─────────●─────────┘
            key_y
            
key_x → Node A (first clockwise)
key_y → Node B (first clockwise)
```

### Node Addition

Only keys between new node and predecessor are redistributed.

```
Before: A handles keys from B to A

    ┌─────────────────┐
    │                 │
  Node A ←────────── Node B
    
After: C added between B and A

    ┌─────────────────┐
    │     Node C      │
  Node A ←──●←───── Node B
  
Only keys from B to C move to C
```

**Improvement:** Only ~K/N keys move (K keys, N nodes).

## Virtual Nodes (Vnodes)

### Problem with Basic Consistent Hashing

With few physical nodes, distribution can be uneven.

```
Node A: 60% of ring
Node B: 30% of ring
Node C: 10% of ring
```

### Solution: Virtual Nodes

Each physical node has multiple positions on the ring.

```
        A1    B1
    ┌───●─────●───┐
    │             │
   A2●           ●C1
    │             │
    └───●─────●───┘
        C2    B2
        
Physical Node A → Virtual: A1, A2
Physical Node B → Virtual: B1, B2
Physical Node C → Virtual: C1, C2
```

**Benefits:**
- More even distribution
- Smoother load balancing when nodes change
- Handle heterogeneous nodes (more vnodes for powerful servers)

## Implementation

### Basic Structure

```python
import hashlib
import bisect

class ConsistentHash:
    def __init__(self, nodes=None, virtual_nodes=100):
        self.virtual_nodes = virtual_nodes
        self.ring = {}
        self.sorted_keys = []
        
        if nodes:
            for node in nodes:
                self.add_node(node)
    
    def _hash(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
    
    def add_node(self, node):
        for i in range(self.virtual_nodes):
            vnode_key = f"{node}:{i}"
            hash_val = self._hash(vnode_key)
            self.ring[hash_val] = node
            bisect.insort(self.sorted_keys, hash_val)
    
    def remove_node(self, node):
        for i in range(self.virtual_nodes):
            vnode_key = f"{node}:{i}"
            hash_val = self._hash(vnode_key)
            del self.ring[hash_val]
            self.sorted_keys.remove(hash_val)
    
    def get_node(self, key):
        if not self.ring:
            return None
        
        hash_val = self._hash(key)
        idx = bisect.bisect_right(self.sorted_keys, hash_val)
        
        # Wrap around to first node
        if idx == len(self.sorted_keys):
            idx = 0
        
        return self.ring[self.sorted_keys[idx]]
```

### Usage

```python
ch = ConsistentHash(['server1', 'server2', 'server3'])

# Get node for keys
ch.get_node('user:123')  # → server2
ch.get_node('user:456')  # → server1

# Add node (minimal redistribution)
ch.add_node('server4')

# Remove node
ch.remove_node('server2')
```

## Replication with Consistent Hashing

### N Replicas

Store data on N consecutive nodes.

```
        N1    N2
    ┌───●─────●───┐
    │             │
   N4●     ●key  ●N3
    │             │
    └─────────────┘
    
key stored on: N2, N3, N4 (next 3 nodes clockwise)
```

### Replication Factor

```
N = 3 (store on 3 nodes)
W = 2 (write to at least 2)
R = 2 (read from at least 2)

W + R > N → Strong consistency
```

## Use Cases

### Distributed Caching

```
Cache Servers: A, B, C
key "user:123" → hash → Server B

All clients use same hash → same server for same key
```

**Examples:** Memcached, Redis Cluster

### Database Sharding

```
Shards: S1, S2, S3
user_id → hash → Shard S2
```

### Load Balancing

```
Servers: Web1, Web2, Web3
session_id → hash → Web2

Same session always routes to same server
```

### Content Distribution

```
CDN Edges: E1, E2, E3
URL → hash → Edge E1

Content cached at consistent edge
```

## Real-World Implementations

### Amazon DynamoDB
- Uses consistent hashing for partition placement
- Virtual nodes for even distribution
- Preference lists for replication

### Apache Cassandra
- Token ring based on consistent hashing
- Virtual nodes (vnodes)
- Configurable replication factor

### Discord
- Consistent hashing for message routing
- Shard assignment for guilds

## Comparison with Alternatives

| Approach | Redistribution | Complexity |
|----------|----------------|------------|
| Hash % N | ~100% on change | Low |
| Consistent Hashing | ~K/N | Medium |
| Range Partitioning | Variable | Medium |
| Directory-based | 0% | High (extra hop) |

## Interview Tips

1. Start with the problem (naive hashing redistribution)
2. Explain the ring concept visually
3. Discuss virtual nodes for even distribution
4. Mention replication across consecutive nodes
5. Give real-world examples (Cassandra, DynamoDB)
6. Discuss trade-offs (complexity vs redistribution)

## Related Topics

- [Databases](databases.md)
- [Caching](caching.md)
- [Scalability](../01_fundamentals/scalability.md)
