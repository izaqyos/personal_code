"""
Week 6, Day 3: heapq and Priority Queues

Learning Objectives:
- Master heapq module for heap operations
- Learn priority queue implementation
- Understand heap properties (min-heap)
- Practice top-k problems
- Apply heaps to real-world scenarios

Time: 10-15 minutes
"""

import heapq
from typing import List, Any

# ============================================================
# EXERCISE 1: heapq Basics
# ============================================================

def heapq_basics():
    """
    Learn basic heap operations.
    
    Heap: Binary tree where parent <= children (min-heap)
    """
    print("--- Exercise 1: heapq Basics ---")
    
    # Create heap from list
    numbers = [5, 2, 8, 1, 9, 3]
    heapq.heapify(numbers)
    print(f"After heapify: {numbers}")
    print(f"  Smallest element: {numbers[0]}")
    
    # Push element
    heapq.heappush(numbers, 0)
    print(f"After heappush(0): {numbers}")
    
    # Pop smallest
    smallest = heapq.heappop(numbers)
    print(f"Popped: {smallest}, remaining: {numbers}")
    
    # Push and pop in one operation
    replaced = heapq.heappushpop(numbers, 4)
    print(f"heappushpop(4): replaced {replaced}, heap: {numbers}")
    
    print()

# ============================================================
# EXERCISE 2: Finding Top K Elements
# ============================================================

def top_k_elements():
    """
    Find k largest/smallest elements efficiently.
    
    TODO: Use heapq.nlargest and heapq.nsmallest
    """
    print("--- Exercise 2: Top K Elements ---")
    
    numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    
    # K largest
    k = 3
    largest = heapq.nlargest(k, numbers)
    print(f"Numbers: {numbers}")
    print(f"{k} largest: {largest}")
    
    # K smallest
    smallest = heapq.nsmallest(k, numbers)
    print(f"{k} smallest: {smallest}")
    
    # With key function
    words = ['banana', 'pie', 'Washington', 'book', 'a']
    longest = heapq.nlargest(3, words, key=len)
    print(f"\nWords: {words}")
    print(f"3 longest: {longest}")
    
    print()

# ============================================================
# EXERCISE 3: Priority Queue Implementation
# ============================================================

class PriorityQueue:
    """
    Priority queue using heapq.
    
    TODO: Implement priority queue with heap
    """
    
    def __init__(self):
        self._queue = []
        self._index = 0  # For tie-breaking
    
    def push(self, item, priority):
        """Add item with priority (lower number = higher priority)"""
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1
    
    def pop(self):
        """Remove and return highest priority item"""
        if self._queue:
            return heapq.heappop(self._queue)[-1]
        raise IndexError("pop from empty priority queue")
    
    def peek(self):
        """Return highest priority item without removing"""
        if self._queue:
            return self._queue[0][-1]
        raise IndexError("peek from empty priority queue")
    
    def is_empty(self):
        """Check if queue is empty"""
        return len(self._queue) == 0
    
    def __len__(self):
        return len(self._queue)

def test_priority_queue():
    """Test priority queue"""
    print("--- Exercise 3: Priority Queue ---")
    
    pq = PriorityQueue()
    
    # Add tasks with priorities
    pq.push("Write docs", priority=3)
    pq.push("Fix critical bug", priority=1)
    pq.push("Code review", priority=2)
    pq.push("Update tests", priority=3)
    
    print("Processing tasks by priority:")
    while not pq.is_empty():
        task = pq.pop()
        print(f"  {task}")
    
    print()

# ============================================================
# EXERCISE 4: Merge K Sorted Lists
# ============================================================

def merge_k_sorted():
    """
    Merge k sorted lists efficiently using heap.
    
    TODO: Use heap for efficient merging
    """
    print("--- Exercise 4: Merge K Sorted Lists ---")
    
    def merge_k_lists(lists):
        """Merge k sorted lists into one sorted list"""
        heap = []
        result = []
        
        # Initialize heap with first element from each list
        for i, lst in enumerate(lists):
            if lst:
                heapq.heappush(heap, (lst[0], i, 0))
        
        # Extract min and add next element from same list
        while heap:
            val, list_idx, elem_idx = heapq.heappop(heap)
            result.append(val)
            
            # Add next element from same list
            if elem_idx + 1 < len(lists[list_idx]):
                next_val = lists[list_idx][elem_idx + 1]
                heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))
        
        return result
    
    lists = [
        [1, 4, 7],
        [2, 5, 8],
        [3, 6, 9]
    ]
    
    print("Input lists:")
    for i, lst in enumerate(lists):
        print(f"  List {i+1}: {lst}")
    
    merged = merge_k_lists(lists)
    print(f"\nMerged: {merged}")
    
    print()

# ============================================================
# EXERCISE 5: Running Median
# ============================================================

class RunningMedian:
    """
    Calculate running median using two heaps.
    
    TODO: Use max-heap and min-heap
    """
    
    def __init__(self):
        self.small = []  # Max-heap (negated values)
        self.large = []  # Min-heap
    
    def add(self, num):
        """Add number and maintain median"""
        # Add to max-heap (small)
        heapq.heappush(self.small, -num)
        
        # Balance: move largest from small to large
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        
        # Balance sizes
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        elif len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)
    
    def get_median(self):
        """Get current median"""
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2

def test_running_median():
    """Test running median"""
    print("--- Exercise 5: Running Median ---")
    
    rm = RunningMedian()
    numbers = [5, 15, 1, 3, 8]
    
    print("Adding numbers and tracking median:")
    for num in numbers:
        rm.add(num)
        print(f"  Added {num}, median: {rm.get_median()}")
    
    print()

# ============================================================
# EXERCISE 6: Real-World Scenario - Task Scheduler
# ============================================================

class TaskScheduler:
    """
    Schedule tasks by deadline using heap.
    
    TODO: Implement deadline-based scheduling
    """
    
    def __init__(self):
        self.tasks = []
    
    def add_task(self, name, deadline, duration):
        """Add task with deadline"""
        heapq.heappush(self.tasks, (deadline, duration, name))
    
    def get_next_task(self):
        """Get task with earliest deadline"""
        if self.tasks:
            deadline, duration, name = heapq.heappop(self.tasks)
            return {'name': name, 'deadline': deadline, 'duration': duration}
        return None
    
    def peek_next(self):
        """See next task without removing"""
        if self.tasks:
            deadline, duration, name = self.tasks[0]
            return {'name': name, 'deadline': deadline, 'duration': duration}
        return None

def test_task_scheduler():
    """Test task scheduler"""
    print("--- Exercise 6: Task Scheduler ---")
    
    scheduler = TaskScheduler()
    
    # Add tasks with deadlines (hours from now)
    scheduler.add_task("Write report", deadline=8, duration=2)
    scheduler.add_task("Team meeting", deadline=2, duration=1)
    scheduler.add_task("Code review", deadline=4, duration=1)
    scheduler.add_task("Deploy app", deadline=6, duration=3)
    
    print("Tasks scheduled by deadline:")
    while True:
        task = scheduler.get_next_task()
        if not task:
            break
        print(f"  {task['name']}: deadline in {task['deadline']}h, duration {task['duration']}h")
    
    print()

# ============================================================
# EXERCISE 7: K Closest Points
# ============================================================

def k_closest_points():
    """
    Find k closest points to origin.
    
    TODO: Use heap for efficient solution
    """
    print("--- Exercise 7: K Closest Points ---")
    
    def distance(point):
        """Calculate distance from origin"""
        return point[0]**2 + point[1]**2
    
    def k_closest(points, k):
        """Find k closest points to origin"""
        # Use max-heap of size k
        heap = []
        
        for point in points:
            dist = distance(point)
            if len(heap) < k:
                heapq.heappush(heap, (-dist, point))
            elif dist < -heap[0][0]:
                heapq.heapreplace(heap, (-dist, point))
        
        return [point for _, point in heap]
    
    points = [(1, 3), (2, 2), (3, 4), (1, 1), (5, 1)]
    k = 3
    
    print(f"Points: {points}")
    closest = k_closest(points, k)
    print(f"{k} closest to origin: {closest}")
    
    # Show distances
    print("\nDistances:")
    for point in closest:
        dist = distance(point)**0.5
        print(f"  {point}: {dist:.2f}")
    
    print()

# ============================================================
# BONUS CHALLENGE: Sliding Window Maximum
# ============================================================

def sliding_window_maximum():
    """
    Find maximum in each sliding window.
    
    TODO: Use heap for sliding window
    """
    print("--- Bonus Challenge: Sliding Window Maximum ---")
    
    def max_sliding_window(nums, k):
        """Find max in each window of size k"""
        if not nums or k == 0:
            return []
        
        result = []
        heap = []
        
        for i, num in enumerate(nums):
            # Add current element
            heapq.heappush(heap, (-num, i))
            
            # Remove elements outside window
            while heap and heap[0][1] <= i - k:
                heapq.heappop(heap)
            
            # Add to result when window is full
            if i >= k - 1:
                result.append(-heap[0][0])
        
        return result
    
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    
    result = max_sliding_window(nums, k)
    print(f"Array: {nums}")
    print(f"Window size: {k}")
    print(f"Maximums: {result}")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    Heap Operations:
    - heappush: O(log n)
    - heappop: O(log n)
    - heapify: O(n)
    - peek (heap[0]): O(1)
    
    Top K Problems:
    - nlargest/nsmallest: O(n log k)
    - Better than sorting: O(n log n)
    
    Priority Queue:
    - push: O(log n)
    - pop: O(log n)
    - peek: O(1)
    
    Space Complexity:
    - Heap: O(n)
    - Priority queue: O(n)
    
    Benefits:
    - Efficient for top-k problems
    - O(1) access to min/max
    - Better than sorting for partial ordering
    
    Use Cases:
    - Priority queues
    - Top k elements
    - Merge k sorted lists
    - Running median
    - Task scheduling
    - Dijkstra's algorithm
    
    Min-Heap vs Max-Heap:
    - Python heapq: min-heap only
    - Max-heap: negate values
    
    Best Practices:
    - Use nlargest/nsmallest for top-k
    - Maintain heap invariant
    - Consider heap for partial sorting
    - Use for streaming data
    
    Common Patterns:
    - Top k: heap of size k
    - Running median: two heaps
    - Merge k lists: heap with indices
    - Sliding window: heap with cleanup
    
    Security Considerations:
    - Validate input sizes
    - Consider memory limits
    - Handle edge cases (empty, single element)
    - Prevent heap exhaustion
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 6, Day 3: heapq and Priority Queues")
    print("=" * 60)
    print()
    
    heapq_basics()
    top_k_elements()
    test_priority_queue()
    merge_k_sorted()
    test_running_median()
    test_task_scheduler()
    k_closest_points()
    sliding_window_maximum()
    
    print("=" * 60)
    print("✅ Day 3 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. heapq provides min-heap operations")
    print("2. Efficient for top-k problems: O(n log k)")
    print("3. Priority queues for task scheduling")
    print("4. Two heaps for running median")

