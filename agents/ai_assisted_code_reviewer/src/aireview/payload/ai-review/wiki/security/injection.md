# Injection

### SEC-001: Parameterize every SQL query
**Severity:** blocker
**Why:** String-built SQL (concatenation or template literals) with any request-derived value is SQL injection. Our `db.query(sql, params)` helper parameterizes; `db.raw` with interpolation does not.

**Bad:**
```ts
const rows = await db.raw(`SELECT * FROM invoices WHERE status = '${req.query.status}'`);
```

**Good:**
```ts
const rows = await db.query("SELECT * FROM invoices WHERE status = $1 AND tenant_id = $2", [status, tenantId]);
```

### SEC-006: No shell execution with request-derived input
**Severity:** blocker
**Why:** `child_process.exec` runs through a shell; any user input becomes command injection. Use `execFile`/`spawn` with an argument array and an allow-list.

**Bad:**
```ts
exec(`convert ${req.query.file} out.png`);
```

**Good:**
```ts
if (!ALLOWED.has(file)) throw new HttpError(400, "bad file");
execFile("convert", [file, "out.png"]);
```

### SEC-009: Don't fetch arbitrary user-supplied URLs (SSRF)
**Severity:** major
**Why:** Server-side fetches of user URLs can reach internal services and cloud metadata (169.254.169.254). Use the `safeFetch` helper, which enforces an allow-list.

**Bad:**
```ts
const r = await fetch(req.body.webhookUrl);
```

**Good:**
```ts
const r = await safeFetch(req.body.webhookUrl, { allowHosts: config.webhookHosts });
```
