# Week 11: Concurrency (Threading & Multiprocessing)

Master concurrent programming with threads and processes.

## Overview

This week focuses on concurrency - running multiple tasks simultaneously using threading and multiprocessing. Learn when to use each approach, how to synchronize access to shared resources, and how to build high-performance concurrent applications.

## Daily Breakdown

### Day 1: Threading Basics
- Thread creation
- Thread lifecycle
- Daemon threads
- Thread pools
- GIL implications

### Day 2: Thread Synchronization
- Locks and RLocks
- Semaphores
- Events
- Conditions
- Barriers

### Day 3: Thread-Safe Data Structures
- Queue module
- Producer-consumer pattern
- Priority queues
- Thread-safe collections
- Communication patterns

### Day 4: Multiprocessing Basics
- Process creation
- Process pools
- Inter-process communication
- Shared memory
- Manager objects

### Day 5: concurrent.futures
- ThreadPoolExecutor
- ProcessPoolExecutor
- Futures and callbacks
- Exception handling
- Best practices

### Day 6: Performance & Optimization
- CPU-bound vs I/O-bound
- Choosing threading vs multiprocessing
- Profiling concurrent code
- Common pitfalls
- Performance tuning

### Day 7: Review & Challenge
- Web scraper (threading)
- Data processor (multiprocessing)
- Task scheduler
- Parallel file processor
- Complete concurrent applications

## Threading vs Multiprocessing

| Aspect | Threading | Multiprocessing |
|--------|-----------|-----------------|
| **Use Case** | I/O-bound tasks | CPU-bound tasks |
| **GIL** | Limited by GIL | No GIL limitation |
| **Memory** | Shared memory | Separate memory |
| **Overhead** | Low | Higher |
| **Communication** | Easy (shared state) | IPC required |
| **Safety** | Need synchronization | Isolated by default |

## Quick Reference

```python
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from queue import Queue

# Threading
def worker(name):
    print(f"Worker {name} starting")
    # Do work
    print(f"Worker {name} done")

thread = threading.Thread(target=worker, args=("A",))
thread.start()
thread.join()

# Thread pool
with ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(worker, range(10))

# Multiprocessing
def cpu_task(n):
    return n * n

with ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(cpu_task, range(100)))

# Thread-safe queue
queue = Queue()
queue.put(item)
item = queue.get()

# Lock
lock = threading.Lock()
with lock:
    # Critical section
    pass
```

## The GIL (Global Interpreter Lock)

**What is it?**
- Python's mechanism to ensure thread safety
- Only one thread executes Python bytecode at a time
- Limits CPU-bound multi-threading performance

**Implications:**
- Threading good for I/O-bound tasks
- Multiprocessing needed for CPU-bound tasks
- C extensions can release GIL

## Learning Outcomes

✅ Understand threading and multiprocessing  
✅ Choose appropriate concurrency model  
✅ Implement thread synchronization  
✅ Use thread-safe data structures  
✅ Work with process pools  
✅ Handle concurrent exceptions  
✅ Build high-performance applications  

## Next Steps

🎯 **Week 12:** Async Programming  
Learn async/await and asyncio.

---

*Master concurrent programming for better performance! 🐍*

