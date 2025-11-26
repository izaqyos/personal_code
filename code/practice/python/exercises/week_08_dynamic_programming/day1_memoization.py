"""
Week 8, Day 1: Memoization (Top-Down DP)

Learning Objectives:
- Understand memoization concept
- Learn top-down dynamic programming
- Practice recursive solutions with caching
- Use functools.lru_cache
- Solve problems with overlapping subproblems

Time: 10-15 minutes
"""

from functools import lru_cache
import time

# ============================================================
# EXERCISE 1: Fibonacci with Memoization
# ============================================================

def fibonacci_comparison():
    """
    Compare naive vs memoized Fibonacci.
    
    Fibonacci: Classic DP problem
    """
    print("--- Exercise 1: Fibonacci Comparison ---")
    
    # Naive recursive (exponential)
    def fib_naive(n):
        """Naive Fibonacci - O(2^n)"""
        if n <= 1:
            return n
        return fib_naive(n - 1) + fib_naive(n - 2)
    
    # Memoized (manual)
    def fib_memo(n, memo=None):
        """Memoized Fibonacci - O(n)"""
        if memo is None:
            memo = {}
        
        if n in memo:
            return memo[n]
        
        if n <= 1:
            return n
        
        memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
        return memo[n]
    
    # Using lru_cache
    @lru_cache(maxsize=None)
    def fib_lru(n):
        """Fibonacci with lru_cache - O(n)"""
        if n <= 1:
            return n
        return fib_lru(n - 1) + fib_lru(n - 2)
    
    n = 35
    
    print(f"Computing Fibonacci({n}):")
    
    start = time.perf_counter()
    result_naive = fib_naive(n)
    time_naive = time.perf_counter() - start
    print(f"  Naive: {result_naive} ({time_naive:.4f}s)")
    
    start = time.perf_counter()
    result_memo = fib_memo(n)
    time_memo = time.perf_counter() - start
    print(f"  Memoized: {result_memo} ({time_memo:.6f}s)")
    
    start = time.perf_counter()
    result_lru = fib_lru(n)
    time_lru = time.perf_counter() - start
    print(f"  LRU Cache: {result_lru} ({time_lru:.6f}s)")
    
    print(f"\n💡 Speedup: {time_naive / time_memo:.0f}x faster!")
    
    print()

# ============================================================
# EXERCISE 2: functools.lru_cache
# ============================================================

def lru_cache_demo():
    """
    Learn functools.lru_cache decorator.
    
    TODO: Use built-in memoization
    """
    print("--- Exercise 2: functools.lru_cache ---")
    
    @lru_cache(maxsize=128)
    def expensive_function(n):
        """Simulate expensive computation"""
        print(f"  Computing for n={n}...")
        time.sleep(0.1)  # Simulate work
        return n * n
    
    print("First calls (cache misses):")
    for i in [1, 2, 3, 1, 2]:
        result = expensive_function(i)
        print(f"    f({i}) = {result}")
    
    print("\nCache info:")
    print(f"  {expensive_function.cache_info()}")
    
    print("\n💡 lru_cache:")
    print("  • maxsize=None: Unlimited cache")
    print("  • maxsize=128: LRU eviction (default)")
    print("  • Automatic memoization")
    
    print()

# ============================================================
# EXERCISE 3: Climbing Stairs
# ============================================================

def climbing_stairs():
    """
    Count ways to climb n stairs.
    
    TODO: Can climb 1 or 2 steps at a time
    """
    print("--- Exercise 3: Climbing Stairs ---")
    
    @lru_cache(maxsize=None)
    def climb_stairs(n):
        """Count ways to climb n stairs"""
        if n <= 2:
            return n
        return climb_stairs(n - 1) + climb_stairs(n - 2)
    
    def climb_stairs_manual(n, memo=None):
        """Manual memoization"""
        if memo is None:
            memo = {}
        
        if n in memo:
            return memo[n]
        
        if n <= 2:
            return n
        
        memo[n] = climb_stairs_manual(n - 1, memo) + climb_stairs_manual(n - 2, memo)
        return memo[n]
    
    for n in [5, 10, 20]:
        ways = climb_stairs(n)
        print(f"Stairs: {n}, Ways: {ways}")
    
    print("\n💡 Similar to Fibonacci!")
    
    print()

# ============================================================
# EXERCISE 4: House Robber
# ============================================================

def house_robber():
    """
    Maximum money robbing non-adjacent houses.
    
    TODO: Cannot rob adjacent houses
    """
    print("--- Exercise 4: House Robber ---")
    
    def rob(houses):
        """Maximum money from non-adjacent houses"""
        @lru_cache(maxsize=None)
        def rob_from(i):
            """Max money from index i onwards"""
            if i >= len(houses):
                return 0
            
            # Rob this house + skip next, or skip this house
            return max(
                houses[i] + rob_from(i + 2),  # Rob
                rob_from(i + 1)                # Skip
            )
        
        return rob_from(0)
    
    test_cases = [
        [1, 2, 3, 1],
        [2, 7, 9, 3, 1],
        [5, 3, 4, 11, 2]
    ]
    
    for houses in test_cases:
        max_money = rob(houses)
        print(f"Houses: {houses}")
        print(f"  Max money: ${max_money}\n")
    
    print()

# ============================================================
# EXERCISE 5: Longest Increasing Subsequence Length
# ============================================================

def lis_length():
    """
    Find length of longest increasing subsequence.
    
    TODO: Use memoization for LIS
    """
    print("--- Exercise 5: LIS Length ---")
    
    def length_of_lis(nums):
        """Length of longest increasing subsequence"""
        @lru_cache(maxsize=None)
        def dp(i, prev):
            """LIS from index i with previous value"""
            if i == len(nums):
                return 0
            
            # Skip current
            skip = dp(i + 1, prev)
            
            # Take current if valid
            take = 0
            if nums[i] > prev:
                take = 1 + dp(i + 1, nums[i])
            
            return max(skip, take)
        
        return dp(0, float('-inf'))
    
    test_cases = [
        [10, 9, 2, 5, 3, 7, 101, 18],
        [0, 1, 0, 3, 2, 3],
        [7, 7, 7, 7, 7]
    ]
    
    for nums in test_cases:
        length = length_of_lis(nums)
        print(f"Array: {nums}")
        print(f"  LIS length: {length}\n")
    
    print()

# ============================================================
# EXERCISE 6: Coin Change (Minimum Coins)
# ============================================================

def coin_change():
    """
    Minimum coins to make amount.
    
    TODO: Use memoization for coin change
    """
    print("--- Exercise 6: Coin Change ---")
    
    def min_coins(coins, amount):
        """Minimum coins to make amount"""
        @lru_cache(maxsize=None)
        def dp(remaining):
            """Min coins for remaining amount"""
            if remaining == 0:
                return 0
            if remaining < 0:
                return float('inf')
            
            min_count = float('inf')
            for coin in coins:
                count = dp(remaining - coin)
                if count != float('inf'):
                    min_count = min(min_count, count + 1)
            
            return min_count
        
        result = dp(amount)
        return result if result != float('inf') else -1
    
    test_cases = [
        ([1, 2, 5], 11),
        ([2], 3),
        ([1, 3, 4], 6)
    ]
    
    for coins, amount in test_cases:
        min_count = min_coins(coins, amount)
        print(f"Coins: {coins}, Amount: {amount}")
        print(f"  Min coins: {min_count}\n")
    
    print()

# ============================================================
# EXERCISE 7: Real-World Scenario - Text Justification Cost
# ============================================================

def text_justification():
    """
    Minimum cost to justify text.
    
    TODO: Calculate optimal line breaks
    """
    print("--- Exercise 7: Text Justification ---")
    
    def min_cost(words, max_width):
        """Minimum cost to justify text"""
        n = len(words)
        
        @lru_cache(maxsize=None)
        def dp(i):
            """Min cost from word i onwards"""
            if i == n:
                return 0
            
            min_cost_val = float('inf')
            line_length = 0
            
            # Try putting words i, i+1, ..., j on same line
            for j in range(i, n):
                if j > i:
                    line_length += 1  # Space
                line_length += len(words[j])
                
                if line_length > max_width:
                    break
                
                # Cost = (spaces left)^2 + cost of rest
                spaces_left = max_width - line_length
                cost = spaces_left ** 2
                
                # Last line has no cost
                if j == n - 1:
                    cost = 0
                
                min_cost_val = min(min_cost_val, cost + dp(j + 1))
            
            return min_cost_val
        
        return dp(0)
    
    words = ["This", "is", "an", "example", "of", "text"]
    max_width = 16
    
    print(f"Words: {words}")
    print(f"Max width: {max_width}")
    cost = min_cost(words, max_width)
    print(f"Min cost: {cost}")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    Memoization (Top-Down DP):
    - Time: O(states × work per state)
    - Space: O(states) for cache + O(depth) for recursion
    
    Without Memoization:
    - Fibonacci: O(2^n) → With memo: O(n)
    - Exponential → Polynomial
    
    When to Use:
    - Overlapping subproblems
    - Optimal substructure
    - Natural recursive formulation
    
    Advantages:
    - Easy to implement (add cache)
    - Only computes needed states
    - Natural problem decomposition
    
    Disadvantages:
    - Recursion depth limit
    - Function call overhead
    - May use more space than tabulation
    
    Best Practices:
    - Use lru_cache for simplicity
    - Consider recursion depth
    - Clear cache when needed
    - Document state meaning
    
    Common Patterns:
    - Fibonacci-like: f(n) = f(n-1) + f(n-2)
    - Decision: max(take, skip)
    - Optimization: min/max over choices
    
    Security Considerations:
    - Limit recursion depth
    - Validate inputs
    - Clear cache for sensitive data
    - Consider memory limits
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 8, Day 1: Memoization (Top-Down DP)")
    print("=" * 60)
    print()
    
    fibonacci_comparison()
    lru_cache_demo()
    climbing_stairs()
    house_robber()
    lis_length()
    coin_change()
    text_justification()
    
    print("=" * 60)
    print("✅ Day 1 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. Memoization = recursion + caching")
    print("2. Use functools.lru_cache for easy memoization")
    print("3. Converts exponential to polynomial time")
    print("4. Perfect for overlapping subproblems")

