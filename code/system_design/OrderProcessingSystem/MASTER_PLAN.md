# Project Plan: Order Processing System

This doc outlines the plan to design and build the Order Processing System.

### Part 1: Design & Analysis
1.  **Review Existing Docs**: Go through current `.md` files. Check if design matches reqs. Find gaps.
2.  **High-Level Arch**: Create a simple HLD for mgmt review.
    *   Arch diagram (components, flows).
    *   Tech stack (Node.js, Postgres, SQS) with reasons.
    *   Patterns for reliability & idempotency.

### Part 2: PoC Implementation (in `OrderProcessingSystemRepo/`)
1.  **Setup**: Init Node.js/TS project with `docker-compose`.
    *   Services: `order-service`, `delivery-service`.
    *   Infra: Postgres, SQS (ElasticMQ), Redis.
2.  **`order-service`**:
    *   JWT/OAuth2 auth with Passport (`POST /auth/token`).
    *   `POST /orders` endpoint (JWT-protected, validation, Redis idempotency).
    *   Save orders to PG with transactions.
    *   Send `order-created` to SQS with retry (`axios-retry`).
    *   Mock product availability check.
    *   Health check endpoint (`/health`).
    *   Structured logging (Winston).
3.  **`delivery-service`**:
    *   SQS consumer for `order-created` with circuit breaker (`opossum`).
    *   Simulate delivery.
    *   Send `order-shipped`, `order-delivered` events with deduplication.
    *   Health check endpoint (`/health`).
    *   Structured logging (Winston).
4.  **Order Status Sync**:
    *   `order-service` consumes delivery events to update PG.
5.  **Non-Functional Features**:
    *   Docker Compose with service replicas for scalability testing.
    *   Redis-based idempotency with request fingerprinting (internal).
    *   Basic observability (logs, health checks, correlation IDs).
6.  **Testing**: Add unit tests for key flows + non-functional features.

### Part 3: Docs
1.  **PoC README**: How to setup & run.
2.  **Final Review**: Check work against goals. 