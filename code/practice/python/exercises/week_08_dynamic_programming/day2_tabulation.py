"""
Week 8, Day 2: Tabulation (Bottom-Up DP)

Learning Objectives:
- Understand tabulation concept
- Learn bottom-up dynamic programming
- Practice iterative DP solutions
- Compare with memoization
- Solve problems with DP tables

Time: 10-15 minutes
"""

# ============================================================
# EXERCISE 1: Fibonacci with Tabulation
# ============================================================

def fibonacci_tabulation():
    """
    Fibonacci using tabulation (bottom-up).
    
    Tabulation: Build table from base cases up
    """
    print("--- Exercise 1: Fibonacci Tabulation ---")
    
    def fib_table(n):
        """Tabulation - O(n) time, O(n) space"""
        if n <= 1:
            return n
        
        dp = [0] * (n + 1)
        dp[1] = 1
        
        for i in range(2, n + 1):
            dp[i] = dp[i-1] + dp[i-2]
        
        return dp[n]
    
    def fib_optimized(n):
        """Space-optimized - O(n) time, O(1) space"""
        if n <= 1:
            return n
        
        prev2, prev1 = 0, 1
        
        for _ in range(2, n + 1):
            current = prev1 + prev2
            prev2, prev1 = prev1, current
        
        return prev1
    
    for n in [10, 20, 30]:
        result = fib_table(n)
        result_opt = fib_optimized(n)
        print(f"fib({n}) = {result} (optimized: {result_opt})")
    
    print("\n💡 Tabulation: Iterative, no recursion")
    print("💡 Can optimize space by keeping only needed values")
    
    print()

# ============================================================
# EXERCISE 2: Climbing Stairs (Tabulation)
# ============================================================

def climbing_stairs_tabulation():
    """
    Count ways to climb stairs (bottom-up).
    
    TODO: Build DP table iteratively
    """
    print("--- Exercise 2: Climbing Stairs (Tabulation) ---")
    
    def climb_stairs(n):
        """Tabulation approach"""
        if n <= 2:
            return n
        
        dp = [0] * (n + 1)
        dp[1] = 1
        dp[2] = 2
        
        for i in range(3, n + 1):
            dp[i] = dp[i-1] + dp[i-2]
        
        return dp[n]
    
    def climb_stairs_optimized(n):
        """Space-optimized"""
        if n <= 2:
            return n
        
        prev2, prev1 = 1, 2
        
        for _ in range(3, n + 1):
            current = prev1 + prev2
            prev2, prev1 = prev1, current
        
        return prev1
    
    for n in [5, 10, 20]:
        ways = climb_stairs(n)
        print(f"Stairs: {n}, Ways: {ways}")
    
    print()

# ============================================================
# EXERCISE 3: House Robber (Tabulation)
# ============================================================

def house_robber_tabulation():
    """
    Maximum money robbing (bottom-up).
    
    TODO: Build DP table for house robber
    """
    print("--- Exercise 3: House Robber (Tabulation) ---")
    
    def rob(houses):
        """Tabulation approach"""
        if not houses:
            return 0
        if len(houses) == 1:
            return houses[0]
        
        n = len(houses)
        dp = [0] * n
        dp[0] = houses[0]
        dp[1] = max(houses[0], houses[1])
        
        for i in range(2, n):
            dp[i] = max(dp[i-1], houses[i] + dp[i-2])
        
        return dp[n-1]
    
    def rob_optimized(houses):
        """Space-optimized"""
        if not houses:
            return 0
        if len(houses) == 1:
            return houses[0]
        
        prev2 = houses[0]
        prev1 = max(houses[0], houses[1])
        
        for i in range(2, len(houses)):
            current = max(prev1, houses[i] + prev2)
            prev2, prev1 = prev1, current
        
        return prev1
    
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
# EXERCISE 4: Longest Common Subsequence
# ============================================================

def longest_common_subsequence():
    """
    Find LCS length using tabulation.
    
    TODO: 2D DP table for LCS
    """
    print("--- Exercise 4: Longest Common Subsequence ---")
    
    def lcs(text1, text2):
        """LCS using tabulation"""
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i-1] == text2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        return dp[m][n]
    
    def lcs_with_string(text1, text2):
        """LCS with actual subsequence"""
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i-1] == text2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        # Reconstruct LCS
        lcs_str = []
        i, j = m, n
        while i > 0 and j > 0:
            if text1[i-1] == text2[j-1]:
                lcs_str.append(text1[i-1])
                i -= 1
                j -= 1
            elif dp[i-1][j] > dp[i][j-1]:
                i -= 1
            else:
                j -= 1
        
        return dp[m][n], ''.join(reversed(lcs_str))
    
    test_cases = [
        ("abcde", "ace"),
        ("abc", "abc"),
        ("abc", "def")
    ]
    
    for text1, text2 in test_cases:
        length, subsequence = lcs_with_string(text1, text2)
        print(f"Text1: '{text1}', Text2: '{text2}'")
        print(f"  LCS: '{subsequence}' (length: {length})\n")
    
    print()

# ============================================================
# EXERCISE 5: 0/1 Knapsack
# ============================================================

def knapsack_01():
    """
    0/1 Knapsack problem with tabulation.
    
    TODO: 2D DP for knapsack
    """
    print("--- Exercise 5: 0/1 Knapsack ---")
    
    def knapsack(weights, values, capacity):
        """0/1 Knapsack using tabulation"""
        n = len(weights)
        dp = [[0] * (capacity + 1) for _ in range(n + 1)]
        
        for i in range(1, n + 1):
            for w in range(capacity + 1):
                # Don't take item i-1
                dp[i][w] = dp[i-1][w]
                
                # Take item i-1 if it fits
                if weights[i-1] <= w:
                    dp[i][w] = max(
                        dp[i][w],
                        values[i-1] + dp[i-1][w - weights[i-1]]
                    )
        
        return dp[n][capacity]
    
    def knapsack_optimized(weights, values, capacity):
        """Space-optimized (1D array)"""
        n = len(weights)
        dp = [0] * (capacity + 1)
        
        for i in range(n):
            # Traverse backwards to avoid using updated values
            for w in range(capacity, weights[i] - 1, -1):
                dp[w] = max(dp[w], values[i] + dp[w - weights[i]])
        
        return dp[capacity]
    
    weights = [1, 3, 4, 5]
    values = [1, 4, 5, 7]
    capacity = 7
    
    print(f"Weights: {weights}")
    print(f"Values: {values}")
    print(f"Capacity: {capacity}")
    
    max_value = knapsack(weights, values, capacity)
    print(f"\nMax value: {max_value}")
    
    print()

# ============================================================
# EXERCISE 6: Coin Change (Count Ways)
# ============================================================

def coin_change_ways():
    """
    Count ways to make amount with coins.
    
    TODO: Tabulation for counting combinations
    """
    print("--- Exercise 6: Coin Change (Count Ways) ---")
    
    def count_ways(coins, amount):
        """Count ways to make amount"""
        dp = [0] * (amount + 1)
        dp[0] = 1  # One way to make 0
        
        for coin in coins:
            for i in range(coin, amount + 1):
                dp[i] += dp[i - coin]
        
        return dp[amount]
    
    test_cases = [
        ([1, 2, 5], 5),
        ([2], 3),
        ([1, 2, 3], 4)
    ]
    
    for coins, amount in test_cases:
        ways = count_ways(coins, amount)
        print(f"Coins: {coins}, Amount: {amount}")
        print(f"  Ways: {ways}\n")
    
    print()

# ============================================================
# EXERCISE 7: Edit Distance
# ============================================================

def edit_distance():
    """
    Minimum edits to convert one string to another.
    
    TODO: 2D DP for edit distance
    """
    print("--- Exercise 7: Edit Distance ---")
    
    def min_distance(word1, word2):
        """Minimum edit distance (Levenshtein)"""
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        # Base cases
        for i in range(m + 1):
            dp[i][0] = i  # Delete all
        for j in range(n + 1):
            dp[0][j] = j  # Insert all
        
        # Fill table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i-1] == word2[j-1]:
                    dp[i][j] = dp[i-1][j-1]  # No operation
                else:
                    dp[i][j] = 1 + min(
                        dp[i-1][j],      # Delete
                        dp[i][j-1],      # Insert
                        dp[i-1][j-1]     # Replace
                    )
        
        return dp[m][n]
    
    test_cases = [
        ("horse", "ros"),
        ("intention", "execution"),
        ("kitten", "sitting")
    ]
    
    for word1, word2 in test_cases:
        distance = min_distance(word1, word2)
        print(f"'{word1}' -> '{word2}'")
        print(f"  Edit distance: {distance}\n")
    
    print()

# ============================================================
# MEMOIZATION VS TABULATION
# ============================================================

def memo_vs_tabulation():
    """
    Compare memoization and tabulation.
    """
    print("--- Memoization vs Tabulation ---")
    
    print("=" * 60)
    print("COMPARISON")
    print("=" * 60)
    
    comparison = [
        ("Aspect", "Memoization (Top-Down)", "Tabulation (Bottom-Up)"),
        ("Approach", "Recursive", "Iterative"),
        ("Direction", "Top-down", "Bottom-up"),
        ("Space", "O(states) + O(depth)", "O(states)"),
        ("Overhead", "Function calls", "Loops"),
        ("Compute", "Only needed states", "All states"),
        ("Implementation", "Easier (add cache)", "More planning"),
        ("Stack overflow", "Possible", "No"),
    ]
    
    print()
    for row in comparison:
        print(f"{row[0]:<18} {row[1]:<25} {row[2]:<25}")
    
    print("\n" + "=" * 60)
    
    print("\n💡 When to use:")
    print("  • Memoization: Natural recursion, not all states needed")
    print("  • Tabulation: Avoid recursion, need all states, optimize space")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Tabulation complexity analysis.
    
    Time Complexity:
    - Same as memoization: O(states × work per state)
    - No recursion overhead
    
    Space Complexity:
    - O(states) for DP table
    - No recursion stack
    - Can often optimize to O(1) or O(n)
    
    Advantages:
    - No recursion depth limit
    - No function call overhead
    - Easier to optimize space
    - All states computed
    
    Disadvantages:
    - Less intuitive
    - Must determine order
    - Computes all states (even unneeded)
    
    Space Optimization:
    - Keep only needed rows/columns
    - Use rolling arrays
    - Fibonacci: O(n) → O(1)
    - 2D DP: O(m×n) → O(min(m,n))
    
    Best Practices:
    - Start with memoization
    - Convert to tabulation if needed
    - Optimize space after correctness
    - Document table meaning
    
    Common Patterns:
    - 1D: dp[i] depends on dp[i-1], dp[i-2]
    - 2D: dp[i][j] depends on neighbors
    - Fill order: left-to-right, top-to-bottom
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 8, Day 2: Tabulation (Bottom-Up DP)")
    print("=" * 60)
    print()
    
    fibonacci_tabulation()
    climbing_stairs_tabulation()
    house_robber_tabulation()
    longest_common_subsequence()
    knapsack_01()
    coin_change_ways()
    edit_distance()
    memo_vs_tabulation()
    
    print("=" * 60)
    print("✅ Day 2 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. Tabulation = iterative DP with table")
    print("2. No recursion, no stack overflow")
    print("3. Can optimize space efficiently")
    print("4. Choose based on problem and constraints")


