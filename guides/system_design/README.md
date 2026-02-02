# System Design Knowledge Base

A comprehensive guide to system design concepts for interview preparation and real-world architecture.

## Contents

### [01. Fundamentals](01_fundamentals/)
Core concepts every system designer must understand.

- [Scalability](01_fundamentals/scalability.md) - Horizontal vs vertical, scaling strategies
- [Availability & Reliability](01_fundamentals/availability_reliability.md) - SLAs, SLOs, fault tolerance
- [CAP Theorem](01_fundamentals/cap_theorem.md) - Consistency, Availability, Partition tolerance
- [PACELC Theorem](01_fundamentals/pacelc.md) - Extension of CAP for latency tradeoffs
- [Latency & Throughput](01_fundamentals/latency_throughput.md) - Performance fundamentals

### [02. Building Blocks](02_building_blocks/)
Core components used in distributed systems.

- [Load Balancers](02_building_blocks/load_balancers.md) - L4/L7, algorithms, health checks
- [Caching](02_building_blocks/caching.md) - Strategies, invalidation, CDN
- [Databases](02_building_blocks/databases.md) - SQL vs NoSQL, replication, sharding
- [Message Queues](02_building_blocks/message_queues.md) - Pub/sub, exactly-once, Kafka vs RabbitMQ
- [CDN](02_building_blocks/cdn.md) - Content delivery, edge caching
- [Consistent Hashing](02_building_blocks/consistent_hashing.md) - Distributed data placement
- [API Gateway](02_building_blocks/api_gateway.md) - Routing, authentication, rate limiting
- [Proxies](02_building_blocks/proxies.md) - Forward vs reverse, use cases

### [03. Design Patterns](03_design_patterns/)
Architectural patterns for distributed systems.

- [Microservices](03_design_patterns/microservices.md) - Service decomposition, boundaries
- [Event-Driven Architecture](03_design_patterns/event_driven.md) - Event sourcing, CQRS
- [Saga Pattern](03_design_patterns/saga_pattern.md) - Distributed transactions
- [Circuit Breaker](03_design_patterns/circuit_breaker.md) - Fault tolerance
- [Rate Limiting](03_design_patterns/rate_limiting.md) - Token bucket, sliding window

### [04. Case Studies](04_case_studies/)
Complete system design walkthroughs.

- [URL Shortener](04_case_studies/url_shortener.md) - TinyURL design
- [Rate Limiter](04_case_studies/rate_limiter.md) - API rate limiting service
- [Chat System](04_case_studies/chat_system.md) - WhatsApp/Slack style
- [Video Streaming](04_case_studies/video_streaming.md) - Netflix/YouTube architecture
- [E-Commerce](04_case_studies/ecommerce.md) - Amazon-style marketplace

## Learning Path

| Week | Focus | Topics |
|------|-------|--------|
| 1 | Fundamentals | Scalability, CAP, Latency |
| 2 | Building Blocks I | Load Balancers, Caching |
| 3 | Building Blocks II | Databases, Message Queues |
| 4 | Patterns | Microservices, Event-Driven |
| 5-6 | Case Studies | URL Shortener through E-Commerce |

## Interview Preparation

For system design interviews:
1. Clarify requirements (functional & non-functional)
2. Estimate scale (users, data, QPS)
3. Design high-level architecture
4. Deep dive into components
5. Discuss tradeoffs
6. Address bottlenecks

## Related Resources

- [Practice Exercises](../../code/practice/system_design/) - Hands-on design problems
- [Order Processing System](../../code/system_design/OrderProcessingSystem/) - Full implementation example

## References

- Udemy: System Design Interview Prep
- Udemy: Mastering System Design
- Designing Data-Intensive Applications (Kleppmann)
- System Design Interview (Alex Xu)
