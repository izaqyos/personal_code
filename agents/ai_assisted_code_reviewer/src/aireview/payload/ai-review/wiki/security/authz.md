# Authentication & Authorization

Every request is either public (explicitly listed) or authenticated via `requireAuth`.
Authenticated is not authorized: a user may only touch resources in their own tenant.

### SEC-002: Scope every resource lookup to the caller's tenant
**Severity:** blocker
**Why:** Loading a record by a client-supplied id without checking ownership lets any logged-in user read or modify other tenants' data (IDOR). This is our #1 pentest finding.
**Applies to:** route handlers and services that fetch/update/delete by id.

**Bad:**
```ts
router.get("/invoices/:id", async (req, res) => {
  const invoice = await db.invoices.findById(req.params.id);
  res.json(invoice);
});
```

**Good:**
```ts
router.get("/invoices/:id", async (req, res, next) => {
  const invoice = await db.invoices.findOne({ id: req.params.id, tenantId: req.user.tenantId });
  if (!invoice) return next(new HttpError(404, "not found")); // 404, not 403: don't leak existence
  res.json(invoice);
});
```

### SEC-007: New routers must be mounted behind `requireAuth`
**Severity:** blocker
**Why:** `app.use("/x", router)` without `requireAuth` exposes every handler in the router publicly. Public endpoints must be listed in `src/routes/public.ts` and reviewed by security.

**Bad:**
```ts
app.use("/invoices", invoicesRouter);
```

**Good:**
```ts
app.use("/invoices", requireAuth, invoicesRouter);
```

### SEC-008: Role checks use `requireRole`, never client-supplied flags
**Severity:** blocker
**Why:** Fields like `req.body.isAdmin` or `req.query.role` are attacker-controlled. Roles come only from the verified session (`req.user.roles`).

**Bad:**
```ts
if (req.body.isAdmin) await deleteTenant(req.params.id);
```

**Good:**
```ts
router.delete("/tenants/:id", requireRole("admin"), deleteTenantHandler);
```
