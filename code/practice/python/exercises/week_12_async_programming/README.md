# Week 12: Async Programming (asyncio)

Master asynchronous programming with async/await and asyncio.

## Overview

This week focuses on asynchronous programming - writing concurrent code that's efficient for I/O-bound tasks without the complexity of threading. Learn async/await syntax, asyncio event loop, and how to build high-performance async applications.

## Daily Breakdown

### Day 1: Async Basics
- async/await syntax
- Coroutines
- Event loop
- Running async code
- Basic async patterns

### Day 2: asyncio Tasks
- Creating tasks
- Task management
- Gathering results
- Timeouts and cancellation
- Task groups

### Day 3: Async I/O
- Async file I/O
- Async network I/O
- Streams
- Protocols
- aiohttp basics

### Day 4: Synchronization Primitives
- Async locks
- Async events
- Async semaphores
- Async queues
- Coordination patterns

### Day 5: Async Context Managers & Iterators
- Async context managers
- Async iterators
- Async generators
- Async comprehensions
- Advanced patterns

### Day 6: Real-World Async
- Web scraping with aiohttp
- Async database access
- API clients
- Error handling
- Best practices

### Day 7: Review & Challenge
- Async web crawler
- Concurrent API client
- Real-time data processor
- Async task scheduler
- Complete async applications

## Async vs Threading vs Multiprocessing

| Approach | Best For | Pros | Cons |
|----------|----------|------|------|
| **Async** | I/O-bound, many tasks | Efficient, scalable | Complex, single-threaded |
| **Threading** | I/O-bound, shared state | Simple, shared memory | GIL, synchronization |
| **Multiprocessing** | CPU-bound | True parallelism | High overhead, IPC |

## Quick Reference

```python
import asyncio
import aiohttp

# Basic async function
async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

# Run async code
asyncio.run(fetch_data('https://example.com'))

# Multiple tasks
async def main():
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results

# With timeout
async def with_timeout():
    try:
        result = await asyncio.wait_for(
            fetch_data(url),
            timeout=5.0
        )
    except asyncio.TimeoutError:
        print("Timeout!")

# Async context manager
async with aiohttp.ClientSession() as session:
    # Use session
    pass

# Async iterator
async for item in async_generator():
    process(item)
```

## Key Concepts

**Coroutine:**
- Function defined with `async def`
- Returns coroutine object
- Must be awaited or scheduled

**Event Loop:**
- Core of asyncio
- Manages and executes coroutines
- Handles I/O operations

**Task:**
- Wrapper around coroutine
- Scheduled on event loop
- Can be cancelled

**await:**
- Suspends coroutine execution
- Allows other coroutines to run
- Returns result when ready

## Common Patterns

```python
# Gather (run concurrently, wait for all)
results = await asyncio.gather(coro1(), coro2(), coro3())

# Wait with timeout
done, pending = await asyncio.wait(
    tasks,
    timeout=10.0
)

# As completed (process as they finish)
for coro in asyncio.as_completed(coros):
    result = await coro
    process(result)

# Create task
task = asyncio.create_task(coro())
result = await task

# Sleep
await asyncio.sleep(1.0)
```

## Learning Outcomes

✅ Understand async/await syntax  
✅ Work with asyncio event loop  
✅ Create and manage async tasks  
✅ Implement async I/O operations  
✅ Use async synchronization primitives  
✅ Build async web clients  
✅ Handle errors in async code  
✅ Choose appropriate concurrency model  

## When to Use Async

**Good for:**
- Web scraping
- API clients
- Network services
- I/O-heavy applications
- Many concurrent connections

**Not ideal for:**
- CPU-bound tasks
- Simple scripts
- Legacy code integration
- Blocking libraries

## Next Steps

🎯 Continue practicing with real-world projects!  
🎯 Explore advanced async patterns  
🎯 Build production async applications  

---

*Master async programming for scalable applications! 🐍*

