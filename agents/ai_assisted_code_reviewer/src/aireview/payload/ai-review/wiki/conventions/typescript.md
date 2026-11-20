# TypeScript conventions

Formatting and basic lint (eslint, prettier) run in CI — don't report what they catch.
These are the rules lint can't express.

### CONV-001: No `any` in exported or handler signatures
**Severity:** minor
**Why:** `any` at a boundary silently disables type checking for every caller. Use a real type, `unknown` + narrowing, or a zod-inferred type.

**Bad:**
```ts
export function toDto(row: any): any { ... }
```

**Good:**
```ts
export function toDto(row: InvoiceRow): InvoiceDto { ... }
```

### CONV-002: Never swallow errors
**Severity:** major
**Why:** An empty `catch`, or a `catch` that returns success, hides failures from users, alerts and on-call. Either handle the specific error meaningfully or rethrow / `next(err)`.

**Bad:**
```ts
try { await charge(invoice); } catch (e) {}
try { ... } catch { return res.json({ ok: true }); }
```

**Good:**
```ts
try { await charge(invoice); }
catch (e) { if (e instanceof CardDeclined) return next(new HttpError(402, "card declined")); throw e; }
```

### CONV-003: Use `logger`, not `console`
**Severity:** minor
**Why:** `console.*` bypasses structured logging (no request id, level, or redaction).

**Bad:**
```ts
console.log("loaded invoices", count);
```

**Good:**
```ts
logger.debug("loaded invoices", { count });
```
