# 🎯 **System Design Review Questions & Answers**

## **📋 QUICK REFERENCE Q&A**

### **🏗️ HIGH-LEVEL ARCHITECTURE**

**Q: Describe your system architecture in 30 seconds.**
**A:** 2-service microservices: Order Service (API + auth) + Delivery Service (logistics worker). Async communication via SQS FIFO queues. PostgreSQL for ACID compliance, Redis for idempotency. Docker orchestration with health checks.

**Q: Why 2 services instead of monolith or many microservices?**
**A:** KISS principle - clear domain separation without operational overhead. Reduces complexity while maintaining scalability. Avoids distributed transaction complexity of 4+ services.

**Q: Walk me through order creation to delivery.**
**A:** Client → JWT auth → POST order → DB save → SQS publish → Delivery service polls → Process shipment → Status update via SQS → Order service updates DB → Customer notification.

---

### **💾 DATA & PERSISTENCE**

**Q: Why PostgreSQL over NoSQL?**
**A:** Order processing needs ACID transactions for financial consistency. Complex relationships (orders→items→shipments). Strong consistency over eventual consistency for money operations.

**Q: How do you handle data consistency across services?**
**A:** Within service: ACID transactions. Between services: Eventually consistent via message queues. Acceptable for order status updates (seconds delay OK).

**Q: Explain your database schema design.**
**A:** 4 tables: `orders` (main), `order_items` (1:N), `shipments` (1:1), `delivery_events` (audit trail). Proper indexes on customer_id, status, timestamps.

---

### **📡 MESSAGING & COMMUNICATION**

**Q: Why SQS over Kafka/RabbitMQ?**
**A:** Cost-optimized for scale. SQS FIFO gives ordering + exactly-once processing with zero ops overhead. Kafka overkill for this throughput. RabbitMQ needs infrastructure management.

**Q: How do you ensure message ordering?**
**A:** SQS FIFO queues with **time-partitioned MessageGroupId** using 30-second windows. Orders within each 30-second window are processed in strict FIFO order, with parallel processing between windows. This provides excellent fairness (max 30-second unfairness) while achieving ~600 TPS throughput.

**Q: What happens if message processing fails?**
**A:** Multi-layer protection: 30-second processing timeout → max 3 automatic retries → message deleted to prevent partition blocking → logged to simulated DLQ for manual investigation. This prevents stuck orders from blocking entire FIFO partitions.

**Q: What's the throughput of your hybrid FIFO approach?**
**A:** ~600 orders/second with 30-second time windows. This balances fairness (max 30-second unfairness) with reasonable throughput. Window size can be tuned: larger windows = better fairness but lower throughput, smaller windows = higher throughput but less fairness.

**Q: How do you prevent stuck orders from blocking the FIFO queue?**
**A:** Multiple protections: 1) 30-second partitions limit blast radius (only ~30 orders affected), 2) 30-second processing timeout prevents hanging, 3) Max 3 retries then message deletion to unblock partition, 4) Failed messages logged for manual recovery. A stuck order can't block more than its own 30-second partition.

---

### **🛡️ RELIABILITY & RESILIENCE**

**Q: How do you handle failures?**
**A:** Multi-layer: Circuit breakers (opossum), retry logic (axios-retry), graceful degradation (Redis down = orders still work), health checks, structured logging.

**Q: Explain your idempotency strategy.**
**A:** Redis cache with request fingerprint (customer_id + items + timestamp). 24h TTL. Prevents duplicate orders from double-clicks. SQS FIFO provides additional deduplication.

**Q: What's your disaster recovery plan?**
**A:** Database backups, stateless services (quick restart), message durability in SQS, infrastructure as code for rapid rebuild.

---

### **🔐 SECURITY**

**Q: Describe your authentication approach.**
**A:** JWT tokens with 24h expiry, OAuth2 client credentials flow, Passport.js middleware. Simplified for PoC - production would add refresh tokens.

**Q: How do you prevent common security vulnerabilities?**
**A:** Input validation, Helmet.js security headers, JWT validation, database constraints, structured logging for audit.

**Q: What about rate limiting and DDoS protection?**
**A:** Currently basic. Production: API Gateway with rate limiting, WAF, circuit breakers prevent resource exhaustion.

---

### **📈 PERFORMANCE & SCALABILITY**

**Q: How does your system scale?**
**A:** Horizontal scaling: Stateless services behind load balancers. Database: read replicas + connection pooling. SQS auto-scales. Auto Scaling Groups based on CPU + queue depth.

**Q: What are the performance bottlenecks?**
**A:** Database write capacity (~1000 orders/sec), connection pool limits, SQS polling frequency. Solutions: sharding, read replicas, optimized queries.

**Q: How do you handle traffic spikes?**
**A:** Auto-scaling triggers, queue buffering absorbs spikes, circuit breakers prevent cascade failures, caching reduces DB load.

---

### **📊 MONITORING & OBSERVABILITY**

**Q: How do you monitor system health?**
**A:** Health check endpoints (service + dependencies), structured logging with correlation IDs, metrics collection. Production: ELK stack + Prometheus/Grafana.

**Q: What's the current status of real-time notifications?**
**A:** Designed but not implemented. Currently customers poll `GET /orders/:id` for status updates. WebSocket/SSE implementation is planned - need to add status update consumer and notification service.

**Q: How do you debug issues across services?**
**A:** Correlation IDs trace requests across services, structured JSON logs, audit trail in delivery_events table, comprehensive error handling.

**Q: What key metrics do you track?**
**A:** Request latency, error rates, queue depths, database connection usage, order processing times, health check status.

---

### **⚖️ TRADE-OFFS & DECISIONS**

**Q: What are your main architectural trade-offs?**
**A:** 
- **Simplicity vs Features**: 2 services vs microservice mesh
- **Consistency vs Performance**: ACID transactions vs eventual consistency  
- **Cost vs Redundancy**: Single region vs multi-region HA
- **Speed vs Completeness**: Simplified auth vs full OAuth2 server

**Q: Why TypeScript/Node.js over Java/Python?**
**A:** I/O-optimized for APIs, async nature perfect for message processing, strong typing, rich ecosystem, faster development cycle.

**Q: How would you change this for 10x scale?**
**A:** Read replicas, database sharding, Redis clustering, multiple regions, event sourcing, CQRS for complex queries, microservice mesh.

---

### **🎯 BUSINESS LOGIC**

**Q: Why simplify status model to 3 states?**
**A:** PoC focus on core flow. `PENDING_SHIPMENT → SHIPPED → DELIVERED` proves concept without complexity. Production adds detailed tracking states.

**Q: How do you handle order modifications/cancellations?**
**A:** Current: Not implemented (PoC scope). Production: Event sourcing pattern, compensation transactions, status-based rules.

**Q: What about inventory management?**
**A:** Current: Mock availability check. Production: Separate inventory service, reservation system, eventual consistency with compensation.

---

## **🚀 RAPID-FIRE TECHNICAL QUESTIONS**

**Q: Message queue vs direct HTTP calls?**
**A:** Async decoupling, better fault tolerance, natural backpressure, ordering guarantees.

**Q: Database per service vs shared database?**
**A:** Database per service - true service independence, separate scaling, technology choice freedom.

**Q: Synchronous vs asynchronous processing?**
**A:** Async for non-critical operations (delivery updates), sync for immediate feedback (order creation response).

**Q: How do you version your APIs?**
**A:** URL versioning (`/v1/orders`), backward compatibility, gradual migration strategies.

**Q: Container orchestration choice?**
**A:** Docker Compose for dev, Kubernetes for production (auto-scaling, service discovery, rolling deployments).

---

## **📝 KEY TALKING POINTS**

### **Strengths to Emphasize:**
- ✅ **Pragmatic technology choices** based on scale and cost
- ✅ **Production-ready patterns** even in PoC
- ✅ **Clear trade-off reasoning** for every decision
- ✅ **Horizontal scalability** from day one
- ✅ **Operational simplicity** while maintaining reliability

### **Areas for Enhancement:**
- 🔄 **Missing: Real-time notifications** (WebSocket/SSE)
- 🔄 **Missing: Status update consumer** (Order Service)
- 🔄 **Bug: Queue naming mismatch** (delivery-status-queue.fifo)
- 🔄 Event sourcing for better audit trail
- 🔄 Integration testing framework
- 🔄 Infrastructure as Code (Terraform)
- 🔄 Full OAuth2 implementation
- 🔄 Comprehensive monitoring stack

**💡 Pro Tip:** Always relate technical decisions back to business value and cost considerations!

---

## **🔧 IMPLEMENTATION DETAILS**

### **Technology Stack Justification**
- **Node.js + TypeScript**: I/O optimized, strong typing, mature ecosystem
- **PostgreSQL**: ACID compliance for financial data
- **Redis**: High-performance caching and idempotency
- **SQS FIFO**: Managed queuing with ordering guarantees
- **Docker**: Consistent environments and easy deployment

### **Non-Functional Requirements Coverage**
- **Reliability**: Circuit breakers, retries, health checks
- **Scalability**: Horizontal scaling, stateless design
- **Security**: JWT auth, input validation, secure headers
- **Observability**: Structured logging, correlation IDs, metrics
- **Performance**: Connection pooling, caching, indexes

### **Production Readiness Checklist**
- ✅ Health check endpoints
- ✅ Structured logging with correlation IDs
- ✅ Error handling and graceful degradation
- ✅ Database transactions and constraints
- ✅ Message queue durability
- ✅ Security middleware and validation
- ✅ Docker containerization
- ✅ Environment configuration
- ❌ **Missing: Status update consumer for order synchronization**
- ❌ **Missing: Real-time notifications (WebSocket/SSE)**
- ⚠️ Missing: Comprehensive monitoring, distributed tracing, infrastructure as code

---

*Created: $(date)*
*Project: Order Processing System PoC*
*Status: Ready for technical review*