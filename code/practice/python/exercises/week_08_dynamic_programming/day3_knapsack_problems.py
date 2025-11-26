"""
Week 8, Day 3: Knapsack Problems

Learning Objectives:
- Master 0/1 knapsack problem
- Learn unbounded knapsack
- Practice subset sum
- Understand partition problems
- Solve knapsack variations

Time: 10-15 minutes
"""

# ============================================================
# EXERCISE 1: 0/1 Knapsack (Complete)
# ============================================================

def knapsack_01_complete():
    """
    Complete 0/1 knapsack with item tracking.
    
    0/1: Each item used at most once
    """
    print("--- Exercise 1: 0/1 Knapsack (Complete) ---")
    
    def knapsack(weights, values, capacity):
        """0/1 knapsack with items used"""
        n = len(weights)
        dp = [[0] * (capacity + 1) for _ in range(n + 1)]
        
        # Fill DP table
        for i in range(1, n + 1):
            for w in range(capacity + 1):
                dp[i][w] = dp[i-1][w]  # Don't take
                if weights[i-1] <= w:
                    dp[i][w] = max(
                        dp[i][w],
                        values[i-1] + dp[i-1][w - weights[i-1]]
                    )
        
        # Reconstruct items
        items = []
        w = capacity
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i-1][w]:
                items.append(i-1)
                w -= weights[i-1]
        
        return dp[n][capacity], items[::-1]
    
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    capacity = 8
    
    print(f"Items: {list(zip(weights, values))}")
    print(f"Capacity: {capacity}")
    
    max_value, items = knapsack(weights, values, capacity)
    print(f"\nMax value: {max_value}")
    print(f"Items used (indices): {items}")
    print(f"Total weight: {sum(weights[i] for i in items)}")
    
    print()

# ============================================================
# EXERCISE 2: Unbounded Knapsack
# ============================================================

def unbounded_knapsack():
    """
    Unbounded knapsack - unlimited items.
    
    TODO: Can use each item multiple times
    """
    print("--- Exercise 2: Unbounded Knapsack ---")
    
    def knapsack_unbounded(weights, values, capacity):
        """Unbounded knapsack"""
        dp = [0] * (capacity + 1)
        
        for w in range(capacity + 1):
            for i in range(len(weights)):
                if weights[i] <= w:
                    dp[w] = max(dp[w], values[i] + dp[w - weights[i]])
        
        return dp[capacity]
    
    weights = [1, 3, 4]
    values = [15, 50, 60]
    capacity = 8
    
    print(f"Items (can reuse): {list(zip(weights, values))}")
    print(f"Capacity: {capacity}")
    
    max_value = knapsack_unbounded(weights, values, capacity)
    print(f"\nMax value: {max_value}")
    
    print("\n💡 Difference from 0/1:")
    print("  • Can use each item multiple times")
    print("  • Simpler DP: dp[w] uses dp[w - weight]")
    
    print()

# ============================================================
# EXERCISE 3: Subset Sum
# ============================================================

def subset_sum():
    """
    Check if subset sums to target.
    
    TODO: Special case of 0/1 knapsack
    """
    print("--- Exercise 3: Subset Sum ---")
    
    def can_partition_sum(nums, target):
        """Check if subset sums to target"""
        dp = [False] * (target + 1)
        dp[0] = True  # Empty subset sums to 0
        
        for num in nums:
            # Traverse backwards to avoid using same element twice
            for s in range(target, num - 1, -1):
                dp[s] = dp[s] or dp[s - num]
        
        return dp[target]
    
    def find_subset(nums, target):
        """Find actual subset"""
        n = len(nums)
        dp = [[False] * (target + 1) for _ in range(n + 1)]
        
        for i in range(n + 1):
            dp[i][0] = True
        
        for i in range(1, n + 1):
            for s in range(target + 1):
                dp[i][s] = dp[i-1][s]  # Don't take
                if nums[i-1] <= s:
                    dp[i][s] = dp[i][s] or dp[i-1][s - nums[i-1]]
        
        if not dp[n][target]:
            return None
        
        # Reconstruct subset
        subset = []
        s = target
        for i in range(n, 0, -1):
            if dp[i][s] and not dp[i-1][s]:
                subset.append(nums[i-1])
                s -= nums[i-1]
        
        return subset
    
    test_cases = [
        ([3, 34, 4, 12, 5, 2], 9),
        ([1, 2, 3, 7], 6),
        ([1, 2, 5], 4)
    ]
    
    for nums, target in test_cases:
        can_sum = can_partition_sum(nums, target)
        subset = find_subset(nums, target) if can_sum else None
        print(f"Array: {nums}, Target: {target}")
        print(f"  Can sum: {can_sum}")
        if subset:
            print(f"  Subset: {subset} (sum: {sum(subset)})")
        print()
    
    print()

# ============================================================
# EXERCISE 4: Partition Equal Subset Sum
# ============================================================

def partition_equal():
    """
    Partition array into two equal sum subsets.
    
    TODO: Check if sum/2 is achievable
    """
    print("--- Exercise 4: Partition Equal Subset Sum ---")
    
    def can_partition(nums):
        """Check if can partition into equal sums"""
        total = sum(nums)
        
        # If odd sum, can't partition equally
        if total % 2 != 0:
            return False
        
        target = total // 2
        dp = [False] * (target + 1)
        dp[0] = True
        
        for num in nums:
            for s in range(target, num - 1, -1):
                dp[s] = dp[s] or dp[s - num]
        
        return dp[target]
    
    test_cases = [
        [1, 5, 11, 5],
        [1, 2, 3, 5],
        [2, 2, 1, 1]
    ]
    
    for nums in test_cases:
        can_part = can_partition(nums)
        print(f"Array: {nums} (sum: {sum(nums)})")
        print(f"  Can partition: {can_part}\n")
    
    print()

# ============================================================
# EXERCISE 5: Minimum Subset Sum Difference
# ============================================================

def min_subset_diff():
    """
    Minimize difference between two subset sums.
    
    TODO: Find closest to sum/2
    """
    print("--- Exercise 5: Minimum Subset Sum Difference ---")
    
    def min_difference(nums):
        """Minimum difference between two subsets"""
        total = sum(nums)
        target = total // 2
        
        # Find all possible sums up to target
        dp = [False] * (target + 1)
        dp[0] = True
        
        for num in nums:
            for s in range(target, num - 1, -1):
                dp[s] = dp[s] or dp[s - num]
        
        # Find largest achievable sum <= target
        for s in range(target, -1, -1):
            if dp[s]:
                # One subset has sum s, other has total - s
                return total - 2 * s
        
        return total
    
    test_cases = [
        [1, 6, 11, 5],
        [1, 2, 7],
        [3, 9, 7, 3]
    ]
    
    for nums in test_cases:
        min_diff = min_difference(nums)
        print(f"Array: {nums} (sum: {sum(nums)})")
        print(f"  Min difference: {min_diff}\n")
    
    print()

# ============================================================
# EXERCISE 6: Target Sum
# ============================================================

def target_sum():
    """
    Count ways to assign +/- to reach target.
    
    TODO: Convert to subset sum problem
    """
    print("--- Exercise 6: Target Sum ---")
    
    def find_target_sum_ways(nums, target):
        """Count ways to reach target with +/-"""
        total = sum(nums)
        
        # Check if possible
        if abs(target) > total or (total + target) % 2 != 0:
            return 0
        
        # Convert to subset sum problem
        # Let P = positive subset, N = negative subset
        # P + N = total, P - N = target
        # => P = (total + target) / 2
        subset_sum = (total + target) // 2
        
        # Count subsets with sum = subset_sum
        dp = [0] * (subset_sum + 1)
        dp[0] = 1
        
        for num in nums:
            for s in range(subset_sum, num - 1, -1):
                dp[s] += dp[s - num]
        
        return dp[subset_sum]
    
    test_cases = [
        ([1, 1, 1, 1, 1], 3),
        ([1, 2, 3], 0),
        ([1, 0], 1)
    ]
    
    for nums, target in test_cases:
        ways = find_target_sum_ways(nums, target)
        print(f"Array: {nums}, Target: {target}")
        print(f"  Ways: {ways}\n")
    
    print()

# ============================================================
# EXERCISE 7: Real-World Scenario - Budget Allocation
# ============================================================

def budget_allocation():
    """
    Maximize value within budget constraints.
    
    TODO: Multi-constraint knapsack
    """
    print("--- Exercise 7: Budget Allocation ---")
    
    def max_value_budget(projects, budget):
        """Maximize value within budget"""
        # projects = [(cost, value, name), ...]
        n = len(projects)
        dp = [0] * (budget + 1)
        selected = [[] for _ in range(budget + 1)]
        
        for i in range(n):
            cost, value, name = projects[i]
            for b in range(budget, cost - 1, -1):
                if dp[b - cost] + value > dp[b]:
                    dp[b] = dp[b - cost] + value
                    selected[b] = selected[b - cost] + [name]
        
        return dp[budget], selected[budget]
    
    projects = [
        (10, 60, "Project A"),
        (20, 100, "Project B"),
        (30, 120, "Project C"),
        (15, 80, "Project D")
    ]
    budget = 50
    
    print("Projects (cost, value):")
    for cost, value, name in projects:
        print(f"  {name}: ${cost}k, value {value}")
    
    print(f"\nBudget: ${budget}k")
    
    max_val, selected = max_value_budget(projects, budget)
    print(f"\nMax value: {max_val}")
    print(f"Selected: {selected}")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Knapsack Problems Complexity:
    
    0/1 Knapsack:
    - Time: O(n × capacity)
    - Space: O(capacity) with optimization
    - Pseudo-polynomial (depends on capacity value)
    
    Unbounded Knapsack:
    - Time: O(n × capacity)
    - Space: O(capacity)
    - Similar to 0/1 but simpler recurrence
    
    Subset Sum:
    - Time: O(n × sum)
    - Space: O(sum)
    - Special case of 0/1 knapsack
    
    NP-Complete:
    - These are NP-complete problems
    - DP gives pseudo-polynomial solution
    - Exponential in input size (bits)
    
    Space Optimization:
    - 2D → 1D array
    - Traverse backwards for 0/1
    - Forward for unbounded
    
    Variations:
    - Multiple knapsacks
    - Fractional knapsack (greedy)
    - Multi-dimensional knapsack
    - Bounded knapsack
    
    Best Practices:
    - Start with 2D for clarity
    - Optimize to 1D for space
    - Check if unbounded or 0/1
    - Consider greedy for fractional
    
    Security Considerations:
    - Validate input sizes
    - Check for integer overflow
    - Limit capacity values
    - Handle edge cases
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 8, Day 3: Knapsack Problems")
    print("=" * 60)
    print()
    
    knapsack_01_complete()
    unbounded_knapsack()
    subset_sum()
    partition_equal()
    min_subset_diff()
    target_sum()
    budget_allocation()
    
    print("=" * 60)
    print("✅ Day 3 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. 0/1: Each item once, traverse backwards")
    print("2. Unbounded: Items reusable, traverse forward")
    print("3. Subset sum: Special case of knapsack")
    print("4. Many problems reduce to knapsack")


