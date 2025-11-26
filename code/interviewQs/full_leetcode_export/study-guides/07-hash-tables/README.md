# Hash Tables - Complete Guide

## 📋 Pattern Recognition

**When to use Hash Tables:**
- Need O(1) lookup, insert, delete
- "Find pair/triplet with sum = target"
- Count frequencies
- Track seen elements
- Group/categorize elements

**Keywords:** frequency, count, unique, duplicate, group, anagram

---

## 🎯 Hash Table Basics

```python
# Dictionary (Hash Map)
freq = {}
freq['a'] = freq.get('a', 0) + 1

# Or use defaultdict
from collections import defaultdict
freq = defaultdict(int)
freq['a'] += 1  # Auto-initializes to 0

# Set (for existence checks)
seen = set()
if x in seen:  # O(1) lookup
    pass
seen.add(x)
```

---

## 🔧 Pattern 1: Two Sum Pattern

```python
def twoSum(nums: list[int], target: int) -> list[int]:
    """
    LeetCode #1 - Most asked interview question!
    
    Time: O(n), Space: O(n)
    """
    seen = {}  # value -> index
    
    for i, num in enumerate(nums):
        complement = target - num
        
        if complement in seen:
            return [seen[complement], i]
        
        seen[num] = i
    
    return []
```

### Two Sum Variations
```python
# Count pairs with sum = k
def countPairs(nums: list[int], k: int) -> int:
    """
    Time: O(n), Space: O(n)
    """
    from collections import Counter
    freq = Counter(nums)
    count = 0
    
    for num in freq:
        complement = k - num
        if complement in freq:
            if num == complement:
                # Same number - choose 2
                count += freq[num] * (freq[num] - 1) // 2
            elif num < complement:  # Avoid double counting
                count += freq[num] * freq[complement]
    
    return count
```

---

## 🔧 Pattern 2: Frequency Counting

```python
def topKFrequent(nums: list[int], k: int) -> list[int]:
    """
    LeetCode #347
    Find k most frequent elements
    
    Time: O(n), Space: O(n)
    """
    from collections import Counter
    
    # Count frequencies
    freq = Counter(nums)
    
    # Bucket sort by frequency
    buckets = [[] for _ in range(len(nums) + 1)]
    
    for num, count in freq.items():
        buckets[count].append(num)
    
    # Collect k most frequent
    result = []
    for i in range(len(buckets) - 1, -1, -1):
        for num in buckets[i]:
            result.append(num)
            if len(result) == k:
                return result
    
    return result
```

### First Unique Character
```python
def firstUniqChar(s: str) -> int:
    """
    LeetCode #387
    Time: O(n), Space: O(1) - only 26 letters
    """
    from collections import Counter
    freq = Counter(s)
    
    for i, char in enumerate(s):
        if freq[char] == 1:
            return i
    
    return -1
```

---

## 🔧 Pattern 3: Group Anagrams

```python
def groupAnagrams(strs: list[str]) -> list[list[str]]:
    """
    LeetCode #49 🚨 INTERVIEW FAVORITE
    Group strings that are anagrams
    
    Time: O(n*k) where k = max length
    Space: O(n*k)
    """
    from collections import defaultdict
    
    groups = defaultdict(list)
    
    for s in strs:
        # Use sorted string as key
        # Alternative: use character count as key
        key = ''.join(sorted(s))
        groups[key].append(s)
    
    return list(groups.values())
```

### Character Count Key (More efficient)
```python
def groupAnagrams_optimized(strs: list[str]) -> list[list[str]]:
    """
    Use character frequency as key
    Time: O(n*k), Space: O(n*k)
    """
    from collections import defaultdict
    
    groups = defaultdict(list)
    
    for s in strs:
        # Count chars: [1,0,0,1,0,...] for "aad"
        count = [0] * 26
        for char in s:
            count[ord(char) - ord('a')] += 1
        
        # Tuple is hashable (list is not)
        key = tuple(count)
        groups[key].append(s)
    
    return list(groups.values())
```

---

## 🔧 Pattern 4: Subarray Sum with Hash Map

```python
def subarraySum(nums: list[int], k: int) -> int:
    """
    LeetCode #560
    Count subarrays with sum = k
    
    Key insight: prefix_sum[j] - prefix_sum[i] = k
    → prefix_sum[i] = prefix_sum[j] - k
    
    Time: O(n), Space: O(n)
    """
    from collections import defaultdict
    
    count = 0
    prefix_sum = 0
    sum_count = defaultdict(int)
    sum_count[0] = 1  # Empty subarray has sum 0
    
    for num in nums:
        prefix_sum += num
        
        # How many times have we seen (prefix_sum - k)?
        count += sum_count[prefix_sum - k]
        
        # Record current prefix sum
        sum_count[prefix_sum] += 1
    
    return count

# Example: nums = [1,1,1], k = 2
# i=0: prefix=1, count=0, sum_count={0:1, 1:1}
# i=1: prefix=2, count=1 (found 2-2=0), sum_count={0:1, 1:1, 2:1}
# i=2: prefix=3, count=2 (found 3-2=1), sum_count={0:1, 1:1, 2:1, 3:1}
```

### Longest Subarray with Sum K
```python
def maxSubArrayLen(nums: list[int], k: int) -> int:
    """
    LeetCode #325 (Premium)
    Longest subarray with sum = k
    
    Time: O(n), Space: O(n)
    """
    prefix_sum = 0
    sum_index = {0: -1}  # prefix_sum -> first index
    max_len = 0
    
    for i, num in enumerate(nums):
        prefix_sum += num
        
        if prefix_sum - k in sum_index:
            max_len = max(max_len, i - sum_index[prefix_sum - k])
        
        # Only store first occurrence
        if prefix_sum not in sum_index:
            sum_index[prefix_sum] = i
    
    return max_len
```

---

## 🔧 Pattern 5: Isomorphic Strings

```python
def isIsomorphic(s: str, t: str) -> bool:
    """
    LeetCode #205
    "egg" and "add" → True (e→a, g→d)
    "foo" and "bar" → False (o maps to both a and r)
    
    Time: O(n), Space: O(1) - at most 256 ASCII chars
    """
    if len(s) != len(t):
        return False
    
    s_to_t = {}
    t_to_s = {}
    
    for c1, c2 in zip(s, t):
        # Check s -> t mapping
        if c1 in s_to_t:
            if s_to_t[c1] != c2:
                return False
        else:
            s_to_t[c1] = c2
        
        # Check t -> s mapping
        if c2 in t_to_s:
            if t_to_s[c2] != c1:
                return False
        else:
            t_to_s[c2] = c1
    
    return True
```

---

## 🔧 Pattern 6: Longest Consecutive Sequence

```python
def longestConsecutive(nums: list[int]) -> int:
    """
    LeetCode #128
    [100,4,200,1,3,2] → 4 (sequence: [1,2,3,4])
    
    Key insight: Use set for O(1) lookup
    Only start counting from sequence start (no num-1 in set)
    
    Time: O(n), Space: O(n)
    """
    num_set = set(nums)
    max_length = 0
    
    for num in num_set:
        # Only start from beginning of sequence
        if num - 1 not in num_set:
            current = num
            length = 1
            
            # Count consecutive numbers
            while current + 1 in num_set:
                current += 1
                length += 1
            
            max_length = max(max_length, length)
    
    return max_length
```

---

## 🔧 Pattern 7: LRU Cache with OrderedDict

```python
from collections import OrderedDict

class LRUCache:
    """
    LeetCode #146 🚨 MOST ASKED DESIGN PROBLEM
    
    Operations: O(1)
    Space: O(capacity)
    """
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity
    
    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        
        # Move to end (mark as recently used)
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # Update and move to end
            self.cache.move_to_end(key)
        
        self.cache[key] = value
        
        if len(self.cache) > self.capacity:
            # Remove least recently used (first item)
            self.cache.popitem(last=False)
```

---

## 🎓 Key Problems by Pattern

**Two Sum Family:**
- #1 Two Sum 🚨
- #167 Two Sum II
- #170 Two Sum III (Premium)
- #653 Two Sum IV - BST

**Frequency:**
- #347 Top K Frequent Elements
- #387 First Unique Character
- #383 Ransom Note

**Grouping:**
- #49 Group Anagrams 🚨
- #249 Group Shifted Strings (Premium)

**Subarray Sum:**
- #560 Subarray Sum Equals K
- #523 Continuous Subarray Sum
- #325 Maximum Size Subarray Sum Equals k (Premium)

**Consecutive:**
- #128 Longest Consecutive Sequence
- #298 Binary Tree Longest Consecutive Sequence (Premium)

**Design:**
- #146 LRU Cache 🚨
- #380 Insert Delete GetRandom O(1)

---

## 🚨 Common Mistakes

1. **Using list for membership check:**
   ```python
   # WRONG - O(n)
   if x in my_list:
   
   # CORRECT - O(1)
   if x in my_set:
   ```

2. **Modifying dict while iterating:**
   ```python
   # WRONG
   for key in dict:
       del dict[key]
   
   # CORRECT
   keys_to_delete = list(dict.keys())
   for key in keys_to_delete:
       del dict[key]
   ```

3. **Forgetting default value:**
   ```python
   # WRONG - KeyError if not exists
   count[key] += 1
   
   # CORRECT
   count[key] = count.get(key, 0) + 1
   # Or use defaultdict
   ```

---

## 💡 Pro Tips

**When to use what:**
- `dict` - Count, map, cache
- `set` - Existence, uniqueness, duplicates
- `Counter` - Frequency counting (from collections)
- `defaultdict` - Auto-initialize values
- `OrderedDict` - Maintain insertion order + efficient reordering

**Space-time tradeoff:**
- Hash table: O(n) space for O(1) operations
- Without hash: O(1) space but O(n) or O(n²) time

**Collision handling:**
- Python's dict uses open addressing
- Worst case: O(n) but amortized O(1)

---

**Hash tables are your interview best friend - master them!**

