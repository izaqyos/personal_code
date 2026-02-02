# Exercise: Data Placement Strategy

## Objective
Design data placement for distributed storage.

## Requirements
- 100 PB total storage
- 1000 storage nodes
- Multiple datacenters
- Handle node failures gracefully

## Tasks

### Task 1: Placement Algorithm
Choose and explain:
- Random placement: ___
- Consistent hashing: ___
- CRUSH (Ceph-style): ___

### Task 2: Failure Domains
Design hierarchy:
```
Datacenter → Rack → Node → Disk
```
How to ensure replicas span failure domains?

### Task 3: Rebalancing
When a node fails or is added:
- Detection: ___
- Rebalancing strategy: ___
- Throttling: ___

---

<details>
<summary>Solution</summary>

**Placement:** CRUSH for hierarchical awareness + configurable policies.

**Failure domains:** Ensure 3 replicas are in 3 different racks minimum.

**Rebalancing:** Gradual migration, limit to 10% network capacity.

</details>
