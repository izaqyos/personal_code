# System Design: Order Processing PoC

### 1. Overview
This document outlines the final architecture for the Order Processing Proof of Concept (PoC). The design prioritizes simplicity, reliability, and scalability by using a focused microservice architecture and managed cloud services.
I wanted to build a lean, relatively low cost for services and hardware and low operational and development costs. So in general I favour to reuse proven libraries and services rather than reinvent the wheel. Also I choose the most optimal tool for the task. For example: after research I chose AWS SQS over solace/kafka/rabbitMQ b/c it solves the problem for this targeted scale and the lowest operational cost.

### 2. Core Components
The system is composed of two primary microservices:
*   **Order Service**: Manages the order lifecycle, authentication, and customer notifications. It exposes a REST API for order creation (with JWT/OAuth2 auth), validates incoming data, persists order state, communicates with the Delivery Service via message queues, and provides status updates to customers via polling (*real-time notifications planned but not implemented*).
*   **Delivery Service**: Handles the logistics workflow. It listens for new order events, simulates the shipment process, and publishes delivery status updates back to the Order Service.

same KISS principal here. I didn't want to overdo w/ too many microservices. a reasonable # of microservices helps reduce dev costs and operational costs by keeping clear and consistent boundaries and full separation of concerns

### 3. Architecture & Data Flow

The data flows asynchronously between the services using AWS SQS, which ensures reliable, decoupled communication.

**Flow:**
1.  A client authenticates via `POST /auth/token` (OAuth2 client credentials) and gets a JWT.
2.  Client sends a `POST /orders` request with `Authorization: Bearer <jwt>` to the **Order Service**.
3.  The service validates JWT, validates the request, and saves the new order to its PostgreSQL database with a `PENDING_SHIPMENT` status.
4.  The **Order Service** sends an `order-created` message to the `orders-queue` in SQS.
5.  The **Delivery Service** continuously polls the `orders-queue`, receives the message, and begins processing the shipment.
6.  When the delivery status changes (e.g., "shipped"), the **Delivery Service** sends an `order-shipped` message to the `delivery-status-queue`.
7.  **[NOT YET IMPLEMENTED]** The **Order Service** should poll the `delivery-status-queue` for messages and update order status. Currently, status updates require manual API calls.
8.  **Customer Notifications**: When order status changes, customers can poll `GET /orders/:id` for updates. *Real-time notifications via WebSocket/SSE are designed but not yet implemented.*

### 4. Architecture Diagram

```mermaid
graph TB
    %% Client Layer
    C[Customer App]
    
    %% API Layer
    subgraph "Order Service (Auto-scaled)"
        AUTH[Auth Endpoint<br/>POST /auth/token]
        API[Order API<br/>POST /orders<br/>GET /orders/:id]
        NOTIFY[Customer Notifications<br/>Polling API<br/>*WebSocket/SSE planned*]
    end
    
    %% Data Layer
    subgraph "Data & Cache"
        ODB[(Order DB<br/>PostgreSQL)]
        Redis[(Redis<br/>Idempotency)]
    end
    
    %% Message Layer
    subgraph "Message Queues (FIFO)"
        OrderQ[orders-queue.fifo]
        StatusQ[delivery-status-queue.fifo]
    end
    
    %% Delivery Layer
    subgraph "Delivery Service (Auto-scaled)"
        WORKER[Delivery Worker<br/>SQS Consumer]
        DDB[(Delivery DB<br/>PostgreSQL)]
    end
    
    %% Observability (separate)
    subgraph "Observability"
        LOGS[Structured Logs]
        METRICS[Metrics & Health]
    end
    
    %% Main Flow
    C -->|1. Get JWT| AUTH
    C -->|2. Create Order| API
    API -->|Check duplicates| Redis
    API -->|3. Store order| ODB
    API -->|4. Send order event| OrderQ
    
    %% Delivery Processing
    WORKER -->|5. Poll orders| OrderQ
    WORKER -->|6. Process shipment| DDB
    WORKER -->|7. Send status update| StatusQ
    
    %% Status Updates Back to Customer (NOT YET IMPLEMENTED)
    API -.->|8. Poll status changes| StatusQ
    API -.->|9. Update order status| ODB
    NOTIFY -.->|10. Real-time updates| C
    API -.->|Trigger notifications| NOTIFY
    
    %% Observability connections (dotted)
    API -.-> LOGS
    WORKER -.-> LOGS
    API -.-> METRICS
    WORKER -.-> METRICS
```

### 5. Architecture Summary

This design implements a focused 2-service microservices architecture that meets all functional and non-functional requirements:

#### 🔐 **Authentication Flow:**
1. Customer gets JWT token from auth endpoint
2. Uses JWT for all subsequent API calls

#### 📦 **Order Processing:**
3. Order API validates and stores orders
4. Checks Redis for duplicate requests (idempotency)
5. Publishes order events to SQS FIFO queue

#### 🚚 **Delivery Processing:**
6. Delivery worker polls orders queue
7. Processes shipments and updates delivery DB
8. Publishes status updates back to queue

#### 📱 **Customer Notifications:**
9. **[PLANNED]** Order service polls status updates  
10. **[PLANNED]** Sends real-time notifications to customers via WebSocket/SSE
11. **[CURRENT]** Customers poll `GET /orders/:id` for status updates

#### 📊 **Observability:**
- Winston structured logs for monitoring
- Health check endpoints for all services

#### **Key Features:**
- **FIFO Queues**: Ensures message ordering
- **Auto-scaling**: Both services can scale horizontally
- **Idempotency**: Redis prevents duplicate processing
- **Real-time Updates**: Planned for WebSocket/SSE (*currently polling-based*)

### 6. Technology Choices & Rationale
*   **Services (Node.js/TypeScript)**: Chosen for its efficiency in I/O-heavy applications and strong typing with TypeScript, which enhances developer productivity and code quality.
*   **Authentication (JWT/OAuth2 + Passport)**: Industry-standard auth with client credentials flow. Passport.js provides clean middleware integration with Express. **PoC Simplification**: Using basic JWT tokens (24h expiry) without refresh token complexity to focus on core order flow rather than auth edge cases.
*   **Customer Notifications**: Currently via REST API polling (`GET /orders/:id`). Real-time updates via WebSocket/Server-Sent Events are planned for future implementation.
*   **Messaging (AWS SQS FIFO)**: A fully managed service with FIFO (First-In-First-Out) ordering guarantees. Essential for order processing to ensure delivery events are processed in correct sequence. Provides both ordering and exactly-once processing.
*   **Database (PostgreSQL)**: A robust, open-source relational database that provides data integrity and is well-suited for structured order data.
*   **Local PoC Stack (Docker Compose)**: We will use Docker to orchestrate our services locally. For SQS, we'll use `softwaremill/elasticmq-native`, a lightweight, in-memory SQS-compatible mock.

#### 6.1 PoC Design Decisions

**Simplified Authentication Approach:**
- **Decision**: Use basic JWT tokens with 24-hour expiry, no refresh tokens
- **Rationale**: 
  - Focus PoC effort on core order processing flow, not auth complexity
  - Reduce development and operational costs during proof-of-concept phase
  - Avoid unnecessary token rotation logic, refresh storage, and related infrastructure
  - Aligns with lean approach: "choose the most optimal tool for the task"
- **Production Path**: Refresh tokens and proper OAuth2 flows can be added when scaling beyond PoC

**Simplified Status Model:**
- **Decision**: Use 3 order statuses (`PENDING_SHIPMENT`, `SHIPPED`, `DELIVERED`) and 3 delivery statuses (`PROCESSING`, `SHIPPED`, `DELIVERED`)
- **Rationale**:
  - Proves core order flow without status complexity overhead
  - Reduces development time and testing surface area
  - Follows KISS principle while demonstrating key functionality
  - Easier to debug and trace issues during PoC phase
- **Production Path**: Full 8-status order model with detailed delivery tracking can be added later

### 7. Non-Functional Requirements

#### 7.1 Reliability & Eventual Consistency
*   **SQS FIFO Guarantees**: Message ordering, exactly-once processing, dead letter queues, automatic retries
*   **Database Transactions**: ACID properties ensure data consistency within each service
*   **Retry Mechanisms**: Using `axios-retry` for HTTP calls between services
*   **Circuit Breakers**: `opossum` library for service-to-service communication protection

#### 7.2 Scalability
*   **Production**: AWS Auto Scaling Groups based on CPU/memory metrics and SQS queue depth
*   **PoC**: Docker Compose `replicas` to simulate horizontal scaling
*   **Stateless Services**: All services designed to be horizontally scalable
*   **Database Connection Pooling**: PgBouncer for efficient DB connection management

#### 7.3 Idempotency
*   **Redis Cache**: Store request fingerprints with TTL (e.g., `order:create:{hash}:24h`) - generates hash from customer_id + items + timestamp to prevent duplicate orders if customers click submit multiple times
*   **Request Fingerprinting**: Hash of customer_id + items + timestamp for duplicate detection
*   **SQS FIFO Deduplication**: Built-in message deduplication with MessageGroupId and MessageDeduplicationId
*   **Database Constraints**: Unique constraints prevent duplicate records

#### 7.4 Observability
*   **Structured Logging**: Winston with JSON format, correlation IDs for request tracing
*   **Production Monitoring**: 
    - Logs → ELK Stack (Elasticsearch, Logstash, Kibana)
    - Metrics → Prometheus + Grafana
    - Distributed Tracing → Jaeger
*   **PoC Monitoring**: Docker logs + basic health check endpoints
*   **Key Metrics**: Request latency, error rates, queue depths, database performance 