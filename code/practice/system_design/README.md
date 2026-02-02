# System Design Practice

Hands-on exercises for system design concepts. Each topic includes problems at three difficulty levels.

## Structure

Each topic directory contains:
- `beginner/` - Foundational exercises, component-level design
- `intermediate/` - Integration exercises, tradeoff analysis
- `advanced/` - Full system design, scale challenges

## Topics

### Building Block Exercises
| # | Topic | Focus |
|---|-------|-------|
| 01 | [Load Balancing](01_load_balancing/) | LB algorithms, health checks, session affinity |
| 02 | [Caching](02_caching/) | Cache strategies, invalidation, consistency |
| 03 | [Databases](03_databases/) | Sharding, replication, indexing |
| 04 | [Message Queues](04_message_queues/) | Pub/sub, exactly-once, ordering |
| 05 | [Rate Limiting](05_rate_limiting/) | Token bucket, sliding window, distributed |

### Full System Exercises
| # | Topic | Focus |
|---|-------|-------|
| 06 | [URL Shortener](06_url_shortener/) | Hash generation, redirection, analytics |
| 07 | [Chat System](07_chat_system/) | Real-time messaging, presence, history |
| 08 | [Notification System](08_notification_system/) | Push, email, SMS, delivery guarantees |
| 09 | [Video Streaming](09_video_streaming/) | Encoding, CDN, adaptive bitrate |
| 10 | [Distributed Storage](10_distributed_storage/) | Object store, replication, consistency |
| 11 | [Search System](11_search_system/) | Indexing, ranking, typeahead |
| 12 | [Payment System](12_payment_system/) | Transactions, idempotency, reconciliation |

## How to Use

1. Read the problem statement in each exercise file
2. Sketch your design (paper or diagramming tool)
3. Consider: requirements, scale, components, tradeoffs
4. Compare with solution hints (hidden by default)
5. Iterate and improve

## Progress Tracking

Use the [LEARNING_ROADMAP.md](LEARNING_ROADMAP.md) to track your progress through a suggested weekly schedule.

## Exercise Format

Each exercise file includes:
- **Problem Statement** - What to design
- **Requirements** - Functional and non-functional
- **Constraints** - Scale estimates
- **Questions to Answer** - Design prompts
- **Solution Hints** (collapsed) - Key insights

## Related Resources

- [System Design KB](../../../guides/system_design/) - Theory and concepts
- [Performance Practice](../performance/) - Capacity estimation
