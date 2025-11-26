# Heaps & Priority Queues - Complete Guide

## 📋 Pattern Recognition

**When to use Heaps:**
- Find "top K" elements
- "Kth largest/smallest"
- Merge sorted lists/arrays
- Median maintenance in stream
- Scheduling tasks

**Keywords:** kth, largest, smallest, top k, merge, median, priority

---

## 🎯 Heap Basics

### What is a Heap?
- Complete binary tree
- **Min Heap:** Parent ≤ children
- **Max Heap:** Parent ≥ children
- Operations: O(log n) insert/delete, O(1) peek

### Python heapq (Min Heap Only!)
```python
import heapq

# Create heap
heap = []
heapq.heappush(heap, 5)
heapq.heappush(heap, 1)
heapq.heappush(heap, 3)

# Or heapify existing list
nums = [5, 1, 3, 7, 2]
heapq.heapify(nums)  # O(n)

# Pop minimum
min_val = heapq.heappop(heap)  # O(log n)

# Peek minimum
min_val = heap[0]  # O(1)

# For MAX HEAP: negate values!
max_heap = []
heapq.heappush(max_heap, -5)
max_val = -heapq.heappop(max_heap)
```

---

## 🔧 Pattern 1: Top K Elements

### Problem 1: Kth Largest Element
```python
def findKthLargest(nums: list[int], k: int) -> int:
    """
    LeetCode #215
    
    Method 1: Min heap of size k
    Time: O(n log k), Space: O(k)
    """
    import heapq
    
    # Maintain min heap of k largest elements
    heap = []
    
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)  # Remove smallest
    
    return heap[0]  # Kth largest


def findKthLargest_quickselect(nums: list[int], k: int) -> int:
    """
    Method 2: Quickselect (better average case)
    Time: O(n) average, O(n²) worst, Space: O(1)
    """
    k = len(nums) - k  # Convert to 0-indexed from end
    
    def quickselect(left, right):
        pivot = nums[right]
        p = left
        
        for i in range(left, right):
            if nums[i] <= pivot:
                nums[p], nums[i] = nums[i], nums[p]
                p += 1
        
        nums[p], nums[right] = nums[right], nums[p]
        
        if p < k:
            return quickselect(p + 1, right)
        elif p > k:
            return quickselect(left, p - 1)
        else:
            return nums[p]
    
    return quickselect(0, len(nums) - 1)
```

### Problem 2: Top K Frequent Elements
```python
def topKFrequent(nums: list[int], k: int) -> list[int]:
    """
    LeetCode #347
    
    Time: O(n log k), Space: O(n)
    """
    from collections import Counter
    import heapq
    
    count = Counter(nums)
    
    # Min heap of (frequency, num) pairs
    return heapq.nlargest(k, count.keys(), key=count.get)
```

---

## 🔧 Pattern 2: Two Heaps (Median Maintenance) 🚨 CRITICAL

### Problem 3: Find Median from Data Stream
```python
import heapq

class MedianFinder:
    """
    LeetCode #295 - THE two heaps pattern
    
    Strategy:
    - max_heap: smaller half (negated)
    - min_heap: larger half
    - Balance: |max_heap| = |min_heap| or |max_heap| = |min_heap| + 1
    
    Time: O(log n) add, O(1) median
    """
    def __init__(self):
        self.max_heap = []  # smaller half (negated)
        self.min_heap = []  # larger half
    
    def addNum(self, num: int) -> None:
        # Add to max_heap (smaller half)
        heapq.heappush(self.max_heap, -num)
        
        # Balance: largest of small half <= smallest of large half
        heapq.heappush(self.min_heap, -heapq.heappop(self.max_heap))
        
        # Balance sizes
        if len(self.min_heap) > len(self.max_heap):
            heapq.heappush(self.max_heap, -heapq.heappop(self.min_heap))
    
    def findMedian(self) -> float:
        if len(self.max_heap) > len(self.min_heap):
            return -self.max_heap[0]
        return (-self.max_heap[0] + self.min_heap[0]) / 2
```

**Visual:**
```
max_heap (smaller)  |  min_heap (larger)
    [1, 2, 3]       |      [5, 6, 7]
         ↑          |       ↑
      max(small)    |    min(large)
      
Median = (3 + 5) / 2 = 4
```

---

## 🔧 Pattern 3: K-Way Merge

### Problem 4: Merge K Sorted Lists
```python
import heapq

def mergeKLists(lists: list[ListNode]) -> ListNode:
    """
    LeetCode #23
    
    Strategy: Min heap with (value, list_index, node)
    
    Time: O(N log k) where N = total nodes, k = lists
    Space: O(k)
    """
    heap = []
    
    # Add first node from each list
    for i, head in enumerate(lists):
        if head:
            heapq.heappush(heap, (head.val, i, head))
    
    dummy = ListNode()
    current = dummy
    
    while heap:
        val, i, node = heapq.heappop(heap)
        current.next = node
        current = current.next
        
        # Add next node from same list
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    
    return dummy.next
```

### Problem 5: Kth Smallest in Sorted Matrix
```python
def kthSmallest(matrix: list[list[int]], k: int) -> int:
    """
    LeetCode #378
    
    Each row and column sorted
    
    Time: O(k log min(k, n)), Space: O(min(k, n))
    """
    n = len(matrix)
    heap = []
    
    # Add first element of each row
    for r in range(min(n, k)):
        heapq.heappush(heap, (matrix[r][0], r, 0))
    
    result = 0
    for _ in range(k):
        result, r, c = heapq.heappop(heap)
        
        # Add next element in same row
        if c + 1 < n:
            heapq.heappush(heap, (matrix[r][c + 1], r, c + 1))
    
    return result
```

---

## 🔧 Pattern 4: Scheduling & Intervals

### Problem 6: Meeting Rooms II
```python
def minMeetingRooms(intervals: list[list[int]]) -> int:
    """
    LeetCode #253 (Premium)
    
    Min rooms needed for all meetings
    
    Time: O(n log n), Space: O(n)
    """
    if not intervals:
        return 0
    
    # Sort by start time
    intervals.sort(key=lambda x: x[0])
    
    # Min heap of end times
    heap = []
    heapq.heappush(heap, intervals[0][1])
    
    for start, end in intervals[1:]:
        # If earliest ending meeting ends before this starts
        if heap[0] <= start:
            heapq.heappop(heap)
        
        heapq.heappush(heap, end)
    
    return len(heap)
```

### Problem 7: Task Scheduler
```python
def leastInterval(tasks: list[str], n: int) -> int:
    """
    LeetCode #621
    
    Tasks with cooldown period n
    
    Time: O(m) where m = total time, Space: O(1) - only 26 letters
    """
    from collections import Counter
    import heapq
    
    # Count frequencies
    freq = Counter(tasks)
    
    # Max heap of frequencies (negated)
    heap = [-f for f in freq.values()]
    heapq.heapify(heap)
    
    time = 0
    
    while heap:
        cycle = []
        
        # Process batch of n+1
        for _ in range(n + 1):
            if heap:
                freq = -heapq.heappop(heap)
                if freq > 1:
                    cycle.append(freq - 1)
        
        # Add back remaining tasks
        for f in cycle:
            heapq.heappush(heap, -f)
        
        # Add time for this cycle
        time += (n + 1) if heap else len(cycle)
    
    return time
```

---

## 🔧 Pattern 5: Find K Pairs

### Problem 8: Find K Pairs with Smallest Sums
```python
def kSmallestPairs(nums1: list[int], nums2: list[int], k: int) -> list[list[int]]:
    """
    LeetCode #373
    
    Time: O(k log k), Space: O(k)
    """
    if not nums1 or not nums2:
        return []
    
    heap = []
    
    # Add first k pairs (nums1[i], nums2[0])
    for i in range(min(k, len(nums1))):
        heapq.heappush(heap, (nums1[i] + nums2[0], i, 0))
    
    result = []
    
    while heap and len(result) < k:
        _, i, j = heapq.heappop(heap)
        result.append([nums1[i], nums2[j]])
        
        # Add next pair from nums2
        if j + 1 < len(nums2):
            heapq.heappush(heap, (nums1[i] + nums2[j + 1], i, j + 1))
    
    return result
```

---

## 🎓 Practice Problems

### Easy
1. #1046 Last Stone Weight
2. #703 Kth Largest in Stream

### Medium
1. **#215 Kth Largest Element** 🚨
2. **#347 Top K Frequent Elements** 🚨
3. **#23 Merge k Sorted Lists** 🚨
4. #378 Kth Smallest in Sorted Matrix
5. #373 Find K Pairs
6. #621 Task Scheduler
7. #253 Meeting Rooms II (Premium)

### Hard
1. **#295 Find Median from Data Stream** 🚨 **MUST DO**
2. #480 Sliding Window Median
3. #218 The Skyline Problem

---

## 🐛 Common Mistakes

### Mistake 1: Forgetting Python Has Min Heap Only
```python
# ❌ WRONG - This is min heap!
heap = [5, 3, 7]
heapq.heapify(heap)
print(heap[0])  # 3, not 7!

# ✅ CORRECT - Negate for max heap
heap = [-5, -3, -7]
heapq.heapify(heap)
print(-heap[0])  # 7
```

### Mistake 2: Wrong Heap Size for Kth Element
```python
# For Kth LARGEST: use min heap of size k
# For Kth SMALLEST: use max heap of size k
```

### Mistake 3: Not Handling Ties in Heap
```python
# When heap elements are complex objects
heapq.heappush(heap, (priority, unique_id, data))
#                                ↑ ensures no comparison of data
```

---

## 💡 Decision Tree

```
Need min/max from stream?
│
├─ Single min/max → Use single heap
│
├─ Kth largest/smallest → Use heap of size k
│
├─ Median → Two heaps (max + min)
│
└─ Merge sorted → K-way merge with heap
```

---

## 📊 Complexity Cheatsheet

| Operation | Time | Space |
|-----------|------|-------|
| Insert | O(log n) | - |
| Delete min/max | O(log n) | - |
| Peek min/max | O(1) | - |
| Heapify | O(n) | O(1) |
| K from N | O(n log k) | O(k) |
| Median (two heaps) | O(log n) insert | O(n) |

---

**Remember:** Heaps are for finding extremes efficiently! Master the two heaps pattern for median - it's a classic interview question!

