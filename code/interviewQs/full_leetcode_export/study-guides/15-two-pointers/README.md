# Two Pointers - Complete Guide

## 📋 Pattern Recognition

**When to use Two Pointers:**
- Array/string is **sorted** (or you can sort it)
- Need to find pairs/triplets with specific properties
- Need to partition or rearrange in-place
- "Find pair that sums to X"
- "Remove duplicates in-place"
- "Reverse in-place"

**Keywords:** sorted, pair, triplet, partition, in-place, palindrome, container

---

## 🎯 Core Patterns

### Pattern 1: Opposite Direction (Converging)
**When:** Sorted array, find pairs, palindrome check

```python
def twoSum_sorted(nums: list[int], target: int) -> list[int]:
    """
    Find two numbers that add up to target in sorted array
    LeetCode #167
    
    Time: O(n), Space: O(1)
    """
    left, right = 0, len(nums) - 1
    
    while left < right:
        current_sum = nums[left] + nums[right]
        
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1   # Need larger sum
        else:
            right -= 1  # Need smaller sum
    
    return [-1, -1]
```

**Visual:**
```
[1, 2, 3, 4, 5, 6], target = 7
 ↑                 ↑
left             right
Sum = 1 + 6 = 7 ✓

[1, 2, 3, 4, 5, 6], target = 10
 ↑                 ↑
left             right
Sum = 1 + 6 = 7 < 10, move left →
```

---

### Pattern 2: Same Direction (Fast & Slow)
**When:** Remove elements in-place, find cycle, sliding window

```python
def removeDuplicates(nums: list[int]) -> int:
    """
    Remove duplicates from sorted array in-place
    LeetCode #26
    
    Slow pointer: position to place next unique element
    Fast pointer: explores the array
    
    Time: O(n), Space: O(1)
    """
    if not nums:
        return 0
    
    slow = 0  # Position for next unique element
    
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    
    return slow + 1  # Length of unique elements
```

**Visual:**
```
[1, 1, 2, 2, 3]
 s  f
 
[1, 1, 2, 2, 3]
 s     f         (nums[f] != nums[s], so s++ and copy)
 
[1, 2, 2, 2, 3]
    s     f
    
[1, 2, 3, 2, 3]  (final state, first 3 elements are unique)
       s        f
```

---

### Pattern 3: Sliding Window (Fixed/Variable Size)
**When:** Subarray/substring problems, maintain window of elements

```python
def maxAverage(nums: list[int], k: int) -> float:
    """
    Maximum average of subarray of size k
    LeetCode #643
    
    Fixed window size
    Time: O(n), Space: O(1)
    """
    # Initial window sum
    window_sum = sum(nums[:k])
    max_sum = window_sum
    
    # Slide window
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]  # Add new, remove old
        max_sum = max(max_sum, window_sum)
    
    return max_sum / k
```

---

## 💡 Complete Patterns & Solutions

### Pattern A: Two Sum Variants

#### 1. Two Sum (Sorted Array)
```python
def twoSum(numbers: list[int], target: int) -> list[int]:
    """LeetCode #167 - Two pointers on sorted array"""
    left, right = 0, len(numbers) - 1
    
    while left < right:
        total = numbers[left] + numbers[right]
        if total == target:
            return [left + 1, right + 1]  # 1-indexed
        elif total < target:
            left += 1
        else:
            right -= 1
    
    return []
```

#### 2. Three Sum
```python
def threeSum(nums: list[int]) -> list[list[int]]:
    """
    Find all unique triplets that sum to zero
    LeetCode #15
    
    Strategy: Sort + fix one number + two pointers for other two
    Time: O(n²), Space: O(1)
    """
    nums.sort()
    result = []
    
    for i in range(len(nums) - 2):
        # Skip duplicates for first number
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        left, right = i + 1, len(nums) - 1
        target = -nums[i]
        
        while left < right:
            total = nums[left] + nums[right]
            
            if total == target:
                result.append([nums[i], nums[left], nums[right]])
                
                # Skip duplicates for second number
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                # Skip duplicates for third number
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
            elif total < target:
                left += 1
            else:
                right -= 1
    
    return result
```

**Key Insight for 3Sum:**
- Sort first: O(n log n)
- Fix first element: O(n)
- Two pointers for remaining two: O(n)
- Total: O(n²)
- Skip duplicates at all three positions!

#### 3. Four Sum
```python
def fourSum(nums: list[int], target: int) -> list[list[int]]:
    """
    Find all unique quadruplets that sum to target
    LeetCode #18
    
    Strategy: Sort + fix two numbers + two pointers
    Time: O(n³), Space: O(1)
    """
    nums.sort()
    result = []
    n = len(nums)
    
    for i in range(n - 3):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        for j in range(i + 1, n - 2):
            if j > i + 1 and nums[j] == nums[j - 1]:
                continue
            
            left, right = j + 1, n - 1
            remaining = target - nums[i] - nums[j]
            
            while left < right:
                total = nums[left] + nums[right]
                
                if total == remaining:
                    result.append([nums[i], nums[j], nums[left], nums[right]])
                    
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    
                    left += 1
                    right -= 1
                elif total < remaining:
                    left += 1
                else:
                    right -= 1
    
    return result
```

---

### Pattern B: In-Place Array Manipulation

#### 1. Move Zeroes
```python
def moveZeroes(nums: list[int]) -> None:
    """
    Move all 0's to end while maintaining order of non-zero elements
    LeetCode #283
    
    Time: O(n), Space: O(1)
    """
    slow = 0  # Position for next non-zero element
    
    # Move all non-zero elements to front
    for fast in range(len(nums)):
        if nums[fast] != 0:
            nums[slow] = nums[fast]
            slow += 1
    
    # Fill remaining with zeros
    for i in range(slow, len(nums)):
        nums[i] = 0
```

**Optimized version (fewer writes):**
```python
def moveZeroes_optimized(nums: list[int]) -> None:
    """Only swap when necessary"""
    slow = 0
    
    for fast in range(len(nums)):
        if nums[fast] != 0:
            # Swap only if positions are different
            nums[slow], nums[fast] = nums[fast], nums[slow]
            slow += 1
```

#### 2. Remove Element
```python
def removeElement(nums: list[int], val: int) -> int:
    """
    Remove all occurrences of val in-place
    LeetCode #27
    
    Time: O(n), Space: O(1)
    """
    slow = 0
    
    for fast in range(len(nums)):
        if nums[fast] != val:
            nums[slow] = nums[fast]
            slow += 1
    
    return slow
```

#### 3. Sort Colors (Dutch National Flag)
```python
def sortColors(nums: list[int]) -> None:
    """
    Sort array of 0s, 1s, and 2s in-place
    LeetCode #75
    
    Three pointers: low, mid, high
    - [0...low-1]: all 0s
    - [low...mid-1]: all 1s
    - [mid...high]: unexplored
    - [high+1...n-1]: all 2s
    
    Time: O(n), Space: O(1)
    """
    low, mid, high = 0, 0, len(nums) - 1
    
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:  # nums[mid] == 2
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
            # Don't increment mid! Need to check swapped element
```

---

### Pattern C: Container / Area Problems

#### Container With Most Water
```python
def maxArea(height: list[int]) -> int:
    """
    Find two lines that form container with most water
    LeetCode #11
    
    Greedy: Start with widest, move pointer with smaller height
    Time: O(n), Space: O(1)
    """
    left, right = 0, len(height) - 1
    max_area = 0
    
    while left < right:
        # Width * min height
        width = right - left
        current_area = width * min(height[left], height[right])
        max_area = max(max_area, current_area)
        
        # Move pointer with smaller height (greedy)
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return max_area
```

**Why this works:**
- Start with maximum width
- To get larger area, need taller height
- Move pointer with smaller height (can't improve with current height)

---

### Pattern D: Partition Problems

#### Partition Array
```python
def partition(nums: list[int], pivot: int) -> None:
    """
    Partition array: elements < pivot on left, >= pivot on right
    Used in QuickSort
    
    Time: O(n), Space: O(1)
    """
    left = 0
    right = len(nums) - 1
    
    while left <= right:
        while left <= right and nums[left] < pivot:
            left += 1
        while left <= right and nums[right] >= pivot:
            right -= 1
        
        if left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1
```

---

### Pattern E: String/Array Reversal

#### Reverse String
```python
def reverseString(s: list[str]) -> None:
    """
    Reverse string in-place
    LeetCode #344
    
    Time: O(n), Space: O(1)
    """
    left, right = 0, len(s) - 1
    
    while left < right:
        s[left], s[right] = s[right], s[left]
        left += 1
        right -= 1
```

#### Valid Palindrome
```python
def isPalindrome(s: str) -> bool:
    """
    Check if string is palindrome (ignoring non-alphanumeric)
    LeetCode #125
    
    Time: O(n), Space: O(1)
    """
    left, right = 0, len(s) - 1
    
    while left < right:
        # Skip non-alphanumeric from left
        while left < right and not s[left].isalnum():
            left += 1
        # Skip non-alphanumeric from right
        while left < right and not s[right].isalnum():
            right -= 1
        
        # Compare (case-insensitive)
        if s[left].lower() != s[right].lower():
            return False
        
        left += 1
        right -= 1
    
    return True
```

---

### Pattern F: Trapping Rain Water

```python
def trap(height: list[int]) -> int:
    """
    Calculate trapped rainwater
    LeetCode #42
    
    Two pointers with max heights
    Time: O(n), Space: O(1)
    """
    if not height:
        return 0
    
    left, right = 0, len(height) - 1
    left_max, right_max = height[left], height[right]
    water = 0
    
    while left < right:
        if height[left] < height[right]:
            # Process left side
            if height[left] >= left_max:
                left_max = height[left]
            else:
                water += left_max - height[left]
            left += 1
        else:
            # Process right side
            if height[right] >= right_max:
                right_max = height[right]
            else:
                water += right_max - height[right]
            right -= 1
    
    return water
```

**Key Insight:**
- Water level at position = min(max_left, max_right) - height
- Track max heights from both sides
- Process side with smaller height

---

## 🎓 Practice Problems

### Easy
1. **#167 Two Sum II** - Basic two pointers
2. **#125 Valid Palindrome** - String two pointers
3. **#283 Move Zeroes** - Fast/slow pattern
4. **#26 Remove Duplicates** - In-place modification
5. **#344 Reverse String** - Converging pointers

### Medium
1. **#15 3Sum** - Two pointers + iteration
2. **#11 Container With Most Water** - Greedy two pointers
3. **#75 Sort Colors** - Three pointers (Dutch flag)
4. **#16 3Sum Closest** - Variant of 3Sum
5. **#18 4Sum** - Extension of 3Sum
6. **#713 Subarray Product Less Than K** - Sliding window
7. **#881 Boats to Save People** - Greedy two pointers

### Hard
1. **#42 Trapping Rain Water** - Advanced two pointers
2. **#828 Count Unique Characters** - Complex two pointers

---

## 🐛 Common Mistakes

### Mistake 1: Not Handling Duplicates in 3Sum/4Sum
```python
# ❌ WRONG - Will have duplicates in result
for i in range(len(nums)):
    # Missing duplicate check!
    
# ✅ CORRECT
for i in range(len(nums)):
    if i > 0 and nums[i] == nums[i - 1]:
        continue  # Skip duplicates
```

### Mistake 2: Infinite Loop
```python
# ❌ WRONG
while left < right:
    if condition:
        # Forgot to move pointers!
        pass

# ✅ CORRECT
while left < right:
    if condition:
        left += 1  # or right -= 1
```

### Mistake 3: Array Index Out of Bounds
```python
# ❌ WRONG
while left <= right:  # Should be <, not <=
    nums[left], nums[right] = nums[right], nums[left]

# ✅ CORRECT
while left < right:  # Use < for swapping
    nums[left], nums[right] = nums[right], nums[left]
```

---

## 💡 Decision Tree: Which Two Pointer Pattern?

```
Is the array/string sorted?
│
├─ YES → Can you sort it?
│   │
│   ├─ Finding pairs/triplets? → Opposite direction (converging)
│   ├─ Partition problem? → Opposite direction
│   └─ Container/area? → Opposite direction (greedy)
│
└─ NO → 
    │
    ├─ Remove/modify in-place? → Same direction (fast/slow)
    ├─ Detect cycle? → Fast/slow (different speeds)
    └─ Subarray/substring? → Sliding window
```

---

## 🎯 Pro Tips

### Tip 1: Always Consider Sorting First
- If O(n log n) is acceptable, sorting often enables two pointers
- Compare: Hash map O(n) space vs Sort + Two pointers O(1) space

### Tip 2: Skip Duplicates Carefully
```python
# Skip duplicates AFTER finding solution
if found_solution:
    while left < right and nums[left] == nums[left + 1]:
        left += 1
    while left < right and nums[right] == nums[right - 1]:
        right -= 1
```

### Tip 3: Edge Cases
```python
# Always test:
1. Empty array: []
2. Single element: [1]
3. Two elements: [1, 2]
4. All same: [1, 1, 1, 1]
5. Already sorted/reverse sorted
```

### Tip 4: Fast/Slow Pattern Template
```python
def fast_slow_pattern(arr):
    slow = 0
    for fast in range(len(arr)):
        if condition:
            # Do something
            arr[slow] = arr[fast]
            slow += 1
    return slow
```

---

## 📊 Complexity Cheatsheet

| Pattern | Time | Space | Use Case |
|---------|------|-------|----------|
| Opposite Direction | O(n) | O(1) | Sorted array, find pairs |
| Same Direction | O(n) | O(1) | Remove elements, partition |
| Fast/Slow (cycle) | O(n) | O(1) | Cycle detection |
| Sliding Window | O(n) | O(1) or O(k) | Subarrays |

**Remember:** Two pointers is about space optimization - achieve O(1) space where hash map would use O(n)!

