# Sliding Window - Complete Guide

## 📋 Pattern Recognition

**When to use Sliding Window:**
- Subarray or substring problems
- "Contiguous" or "consecutive" sequence
- "Longest/shortest/maximum/minimum" subarray with condition
- Keywords: subarray, substring, contiguous, window, k elements

**Common Problem Phrases:**
- "Longest substring with at most K distinct characters"
- "Minimum window that contains..."
- "Maximum sum of subarray of size K"
- "Find all anagrams in string"

---

## 🎯 Two Main Types

###Type 1: Fixed Window Size
**Pattern:** Window size is constant (given as K)

```
Array: [1, 2, 3, 4, 5, 6], K = 3

Window 1: [1, 2, 3] 4  5  6
Window 2:  1 [2, 3, 4] 5  6
Window 3:  1  2 [3, 4, 5] 6
Window 4:  1  2  3 [4, 5, 6]
```

### Type 2: Variable Window Size
**Pattern:** Window size changes based on condition

```
Find longest substring with at most 2 distinct chars in "eceba"

e|
ec|
ece|
eceb  (3 distinct - too many!)
 ceb| (shrink from left)
 ceba (3 distinct - too many!)
  eba| (shrink from left)
```

---

## 🔧 Template Code

### Template 1: Fixed Window

```python
def fixed_window(arr: list, k: int):
    """
    Template for fixed window size problems
    Time: O(n), Space: O(1) or O(k)
    """
    # Step 1: Build initial window
    window_sum = sum(arr[:k])  # or other aggregation
    result = window_sum
    
    # Step 2: Slide window
    for i in range(k, len(arr)):
        # Remove leftmost element
        window_sum -= arr[i - k]
        # Add new element
        window_sum += arr[i]
        # Update result
        result = max(result, window_sum)
    
    return result
```

### Template 2: Variable Window (Shrinkable)

```python
def variable_window(arr: list):
    """
    Template for variable window size problems
    Time: O(n), Space: depends on data structure used
    """
    left = 0
    window = {}  # or set, list, etc.
    result = 0
    
    for right in range(len(arr)):
        # Step 1: Expand window by including arr[right]
        window[arr[right]] = window.get(arr[right], 0) + 1
        
        # Step 2: Shrink window while condition violated
        while not is_valid(window):
            window[arr[left]] -= 1
            if window[arr[left]] == 0:
                del window[arr[left]]
            left += 1
        
        # Step 3: Update result
        result = max(result, right - left + 1)
    
    return result
```

---

## 💡 Fixed Window Problems

### Problem 1: Maximum Average Subarray
```python
def findMaxAverage(nums: list[int], k: int) -> float:
    """
    LeetCode #643
    Find max average of subarray of size k
    
    Time: O(n), Space: O(1)
    """
    # Initial window
    window_sum = sum(nums[:k])
    max_sum = window_sum
    
    # Slide window
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]
        max_sum = max(max_sum, window_sum)
    
    return max_sum / k
```

### Problem 2: Max Consecutive Ones III
```python
def longestOnes(nums: list[int], k: int) -> int:
    """
    LeetCode #1004
    Longest subarray of 1's after flipping at most k 0's
    
    Time: O(n), Space: O(1)
    """
    left = 0
    zero_count = 0
    max_length = 0
    
    for right in range(len(nums)):
        # Expand: add nums[right]
        if nums[right] == 0:
            zero_count += 1
        
        # Shrink: if too many zeros
        while zero_count > k:
            if nums[left] == 0:
                zero_count -= 1
            left += 1
        
        # Update result
        max_length = max(max_length, right - left + 1)
    
    return max_length
```

---

## 💡 Variable Window Problems

### Problem 3: Longest Substring Without Repeating Characters
```python
def lengthOfLongestSubstring(s: str) -> int:
    """
    LeetCode #3 - Classic sliding window
    
    Time: O(n), Space: O(min(n, m)) where m is charset size
    """
    char_set = set()
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        # Shrink while duplicate exists
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        
        # Add current character
        char_set.add(s[right])
        max_length = max(max_length, right - left + 1)
    
    return max_length
```

**Alternative with Hash Map (track last seen index):**
```python
def lengthOfLongestSubstring_v2(s: str) -> int:
    """
    More efficient - jump left pointer
    """
    char_index = {}  # char -> last seen index
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        # If char seen and in current window
        if s[right] in char_index and char_index[s[right]] >= left:
            left = char_index[s[right]] + 1
        
        char_index[s[right]] = right
        max_length = max(max_length, right - left + 1)
    
    return max_length
```

### Problem 4: Minimum Window Substring
```python
def minWindow(s: str, t: str) -> str:
    """
    LeetCode #76 - HARD but classic template
    Find minimum window in s that contains all characters of t
    
    Time: O(n + m), Space: O(m)
    """
    if not s or not t:
        return ""
    
    # Count characters in t
    target_count = {}
    for char in t:
        target_count[char] = target_count.get(char, 0) + 1
    
    required = len(target_count)  # Unique chars needed
    formed = 0  # Unique chars currently satisfied
    
    window_counts = {}
    left = 0
    min_len = float('inf')
    min_left = 0
    
    for right in range(len(s)):
        # Expand: add s[right]
        char = s[right]
        window_counts[char] = window_counts.get(char, 0) + 1
        
        # Check if frequency matches
        if char in target_count and window_counts[char] == target_count[char]:
            formed += 1
        
        # Shrink: try to minimize window
        while formed == required and left <= right:
            # Update result
            if right - left + 1 < min_len:
                min_len = right - left + 1
                min_left = left
            
            # Remove leftmost character
            char = s[left]
            window_counts[char] -= 1
            if char in target_count and window_counts[char] < target_count[char]:
                formed -= 1
            
            left += 1
    
    return "" if min_len == float('inf') else s[min_left:min_left + min_len]
```

**This is THE template problem! Master this and everything else is easier!**

### Problem 5: Longest Substring with At Most K Distinct Characters
```python
def lengthOfLongestSubstringKDistinct(s: str, k: int) -> int:
    """
    LeetCode #340 (Premium)
    
    Time: O(n), Space: O(k)
    """
    if k == 0:
        return 0
    
    char_count = {}
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        # Expand: add s[right]
        char_count[s[right]] = char_count.get(s[right], 0) + 1
        
        # Shrink: if too many distinct chars
        while len(char_count) > k:
            char_count[s[left]] -= 1
            if char_count[s[left]] == 0:
                del char_count[s[left]]
            left += 1
        
        # Update result
        max_length = max(max_length, right - left + 1)
    
    return max_length
```

### Problem 6: Find All Anagrams
```python
def findAnagrams(s: str, p: str) -> list[int]:
    """
    LeetCode #438
    Find all start indices of p's anagrams in s
    
    Time: O(n), Space: O(1) - only 26 letters
    """
    if len(p) > len(s):
        return []
    
    # Count frequencies
    p_count = {}
    window_count = {}
    
    for char in p:
        p_count[char] = p_count.get(char, 0) + 1
    
    result = []
    left = 0
    
    for right in range(len(s)):
        # Expand
        char = s[right]
        window_count[char] = window_count.get(char, 0) + 1
        
        # Shrink if window too large
        if right - left + 1 > len(p):
            left_char = s[left]
            window_count[left_char] -= 1
            if window_count[left_char] == 0:
                del window_count[left_char]
            left += 1
        
        # Check if anagram (fixed window size of len(p))
        if right - left + 1 == len(p) and window_count == p_count:
            result.append(left)
    
    return result
```

### Problem 7: Longest Repeating Character Replacement
```python
def characterReplacement(s: str, k: int) -> int:
    """
    LeetCode #424
    Longest substring with same chars after replacing at most k chars
    
    Key insight: window is valid if:
    window_length - max_frequency <= k
    
    Time: O(n), Space: O(1) - only 26 letters
    """
    char_count = {}
    left = 0
    max_length = 0
    max_freq = 0
    
    for right in range(len(s)):
        # Expand
        char_count[s[right]] = char_count.get(s[right], 0) + 1
        max_freq = max(max_freq, char_count[s[right]])
        
        # Shrink if invalid: need to replace more than k chars
        while (right - left + 1) - max_freq > k:
            char_count[s[left]] -= 1
            left += 1
            # Note: max_freq might not be accurate after shrinking,
            # but it doesn't matter for correctness
        
        max_length = max(max_length, right - left + 1)
    
    return max_length
```

### Problem 8: Subarrays with Product Less Than K
```python
def numSubarrayProductLessThanK(nums: list[int], k: int) -> int:
    """
    LeetCode #713
    Count subarrays where product < k
    
    Key insight: For window [left...right], there are (right - left + 1)
    subarrays ending at right
    
    Time: O(n), Space: O(1)
    """
    if k <= 1:
        return 0
    
    product = 1
    left = 0
    count = 0
    
    for right in range(len(nums)):
        # Expand
        product *= nums[right]
        
        # Shrink
        while product >= k:
            product //= nums[left]
            left += 1
        
        # All subarrays ending at right with start in [left...right]
        count += right - left + 1
    
    return count
```

---

## 🎓 Advanced Problems

### Problem 9: Minimum Size Subarray Sum
```python
def minSubArrayLen(target: int, nums: list[int]) -> int:
    """
    LeetCode #209
    Minimum length subarray with sum >= target
    
    Time: O(n), Space: O(1)
    """
    left = 0
    current_sum = 0
    min_length = float('inf')
    
    for right in range(len(nums)):
        current_sum += nums[right]
        
        # Shrink as much as possible
        while current_sum >= target:
            min_length = min(min_length, right - left + 1)
            current_sum -= nums[left]
            left += 1
    
    return min_length if min_length != float('inf') else 0
```

### Problem 10: Subarrays with K Different Integers
```python
def subarraysWithKDistinct(nums: list[int], k: int) -> int:
    """
    LeetCode #992 - HARD
    Exactly K distinct integers
    
    Key trick: exactly(K) = atMost(K) - atMost(K-1)
    
    Time: O(n), Space: O(n)
    """
    def atMostK(k):
        count = {}
        left = 0
        result = 0
        
        for right in range(len(nums)):
            count[nums[right]] = count.get(nums[right], 0) + 1
            
            while len(count) > k:
                count[nums[left]] -= 1
                if count[nums[left]] == 0:
                    del count[nums[left]]
                left += 1
            
            # All subarrays ending at right
            result += right - left + 1
        
        return result
    
    return atMostK(k) - atMostK(k - 1)
```

---

## 🐛 Common Mistakes

### Mistake 1: Not Shrinking Properly
```python
# ❌ WRONG - Only shrinks once
if condition_violated:
    left += 1

# ✅ CORRECT - Shrinks until valid
while condition_violated:
    left += 1
```

### Mistake 2: Off-by-One in Window Size
```python
# Window size calculation:
window_size = right - left + 1  # Inclusive on both ends

# Example: left=0, right=2 → window contains indices 0,1,2 → size=3
```

### Mistake 3: Forgetting to Update Max Frequency
```python
# In character replacement problems:
max_freq = max(max_freq, char_count[s[right]])
# Need to track this to determine if window is valid
```

### Mistake 4: Not Handling Empty Result
```python
# ❌ WRONG
min_length = 0
if found:
    min_length = ...
return min_length  # Returns 0 even if not found!

# ✅ CORRECT
min_length = float('inf')
if found:
    min_length = ...
return min_length if min_length != float('inf') else 0
```

---

## 💡 Decision Tree

```
Sliding Window Problem?
│
├─ Is window size fixed (given K)?
│   │
│   └─ YES → Use Fixed Window Template
│       - Initialize window of size K
│       - Slide by removing left, adding right
│       - Time: O(n)
│
└─ NO → Window size varies
    │
    ├─ Find LONGEST/MAXIMUM with condition?
    │   └─ Expand right, shrink left when invalid
    │       - Track max_length throughout
    │
    ├─ Find SHORTEST/MINIMUM with condition?
    │   └─ Expand right, shrink left when valid
    │       - Update min_length during shrinking
    │
    └─ COUNT subarrays?
        └─ For each right, count subarrays ending there
            - count += right - left + 1
```

---

## 🎯 Master Template (Annotated)

```python
def sliding_window_template(arr, target):
    """
    Universal template - adapt as needed
    """
    # 1. Initialize window state
    window = {}  # or set, counter, sum, etc.
    left = 0
    result = 0  # or float('inf') for minimum
    
    # 2. Expand window with right pointer
    for right in range(len(arr)):
        # Add arr[right] to window
        window[arr[right]] = window.get(arr[right], 0) + 1
        
        # 3. Shrink window if condition violated
        while not is_valid(window):  # Define your condition
            # Remove arr[left] from window
            window[arr[left]] -= 1
            if window[arr[left]] == 0:
                del window[arr[left]]
            left += 1
        
        # 4. Update result
        # For maximum: result = max(result, right - left + 1)
        # For minimum: result = min(result, right - left + 1)
        # For count: result += right - left + 1
        result = max(result, right - left + 1)
    
    return result
```

---

## 🎓 Practice Progression

### Phase 1: Fixed Window (Easy)
1. #643 Maximum Average Subarray I
2. #1456 Maximum Number of Vowels in Substring

### Phase 2: Basic Variable Window (Easy-Medium)
3. #3 Longest Substring Without Repeating Characters **★**
4. #209 Minimum Size Subarray Sum
5. #1004 Max Consecutive Ones III

### Phase 3: With Hash Map (Medium)
6. #438 Find All Anagrams in String **★**
7. #567 Permutation in String
8. #424 Longest Repeating Character Replacement **★**

### Phase 4: Advanced (Medium-Hard)
9. #76 Minimum Window Substring **★★★ MASTER THIS**
10. #992 Subarrays with K Different Integers **★**
11. #713 Subarray Product Less Than K

---

## 💡 Pro Tips

### Tip 1: Visualize the Window
Always draw it out:
```
s = "abcabcbb", find longest without repeating

a|
ab|
abc|
abca  (duplicate 'a'!)
 bca| (shrink left)
 bcab (duplicate 'b'!)
  cab| (shrink left)
```

### Tip 2: AtMost Trick
"Exactly K" = "At Most K" - "At Most K-1"
Useful when exact count is hard but "at most" is easy

### Tip 3: Hash Map vs Array
```python
# For limited charset (e.g., lowercase letters):
count = [0] * 26  # Faster
count[ord(char) - ord('a')] += 1

# For arbitrary characters:
count = {}  # More flexible
count[char] = count.get(char, 0) + 1
```

### Tip 4: Two Conditions Pattern
Some problems have two conditions:
```python
while condition1 or condition2:
    if condition1:
        # Handle condition1
    if condition2:
        # Handle condition2
    left += 1
```

---

## 📊 Complexity Summary

| Pattern | Time | Space | Notes |
|---------|------|-------|-------|
| Fixed Window | O(n) | O(1) or O(k) | K is window size |
| Variable Window | O(n) | O(k) | K is charset/distinct elements |
| With Hash Map | O(n) | O(min(n,m)) | m is charset size |

**Key Insight:** Each element is visited at most twice (once by right, once by left), so time is O(n)!

**Remember:** Sliding window is an optimization technique that reduces brute force O(n²) to O(n)!

