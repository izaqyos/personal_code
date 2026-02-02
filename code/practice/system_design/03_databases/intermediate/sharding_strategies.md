# Exercise: Database Sharding Design

## Objective
Design sharding strategies for different data access patterns.

## Problem Statement
You're scaling a multi-tenant SaaS application with:
- 10,000 tenants (companies)
- 100M total users
- 1B rows of activity data
- Query patterns vary by feature

## Tasks

### Task 1: Shard Key Selection

For each table, choose a shard key and justify:

**Users Table:**
- Columns: user_id, tenant_id, email, name, created_at
- Query patterns: Lookup by user_id, list users by tenant

Shard key: ___
Justification: ___

**Activity Table:**
- Columns: activity_id, user_id, tenant_id, type, data, timestamp
- Query patterns: Recent activity by user, activity report by tenant

Shard key: ___
Justification: ___

**Billing Table:**
- Columns: invoice_id, tenant_id, amount, status, created_at
- Query patterns: Invoices by tenant, monthly revenue reports

Shard key: ___
Justification: ___

### Task 2: Sharding Scheme

Design the sharding scheme for the Users table:

1. **Hash-based**: How would you distribute 100M users across 16 shards?
   ```
   shard_number = ___
   ```

2. **Range-based**: Define ranges for 16 shards
   ```
   Shard 0: user_id ___
   Shard 1: user_id ___
   ...
   ```

3. **Directory-based**: Design the lookup table schema
   ```sql
   CREATE TABLE ___
   ```

Which approach would you recommend and why?

### Task 3: Cross-Shard Queries

How would you handle these queries?

1. **Query**: Find all users with email domain "@example.com"
   - Problem: ___
   - Solution: ___

2. **Query**: Count total users per tenant (tenant has users across shards)
   - Problem: ___
   - Solution: ___

3. **Query**: Join users with their recent activity
   - Problem: ___
   - Solution: ___

### Task 4: Hotspot Prevention

Tenant A has 10M users (10% of total), Tenant B has 100 users.

1. How does this create a hotspot with tenant_id sharding?

2. Design a solution to distribute Tenant A's load:
   - Approach: ___
   - Implementation: ___

3. What's the trade-off of your solution?

### Task 5: Resharding Plan

Your 16 shards are full. Plan the migration to 32 shards:

1. Strategy choice:
   - [ ] Double shards, migrate in place
   - [ ] Shadow cluster, switchover
   - [ ] Consistent hashing (add incrementally)

2. Steps to minimize downtime:
   ```
   Step 1: ___
   Step 2: ___
   Step 3: ___
   ...
   ```

3. Rollback plan:
   ___

---

<details>
<summary>Hints</summary>

- Shard key should match most common query pattern
- Tenant-based sharding works well for multi-tenant
- Cross-shard queries require scatter-gather
- Consider composite shard keys for hotspots

</details>

<details>
<summary>Solution</summary>

### Task 1: Shard Key Selection

**Users Table:**
- Shard key: **tenant_id**
- Justification: Most queries are tenant-scoped (list users in company), keeps all tenant's users together for efficient queries

**Activity Table:**
- Shard key: **tenant_id** (same as users)
- Justification: Activity reports are by tenant, co-locates with users for potential joins

**Billing Table:**
- Shard key: **tenant_id**
- Justification: All billing queries are tenant-scoped, invoices always accessed by tenant

### Task 2: Sharding Scheme

**Hash-based:**
```
shard_number = hash(tenant_id) % 16
```

**Range-based:**
```
Shard 0: tenant_id 0-624
Shard 1: tenant_id 625-1249
...
Shard 15: tenant_id 9375-9999
```

**Directory-based:**
```sql
CREATE TABLE shard_directory (
    tenant_id INT PRIMARY KEY,
    shard_id INT NOT NULL,
    created_at TIMESTAMP
);
```

**Recommendation:** Hash-based for even distribution with directory for large tenants that need special placement.

### Task 3: Cross-Shard Queries

1. **Email domain search:**
   - Problem: Email not part of shard key, must query all shards
   - Solution: Secondary index (Elasticsearch) on email domain, or async job to maintain domain→tenant mapping

2. **User count per tenant:**
   - Problem: If using user_id sharding, tenant spans shards
   - Solution: With tenant_id sharding, no problem! Otherwise, scatter-gather query to all shards

3. **User-Activity join:**
   - Problem: May be on different shards if different shard keys
   - Solution: Use same shard key (tenant_id) for both tables, queries stay local

### Task 4: Hotspot Prevention

1. **Hotspot problem:** Shard containing Tenant A has 100x more load than shard with Tenant B

2. **Solution - Virtual sharding:**
   ```
   Large tenants get multiple virtual tenant IDs:
   Tenant A → tenant_A_0, tenant_A_1, tenant_A_2, ... tenant_A_9
   
   Users distributed:
   shard = hash(tenant_id + "_" + user_id % 10)
   ```

3. **Trade-off:** Cross-shard queries for single large tenant, more complex routing logic

### Task 5: Resharding Plan

**Strategy:** Consistent hashing with gradual migration

**Steps:**
1. Add 16 new shards to cluster (no traffic yet)
2. Update consistent hash ring to include new shards
3. Start dual-write: writes go to both old and new location
4. Background migration of existing data to new shards
5. Verify data integrity with checksums
6. Switch reads to new locations
7. Stop dual-writes
8. Remove old shard assignments after grace period

**Rollback plan:**
- Keep old shards read-only during migration
- If issues, revert routing to old shards
- Dual-writes ensure old shards have latest data

</details>
