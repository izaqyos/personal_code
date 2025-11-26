# Dynamic Programming - Complete Guide

## 📋 Pattern Recognition

**When to use DP:**
- "Maximum/minimum"
- "Count ways to..."
- "Is it possible to..."
- Overlapping subproblems + optimal substructure
- Can break down into similar smaller subproblems

**Common Keywords:**
- Optimal, maximize, minimize, longest, shortest
- Count number of ways
- "Can we reach...", "is it possible..."
- Sequence, subsequence, substring

---

## 🎯 DP Fundamentals

### What is Dynamic Programming?
1. **Overlapping Subproblems:** Same subproblem solved multiple times
2. **Optimal Substructure:** Optimal solution contains optimal solutions to subproblems
3. **Memoization/Tabulation:** Store solutions to avoid recomputation

### Two Approaches

#### 1. Top-Down (Memoization) - Recursion + Cache
```python
def fib_memoization(n, memo={}):
    """
    Start from n, break down to smaller problems
    Cache results as we go
    """
    if n <= 1:
        return n
    
    if n in memo:
        return memo[n]
    
    memo[n] = fib_memoization(n-1, memo) + fib_memoization(n-2, memo)
    return memo[n]
```

**Pros:** Intuitive, only solves needed subproblems  
**Cons:** Recursion overhead, potential stack overflow

#### 2. Bottom-Up (Tabulation) - Iterative
```python
def fib_tabulation(n):
    """
    Start from smallest problems, build up to n
    No recursion needed
    """
    if n <= 1:
        return n
    
    dp = [0] * (n + 1)
    dp[1] = 1
    
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    
    return dp[n]
```

**Pros:** No recursion, often faster, easier to optimize space  
**Cons:** Must solve all subproblems, less intuitive

#### 3. Space-Optimized
```python
def fib_optimized(n):
    """
    Only keep what's needed
    """
    if n <= 1:
        return n
    
    prev2, prev1 = 0, 1
    
    for i in range(2, n + 1):
        current = prev1 + prev2
        prev2, prev1 = prev1, current
    
    return prev1
```

**Space:** O(n) → O(1)

---

## 🔧 Pattern 1: 1D DP (Linear)

### Problem 1: Climbing Stairs
```python
def climbStairs(n: int) -> int:
    """
    LeetCode #70 - Classic intro problem
    
    Can climb 1 or 2 steps. How many ways to reach top?
    
    Recurrence: dp[i] = dp[i-1] + dp[i-2]
    Base: dp[0] = 1, dp[1] = 1
    
    Time: O(n), Space: O(1) optimized
    """
    if n <= 2:
        return n
    
    prev2, prev1 = 1, 2
    
    for i in range(3, n + 1):
        current = prev1 + prev2
        prev2, prev1 = prev1, current
    
    return prev1
```

### Problem 2: House Robber
```python
def rob(nums: list[int]) -> int:
    """
    LeetCode #198 - Cannot rob adjacent houses
    
    Recurrence: dp[i] = max(dp[i-1], dp[i-2] + nums[i])
                       = max(don't rob i, rob i)
    
    Time: O(n), Space: O(1)
    """
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    
    prev2, prev1 = 0, 0
    
    for num in nums:
        current = max(prev1, prev2 + num)
        prev2, prev1 = prev1, current
    
    return prev1
```

### Problem 3: Decode Ways
```python
def numDecodings(s: str) -> int:
    """
    LeetCode #91 - '1' = 'A', '2' = 'B', ..., '26' = 'Z'
    
    Recurrence:
    dp[i] = dp[i-1] if s[i] valid (1-9)
          + dp[i-2] if s[i-1:i+1] valid (10-26)
    
    Time: O(n), Space: O(1)
    """
    if not s or s[0] == '0':
        return 0
    
    n = len(s)
    prev2, prev1 = 1, 1
    
    for i in range(1, n):
        current = 0
        
        # Single digit (1-9)
        if s[i] != '0':
            current += prev1
        
        # Two digits (10-26)
        two_digit = int(s[i-1:i+1])
        if 10 <= two_digit <= 26:
            current += prev2
        
        prev2, prev1 = prev1, current
    
    return prev1
```

---

## 🔧 Pattern 2: Knapsack (0/1 & Unbounded) 🚨 CRITICAL

### 0/1 Knapsack Template
```python
def knapsack_01(weights, values, capacity):
    """
    Classic 0/1 Knapsack
    Each item can be taken 0 or 1 time
    
    dp[i][w] = max value using first i items with capacity w
    
    Recurrence:
    dp[i][w] = max(dp[i-1][w],                    # don't take item i
                   dp[i-1][w-weight[i]] + value[i]) # take item i
    
    Time: O(n * W), Space: O(n * W)
    """
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            # Don't take item i-1
            dp[i][w] = dp[i-1][w]
            
            # Take item i-1 if possible
            if w >= weights[i-1]:
                dp[i][w] = max(dp[i][w], 
                              dp[i-1][w - weights[i-1]] + values[i-1])
    
    return dp[n][capacity]
```

### Problem 4: Partition Equal Subset Sum
```python
def canPartition(nums: list[int]) -> bool:
    """
    LeetCode #416 - Can partition into two equal sum subsets?
    
    Key insight: Find subset with sum = total_sum / 2
    This is 0/1 knapsack: can we make target sum?
    
    Time: O(n * sum), Space: O(sum)
    """
    total = sum(nums)
    
    if total % 2 == 1:
        return False
    
    target = total // 2
    
    # dp[s] = can we make sum s?
    dp = [False] * (target + 1)
    dp[0] = True  # Can always make 0
    
    for num in nums:
        # Traverse backwards to avoid using same element twice
        for s in range(target, num - 1, -1):
            dp[s] = dp[s] or dp[s - num]
    
    return dp[target]
```

### Unbounded Knapsack Template
```python
def knapsack_unbounded(weights, values, capacity):
    """
    Unbounded Knapsack
    Each item can be taken unlimited times
    
    Recurrence:
    dp[w] = max(dp[w],                    # don't take item
                dp[w-weight[i]] + value[i]) # take item i
    
    Note: Different order than 0/1!
    
    Time: O(n * W), Space: O(W)
    """
    dp = [0] * (capacity + 1)
    
    for w in range(1, capacity + 1):
        for i in range(len(weights)):
            if w >= weights[i]:
                dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    
    return dp[capacity]
```

### Problem 5: Coin Change 🚨 MUST DO
```python
def coinChange(coins: list[int], amount: int) -> int:
    """
    LeetCode #322 - Minimum coins to make amount
    
    Unbounded knapsack: each coin can be used unlimited times
    
    Recurrence:
    dp[a] = min coins to make amount a
          = min(dp[a], dp[a - coin] + 1) for each coin
    
    Time: O(n * amount), Space: O(amount)
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # 0 coins needed for amount 0
    
    for a in range(1, amount + 1):
        for coin in coins:
            if a >= coin:
                dp[a] = min(dp[a], dp[a - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1
```

### Problem 6: Coin Change 2 (Count Ways)
```python
def change(amount: int, coins: list[int]) -> int:
    """
    LeetCode #518 - Count ways to make amount
    
    Recurrence:
    dp[a] = number of ways to make amount a
    
    Key: Iterate coins in outer loop to avoid counting duplicates!
    
    Time: O(n * amount), Space: O(amount)
    """
    dp = [0] * (amount + 1)
    dp[0] = 1  # One way to make 0: use no coins
    
    for coin in coins:
        for a in range(coin, amount + 1):
            dp[a] += dp[a - coin]
    
    return dp[amount]
```

---

## 🔧 Pattern 3: Longest Increasing Subsequence (LIS)

### Problem 7: LIS - Basic
```python
def lengthOfLIS(nums: list[int]) -> int:
    """
    LeetCode #300 - Longest Increasing Subsequence
    
    dp[i] = length of LIS ending at index i
    
    Recurrence:
    dp[i] = max(dp[j] + 1) for all j < i where nums[j] < nums[i]
    
    Time: O(n²), Space: O(n)
    """
    if not nums:
        return 0
    
    n = len(nums)
    dp = [1] * n  # Each element is LIS of length 1
    
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)
```

### LIS - Optimal (Binary Search)
```python
def lengthOfLIS_optimal(nums: list[int]) -> int:
    """
    Optimal LIS using binary search
    
    tails[i] = smallest tail of all LIS of length i+1
    
    Time: O(n log n), Space: O(n)
    """
    import bisect
    
    tails = []
    
    for num in nums:
        pos = bisect.bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num
    
    return len(tails)
```

### Problem 8: Russian Doll Envelopes
```python
def maxEnvelopes(envelopes: list[list[int]]) -> int:
    """
    LeetCode #354 - 2D LIS problem
    
    Envelope (w, h) can fit in (W, H) if w < W and h < H
    
    Key insight:
    1. Sort by width ascending, height descending
    2. Find LIS on heights
    
    Time: O(n log n), Space: O(n)
    """
    import bisect
    
    # Sort: width ascending, height descending
    envelopes.sort(key=lambda x: (x[0], -x[1]))
    
    # LIS on heights
    tails = []
    for _, h in envelopes:
        pos = bisect.bisect_left(tails, h)
        if pos == len(tails):
            tails.append(h)
        else:
            tails[pos] = h
    
    return len(tails)
```

---

## 🔧 Pattern 4: Longest Common Subsequence (LCS)

### Problem 9: LCS Template
```python
def longestCommonSubsequence(text1: str, text2: str) -> int:
    """
    LeetCode #1143 - Classic LCS
    
    dp[i][j] = LCS of text1[0:i] and text2[0:j]
    
    Recurrence:
    if text1[i-1] == text2[j-1]:
        dp[i][j] = dp[i-1][j-1] + 1
    else:
        dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    Time: O(m * n), Space: O(m * n)
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]
```

### Problem 10: Edit Distance
```python
def minDistance(word1: str, word2: str) -> int:
    """
    LeetCode #72 - Minimum edit distance (Levenshtein)
    
    Operations: insert, delete, replace
    
    dp[i][j] = min edits to convert word1[0:i] to word2[0:j]
    
    Recurrence:
    if word1[i-1] == word2[j-1]:
        dp[i][j] = dp[i-1][j-1]
    else:
        dp[i][j] = 1 + min(
            dp[i-1][j],     # delete from word1
            dp[i][j-1],     # insert into word1
            dp[i-1][j-1]    # replace
        )
    
    Time: O(m * n), Space: O(m * n)
    """
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Base cases
    for i in range(m + 1):
        dp[i][0] = i  # Delete all from word1
    for j in range(n + 1):
        dp[0][j] = j  # Insert all into word1
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],      # delete
                    dp[i][j-1],      # insert
                    dp[i-1][j-1]     # replace
                )
    
    return dp[m][n]
```

---

## 🔧 Pattern 5: Grid/2D DP

### Problem 11: Unique Paths
```python
def uniquePaths(m: int, n: int) -> int:
    """
    LeetCode #62 - Count paths from top-left to bottom-right
    
    dp[i][j] = number of paths to cell (i, j)
    
    Recurrence:
    dp[i][j] = dp[i-1][j] + dp[i][j-1]
    
    Time: O(m * n), Space: O(n) optimized
    """
    dp = [1] * n  # First row all 1s
    
    for i in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j-1]
    
    return dp[n-1]
```

### Problem 12: Minimum Path Sum
```python
def minPathSum(grid: list[list[int]]) -> int:
    """
    LeetCode #64 - Minimum sum path from top-left to bottom-right
    
    dp[i][j] = min path sum to reach (i, j)
    
    Recurrence:
    dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])
    
    Time: O(m * n), Space: O(n)
    """
    m, n = len(grid), len(grid[0])
    dp = [0] * n
    dp[0] = grid[0][0]
    
    # First row
    for j in range(1, n):
        dp[j] = dp[j-1] + grid[0][j]
    
    # Rest of grid
    for i in range(1, m):
        dp[0] += grid[i][0]  # First column
        for j in range(1, n):
            dp[j] = grid[i][j] + min(dp[j], dp[j-1])
    
    return dp[n-1]
```

---

## 🔧 Pattern 6: Palindrome DP

### Problem 13: Longest Palindromic Substring
```python
def longestPalindrome(s: str) -> str:
    """
    LeetCode #5 - Longest palindromic substring
    
    dp[i][j] = is s[i:j+1] a palindrome?
    
    Recurrence:
    dp[i][j] = s[i] == s[j] and dp[i+1][j-1]
    
    Time: O(n²), Space: O(n²)
    """
    n = len(s)
    if n < 2:
        return s
    
    dp = [[False] * n for _ in range(n)]
    start, max_len = 0, 1
    
    # Every single character is palindrome
    for i in range(n):
        dp[i][i] = True
    
    # Check substrings of length 2+
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            
            if s[i] == s[j]:
                if length == 2 or dp[i+1][j-1]:
                    dp[i][j] = True
                    start, max_len = i, length
    
    return s[start:start + max_len]
```

### Expand Around Center (Better for Substring)
```python
def longestPalindrome_expand(s: str) -> str:
    """
    Expand around center approach
    
    Time: O(n²), Space: O(1)
    """
    def expand(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return left + 1, right - 1
    
    start, end = 0, 0
    
    for i in range(len(s)):
        # Odd length palindrome
        l1, r1 = expand(i, i)
        # Even length palindrome
        l2, r2 = expand(i, i + 1)
        
        # Update if longer
        if r1 - l1 > end - start:
            start, end = l1, r1
        if r2 - l2 > end - start:
            start, end = l2, r2
    
    return s[start:end+1]
```

---

## 💡 DP Decision Tree

```
Can I break problem into smaller similar subproblems?
│
├─ YES → Do subproblems overlap?
│   │
│   ├─ YES → Use DP!
│   │   │
│   │   ├─ 1D array? (sequences, stairs, house robber)
│   │   ├─ 2D array? (grids, LCS, edit distance)
│   │   ├─ Knapsack? (subset sum, coin change)
│   │   └─ LIS/LCS? (increasing, common subsequence)
│   │
│   └─ NO → Use Divide & Conquer
│
└─ NO → Not DP (try greedy, other algorithms)
```

---

## 🐛 Common Mistakes

### Mistake 1: Wrong Base Case
```python
# ❌ WRONG
dp[0] = 1  # Should be 0 for some problems

# ✅ Think carefully about base case meaning
dp[0] = 0  # For coin change (0 coins for amount 0)
dp[0] = 1  # For climbing stairs (1 way to stay at ground)
```

### Mistake 2: 0/1 Knapsack Loop Order
```python
# ❌ WRONG - Forward iteration uses same element multiple times
for num in nums:
    for s in range(num, target + 1):
        dp[s] = dp[s] or dp[s - num]

# ✅ CORRECT - Backward iteration
for num in nums:
    for s in range(target, num - 1, -1):
        dp[s] = dp[s] or dp[s - num]
```

### Mistake 3: LCS Index Confusion
```python
# ❌ WRONG
if text1[i] == text2[j]:
    dp[i][j] = dp[i-1][j-1] + 1

# ✅ CORRECT - Remember dp is 1-indexed
if text1[i-1] == text2[j-1]:
    dp[i][j] = dp[i-1][j-1] + 1
```

---

## 🎓 Practice Problems

### Easy (Build Foundation)
1. #70 Climbing Stairs
2. #746 Min Cost Climbing Stairs
3. #198 House Robber
4. #121 Best Time to Buy/Sell Stock

### Medium (Core Patterns)
1. #322 Coin Change 🚨 **MUST DO**
2. #300 Longest Increasing Subsequence 🚨
3. #1143 Longest Common Subsequence 🚨
4. #416 Partition Equal Subset Sum (0/1 Knapsack)
5. #518 Coin Change 2 (Unbounded)
6. #62 Unique Paths
7. #64 Minimum Path Sum
8. #139 Word Break
9. #152 Maximum Product Subarray

### Hard (Master Level)
1. #72 Edit Distance 🚨
2. #354 Russian Doll Envelopes (2D LIS)
3. #312 Burst Balloons (Interval DP)
4. #1000 Minimum Cost to Merge Stones

---

**Remember:** DP is about recognizing patterns! Master the core patterns (Knapsack, LIS, LCS, Grid) and you can solve 80% of DP problems!

