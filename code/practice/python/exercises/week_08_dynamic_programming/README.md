# Week 8: Dynamic Programming

Master dynamic programming - one of the most powerful problem-solving techniques.

## Overview

This week focuses on Dynamic Programming (DP) - a method for solving complex problems by breaking them down into simpler subproblems. Learn memoization, tabulation, and various DP patterns essential for optimization problems.

## Daily Breakdown

### Day 1: Memoization (Top-Down DP)
**File:** `day1_memoization.py`

Learn top-down DP with caching:
- Recursion + memoization
- `functools.lru_cache`
- Fibonacci, climbing stairs
- House robber, coin change
- Exponential → Polynomial time

**Key Concepts:**
- Add caching to recursive solutions
- Only compute needed states
- Natural problem decomposition

---

### Day 2: Tabulation (Bottom-Up DP)
**File:** `day2_tabulation.py`

Master bottom-up DP:
- Iterative DP with tables
- Space optimization
- LCS, edit distance
- 0/1 knapsack
- No recursion overhead

**Complexity:**
- Same time as memoization
- Often better space usage
- No stack overflow risk

---

### Day 3: Knapsack Problems
**File:** `day3_knapsack_problems.py`

Master knapsack variations:
- 0/1 knapsack (each item once)
- Unbounded knapsack (unlimited items)
- Subset sum
- Partition problems
- Target sum

**Key Points:**
- Pseudo-polynomial time
- 0/1: Traverse backwards
- Unbounded: Traverse forward

---

### Day 4: String DP Problems
**File:** `day4_string_problems.py`

Solve string DP problems:
- Longest palindromic substring
- LCS vs LCS (substring)
- Wildcard & regex matching
- Distinct subsequences
- Interleaving strings

**Complexity:**
- Usually O(m × n) for two strings
- 2D DP tables common
- Space optimizable

---

### Day 5: Matrix Chain & Interval DP
**File:** `day5_matrix_chain.py`

Learn interval DP pattern:
- Matrix chain multiplication
- Burst balloons
- Palindrome partitioning
- Optimal BST
- Cutting problems

**Pattern:**
- Process by increasing interval length
- Try all split points
- Typically O(n³) time

---

### Day 6: State Machine DP
**File:** `day6_state_machine.py`

Master state-based DP:
- Stock trading (various constraints)
- Paint house
- Job scheduling
- State transitions
- Constraint encoding

**Key Concepts:**
- Define states clearly
- Track transitions
- Often O(1) space optimizable

---

### Day 7: Review & Challenge
**File:** `day7_review_challenge.py`

Apply all DP concepts:
- **Challenge 1:** Unique paths with obstacles
- **Challenge 2:** Maximum product subarray
- **Challenge 3:** Word break II
- **Challenge 4:** Russian doll envelopes
- **Challenge 5:** Maximal rectangle
- **Challenge 6:** Scramble string
- **Challenge 7:** Frog jump

---

## Quick Reference

### Memoization Template

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def dp(state):
    # Base case
    if base_condition:
        return base_value
    
    # Recursive case
    return combine(dp(next_state1), dp(next_state2))
```

### Tabulation Template

```python
def dp_tabulation(n):
    # Initialize DP table
    dp = [0] * (n + 1)
    dp[0] = base_value
    
    # Fill table
    for i in range(1, n + 1):
        dp[i] = combine(dp[i-1], dp[i-2], ...)
    
    return dp[n]
```

### 0/1 Knapsack

```python
def knapsack_01(weights, values, capacity):
    dp = [0] * (capacity + 1)
    
    for i in range(len(weights)):
        # Traverse backwards
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], values[i] + dp[w - weights[i]])
    
    return dp[capacity]
```

### Longest Common Subsequence

```python
def lcs(text1, text2):
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

---

## DP Problem Identification

**Signs of DP Problem:**
1. Overlapping subproblems
2. Optimal substructure
3. Counting/optimization
4. "Find maximum/minimum"
5. "Count number of ways"

**Common Patterns:**
- Fibonacci-like: `dp[i] = dp[i-1] + dp[i-2]`
- Decision: `max(take, skip)`
- Knapsack: Include/exclude items
- String: Match/no-match characters
- Interval: Try all split points
- State machine: Transition between states

---

## Complexity Summary

| Problem Type | Time | Space | Pattern |
|--------------|------|-------|---------|
| **Fibonacci** | O(n) | O(1)* | 1D DP |
| **Knapsack** | O(n × W) | O(W) | Pseudo-polynomial |
| **LCS** | O(m × n) | O(min(m,n))* | 2D DP |
| **Edit Distance** | O(m × n) | O(min(m,n))* | 2D DP |
| **Matrix Chain** | O(n³) | O(n²) | Interval DP |
| **Stock Trading** | O(n) | O(1)* | State machine |

*With space optimization

---

## When to Use Each Approach

| Approach | When to Use |
|----------|-------------|
| **Memoization** | Natural recursion, not all states needed |
| **Tabulation** | Avoid recursion, need all states, optimize space |
| **Greedy** | Local optimum = global optimum |
| **Divide & Conquer** | Independent subproblems |

---

## Learning Outcomes

After completing Week 8, you should be able to:

✅ Identify DP problems  
✅ Choose memoization vs tabulation  
✅ Solve knapsack variations  
✅ Handle string DP problems  
✅ Apply interval DP pattern  
✅ Model state machines  
✅ Optimize space complexity  
✅ Solve complex optimization problems  

---

## Running the Exercises

```bash
# Run individual days
python day1_memoization.py
python day2_tabulation.py
python day3_knapsack_problems.py
python day4_string_problems.py
python day5_matrix_chain.py
python day6_state_machine.py
python day7_review_challenge.py

# Run all
for day in day*.py; do python "$day"; done
```

---

## Additional Resources

**Official Documentation:**
- [functools.lru_cache](https://docs.python.org/3/library/functools.html#functools.lru_cache)

**Further Reading:**
- [Dynamic Programming](https://realpython.com/python-thinking-recursively/)
- [DP Patterns](https://leetcode.com/discuss/general-discussion/458695/dynamic-programming-patterns)

---

## Next Steps

🎯 **Week 9:** Standard Library - Text & Data  
Learn Python's powerful standard library modules.

---

## Notes

- DP is one of the most important techniques
- Practice identifying DP problems
- Start with memoization, optimize to tabulation
- Draw tables to understand state transitions
- Space optimization comes after correctness

**Time Investment:** ~10-15 minutes per day, 15-20 minutes for Day 7  
**Total:** ~90 minutes for the week

---

*Master DP and unlock powerful problem-solving! 🐍*


