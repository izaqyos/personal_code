# Exercise: Distributed Storage Basics

## Objective
Understand distributed storage fundamentals.

## Tasks

### Task 1: Replication vs Erasure Coding
Compare approaches:
| Aspect | Replication (3x) | Erasure Coding |
|--------|------------------|----------------|
| Storage overhead | | |
| Read performance | | |
| Write performance | | |
| Recovery time | | |

### Task 2: Consistency Models
When to use each:
- Strong consistency: ___
- Eventual consistency: ___
- Read-your-writes: ___

### Task 3: Metadata Design
Design metadata for an object storage system:
```json
{
  "object_id": "...",
  // TODO: What else?
}
```

---

<details>
<summary>Solution</summary>

**Replication:** 200% overhead, fast reads, moderate writes, fast recovery.
**Erasure Coding:** ~50% overhead, slower reads, slower writes, slower recovery.

**Metadata:** object_id, bucket, key, size, checksum, created_at, storage_class, version.

</details>
