# Exercise: Rate Limiting Algorithms

## Objective
Understand and implement basic rate limiting algorithms.

## Tasks

### Task 1: Fixed Window Counter

Implement a fixed window counter for 100 requests/minute:

```python
class FixedWindowCounter:
    def __init__(self, limit, window_seconds):
        self.limit = limit
        self.window_seconds = window_seconds
        # TODO: Initialize state
    
    def is_allowed(self):
        # TODO: Implement
        pass
```

Test your implementation:
```
Time 0:00 - 50 requests → All allowed
Time 0:30 - 40 requests → All allowed
Time 0:59 - 20 requests → 10 allowed, 10 rejected
Time 1:00 - 10 requests → All allowed (new window)
```

### Task 2: Sliding Window Log

Implement a sliding window log for the same limit:

```python
class SlidingWindowLog:
    def __init__(self, limit, window_seconds):
        self.limit = limit
        self.window_seconds = window_seconds
        self.requests = []  # List of timestamps
    
    def is_allowed(self):
        # TODO: Implement
        pass
```

### Task 3: Token Bucket

Implement a token bucket with:
- Capacity: 10 tokens
- Refill rate: 2 tokens/second

```python
class TokenBucket:
    def __init__(self, capacity, refill_rate):
        # TODO: Initialize
        pass
    
    def allow(self, tokens=1):
        # TODO: Implement
        pass
```

Test scenarios:
```
Initial: 10 tokens
Request 5 tokens → Allowed, 5 remaining
Wait 2 seconds → 5 + 4 = 9 tokens
Request 10 tokens → Rejected (only 9)
Request 9 tokens → Allowed, 0 remaining
```

### Task 4: Algorithm Comparison

Fill in the comparison table:

| Feature | Fixed Window | Sliding Log | Token Bucket |
|---------|--------------|-------------|--------------|
| Memory usage | | | |
| Allows bursts | | | |
| Boundary issues | | | |
| Implementation complexity | | | |

### Task 5: Choose the Algorithm

For each scenario, choose the best algorithm:

1. **API rate limiting for paying customers**
   - Algorithm: ___
   - Why: ___

2. **DDoS protection at network edge**
   - Algorithm: ___
   - Why: ___

3. **Database connection limiting**
   - Algorithm: ___
   - Why: ___

---

<details>
<summary>Hints</summary>

- Fixed window: O(1) memory, but has boundary burst issue
- Sliding log: Accurate, but O(n) memory
- Token bucket: Allows controlled bursts, O(1) memory
- Consider the trade-offs for each use case

</details>

<details>
<summary>Solution</summary>

### Task 1: Fixed Window Counter

```python
import time

class FixedWindowCounter:
    def __init__(self, limit, window_seconds):
        self.limit = limit
        self.window_seconds = window_seconds
        self.window_start = 0
        self.count = 0
    
    def is_allowed(self):
        now = time.time()
        current_window = int(now // self.window_seconds) * self.window_seconds
        
        if current_window != self.window_start:
            # New window
            self.window_start = current_window
            self.count = 0
        
        if self.count < self.limit:
            self.count += 1
            return True
        return False
```

### Task 2: Sliding Window Log

```python
import time

class SlidingWindowLog:
    def __init__(self, limit, window_seconds):
        self.limit = limit
        self.window_seconds = window_seconds
        self.requests = []
    
    def is_allowed(self):
        now = time.time()
        cutoff = now - self.window_seconds
        
        # Remove old requests
        self.requests = [t for t in self.requests if t > cutoff]
        
        if len(self.requests) < self.limit:
            self.requests.append(now)
            return True
        return False
```

### Task 3: Token Bucket

```python
import time

class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()
    
    def allow(self, tokens=1):
        self._refill()
        
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False
    
    def _refill(self):
        now = time.time()
        elapsed = now - self.last_refill
        refill_amount = elapsed * self.refill_rate
        
        self.tokens = min(self.capacity, self.tokens + refill_amount)
        self.last_refill = now
```

### Task 4: Algorithm Comparison

| Feature | Fixed Window | Sliding Log | Token Bucket |
|---------|--------------|-------------|--------------|
| Memory usage | O(1) | O(n) | O(1) |
| Allows bursts | Yes (at boundary) | No | Yes (controlled) |
| Boundary issues | Yes (2x at boundary) | No | No |
| Implementation | Simple | Medium | Medium |

### Task 5: Choose the Algorithm

1. **API rate limiting:** Token Bucket
   - Allows controlled bursts for UX
   - Fair across time

2. **DDoS protection:** Fixed Window or Token Bucket
   - O(1) memory critical at scale
   - Simple to implement in hardware/edge

3. **Database connections:** Token Bucket
   - Controls burst of connections
   - Smooth connection rate

</details>
