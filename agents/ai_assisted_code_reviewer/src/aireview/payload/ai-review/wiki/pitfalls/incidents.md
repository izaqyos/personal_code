# Incident-derived pitfalls

Each rule here exists because it caused a production incident. Link the postmortem.

### PIT-001: Cap pagination limits (INC-2025-117)
**Severity:** major
**Why:** A client sent `?limit=1000000`; the endpoint loaded 1M invoices into memory and took down the API pods. Every `limit` from the request must be capped (max 100) server-side.

**Bad:**
```ts
const limit = Number(req.query.limit ?? 20);
```

**Good:**
```ts
const limit = Math.min(Number(req.query.limit ?? 20), 100);
```

### PIT-002: Don't `await` inside `forEach` (INC-2026-031)
**Severity:** major
**Why:** `array.forEach(async ...)` doesn't wait; the handler returned before emails were sent and errors became unhandled rejections that crashed the worker. Use `for...of` or `Promise.all`.

**Bad:**
```ts
invoices.forEach(async (inv) => { await sendReminder(inv); });
```

**Good:**
```ts
await Promise.all(invoices.map((inv) => sendReminder(inv)));
```
