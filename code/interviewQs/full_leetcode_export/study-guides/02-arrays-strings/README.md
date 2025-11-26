# Arrays & Strings - Complete Guide

## 📋 Pattern Recognition

**When to use these techniques:**
- Manipulating array elements in-place
- String transformations
- Interval merging/overlapping
- Matrix operations
- Prefix sum for range queries

**Keywords:** in-place, rotate, merge, intervals, subarray, substring

---

## 🔧 Pattern 1: Two Pointers (In-Place)

### Reverse Array
```python
def reverse(nums: list[int]) -> None:
    """
    Reverse array in-place
    Time: O(n), Space: O(1)
    """
    left, right = 0, len(nums) - 1
    
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1
```

### Remove Duplicates
```python
def removeDuplicates(nums: list[int]) -> int:
    """
    LeetCode #26
    Remove duplicates from sorted array in-place
    
    Time: O(n), Space: O(1)
    """
    if not nums:
        return 0
    
    # Write pointer
    write = 1
    
    for read in range(1, len(nums)):
        if nums[read] != nums[read - 1]:
            nums[write] = nums[read]
            write += 1
    
    return write
```

### Move Zeros
```python
def moveZeroes(nums: list[int]) -> None:
    """
    LeetCode #283
    Move all zeros to end, maintain relative order
    
    Time: O(n), Space: O(1)
    """
    write = 0
    
    # Move all non-zeros to front
    for read in range(len(nums)):
        if nums[read] != 0:
            nums[write] = nums[read]
            write += 1
    
    # Fill rest with zeros
    for i in range(write, len(nums)):
        nums[i] = 0
```

---

## 🔧 Pattern 2: Array Rotation

```python
def rotate(nums: list[int], k: int) -> None:
    """
    LeetCode #189
    Rotate array to right by k steps
    [1,2,3,4,5,6,7] k=3 → [5,6,7,1,2,3,4]
    
    Time: O(n), Space: O(1)
    """
    n = len(nums)
    k = k % n  # Handle k > n
    
    # Reverse entire array
    reverse_range(nums, 0, n - 1)
    # Reverse first k elements
    reverse_range(nums, 0, k - 1)
    # Reverse remaining elements
    reverse_range(nums, k, n - 1)

def reverse_range(nums, start, end):
    while start < end:
        nums[start], nums[end] = nums[end], nums[start]
        start += 1
        end -= 1

# Example: [1,2,3,4,5,6,7], k=3
# Step 1: [7,6,5,4,3,2,1]
# Step 2: [5,6,7,4,3,2,1]
# Step 3: [5,6,7,1,2,3,4]
```

---

## 🔧 Pattern 3: Merge Intervals 🚨 CRITICAL

```python
def merge(intervals: list[list[int]]) -> list[list[int]]:
    """
    LeetCode #56
    Merge overlapping intervals
    [[1,3],[2,6],[8,10],[15,18]] → [[1,6],[8,10],[15,18]]
    
    Time: O(n log n), Space: O(n)
    """
    if not intervals:
        return []
    
    # Sort by start time
    intervals.sort(key=lambda x: x[0])
    
    merged = [intervals[0]]
    
    for current in intervals[1:]:
        last = merged[-1]
        
        if current[0] <= last[1]:
            # Overlapping - merge
            last[1] = max(last[1], current[1])
        else:
            # Non-overlapping - add new interval
            merged.append(current)
    
    return merged
```

### Insert Interval
```python
def insert(intervals: list[list[int]], newInterval: list[int]) -> list[list[int]]:
    """
    LeetCode #57
    Insert new interval and merge if necessary
    
    Time: O(n), Space: O(n)
    """
    result = []
    i = 0
    n = len(intervals)
    
    # Add all intervals before newInterval
    while i < n and intervals[i][1] < newInterval[0]:
        result.append(intervals[i])
        i += 1
    
    # Merge overlapping intervals
    while i < n and intervals[i][0] <= newInterval[1]:
        newInterval[0] = min(newInterval[0], intervals[i][0])
        newInterval[1] = max(newInterval[1], intervals[i][1])
        i += 1
    
    result.append(newInterval)
    
    # Add remaining intervals
    while i < n:
        result.append(intervals[i])
        i += 1
    
    return result
```

---

## 🔧 Pattern 4: Prefix Sum

```python
class NumArray:
    """
    LeetCode #303 - Range Sum Query Immutable
    
    Preprocess: O(n), Query: O(1), Space: O(n)
    """
    def __init__(self, nums: list[int]):
        # prefix[i] = sum of nums[0..i-1]
        self.prefix = [0]
        for num in nums:
            self.prefix.append(self.prefix[-1] + num)
    
    def sumRange(self, left: int, right: int) -> int:
        return self.prefix[right + 1] - self.prefix[left]

# Example: nums = [-2, 0, 3, -5, 2, -1]
# prefix = [0, -2, -2, 1, -4, -2, -3]
# sumRange(0, 2) = prefix[3] - prefix[0] = 1 - 0 = 1
# sumRange(2, 5) = prefix[6] - prefix[2] = -3 - (-2) = -1
```

### Subarray Sum Equals K
```python
def subarraySum(nums: list[int], k: int) -> int:
    """
    LeetCode #560
    Count subarrays with sum = k
    
    Time: O(n), Space: O(n)
    """
    from collections import defaultdict
    
    count = 0
    prefix_sum = 0
    sum_count = defaultdict(int)
    sum_count[0] = 1  # Empty subarray
    
    for num in nums:
        prefix_sum += num
        
        # Check if (prefix_sum - k) exists
        # If yes, found subarray with sum k
        count += sum_count[prefix_sum - k]
        
        sum_count[prefix_sum] += 1
    
    return count
```

---

## 🔧 Pattern 5: String Manipulation

### Reverse Words
```python
def reverseWords(s: str) -> str:
    """
    LeetCode #151
    "the sky is blue" → "blue is sky the"
    
    Time: O(n), Space: O(n)
    """
    # Split by whitespace, filter empty strings, reverse, join
    return ' '.join(s.split()[::-1])
```

### String Compression
```python
def compress(chars: list[str]) -> int:
    """
    LeetCode #443
    ["a","a","b","b","c","c","c"] → ["a","2","b","2","c","3"]
    
    Time: O(n), Space: O(1)
    """
    write = 0
    read = 0
    
    while read < len(chars):
        char = chars[read]
        count = 0
        
        # Count consecutive chars
        while read < len(chars) and chars[read] == char:
            read += 1
            count += 1
        
        # Write character
        chars[write] = char
        write += 1
        
        # Write count if > 1
        if count > 1:
            for digit in str(count):
                chars[write] = digit
                write += 1
    
    return write
```

---

## 🔧 Pattern 6: Matrix Operations

### Rotate Image 90°
```python
def rotate(matrix: list[list[int]]) -> None:
    """
    LeetCode #48
    Rotate n×n matrix 90° clockwise in-place
    
    Time: O(n²), Space: O(1)
    """
    n = len(matrix)
    
    # Step 1: Transpose (swap matrix[i][j] with matrix[j][i])
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    
    # Step 2: Reverse each row
    for row in matrix:
        row.reverse()

# Example:
# [1,2,3]    [7,4,1]    [7,4,1]
# [4,5,6] → [8,5,2] → [8,5,2]
# [7,8,9]    [9,6,3]    [9,6,3]
#  Original  Transpose  Reverse rows
```

### Spiral Matrix
```python
def spiralOrder(matrix: list[list[int]]) -> list[int]:
    """
    LeetCode #54
    Traverse matrix in spiral order
    
    Time: O(m*n), Space: O(1) (excluding output)
    """
    if not matrix:
        return []
    
    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    
    while top <= bottom and left <= right:
        # Traverse right
        for col in range(left, right + 1):
            result.append(matrix[top][col])
        top += 1
        
        # Traverse down
        for row in range(top, bottom + 1):
            result.append(matrix[row][right])
        right -= 1
        
        if top <= bottom:
            # Traverse left
            for col in range(right, left - 1, -1):
                result.append(matrix[bottom][col])
            bottom -= 1
        
        if left <= right:
            # Traverse up
            for row in range(bottom, top - 1, -1):
                result.append(matrix[row][left])
            left += 1
    
    return result
```

---

## 🎓 Key Problems by Pattern

**In-Place Manipulation:**
- #26 Remove Duplicates
- #27 Remove Element
- #283 Move Zeroes
- #189 Rotate Array

**Intervals:**
- #56 Merge Intervals 🚨
- #57 Insert Interval 🚨
- #435 Non-overlapping Intervals

**Prefix Sum:**
- #303 Range Sum Query
- #560 Subarray Sum Equals K
- #523 Continuous Subarray Sum

**String:**
- #151 Reverse Words
- #443 String Compression
- #5 Longest Palindromic Substring

**Matrix:**
- #48 Rotate Image
- #54 Spiral Matrix
- #73 Set Matrix Zeroes

---

## 🚨 Common Mistakes

1. **Modifying array while iterating:**
   ```python
   # WRONG
   for i in range(len(nums)):
       nums.pop(i)  # Indices shift!
   
   # CORRECT - use two pointers
   ```

2. **Not handling k > n in rotation:**
   ```python
   k = k % n  # ALWAYS do this first!
   ```

3. **Forgetting to sort intervals:**
   ```python
   intervals.sort(key=lambda x: x[0])  # MUST sort first!
   ```

---

## 💡 Pro Tips

**In-place algorithms:**
- Use read/write pointers
- Process from end to avoid overwriting
- Consider reversing as a tool

**Interval problems:**
1. Always sort by start time first
2. Track last merged interval
3. Check overlap: `start1 <= end2 and start2 <= end1`

**Matrix tricks:**
- Rotate 90°: Transpose + Reverse rows
- Rotate 180°: Reverse rows + Reverse cols
- Spiral: Use 4 boundaries (top, bottom, left, right)

---

**Master these patterns - they appear in 40% of array/string interviews!**

