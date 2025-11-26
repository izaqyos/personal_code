"""
Week 12, Day 7: Review & Challenge - Async Programming

Learning Objectives:
- Review all Week 12 concepts
- Apply async programming techniques
- Build async applications
- Master asyncio
- Create scalable async tools

Challenge: Build async web scrapers and API clients

Time: 15-20 minutes
"""

import asyncio
import time

# ============================================================
# REVIEW: Week 12 Concepts
# ============================================================

def week12_review():
    """Quick review of all Week 12 concepts"""
    print("=" * 60)
    print("WEEK 12 REVIEW")
    print("=" * 60)
    
    print("\nDay 1: Async Basics")
    print("  • async/await syntax")
    print("  • Coroutines")
    print("  • Event loop")
    
    print("\nDay 2: asyncio Tasks")
    print("  • Creating tasks")
    print("  • Task management")
    print("  • Gathering results")
    
    print("\nDay 3: Async I/O")
    print("  • Async file I/O")
    print("  • Async network I/O")
    print("  • aiohttp basics")
    
    print("\nDay 4: Synchronization")
    print("  • Async locks")
    print("  • Async events")
    print("  • Async queues")
    
    print("\nDay 5: Async Context Managers")
    print("  • Async context managers")
    print("  • Async iterators")
    print("  • Async generators")
    
    print("\nDay 6: Real-World Async")
    print("  • Web scraping")
    print("  • API clients")
    print("  • Error handling")
    
    print("\n" + "=" * 60)
    print()

# ============================================================
# CHALLENGE 1: Async Data Fetcher
# ============================================================

async def async_data_fetcher():
    """
    Fetch data asynchronously.
    """
    print("--- Challenge 1: Async Data Fetcher ---")
    
    async def fetch_data(data_id):
        """Simulate async data fetch"""
        await asyncio.sleep(0.1)  # Simulate I/O
        return f"Data-{data_id}"
    
    # Fetch multiple items concurrently
    data_ids = list(range(10))
    
    start = time.time()
    results = await asyncio.gather(*[fetch_data(i) for i in data_ids])
    duration = time.time() - start
    
    print(f"Items fetched: {len(results)}")
    print(f"Time taken: {duration:.4f}s")
    print(f"Average per item: {duration/len(results):.4f}s")
    
    print()

# ============================================================
# CHALLENGE 2: Async Task Manager
# ============================================================

async def async_task_manager():
    """
    Manage multiple async tasks.
    """
    print("--- Challenge 2: Async Task Manager ---")
    
    async def task(task_id, duration):
        """Async task with variable duration"""
        await asyncio.sleep(duration)
        return f"Task-{task_id} completed"
    
    # Create tasks with different durations
    tasks = [
        asyncio.create_task(task(1, 0.1)),
        asyncio.create_task(task(2, 0.2)),
        asyncio.create_task(task(3, 0.15)),
    ]
    
    # Wait for all tasks
    start = time.time()
    results = await asyncio.gather(*tasks)
    duration = time.time() - start
    
    print(f"Tasks: {len(tasks)}")
    print(f"Total time: {duration:.4f}s")
    print(f"Results: {len(results)}")
    
    print()

# ============================================================
# CHALLENGE 3: Async Producer-Consumer
# ============================================================

async def async_producer_consumer():
    """
    Implement async producer-consumer pattern.
    """
    print("--- Challenge 3: Async Producer-Consumer ---")
    
    queue = asyncio.Queue(maxsize=5)
    
    async def producer(queue, items):
        """Produce items"""
        for item in items:
            await queue.put(item)
            print(f"  Produced: {item}")
            await asyncio.sleep(0.01)
        await queue.put(None)  # Sentinel
    
    async def consumer(queue):
        """Consume items"""
        results = []
        while True:
            item = await queue.get()
            if item is None:
                break
            results.append(item * 2)
            print(f"  Consumed: {item} -> {item * 2}")
            await asyncio.sleep(0.02)
        return results
    
    items = [1, 2, 3, 4, 5]
    
    # Run producer and consumer concurrently
    await asyncio.gather(
        producer(queue, items),
        consumer(queue)
    )
    
    print(f"Processed {len(items)} items")
    
    print()

# ============================================================
# CHALLENGE 4: Async with Timeout
# ============================================================

async def async_with_timeout():
    """
    Handle async operations with timeout.
    """
    print("--- Challenge 4: Async with Timeout ---")
    
    async def slow_operation(duration):
        """Slow async operation"""
        await asyncio.sleep(duration)
        return "Completed"
    
    # Test with timeout
    try:
        result = await asyncio.wait_for(slow_operation(0.1), timeout=0.5)
        print(f"Result: {result} (within timeout)")
    except asyncio.TimeoutError:
        print("Result: Timeout!")
    
    # Test timeout exceeded
    try:
        result = await asyncio.wait_for(slow_operation(1.0), timeout=0.1)
        print(f"Result: {result}")
    except asyncio.TimeoutError:
        print("Result: Timeout exceeded")
    
    print()

# ============================================================
# CHALLENGE 5: Async Batch Processor
# ============================================================

async def async_batch_processor():
    """
    Process data in async batches.
    """
    print("--- Challenge 5: Async Batch Processor ---")
    
    async def process_item(item):
        """Process single item"""
        await asyncio.sleep(0.01)
        return item * item
    
    async def process_batch(batch):
        """Process batch concurrently"""
        return await asyncio.gather(*[process_item(item) for item in batch])
    
    # Create data
    data = list(range(50))
    batch_size = 10
    batches = [data[i:i+batch_size] for i in range(0, len(data), batch_size)]
    
    # Process batches
    start = time.time()
    results = []
    for batch in batches:
        batch_results = await process_batch(batch)
        results.extend(batch_results)
    duration = time.time() - start
    
    print(f"Total items: {len(data)}")
    print(f"Batch size: {batch_size}")
    print(f"Batches: {len(batches)}")
    print(f"Time: {duration:.4f}s")
    
    print()

# ============================================================
# CHALLENGE 6: Async Rate Limiter
# ============================================================

async def async_rate_limiter():
    """
    Implement async rate limiting.
    """
    print("--- Challenge 6: Async Rate Limiter ---")
    
    class RateLimiter:
        def __init__(self, rate, per):
            self.rate = rate
            self.per = per
            self.allowance = rate
            self.last_check = time.time()
        
        async def acquire(self):
            current = time.time()
            time_passed = current - self.last_check
            self.last_check = current
            self.allowance += time_passed * (self.rate / self.per)
            
            if self.allowance > self.rate:
                self.allowance = self.rate
            
            if self.allowance < 1.0:
                sleep_time = (1.0 - self.allowance) * (self.per / self.rate)
                await asyncio.sleep(sleep_time)
                self.allowance = 0.0
            else:
                self.allowance -= 1.0
    
    limiter = RateLimiter(rate=5, per=1.0)  # 5 requests per second
    
    async def make_request(request_id):
        await limiter.acquire()
        print(f"  Request {request_id} at {time.time():.2f}")
        return f"Response-{request_id}"
    
    # Make 10 requests (should be rate-limited)
    start = time.time()
    results = await asyncio.gather(*[make_request(i) for i in range(10)])
    duration = time.time() - start
    
    print(f"\nRequests: {len(results)}")
    print(f"Time: {duration:.2f}s")
    
    print()

# ============================================================
# CHALLENGE 7: Complete Async Application
# ============================================================

async def complete_async_application():
    """
    Build complete async application.
    """
    print("--- Challenge 7: Complete Async Application ---")
    
    print("=" * 60)
    print("ASYNC DATA PROCESSOR")
    print("=" * 60)
    
    async def fetch_data(source_id):
        """Fetch data from source"""
        await asyncio.sleep(0.05)
        return {"source": source_id, "data": f"Data-{source_id}"}
    
    async def process_data(data):
        """Process fetched data"""
        await asyncio.sleep(0.02)
        return {**data, "processed": True}
    
    async def save_data(data):
        """Save processed data"""
        await asyncio.sleep(0.01)
        return {**data, "saved": True}
    
    # Pipeline: fetch -> process -> save
    async def pipeline(source_id):
        data = await fetch_data(source_id)
        data = await process_data(data)
        data = await save_data(data)
        return data
    
    # Process multiple sources concurrently
    sources = list(range(10))
    
    start = time.time()
    results = await asyncio.gather(*[pipeline(source_id) for source_id in sources])
    duration = time.time() - start
    
    print(f"\n[Results]")
    print(f"Sources processed: {len(results)}")
    print(f"Total time: {duration:.4f}s")
    print(f"Average per source: {duration/len(results):.4f}s")
    
    print("\n" + "=" * 60)
    print()

# ============================================================
# SELF-ASSESSMENT
# ============================================================

def self_assessment():
    """Self-assessment checklist for Week 12"""
    print("=" * 60)
    print("WEEK 12 SELF-ASSESSMENT")
    print("=" * 60)
    
    checklist = [
        ("async/await", "Can you write async functions?"),
        ("Tasks", "Can you create and manage async tasks?"),
        ("Async I/O", "Can you perform async I/O operations?"),
        ("Synchronization", "Can you use async locks and queues?"),
        ("Context managers", "Can you use async context managers?"),
        ("Error handling", "Can you handle async errors?"),
        ("Async apps", "Can you build async applications?"),
    ]
    
    print("\nRate yourself (1-5) on these concepts:\n")
    for i, (topic, question) in enumerate(checklist, 1):
        print(f"{i}. {topic}")
        print(f"   {question}")
        print()
    
    print("=" * 60)
    print()

# ============================================================
# MAIN EXECUTION
# ============================================================

async def main():
    """Main async function"""
    print("=" * 60)
    print("Week 12, Day 7: Review & Challenge")
    print("=" * 60)
    print()
    
    week12_review()
    
    print("\n" + "=" * 60)
    print("CHALLENGES")
    print("=" * 60 + "\n")
    
    await async_data_fetcher()
    await async_task_manager()
    await async_producer_consumer()
    await async_with_timeout()
    await async_batch_processor()
    await async_rate_limiter()
    await complete_async_application()
    
    self_assessment()
    
    print("=" * 60)
    print("✅ Week 12 Complete!")
    print("=" * 60)
    print("\n🎉 Congratulations! You've completed the first 12 weeks!")
    print("\n📚 Continue practicing with real-world projects!")
    print("\n💡 You now have a solid foundation in Python!")

if __name__ == "__main__":
    asyncio.run(main())

