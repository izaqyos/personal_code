"""
Week 11, Day 7: Review & Challenge - Concurrency

Learning Objectives:
- Review all Week 11 concepts
- Apply concurrency techniques
- Build concurrent applications
- Master threading and multiprocessing
- Create high-performance tools

Challenge: Build concurrent data processors and web scrapers

Time: 15-20 minutes
"""

import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from queue import Queue
import time

# ============================================================
# REVIEW: Week 11 Concepts
# ============================================================

def week11_review():
    """Quick review of all Week 11 concepts"""
    print("=" * 60)
    print("WEEK 11 REVIEW")
    print("=" * 60)
    
    print("\nDay 1: Threading Basics")
    print("  • Thread creation and lifecycle")
    print("  • Thread pools")
    print("  • GIL implications")
    
    print("\nDay 2: Thread Synchronization")
    print("  • Locks and RLocks")
    print("  • Semaphores and Events")
    print("  • Thread coordination")
    
    print("\nDay 3: Thread-Safe Data")
    print("  • Queue module")
    print("  • Producer-consumer pattern")
    print("  • Thread-safe collections")
    
    print("\nDay 4: Multiprocessing")
    print("  • Process creation")
    print("  • Process pools")
    print("  • Inter-process communication")
    
    print("\nDay 5: concurrent.futures")
    print("  • ThreadPoolExecutor")
    print("  • ProcessPoolExecutor")
    print("  • Futures and callbacks")
    
    print("\nDay 6: Performance")
    print("  • CPU-bound vs I/O-bound")
    print("  • Choosing concurrency model")
    print("  • Optimization techniques")
    
    print("\n" + "=" * 60)
    print()

# ============================================================
# CHALLENGE 1: Parallel Data Processor
# ============================================================

def parallel_data_processor():
    """
    Process data in parallel using multiprocessing.
    """
    print("--- Challenge 1: Parallel Data Processor ---")
    
    def process_item(n):
        """Simulate CPU-intensive work"""
        result = sum(i * i for i in range(n))
        return result
    
    data = [1000, 2000, 3000, 4000, 5000]
    
    # Sequential processing
    start = time.time()
    sequential_results = [process_item(n) for n in data]
    sequential_time = time.time() - start
    
    # Parallel processing
    start = time.time()
    with ProcessPoolExecutor(max_workers=4) as executor:
        parallel_results = list(executor.map(process_item, data))
    parallel_time = time.time() - start
    
    print(f"Data items: {len(data)}")
    print(f"Sequential time: {sequential_time:.4f}s")
    print(f"Parallel time: {parallel_time:.4f}s")
    print(f"Speedup: {sequential_time/parallel_time:.2f}x")
    
    print()

# ============================================================
# CHALLENGE 2: Thread Pool Worker
# ============================================================

def thread_pool_worker():
    """
    Use thread pool for I/O-bound tasks.
    """
    print("--- Challenge 2: Thread Pool Worker ---")
    
    def fetch_data(url_id):
        """Simulate I/O operation"""
        time.sleep(0.1)  # Simulate network delay
        return f"Data from URL {url_id}"
    
    urls = list(range(10))
    
    # Using ThreadPoolExecutor
    start = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(fetch_data, urls))
    duration = time.time() - start
    
    print(f"URLs processed: {len(urls)}")
    print(f"Time taken: {duration:.4f}s")
    print(f"Results: {len(results)} items")
    
    print()

# ============================================================
# CHALLENGE 3: Producer-Consumer Pattern
# ============================================================

def producer_consumer_pattern():
    """
    Implement producer-consumer with Queue.
    """
    print("--- Challenge 3: Producer-Consumer Pattern ---")
    
    queue = Queue(maxsize=5)
    
    def producer(queue, items):
        """Produce items"""
        for item in items:
            queue.put(item)
            print(f"  Produced: {item}")
        queue.put(None)  # Sentinel
    
    def consumer(queue):
        """Consume items"""
        results = []
        while True:
            item = queue.get()
            if item is None:
                break
            results.append(item * 2)
            print(f"  Consumed: {item} -> {item * 2}")
            queue.task_done()
        return results
    
    items = [1, 2, 3, 4, 5]
    
    # Create threads
    producer_thread = threading.Thread(target=producer, args=(queue, items))
    consumer_thread = threading.Thread(target=consumer, args=(queue,))
    
    # Start threads
    producer_thread.start()
    consumer_thread.start()
    
    # Wait for completion
    producer_thread.join()
    consumer_thread.join()
    
    print(f"Processed {len(items)} items")
    
    print()

# ============================================================
# CHALLENGE 4: Thread-Safe Counter
# ============================================================

def thread_safe_counter():
    """
    Implement thread-safe counter with Lock.
    """
    print("--- Challenge 4: Thread-Safe Counter ---")
    
    class Counter:
        def __init__(self):
            self.value = 0
            self.lock = threading.Lock()
        
        def increment(self):
            with self.lock:
                self.value += 1
    
    counter = Counter()
    
    def worker(counter, iterations):
        """Increment counter"""
        for _ in range(iterations):
            counter.increment()
    
    # Create threads
    threads = []
    iterations_per_thread = 1000
    num_threads = 5
    
    for _ in range(num_threads):
        thread = threading.Thread(target=worker, args=(counter, iterations_per_thread))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads
    for thread in threads:
        thread.join()
    
    expected = num_threads * iterations_per_thread
    print(f"Threads: {num_threads}")
    print(f"Iterations per thread: {iterations_per_thread}")
    print(f"Expected: {expected}")
    print(f"Actual: {counter.value}")
    print(f"Correct: {counter.value == expected}")
    
    print()

# ============================================================
# CHALLENGE 5: Batch Processor
# ============================================================

def batch_processor():
    """
    Process data in batches with multiprocessing.
    """
    print("--- Challenge 5: Batch Processor ---")
    
    def process_batch(batch):
        """Process a batch of data"""
        return [x * x for x in batch]
    
    # Create data
    data = list(range(100))
    batch_size = 10
    batches = [data[i:i+batch_size] for i in range(0, len(data), batch_size)]
    
    # Process batches in parallel
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(process_batch, batches))
    
    # Flatten results
    all_results = [item for batch in results for item in batch]
    
    print(f"Total items: {len(data)}")
    print(f"Batch size: {batch_size}")
    print(f"Batches: {len(batches)}")
    print(f"Results: {len(all_results)}")
    
    print()

# ============================================================
# CHALLENGE 6: Concurrent File Processor
# ============================================================

def concurrent_file_processor():
    """
    Process multiple files concurrently.
    """
    print("--- Challenge 6: Concurrent File Processor ---")
    
    def process_file(filename):
        """Simulate file processing"""
        time.sleep(0.05)  # Simulate I/O
        return f"Processed {filename}"
    
    files = [f"file{i}.txt" for i in range(20)]
    
    # Process with thread pool
    start = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(process_file, files))
    duration = time.time() - start
    
    print(f"Files: {len(files)}")
    print(f"Workers: 5")
    print(f"Time: {duration:.4f}s")
    print(f"Processed: {len(results)} files")
    
    print()

# ============================================================
# CHALLENGE 7: Complete Concurrent Application
# ============================================================

def complete_concurrent_application():
    """
    Build complete concurrent application.
    """
    print("--- Challenge 7: Complete Concurrent Application ---")
    
    print("=" * 60)
    print("CONCURRENT DATA PROCESSOR")
    print("=" * 60)
    
    def cpu_task(n):
        """CPU-intensive task"""
        return sum(i * i for i in range(n))
    
    def io_task(task_id):
        """I/O-intensive task"""
        time.sleep(0.01)
        return f"IO-{task_id}"
    
    # CPU-bound with multiprocessing
    print("\n[CPU-Bound Tasks]")
    cpu_data = [1000, 2000, 3000, 4000]
    start = time.time()
    with ProcessPoolExecutor(max_workers=4) as executor:
        cpu_results = list(executor.map(cpu_task, cpu_data))
    cpu_time = time.time() - start
    print(f"Tasks: {len(cpu_data)}")
    print(f"Time: {cpu_time:.4f}s")
    
    # I/O-bound with threading
    print("\n[I/O-Bound Tasks]")
    io_data = list(range(20))
    start = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        io_results = list(executor.map(io_task, io_data))
    io_time = time.time() - start
    print(f"Tasks: {len(io_data)}")
    print(f"Time: {io_time:.4f}s")
    
    print("\n" + "=" * 60)
    print()

# ============================================================
# SELF-ASSESSMENT
# ============================================================

def self_assessment():
    """Self-assessment checklist for Week 11"""
    print("=" * 60)
    print("WEEK 11 SELF-ASSESSMENT")
    print("=" * 60)
    
    checklist = [
        ("Threading", "Can you create and manage threads?"),
        ("Synchronization", "Can you use locks and semaphores?"),
        ("Thread-safe", "Can you work with thread-safe data?"),
        ("Multiprocessing", "Can you use multiprocessing?"),
        ("concurrent.futures", "Can you use thread/process pools?"),
        ("Performance", "Can you choose the right approach?"),
        ("Concurrent apps", "Can you build concurrent applications?"),
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

if __name__ == "__main__":
    print("=" * 60)
    print("Week 11, Day 7: Review & Challenge")
    print("=" * 60)
    print()
    
    week11_review()
    
    print("\n" + "=" * 60)
    print("CHALLENGES")
    print("=" * 60 + "\n")
    
    parallel_data_processor()
    thread_pool_worker()
    producer_consumer_pattern()
    thread_safe_counter()
    batch_processor()
    concurrent_file_processor()
    complete_concurrent_application()
    
    self_assessment()
    
    print("=" * 60)
    print("✅ Week 11 Complete!")
    print("=" * 60)
    print("\n🎉 Congratulations! You've mastered concurrency!")
    print("\n📚 Next: Week 12 - Async Programming")
    print("\n💡 Build high-performance concurrent applications!")

