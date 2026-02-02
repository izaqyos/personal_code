# Exercise: S3-like Object Storage

## Objective
Design an S3-compatible object storage system.

## Requirements
- Exabyte scale
- 11 nines durability (99.999999999%)
- 99.99% availability
- Multi-region
- Versioning support
- Lifecycle policies

## Tasks

### Task 1: Architecture Design
Design complete system:
- API layer
- Metadata service
- Data service
- Index service

### Task 2: Durability Calculation
How to achieve 11 nines durability?
- Replication factor: ___
- Failure detection: ___
- Auto-healing: ___

### Task 3: Multi-Region
Design cross-region replication:
- Sync vs async: ___
- Conflict resolution: ___
- Consistency model: ___

### Task 4: Cost Optimization
Design storage tiers:
- Hot: ___
- Warm: ___
- Cold: ___
- Archive: ___

---

<details>
<summary>Solution</summary>

**Durability:** 3 replicas across 3 AZs + erasure coding for cold data + continuous scrubbing.

**11 nines:** P(data loss) = P(3 concurrent failures before repair) ≈ 10^-11.

**Tiers:** Hot (SSD), Warm (HDD), Cold (erasure coded), Archive (tape/deep archive).

</details>
