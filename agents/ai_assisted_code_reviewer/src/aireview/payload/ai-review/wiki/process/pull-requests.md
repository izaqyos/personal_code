# Pull requests

PR hygiene rules. `PR-001`…`PR-005` are enforced by deterministic checks
(`.ai-review/pr-rules.json`); the agent should judge *quality*, e.g. whether the
summary actually matches the diff.

### PR-001: Required description sections are filled in
**Severity:** minor
**Why:** Reviewers and future readers need the what/why, how it was tested, and the risk. Placeholders like "TODO" don't count.

**Bad:**
```md
## Summary
TODO
```

**Good:**
```md
## Summary
Adds GET /invoices/:id so the billing page can show a single invoice (PAY-512).
```

### PR-002: Checklist items are ticked or explained
**Severity:** minor
**Why:** The checklist captures commitments (tests, no secrets). Unticked boxes must be ticked or explained.

**Bad:**
```md
- [ ] I added or updated tests
```

**Good:**
```md
- [x] I added or updated tests
```

### PR-003: Migration PRs include a real rollback plan
**Severity:** major
**Why:** If a migration goes wrong at 3am, on-call needs the exact rollback steps and where the backup is.

**Bad:**
```md
## Risk & Rollback
low risk
```

**Good:**
```md
## Risk & Rollback
Drops users.legacy_email (unused since PAY-410). Backup: s3://backups/... Rollback: run 002 down, restore column from backup with scripts/restore_legacy_email.sql.
```

### PR-004: Reference a ticket
**Severity:** nit
**Why:** Traceability from code to decision.

**Bad:**
```md
Fixes the invoice thing.
```

**Good:**
```md
Ticket: PAY-512
```

### PR-005: Keep PRs reviewable
**Severity:** minor
**Why:** Review quality drops sharply past a few hundred lines. Split refactors from behavior changes.

**Bad:**
```text
+2,300 / -900 across 41 files: refactor + new feature + dependency bump
```

**Good:**
```text
PR 1: refactor (no behavior change). PR 2: feature (+220/-30).
```

### PR-006: The description matches the diff
**Severity:** minor
**Why:** A summary that omits a migration, a new endpoint, or a security-relevant change misleads reviewers. (Judged by the agent, not a tool.)

**Bad:**
```md
## Summary
Small refactor of invoices.   ← diff also drops a column and adds a public endpoint
```

**Good:**
```md
## Summary
Adds GET /invoices/:id and drops users.legacy_email (see rollback below).
```
