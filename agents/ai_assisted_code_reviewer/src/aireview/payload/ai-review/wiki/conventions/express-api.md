# HTTP API conventions (Express)

### API-001: Validate request input with a zod schema
**Severity:** major
**Why:** Unvalidated `req.query`/`req.body`/`req.params` flow into queries and business logic as `any`. Every handler parses input with `validate(schema)` middleware or `schema.parse()` at the top.

**Bad:**
```ts
const limit = req.query.limit;
```

**Good:**
```ts
const Query = z.object({ limit: z.coerce.number().int().min(1).max(100).default(20) });
const { limit } = Query.parse(req.query);
```

### API-002: Errors go through `next(err)` with `HttpError`
**Severity:** major
**Why:** The central error handler sets status, error shape `{error: {code, message}}`, logging and tracing. Ad-hoc `res.status(500).send(e.message)` leaks internals and breaks clients.

**Bad:**
```ts
} catch (e) { res.status(500).send(e.message); }
```

**Good:**
```ts
} catch (e) { next(e); }
```

### API-003: No breaking changes to existing responses
**Severity:** blocker
**Why:** Mobile clients pin old versions for months. Removing/renaming fields or changing types in an existing endpoint breaks them. Add fields; for breaking changes create `/v2`.

**Bad:**
```ts
res.json({ total: invoice.totalCents / 100 }); // was `totalCents` (number of cents)
```

**Good:**
```ts
res.json({ totalCents: invoice.totalCents, total: invoice.totalCents / 100 });
```
