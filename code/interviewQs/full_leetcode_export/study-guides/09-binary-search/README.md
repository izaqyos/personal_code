# Binary Search - Complete Guide

## 📋 Pattern Recognition

**When to use Binary Search:**
- Array is sorted (or rotated sorted)
- "Find target in O(log n)"
- "Minimum/maximum value that satisfies condition"
- "Search space can be divided in half"

**Keywords:** sorted, search, find, minimize, maximize, O(log n)

---

## 🎯 Binary Search Templates

### Template 1: Basic Binary Search
```python
def binary_search(nums: list[int], target: int) -> int:
    """
    Find exact target
    Time: O(log n), Space: O(1)
    """
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = left + (right - left) // 2  # Avoid overflow
        
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1  # Not found
```

### Template 2: Lower Bound (First >= target)
```python
def lower_bound(nums: list[int], target: int) -> int:
    """
    Find first element >= target
    """
    left, right = 0, len(nums)
    
    while left < right:
        mid = left + (right - left) // 2
        
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid
    
    return left
```

### Template 3: Upper Bound (First > target)
```python
def upper_bound(nums: list[int], target: int) -> int:
    """
    Find first element > target
    """
    left, right = 0, len(nums)
    
    while left < right:
        mid = left + (right - left) // 2
        
        if nums[mid] <= target:
            left = mid + 1
        else:
            right = mid
    
    return left
```

---

## 🔧 Pattern 1: Search in Rotated Array

```python
def search(nums: list[int], target: int) -> int:
    """
    LeetCode #33
    Time: O(log n), Space: O(1)
    """
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if nums[mid] == target:
            return mid
        
        # Check which half is sorted
        if nums[left] <= nums[mid]:
            # Left half is sorted
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            # Right half is sorted
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    
    return -1
```

---

## 🔧 Pattern 2: Binary Search on Answer 🚨 CRITICAL

### Problem: Koko Eating Bananas
```python
def minEatingSpeed(piles: list[int], h: int) -> int:
    """
    LeetCode #875
    
    Binary search on answer: speed k
    Time: O(n log m) where m = max(piles)
    """
    def can_finish(k):
        """Can finish all bananas in h hours at speed k?"""
        import math
        hours = sum(math.ceil(pile / k) for pile in piles)
        return hours <= h
    
    left, right = 1, max(piles)
    
    while left < right:
        mid = left + (right - left) // 2
        
        if can_finish(mid):
            right = mid  # Try smaller speed
        else:
            left = mid + 1  # Need larger speed
    
    return left
```

### Problem: Split Array Largest Sum
```python
def splitArray(nums: list[int], k: int) -> int:
    """
    LeetCode #410 - HARD but classic pattern
    
    Binary search on answer: largest sum
    """
    def can_split(max_sum):
        """Can split into k subarrays with max sum <= max_sum?"""
        subarrays = 1
        current_sum = 0
        
        for num in nums:
            if current_sum + num > max_sum:
                subarrays += 1
                current_sum = num
            else:
                current_sum += num
        
        return subarrays <= k
    
    left = max(nums)  # Min possible (each element in own subarray)
    right = sum(nums)  # Max possible (all in one subarray)
    
    while left < right:
        mid = left + (right - left) // 2
        
        if can_split(mid):
            right = mid
        else:
            left = mid + 1
    
    return left
```

---

## 🔧 Pattern 3: Find Peak Element

```python
def findPeakElement(nums: list[int]) -> int:
    """
    LeetCode #162
    Peak: nums[i] > nums[i-1] and nums[i] > nums[i+1]
    
    Time: O(log n), Space: O(1)
    """
    left, right = 0, len(nums) - 1
    
    while left < right:
        mid = left + (right - left) // 2
        
        if nums[mid] < nums[mid + 1]:
            # Peak is on the right
            left = mid + 1
        else:
            # Peak is on the left or at mid
            right = mid
    
    return left
```

---

## 🎓 Key Problems

1. #35 Search Insert Position (Template)
2. #33 Search in Rotated Sorted Array
3. #162 Find Peak Element
4. #875 Koko Eating Bananas (Search on answer)
5. #410 Split Array Largest Sum (Search on answer)

---

## 💡 Pro Tips

**When to "Search on Answer":**
- Problem asks for min/max value that satisfies condition
- Can verify if value works in O(n) or O(n log n)
- Answer space is monotonic

**Remember:** `mid = left + (right - left) // 2` to avoid overflow!

---

**Master binary search on answer - it transforms many hard problems into medium!**

