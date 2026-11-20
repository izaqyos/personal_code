# Migrations & data

We deploy with rolling restarts: old and new code run against the same schema for
minutes. Every migration must be compatible with the previous release.

### MIG-001: Destructive changes use expand/contract
**Severity:** blocker
**Why:** `DROP COLUMN`/`DROP TABLE`/`RENAME`, or adding `NOT NULL` without a default, breaks the still-running old release and loses data irreversibly. Ship in steps: stop reading → deploy → stop writing → deploy → drop, with a backup noted in the PR.

**Bad:**
```sql
ALTER TABLE users DROP COLUMN legacy_email;
```

**Good:**
```sql
-- release N: code no longer reads/writes legacy_email (shipped in PAY-410)
-- release N+1 (this migration), backup: s3://backups/users_legacy_email_2026-11-01
ALTER TABLE users DROP COLUMN legacy_email;
```

### MIG-002: Every migration has a down migration
**Severity:** major
**Why:** Rollback is our first incident response. A migration without `-- down` blocks rollback of the whole release.

**Bad:**
```sql
-- up
CREATE INDEX idx_invoices_status ON invoices(status);
```

**Good:**
```sql
-- up
CREATE INDEX CONCURRENTLY idx_invoices_status ON invoices(status);
-- down
DROP INDEX CONCURRENTLY idx_invoices_status;
```

### MIG-003: Large-table indexes are built concurrently
**Severity:** major
**Why:** Plain `CREATE INDEX` locks writes on the table for the whole build; on `invoices` (80M rows) that's an outage.

**Bad:**
```sql
CREATE INDEX idx_invoices_status ON invoices(status);
```

**Good:**
```sql
CREATE INDEX CONCURRENTLY idx_invoices_status ON invoices(status);
```
