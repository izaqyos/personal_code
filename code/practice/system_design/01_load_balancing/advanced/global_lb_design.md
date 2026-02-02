# Exercise: Global Load Balancing Design

## Objective
Design a global load balancing solution for a multi-region application.

## Problem Statement
You're designing the load balancing infrastructure for a global SaaS platform:

**Requirements:**
- 3 regions: US-East, EU-West, Asia-Pacific
- 10M daily active users globally
- 99.99% availability (52 minutes downtime/year max)
- Latency < 100ms for 95% of users
- Handle regional outages gracefully
- Support both stateless API and stateful WebSocket connections

## Tasks

### Task 1: Architecture Design

Draw a diagram showing:
1. Global DNS/Load Balancing layer
2. Regional load balancers
3. Application servers
4. How traffic flows for a user in London

Consider:
- What technology/service for global load balancing?
- How to route users to nearest region?
- How to handle region failover?

### Task 2: Routing Strategy

Design your routing policy:

1. **Geographic routing**: How do you determine which region serves a user?

2. **Latency-based routing**: How would you implement this as an alternative?

3. **Failover routing**: What triggers failover and where does traffic go?

Complete this decision table:

| User Location | Primary Region | Secondary Region | Failover Trigger |
|---------------|---------------|------------------|------------------|
| New York | | | |
| London | | | |
| Tokyo | | | |
| Sydney | | | |

### Task 3: Session Affinity at Global Scale

For WebSocket connections:

1. How do you ensure a user always connects to the same server?

2. What happens during a regional failover? How do you handle:
   - Active WebSocket connections
   - User state/session data

3. Design a solution for cross-region session management.

### Task 4: Capacity Planning

Given:
- US-East: 40% of traffic (4M users)
- EU-West: 35% of traffic (3.5M users)  
- Asia-Pacific: 25% of traffic (2.5M users)

1. How much spare capacity should each region have to absorb failover traffic?

2. If US-East goes down, can other regions handle the load? Show your calculations.

3. What auto-scaling policies would you implement?

### Task 5: Trade-offs

For each decision, explain the trade-off:

1. Anycast vs DNS-based global load balancing

2. Active-Active vs Active-Passive multi-region

3. Eventual consistency of sessions vs Strong consistency

---

<details>
<summary>Hints</summary>

- Consider AWS Route 53, Cloudflare, or similar for global LB
- For failover capacity, N+1 or N+2 models are common
- WebSocket failover requires client-side reconnection logic
- Anycast provides faster failover but less control

</details>

<details>
<summary>Solution</summary>

### Task 1: Architecture

```
                    ┌─────────────────────────────────┐
                    │    Global DNS (Route 53/CF)     │
                    │    - GeoDNS routing             │
                    │    - Health-based failover      │
                    └───────────────┬─────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        ▼                           ▼                           ▼
┌───────────────┐           ┌───────────────┐           ┌───────────────┐
│   US-East     │           │   EU-West     │           │  Asia-Pacific │
│ ┌───────────┐ │           │ ┌───────────┐ │           │ ┌───────────┐ │
│ │   L7 LB   │ │           │ │   L7 LB   │ │           │ │   L7 LB   │ │
│ └─────┬─────┘ │           │ └─────┬─────┘ │           │ └─────┬─────┘ │
│       │       │           │       │       │           │       │       │
│ ┌─────┴─────┐ │           │ ┌─────┴─────┐ │           │ ┌─────┴─────┐ │
│ │ App Pool  │ │           │ │ App Pool  │ │           │ │ App Pool  │ │
│ └───────────┘ │           │ └───────────┘ │           │ └───────────┘ │
└───────────────┘           └───────────────┘           └───────────────┘
```

London user flow:
1. DNS query → Route 53 returns EU-West IPs (geo-routing)
2. User connects to EU-West regional LB
3. LB routes to healthy app server

### Task 2: Routing Strategy

**Geographic routing:** Route 53 GeoDNS based on DNS resolver location

**Latency-based:** Measure RTT from each region's resolver, return lowest

**Routing table:**

| User Location | Primary Region | Secondary Region | Failover Trigger |
|---------------|---------------|------------------|------------------|
| New York | US-East | EU-West | Health check fail |
| London | EU-West | US-East | Health check fail |
| Tokyo | Asia-Pacific | US-East | Health check fail |
| Sydney | Asia-Pacific | US-East | Health check fail |

### Task 3: Session Affinity

1. **Server affinity:** Cookie with server ID + consistent hashing fallback
2. **Regional failover:**
   - WebSockets: Client detects disconnect, reconnects (new region via DNS)
   - Session data: Stored in cross-region Redis cluster
3. **Cross-region sessions:** 
   - DynamoDB Global Tables or Redis Enterprise Active-Active
   - Session ID → any region can validate

### Task 4: Capacity Planning

Current: US=40%, EU=35%, APAC=25%

**Failover capacity needed:**
- If US fails, EU+APAC must handle 100%
- EU needs: 35% + (40% × 0.6) = 59% capacity
- APAC needs: 25% + (40% × 0.4) = 41% capacity

Each region should run at ~60% to handle failover.

**Auto-scaling policies:**
- Scale out at 70% CPU
- Scale in at 30% CPU
- Minimum instances = normal traffic / 0.6

### Task 5: Trade-offs

1. **Anycast vs DNS:**
   - Anycast: Faster failover (no TTL), but less control, may cause mid-session routing changes
   - DNS: More control, but TTL delays failover, client-side caching issues

2. **Active-Active vs Active-Passive:**
   - Active-Active: Better latency, capacity utilization, but complex data sync
   - Active-Passive: Simpler, but wasted capacity, longer failover

3. **Eventual vs Strong consistency:**
   - Eventual: Better availability, lower latency, but stale reads possible
   - Strong: Consistent, but higher latency, may be unavailable during partitions

</details>
