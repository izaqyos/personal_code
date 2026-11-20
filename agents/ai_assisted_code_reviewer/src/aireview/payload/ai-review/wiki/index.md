# Review Wiki — Index

The team's review knowledge, written for both humans and agents. Each page holds a
few rules; each rule has an ID, a severity, a *Why*, and Bad/Good examples.

**Agents:** match each changed file against the routing table and read only the
routed pages. `*` rows apply to every review.

**Humans:** when the reviewer is wrong, fix the rule here (and add a Good example);
when an incident happens, add a `PIT-*` rule. Run `aireview wiki-lint` after edits.

## Routing

| Paths | Pages | Notes |
|---|---|---|
| `*` | `security/secrets-and-pii.md`, `testing/testing.md`, `process/pull-requests.md` | always |
| `src/routes/**`, `src/api/**`, `src/app.ts`, `src/middleware/**` | `security/authz.md`, `security/injection.md`, `conventions/express-api.md`, `pitfalls/incidents.md` | HTTP surface |
| `src/db/**`, `src/repositories/**`, `**/*.sql` | `security/injection.md`, `data/migrations.md` | data access |
| `migrations/**`, `**/migrations/**` | `data/migrations.md` | schema changes |
| `**/*.ts`, `**/*.tsx` | `conventions/typescript.md`, `pitfalls/incidents.md` | all TypeScript |

## Rule ID prefixes

| Prefix | Area | Page |
|---|---|---|
| `SEC` | Security | `security/*.md` |
| `API` | HTTP API conventions | `conventions/express-api.md` |
| `CONV` | TypeScript conventions | `conventions/typescript.md` |
| `TEST` | Testing | `testing/testing.md` |
| `MIG` | Migrations / data | `data/migrations.md` |
| `PR` | Pull request hygiene | `process/pull-requests.md` |
| `PIT` | Incident-derived pitfalls | `pitfalls/incidents.md` |
