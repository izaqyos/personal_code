# Circuit Breaker Pattern

A fault tolerance pattern that prevents cascading failures by stopping calls to a failing service.

## The Problem

### Cascading Failures

```
Service A → Service B (slow/failing) → Service C
    ↓
 Threads blocked waiting for B
    ↓
 A becomes unresponsive
    ↓
 Callers of A also fail
```

**Result:** One failing service brings down the entire system.

### Resource Exhaustion

When calling a failing service:
- Threads blocked on timeouts
- Connection pools exhausted
- Memory consumed by pending requests
- Latency spikes

## Circuit Breaker Solution

Like an electrical circuit breaker, it "trips" when failures exceed a threshold.

```
        ┌──────────────────────────────────────────┐
        │                                          │
CLOSED ─┼───> Failures exceed threshold ───> OPEN  │
   ↑    │                                     │    │
   │    │                                     │    │
   │    │            (timeout)                │    │
   │    │               ↓                     │    │
   │    │          HALF-OPEN                  │    │
   │    │         /        \                  │    │
   │    │     Success     Failure             │    │
   │    │        │           │                │    │
   └────┼────────┘           └────────────────┘    │
        │                                          │
        └──────────────────────────────────────────┘
```

## States

### CLOSED (Normal Operation)
- Requests pass through normally
- Failures are counted
- If failure threshold exceeded → OPEN

### OPEN (Failing Fast)
- Requests fail immediately
- No calls to downstream service
- After timeout → HALF-OPEN

### HALF-OPEN (Testing Recovery)
- Limited requests allowed through
- If successful → CLOSED
- If failed → OPEN

## Implementation

### Basic Implementation

```python
import time
from enum import Enum
from threading import Lock

class State(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold=5,
        recovery_timeout=30,
        half_open_requests=3
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_requests = half_open_requests
        
        self.state = State.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.lock = Lock()
    
    def call(self, func, *args, **kwargs):
        with self.lock:
            if self.state == State.OPEN:
                if self._should_attempt_reset():
                    self.state = State.HALF_OPEN
                    self.success_count = 0
                else:
                    raise CircuitOpenError()
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _should_attempt_reset(self):
        return (
            time.time() - self.last_failure_time 
            >= self.recovery_timeout
        )
    
    def _on_success(self):
        with self.lock:
            if self.state == State.HALF_OPEN:
                self.success_count += 1
                if self.success_count >= self.half_open_requests:
                    self.state = State.CLOSED
                    self.failure_count = 0
    
    def _on_failure(self):
        with self.lock:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.state == State.HALF_OPEN:
                self.state = State.OPEN
            elif self.failure_count >= self.failure_threshold:
                self.state = State.OPEN
```

### Usage

```python
circuit = CircuitBreaker(
    failure_threshold=5,
    recovery_timeout=30
)

def call_external_service():
    return circuit.call(external_service.get_data)

# With fallback
def get_data_with_fallback():
    try:
        return circuit.call(external_service.get_data)
    except CircuitOpenError:
        return get_cached_data()  # Fallback
```

## Configuration Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| Failure Threshold | Failures before opening | 5 failures |
| Recovery Timeout | Time before testing | 30 seconds |
| Half-Open Requests | Test requests allowed | 3 requests |
| Timeout | Request timeout | 5 seconds |
| Failure Rate | Percentage threshold | 50% |
| Slow Call Rate | Slow call threshold | 100ms |

## Advanced Features

### Sliding Window

Count failures over a time window, not just total.

```python
class SlidingWindowCircuitBreaker:
    def __init__(self, window_size=60, failure_rate_threshold=0.5):
        self.window_size = window_size  # seconds
        self.failure_rate_threshold = failure_rate_threshold
        self.calls = []  # (timestamp, success/failure)
    
    def _failure_rate(self):
        now = time.time()
        # Keep only calls within window
        self.calls = [
            c for c in self.calls 
            if now - c[0] < self.window_size
        ]
        
        if not self.calls:
            return 0
        
        failures = sum(1 for c in self.calls if not c[1])
        return failures / len(self.calls)
```

### Count-Based vs Time-Based

**Count-Based:**
```
Last N calls: [✓, ✓, ✗, ✗, ✗, ✓, ✗]
Failure rate: 4/7 = 57%
```

**Time-Based:**
```
Last 60 seconds: [✓, ✓, ✗, ✗, ✗]
Failure rate: 3/5 = 60%
```

### Slow Call Handling

Count slow calls as failures.

```python
def call(self, func, *args, **kwargs):
    start = time.time()
    try:
        result = func(*args, **kwargs)
        duration = time.time() - start
        
        if duration > self.slow_threshold:
            self._on_slow_call()
        else:
            self._on_success()
        
        return result
    except Exception:
        self._on_failure()
        raise
```

## Fallback Strategies

### Return Cached Data

```python
def get_user(user_id):
    try:
        return circuit.call(user_service.get, user_id)
    except CircuitOpenError:
        return cache.get(f"user:{user_id}")
```

### Default Value

```python
def get_recommendations(user_id):
    try:
        return circuit.call(rec_service.get, user_id)
    except CircuitOpenError:
        return DEFAULT_RECOMMENDATIONS
```

### Fail Gracefully

```python
def get_optional_data():
    try:
        return circuit.call(optional_service.get)
    except CircuitOpenError:
        return None  # Feature degraded but works
```

### Queue for Later

```python
def send_notification(message):
    try:
        circuit.call(notification_service.send, message)
    except CircuitOpenError:
        queue.enqueue(message)  # Retry later
```

## Monitoring

### Metrics to Track

```python
circuit_state_gauge = Gauge('circuit_breaker_state')
circuit_calls_total = Counter('circuit_breaker_calls')
circuit_failures_total = Counter('circuit_breaker_failures')

def call_with_metrics(self, func, *args, **kwargs):
    circuit_calls_total.inc()
    circuit_state_gauge.set(self.state.value)
    
    try:
        return self._call(func, *args, **kwargs)
    except Exception:
        circuit_failures_total.inc()
        raise
```

### Alerting

```yaml
alerts:
  - name: CircuitBreakerOpen
    condition: circuit_breaker_state == "open"
    duration: 5m
    severity: warning
    
  - name: HighFailureRate
    condition: circuit_failures / circuit_calls > 0.5
    duration: 1m
    severity: critical
```

## Libraries

| Library | Language | Features |
|---------|----------|----------|
| resilience4j | Java | Full-featured |
| Polly | .NET | Comprehensive |
| Hystrix | Java | Netflix (deprecated) |
| pybreaker | Python | Simple |
| opossum | Node.js | Promises |
| gobreaker | Go | Lightweight |

### Resilience4j Example

```java
CircuitBreakerConfig config = CircuitBreakerConfig.custom()
    .failureRateThreshold(50)
    .waitDurationInOpenState(Duration.ofSeconds(30))
    .slidingWindowSize(10)
    .build();

CircuitBreaker breaker = CircuitBreaker.of("service", config);

Supplier<String> decorated = CircuitBreaker
    .decorateSupplier(breaker, service::call);

Try.ofSupplier(decorated)
    .recover(throwable -> "fallback");
```

## Combining with Other Patterns

### With Retry

```
Request → Retry (3x) → Circuit Breaker → Service
```

Retry handles transient failures; circuit breaker handles sustained failures.

### With Timeout

```
Request → Timeout (5s) → Circuit Breaker → Service
```

Timeout prevents hanging; circuit breaker prevents repeated timeouts.

### With Bulkhead

```
Request → Bulkhead (limit concurrency) → Circuit Breaker → Service
```

Bulkhead limits impact; circuit breaker stops calls to failing service.

## Interview Tips

1. Explain the cascading failure problem
2. Describe the three states clearly
3. Discuss configuration parameters
4. Plan fallback strategies
5. Consider monitoring and alerting
6. Combine with retry, timeout, bulkhead

## Related Topics

- [Availability & Reliability](../01_fundamentals/availability_reliability.md)
- [Microservices](microservices.md)
- [Rate Limiting](rate_limiting.md)
