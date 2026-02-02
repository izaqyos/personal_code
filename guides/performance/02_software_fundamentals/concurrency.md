# Concurrency Performance

Understanding parallel execution and its performance implications.

## Parallelism vs Concurrency

### Concurrency
Multiple tasks make progress (may not execute simultaneously).
```
Task A: ████░░████░░████
Task B: ░░████░░████░░██
        Time →
```

### Parallelism
Multiple tasks execute simultaneously on multiple cores.
```
Core 1: ████████████████
Core 2: ████████████████
        Time →
```

## Amdahl's Law

Maximum speedup limited by sequential portion:

```
Speedup = 1 / (S + P/N)

Where:
  S = Sequential fraction (0-1)
  P = Parallel fraction (1 - S)
  N = Number of processors
```

### Example
```
90% parallelizable (S = 0.1, P = 0.9):
  2 cores: 1 / (0.1 + 0.9/2) = 1.82x
  4 cores: 1 / (0.1 + 0.9/4) = 3.08x
  8 cores: 1 / (0.1 + 0.9/8) = 4.71x
  ∞ cores: 1 / 0.1 = 10x maximum

50% parallelizable (S = 0.5):
  ∞ cores: 1 / 0.5 = 2x maximum
```

## Threading Models

### Threads
```python
import threading

def worker(data):
    return process(data)

threads = [
    threading.Thread(target=worker, args=(chunk,))
    for chunk in chunks
]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

**Overhead:**
- Thread creation: ~10-100 μs
- Context switch: ~1-10 μs
- Memory: ~1 MB stack per thread

### Thread Pools
```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=8) as executor:
    results = executor.map(process, items)
```

**Benefits:**
- Avoid thread creation overhead
- Limit concurrent threads
- Reuse threads for multiple tasks

### Async/Await (Cooperative)
```python
import asyncio

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, url) for url in urls]
        return await asyncio.gather(*tasks)
```

**Best for:** I/O-bound tasks (network, disk)
**Overhead:** Very low (~1 KB per task)

## Python GIL

Global Interpreter Lock limits Python threading:

```python
# CPU-bound: No parallelism with threads
import threading

def cpu_work():
    sum(range(10_000_000))

# Both threads run on same core (GIL)
t1 = threading.Thread(target=cpu_work)
t2 = threading.Thread(target=cpu_work)
```

### Workarounds

**multiprocessing:**
```python
from multiprocessing import Pool

with Pool(4) as p:
    results = p.map(cpu_work, data)

# True parallelism, separate processes
# Overhead: Process creation + IPC
```

**C extensions (release GIL):**
```python
import numpy as np
# NumPy releases GIL for computation
result = np.dot(large_array1, large_array2)
```

## Lock Contention

### Lock Overhead
```
Uncontended lock: ~20 ns
Contended lock: 1-100 μs (depending on wait)
```

### Reducing Contention
```python
# Bad: Single global lock
lock = threading.Lock()
def increment():
    with lock:
        global counter
        counter += 1

# Better: Per-item locks
class Counter:
    def __init__(self, n):
        self.locks = [threading.Lock() for _ in range(n)]
        self.values = [0] * n
    
    def increment(self, i):
        with self.locks[i]:
            self.values[i] += 1
```

### Lock-Free Data Structures
```python
from queue import Queue  # Thread-safe, lock-free
from collections import deque  # Not thread-safe

# Atomic operations
import threading
counter = threading.local()  # Thread-local storage
```

## Scaling Analysis

### Strong Scaling
Fixed problem size, add more processors.
```
Ideal: Time / N with N processors
Reality: Limited by Amdahl's law
```

### Weak Scaling
Problem size grows with processors.
```
Ideal: Constant time as both grow
Reality: Communication overhead increases
```

## Communication Overhead

### Shared Memory
```
Cache coherence: ~10-100 cycles
False sharing: ~100-1000 cycles (adjacent cache lines)
```

### False Sharing
```python
# Bad: Adjacent data causes cache invalidation
class Counters:
    def __init__(self):
        self.c1 = 0  # Thread 1 updates
        self.c2 = 0  # Thread 2 updates - same cache line!

# Better: Padding to separate cache lines
class PaddedCounters:
    def __init__(self):
        self.c1 = 0
        self._pad1 = [0] * 16  # 64-byte padding
        self.c2 = 0
```

### Message Passing
```
Same machine: ~1-10 μs
Network (datacenter): ~100-500 μs
Network (cross-region): ~10-100 ms
```

## Practical Guidelines

### CPU-Bound Tasks
```
Workers = Number of CPU cores
More workers = Context switch overhead

Optimal: multiprocessing.cpu_count()
```

### I/O-Bound Tasks
```
Workers = Many (hundreds)
Limited by: Memory, file descriptors, connections

Use: asyncio or thread pools
```

### Mixed Workloads
```
Separate pools for CPU and I/O
Route tasks to appropriate pool
```

## Calculation Examples

### Example 1: Parallel Speedup
```
Sort 1 billion numbers, 90% parallelizable:

Single core: 100 seconds
8 cores: 100 / (0.1 + 0.9/8) = 47 seconds
Actual speedup: 2.1x (not 8x)

Bottleneck: 10 second sequential portion
```

### Example 2: Thread Pool Sizing
```
Web server, 100 ms per request, 50% I/O wait:

CPU work: 50 ms per request
8 cores: 8 * 1000 / 50 = 160 requests/second (CPU)

I/O threads: Can handle many more
Optimal: 8 CPU cores + large thread pool for I/O
```

### Example 3: GIL Impact
```python
# Python CPU-bound task:
# Single thread: 10 seconds
# 4 threads: 10 seconds (GIL)
# 4 processes: 2.5 seconds (true parallel)
```

## Quick Reference

### When to Use What

| Workload | Python | Java/Go | C++ |
|----------|--------|---------|-----|
| CPU-bound | multiprocessing | Threads | Threads |
| I/O-bound | asyncio/threads | Threads | Threads/async |
| Mixed | Separate pools | Thread pool | Thread pool |

### Overhead Estimates
```
Thread creation: ~10-100 μs
Process creation: ~1-10 ms
Context switch: ~1-10 μs
Lock acquire: ~20 ns uncontended
```

### Parallelism Limits
```
8 cores, 90% parallel: 4.7x max speedup
8 cores, 99% parallel: 7.5x max speedup
8 cores, 50% parallel: 1.8x max speedup
```

## Related Topics
- [CPU Architecture](../01_hardware_fundamentals/cpu_architecture.md)
- [Language Performance](language_performance.md)
