# Exercise: Health Check Design

## Objective
Design a robust health check system for a load balancer.

## Problem Statement
You're designing a health check system for a critical e-commerce platform with the following requirements:
- 50 backend servers
- 99.99% availability target
- Detection of: server crashes, network issues, application hangs, disk full, memory exhaustion

## Tasks

### Task 1: Health Check Strategy

Design a health check strategy:

1. What types of health checks would you implement?
   - Passive checks: ___
   - Active checks: ___

2. What endpoints would you check and why?

3. What metrics would indicate an unhealthy server?

### Task 2: Configuration Design

Define the configuration for your health checks:

```yaml
health_check:
  interval: ___       # How often to check
  timeout: ___        # Max time to wait for response
  healthy_threshold: ___    # Successes needed to mark healthy
  unhealthy_threshold: ___  # Failures needed to mark unhealthy
  
  checks:
    - type: ___
      path: ___
      expected_status: ___
    # Add more checks...
```

Justify each value you chose.

### Task 3: Edge Cases

How would you handle these scenarios?

1. **Flapping server**: Server alternates between healthy and unhealthy every few seconds

2. **Slow degradation**: Server response time gradually increases from 50ms to 5000ms

3. **Partial failure**: Server responds to /health but actual endpoints are failing

4. **Network partition**: Load balancer can't reach server, but server is actually healthy

### Task 4: Trade-off Analysis

Complete this table:

| Decision | Shorter Interval | Longer Interval |
|----------|-----------------|-----------------|
| Detection time | | |
| Network overhead | | |
| False positives | | |

---

<details>
<summary>Hints</summary>

- Consider both synthetic (active) and real-traffic (passive) health checks
- Think about what each check actually validates
- Health check intervals are typically 5-30 seconds
- Thresholds of 2-3 are common for both healthy and unhealthy

</details>

<details>
<summary>Solution</summary>

### Task 1: Health Check Strategy

**Passive checks:**
- Monitor real request success/failure rates
- Track response times
- Count 5xx errors

**Active checks:**
- HTTP GET to /health endpoint
- TCP connection test
- Custom endpoint that validates dependencies (DB, cache)

**Endpoints:**
- `/health` - Basic liveness
- `/health/ready` - Full readiness (includes dependency checks)
- `/metrics` - Detailed health metrics

**Unhealthy indicators:**
- 5xx error rate > 10%
- Response time > 2000ms
- Connection refused
- Timeout

### Task 2: Configuration

```yaml
health_check:
  interval: 10s        # Balance between detection and overhead
  timeout: 5s          # Give slow responses a chance
  healthy_threshold: 2    # Require 2 successes to trust recovery
  unhealthy_threshold: 3  # Tolerate brief issues
  
  checks:
    - type: http
      path: /health
      expected_status: 200
      
    - type: http
      path: /health/ready
      expected_status: 200
      
    - type: tcp
      port: 8080
```

### Task 3: Edge Cases

1. **Flapping**: Use exponential backoff before marking healthy again; require more consecutive successes (e.g., 5) after flapping detected

2. **Slow degradation**: Include response time in health criteria; gradually reduce traffic weight before marking unhealthy

3. **Partial failure**: Check actual endpoints periodically; use passive monitoring of real traffic success rate

4. **Network partition**: Use multiple check sources; don't remove from pool if other sources report healthy

### Task 4: Trade-off Analysis

| Decision | Shorter Interval | Longer Interval |
|----------|-----------------|-----------------|
| Detection time | Faster (good) | Slower (bad) |
| Network overhead | Higher (bad) | Lower (good) |
| False positives | Higher (bad) | Lower (good) |

</details>
