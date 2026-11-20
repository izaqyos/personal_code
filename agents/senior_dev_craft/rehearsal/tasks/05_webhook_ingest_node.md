# Task 05: CI webhook ingest service (Node/TypeScript + Express, ~30 min)

## Interviewer prompt
"CI sends us a webhook on every build: `POST /webhooks/build` with `{runId, status, repo, failures[]}`.
Accept it, and process it asynchronously (store + notify). CI retries on any non-2xx."

## Hidden NFR hooks
- **Security (critical):** verify the HMAC signature header (`crypto.timingSafeEqual`); zod-validate the body; size limit on the JSON body; no secrets in logs.
- **Resilience (critical):** CI retries → **idempotency by `runId`** (a dedupe store); respond fast (202) and process async.
- **Scalability (basic):** a bounded in-process queue with backpressure (503 + `Retry-After` when full); horizontal scaling needs a real queue (name it).
- **Observability (basic):** structured logs with requestId/runId (AsyncLocalStorage); counters for accepted/duplicate/rejected.
- **Availability (basic):** graceful shutdown on SIGTERM (stop accepting, drain the queue with a deadline); health vs readiness.

## Expert moves
1. Frame: "CI retries on non-2xx, so duplicates are guaranteed, so idempotency is the first design decision".
2. Two designs: process inline (simple, slow responses, retries cause duplicates) vs accept + enqueue (202, fast, needs a dedupe store). Pick the queue.
3. Tests with supertest/`fetch` against `app.listen(0)`: bad signature → 401, invalid body → 400, the same runId twice → one processing, queue full → 503.
4. Use `~/work/git/personal_KB/typescript/typescript-node-playbook.md` (the handler pattern, `next(err)`, zod) and `~/work/git/personal_KB/system-design/scalability-in-code.md` (backpressure).
5. Critic: "is the signature checked on the *raw* body? (JSON re-serialization breaks HMAC)". That's a classic catch to show.

## Likely follow-ups
- "Multiple instances?": move dedupe to Redis `SET NX` with a TTL, and the queue to SQS/Kafka; consumers stay idempotent.
- "Notify Slack on repeated failures of the same test?": an event + consumer (extensibility seam), rate-limited notifications.
- "Replay a day of webhooks after an outage?": idempotency makes replay safe. Store raw payloads for 7 days.
