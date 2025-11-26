# Design Problems - Complete Guide

## 📋 Pattern Recognition

**When to use Design Patterns:**
- "Design a...", "Implement a..."
- Multiple operations with specific time requirements
- "Data structure that supports..."
- Caching, rate limiting, scheduling

**Common Keywords:**
- Design, implement, data structure
- O(1) operations required
- Cache, queue, stack with special properties
- Real-time, stream, online algorithm

---

## 🎯 Key Design Principles

### 1. Identify Required Operations
- What operations are needed?
- What are the time/space constraints?
- What's the usage pattern (reads vs writes)?

### 2. Choose Data Structures
- Hash Map: O(1) lookup
- Doubly Linked List: O(1) insert/delete
- Heap: O(log n) min/max
- Tree: O(log n) ordered operations
- Array: O(1) random access

### 3. Trade-offs
- Time vs Space
- Simplicity vs Performance
- Memory overhead vs Speed

---

## 🔧 Pattern 1: LRU Cache 🚨 MOST IMPORTANT

### Problem: LRU Cache
```python
class ListNode:
    """
    Node for doubly linked list
    """
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None


class LRUCache:
    """
    LeetCode #146 - THE classic design problem
    
    Requirements:
    - get(key): O(1)
    - put(key, value): O(1)
    - Evict least recently used when full
    
    Solution: HashMap + Doubly Linked List
    - HashMap: O(1) access to nodes
    - DLL: O(1) move to front, O(1) remove from back
    
    Space: O(capacity)
    """
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key -> ListNode
        
        # Dummy head and tail for easy insertion/deletion
        self.head = ListNode()
        self.tail = ListNode()
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _remove(self, node: ListNode) -> None:
        """
        Remove node from its current position in DLL
        """
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node
    
    def _add_to_front(self, node: ListNode) -> None:
        """
        Add node right after head (most recently used position)
        """
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
    
    def get(self, key: int) -> int:
        """
        Get value and mark as recently used
        Time: O(1)
        """
        if key not in self.cache:
            return -1
        
        node = self.cache[key]
        
        # Move to front (most recently used)
        self._remove(node)
        self._add_to_front(node)
        
        return node.val
    
    def put(self, key: int, value: int) -> None:
        """
        Put key-value pair, evict LRU if needed
        Time: O(1)
        """
        if key in self.cache:
            # Update existing
            node = self.cache[key]
            node.val = value
            self._remove(node)
            self._add_to_front(node)
        else:
            # Add new
            if len(self.cache) >= self.capacity:
                # Evict LRU (node before tail)
                lru = self.tail.prev
                self._remove(lru)
                del self.cache[lru.key]
            
            # Add new node
            new_node = ListNode(key, value)
            self.cache[key] = new_node
            self._add_to_front(new_node)


# Example usage
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
print(cache.get(1))     # 1
cache.put(3, 3)         # Evicts key 2
print(cache.get(2))     # -1 (not found)
```

**Key Insights:**
- DLL maintains order (head = most recent, tail = least recent)
- HashMap provides O(1) access to nodes
- Dummy nodes simplify edge cases

---

## 🔧 Pattern 2: Two Heaps (Median Finding)

### Problem: Find Median from Data Stream
```python
import heapq

class MedianFinder:
    """
    LeetCode #295 - Find median in stream of numbers
    
    Strategy: Two heaps
    - max_heap: stores smaller half (negated for max behavior)
    - min_heap: stores larger half
    - Keep balanced so median is at heap tops
    
    Time: O(log n) add, O(1) find median
    Space: O(n)
    """
    def __init__(self):
        # Max heap for smaller half (use negative values)
        self.max_heap = []  # stores -num for max heap
        # Min heap for larger half
        self.min_heap = []
    
    def addNum(self, num: int) -> None:
        """
        Add number while maintaining:
        1. max_heap has <= min_heap + 1 elements
        2. max(max_heap) <= min(min_heap)
        """
        # Add to max_heap first (smaller half)
        heapq.heappush(self.max_heap, -num)
        
        # Balance: move largest from max_heap to min_heap
        heapq.heappush(self.min_heap, -heapq.heappop(self.max_heap))
        
        # If min_heap has more elements, rebalance
        if len(self.min_heap) > len(self.max_heap):
            heapq.heappush(self.max_heap, -heapq.heappop(self.min_heap))
    
    def findMedian(self) -> float:
        """
        Return median in O(1)
        """
        if len(self.max_heap) > len(self.min_heap):
            return -self.max_heap[0]
        else:
            return (-self.max_heap[0] + self.min_heap[0]) / 2


# Example
mf = MedianFinder()
mf.addNum(1)
mf.addNum(2)
print(mf.findMedian())  # 1.5
mf.addNum(3)
print(mf.findMedian())  # 2.0
```

**Key Insight:** Two heaps balanced to always have median at tops!

---

## 🔧 Pattern 3: Insert Delete GetRandom O(1)

### Problem: RandomizedSet
```python
import random

class RandomizedSet:
    """
    LeetCode #380 - All operations in O(1)
    
    Requirements:
    - insert(val): O(1)
    - remove(val): O(1)
    - getRandom(): O(1) and uniform distribution
    
    Solution: HashMap + Dynamic Array
    - Array: for O(1) random access
    - HashMap: val -> index for O(1) lookup/delete
    
    Space: O(n)
    """
    def __init__(self):
        self.val_to_index = {}  # val -> index in array
        self.vals = []          # array of values
    
    def insert(self, val: int) -> bool:
        """
        Insert val if not present
        Time: O(1)
        """
        if val in self.val_to_index:
            return False
        
        # Add to end of array
        self.vals.append(val)
        self.val_to_index[val] = len(self.vals) - 1
        return True
    
    def remove(self, val: int) -> bool:
        """
        Remove val if present
        Trick: Swap with last element, then pop
        Time: O(1)
        """
        if val not in self.val_to_index:
            return False
        
        # Get index of val
        idx = self.val_to_index[val]
        last_val = self.vals[-1]
        
        # Move last element to idx
        self.vals[idx] = last_val
        self.val_to_index[last_val] = idx
        
        # Remove last element
        self.vals.pop()
        del self.val_to_index[val]
        
        return True
    
    def getRandom(self) -> int:
        """
        Return random element
        Time: O(1)
        """
        return random.choice(self.vals)
```

**Key Insight:** Swap with last element before deletion maintains O(1)!

---

## 🔧 Pattern 4: Min Stack

### Problem: Min Stack
```python
class MinStack:
    """
    LeetCode #155 - Stack with O(1) min operation
    
    Strategy: Two stacks
    - main_stack: regular stack
    - min_stack: tracks minimum at each level
    
    Space: O(n)
    """
    def __init__(self):
        self.stack = []
        self.min_stack = []
    
    def push(self, val: int) -> None:
        """Time: O(1)"""
        self.stack.append(val)
        
        # Push current min to min_stack
        if not self.min_stack:
            self.min_stack.append(val)
        else:
            self.min_stack.append(min(val, self.min_stack[-1]))
    
    def pop(self) -> None:
        """Time: O(1)"""
        self.stack.pop()
        self.min_stack.pop()
    
    def top(self) -> int:
        """Time: O(1)"""
        return self.stack[-1]
    
    def getMin(self) -> int:
        """Time: O(1)"""
        return self.min_stack[-1]
```

**Alternative:** Store (val, min) pairs in single stack

---

## 🔧 Pattern 5: Time-Based Key-Value Store

### Problem: TimeMap
```python
import bisect

class TimeMap:
    """
    LeetCode #981 - Store values with timestamps
    
    set(key, value, timestamp): store key-value at timestamp
    get(key, timestamp): get value at or before timestamp
    
    Strategy: HashMap of key -> list of (timestamp, value) pairs
    - Timestamps are strictly increasing
    - Use binary search for get
    
    Time: set O(1), get O(log n)
    Space: O(n)
    """
    def __init__(self):
        self.store = {}  # key -> [(timestamp, value), ...]
    
    def set(self, key: str, value: str, timestamp: int) -> None:
        """Time: O(1)"""
        if key not in self.store:
            self.store[key] = []
        self.store[key].append((timestamp, value))
    
    def get(self, key: str, timestamp: int) -> str:
        """
        Binary search for largest timestamp <= given timestamp
        Time: O(log n)
        """
        if key not in self.store:
            return ""
        
        pairs = self.store[key]
        
        # Binary search for timestamp
        left, right = 0, len(pairs) - 1
        result = ""
        
        while left <= right:
            mid = (left + right) // 2
            if pairs[mid][0] <= timestamp:
                result = pairs[mid][1]
                left = mid + 1
            else:
                right = mid - 1
        
        return result
```

---

## 🔧 Pattern 6: Design Hit Counter

### Problem: Hit Counter (Premium #362)
```python
from collections import deque

class HitCounter:
    """
    Count hits in last 5 minutes (300 seconds)
    
    Strategy: Queue with timestamps
    - Remove hits older than 300 seconds
    
    Time: O(1) amortized, Space: O(n)
    """
    def __init__(self):
        self.hits = deque()  # (timestamp, count)
    
    def hit(self, timestamp: int) -> None:
        """Record a hit at timestamp"""
        if self.hits and self.hits[-1][0] == timestamp:
            # Increment count for same timestamp
            self.hits[-1] = (timestamp, self.hits[-1][1] + 1)
        else:
            self.hits.append((timestamp, 1))
    
    def getHits(self, timestamp: int) -> int:
        """
        Get total hits in last 300 seconds
        """
        # Remove old hits
        while self.hits and self.hits[0][0] <= timestamp - 300:
            self.hits.popleft()
        
        # Count remaining hits
        return sum(count for _, count in self.hits)
```

**Optimization:** Use circular array of size 300 for O(1) space

---

## 🔧 Pattern 7: LFU Cache (Harder)

### Problem: LFU Cache
```python
class LFUCache:
    """
    LeetCode #460 - Least Frequently Used cache
    
    Eviction: Remove least frequently used
    Tie-break: Remove least recently used
    
    Requirements: All operations O(1)
    
    Strategy:
    - freq_to_keys: frequency -> DLL of keys
    - key_to_val: key -> value
    - key_to_freq: key -> frequency
    - min_freq: track minimum frequency
    
    Space: O(capacity)
    """
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.min_freq = 0
        self.key_to_val = {}
        self.key_to_freq = {}
        self.freq_to_keys = {}  # freq -> OrderedDict of keys
    
    def _update_freq(self, key: int) -> None:
        """Increase frequency of key"""
        freq = self.key_to_freq[key]
        
        # Remove from old frequency list
        self.freq_to_keys[freq].pop(key)
        
        # If old frequency list empty and was min_freq, increment min_freq
        if not self.freq_to_keys[freq] and freq == self.min_freq:
            self.min_freq += 1
        
        # Add to new frequency list
        new_freq = freq + 1
        self.key_to_freq[key] = new_freq
        if new_freq not in self.freq_to_keys:
            self.freq_to_keys[new_freq] = {}
        self.freq_to_keys[new_freq][key] = None
    
    def get(self, key: int) -> int:
        """Time: O(1)"""
        if key not in self.key_to_val:
            return -1
        
        self._update_freq(key)
        return self.key_to_val[key]
    
    def put(self, key: int, value: int) -> None:
        """Time: O(1)"""
        if self.capacity <= 0:
            return
        
        if key in self.key_to_val:
            # Update existing
            self.key_to_val[key] = value
            self._update_freq(key)
        else:
            # Add new
            if len(self.key_to_val) >= self.capacity:
                # Evict LFU (first key in min_freq list)
                evict_key = next(iter(self.freq_to_keys[self.min_freq]))
                self.freq_to_keys[self.min_freq].pop(evict_key)
                del self.key_to_val[evict_key]
                del self.key_to_freq[evict_key]
            
            # Insert new key
            self.key_to_val[key] = value
            self.key_to_freq[key] = 1
            self.min_freq = 1
            if 1 not in self.freq_to_keys:
                self.freq_to_keys[1] = {}
            self.freq_to_keys[1][key] = None
```

---

## 💡 Common Design Patterns

### Pattern Matrix

| Pattern | Data Structures | Time | Use Case |
|---------|----------------|------|----------|
| LRU Cache | HashMap + DLL | O(1) | Caching |
| Two Heaps | 2 Heaps | O(log n) insert | Median, scheduling |
| RandomSet | HashMap + Array | O(1) | Random access + insert/delete |
| Min Stack | 2 Stacks | O(1) | Stack with min |
| Trie | Tree | O(m) | Prefix matching |
| Segment Tree | Tree | O(log n) | Range queries |

---

## 🎓 Practice Problems

### Easy
1. #155 Min Stack
2. #232 Implement Queue using Stacks
3. #225 Implement Stack using Queues

### Medium
1. **#146 LRU Cache** 🚨 **MUST DO**
2. **#380 Insert Delete GetRandom O(1)** 🚨
3. **#981 Time Based Key-Value Store**
4. **#208 Implement Trie**
5. #284 Peeking Iterator
6. #341 Flatten Nested List Iterator
7. #1472 Design Browser History

### Hard
1. **#295 Find Median from Data Stream** 🚨 **MUST DO**
2. **#460 LFU Cache**
3. #432 All O(1) Data Structure
4. #1172 Dinner Plate Stacks

---

## 🐛 Common Mistakes

### Mistake 1: Not Using Dummy Nodes in DLL
```python
# ❌ Complex edge case handling
if self.head is None:
    self.head = node
else:
    # Complex linking...

# ✅ Dummy nodes simplify
self.head = ListNode()  # Dummy
self.tail = ListNode()  # Dummy
self.head.next = self.tail
```

### Mistake 2: Forgetting to Update HashMap
```python
# In LRU Cache, must update BOTH structures:
self._remove(node)          # Update DLL
self._add_to_front(node)    # Update DLL
# HashMap already has correct reference (no update needed)
```

### Mistake 3: Wrong Min/Max Heap in Python
```python
# ❌ WRONG - Python only has min heap
max_heap = []
heapq.heappush(max_heap, val)  # This is MIN heap!

# ✅ CORRECT - Negate for max heap
max_heap = []
heapq.heappush(max_heap, -val)  # Negate!
value = -heapq.heappop(max_heap)  # Negate back
```

---

## 💡 Pro Tips

### Tip 1: Start with Requirements
```
1. List all operations needed
2. Identify time/space constraints
3. Choose data structures for each operation
4. Find data structure that satisfies all
```

### Tip 2: Common Combinations
- **O(1) access + O(1) delete:** HashMap + DLL
- **O(1) access + O(1) random:** HashMap + Array
- **Min/max + O(log n):** Heap
- **Range queries:** Segment Tree, Fenwick Tree
- **Prefix matching:** Trie

### Tip 3: Draw It!
Always draw the data structure state after each operation

### Tip 4: Edge Cases
```python
# Always test:
1. Empty structure
2. Single element
3. At capacity
4. Duplicate operations
5. Operations on non-existent keys
```

---

**Remember:** Design problems test your ability to combine multiple data structures cleverly. Master LRU Cache (HashMap + DLL) and Two Heaps - they're interview favorites!

