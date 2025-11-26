"""
Week 8, Day 5: Matrix Chain & Interval DP

Learning Objectives:
- Master matrix chain multiplication
- Learn interval DP pattern
- Practice optimal binary search tree
- Understand burst balloons
- Solve interval-based problems

Time: 10-15 minutes
"""

# ============================================================
# EXERCISE 1: Matrix Chain Multiplication
# ============================================================

def matrix_chain_multiplication():
    """
    Minimum multiplications for matrix chain.
    
    Matrix chain: Find optimal parenthesization
    """
    print("--- Exercise 1: Matrix Chain Multiplication ---")
    
    def matrix_chain_order(dims):
        """Min scalar multiplications for chain"""
        n = len(dims) - 1  # Number of matrices
        dp = [[0] * n for _ in range(n)]
        split = [[0] * n for _ in range(n)]
        
        # length is chain length
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                dp[i][j] = float('inf')
                
                # Try all split points
                for k in range(i, j):
                    cost = (dp[i][k] + dp[k+1][j] + 
                           dims[i] * dims[k+1] * dims[j+1])
                    
                    if cost < dp[i][j]:
                        dp[i][j] = cost
                        split[i][j] = k
        
        return dp[0][n-1], split
    
    def print_optimal_parens(split, i, j):
        """Print optimal parenthesization"""
        if i == j:
            return f"A{i}"
        else:
            left = print_optimal_parens(split, i, split[i][j])
            right = print_optimal_parens(split, split[i][j] + 1, j)
            return f"({left} × {right})"
    
    # Dimensions: A1(10×30), A2(30×5), A3(5×60)
    dims = [10, 30, 5, 60]
    
    print(f"Matrix dimensions: {dims}")
    print("Matrices:")
    for i in range(len(dims) - 1):
        print(f"  A{i}: {dims[i]}×{dims[i+1]}")
    
    min_ops, split = matrix_chain_order(dims)
    parens = print_optimal_parens(split, 0, len(dims) - 2)
    
    print(f"\nMin operations: {min_ops}")
    print(f"Optimal order: {parens}")
    
    print()

# ============================================================
# EXERCISE 2: Burst Balloons
# ============================================================

def burst_balloons():
    """
    Maximum coins from bursting balloons.
    
    TODO: Interval DP - last balloon to burst
    """
    print("--- Exercise 2: Burst Balloons ---")
    
    def max_coins(nums):
        """Maximum coins from bursting balloons"""
        # Add 1s at boundaries
        nums = [1] + nums + [1]
        n = len(nums)
        dp = [[0] * n for _ in range(n)]
        
        # length is interval length
        for length in range(2, n):
            for left in range(n - length):
                right = left + length
                
                # Try bursting each balloon last in interval
                for i in range(left + 1, right):
                    coins = (nums[left] * nums[i] * nums[right] +
                            dp[left][i] + dp[i][right])
                    dp[left][right] = max(dp[left][right], coins)
        
        return dp[0][n-1]
    
    test_cases = [
        [3, 1, 5, 8],
        [1, 5],
        [3, 1, 5]
    ]
    
    for nums in test_cases:
        max_val = max_coins(nums)
        print(f"Balloons: {nums}")
        print(f"  Max coins: {max_val}\n")
    
    print()

# ============================================================
# EXERCISE 3: Minimum Cost to Merge Stones
# ============================================================

def merge_stones():
    """
    Minimum cost to merge stones into piles.
    
    TODO: Interval DP with constraints
    """
    print("--- Exercise 3: Minimum Cost to Merge Stones ---")
    
    def merge_stones_cost(stones, k):
        """Min cost to merge into k piles"""
        n = len(stones)
        
        # Check if possible
        if (n - 1) % (k - 1) != 0:
            return -1
        
        # Prefix sums for range sum
        prefix = [0]
        for stone in stones:
            prefix.append(prefix[-1] + stone)
        
        # dp[i][j][p] = min cost to merge stones[i:j+1] into p piles
        dp = [[[float('inf')] * (k + 1) for _ in range(n)] for _ in range(n)]
        
        # Base case: single stone
        for i in range(n):
            dp[i][i][1] = 0
        
        # Fill DP table
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                
                # Merge into p piles
                for p in range(2, k + 1):
                    for mid in range(i, j, k - 1):
                        dp[i][j][p] = min(
                            dp[i][j][p],
                            dp[i][mid][1] + dp[mid+1][j][p-1]
                        )
                
                # Merge p piles into 1
                dp[i][j][1] = dp[i][j][k] + prefix[j+1] - prefix[i]
        
        return dp[0][n-1][1]
    
    test_cases = [
        ([3, 2, 4, 1], 2),
        ([3, 2, 4, 1], 3),
        ([3, 5, 1, 2, 6], 3)
    ]
    
    for stones, k in test_cases:
        cost = merge_stones_cost(stones, k)
        print(f"Stones: {stones}, K: {k}")
        print(f"  Min cost: {cost}\n")
    
    print()

# ============================================================
# EXERCISE 4: Palindrome Partitioning
# ============================================================

def palindrome_partitioning():
    """
    Minimum cuts for palindrome partitioning.
    
    TODO: Interval DP for palindromes
    """
    print("--- Exercise 4: Palindrome Partitioning ---")
    
    def min_cut(s):
        """Minimum cuts to partition into palindromes"""
        n = len(s)
        
        # is_palindrome[i][j] = True if s[i:j+1] is palindrome
        is_pal = [[False] * n for _ in range(n)]
        
        # Build palindrome table
        for i in range(n):
            is_pal[i][i] = True
        
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                if s[i] == s[j]:
                    is_pal[i][j] = (length == 2 or is_pal[i+1][j-1])
        
        # dp[i] = min cuts for s[0:i+1]
        dp = [float('inf')] * n
        
        for i in range(n):
            if is_pal[0][i]:
                dp[i] = 0
            else:
                for j in range(i):
                    if is_pal[j+1][i]:
                        dp[i] = min(dp[i], dp[j] + 1)
        
        return dp[n-1]
    
    test_cases = ["aab", "a", "ab", "racecar"]
    
    for s in test_cases:
        cuts = min_cut(s)
        print(f"String: '{s}'")
        print(f"  Min cuts: {cuts}\n")
    
    print()

# ============================================================
# EXERCISE 5: Optimal Binary Search Tree
# ============================================================

def optimal_bst():
    """
    Construct optimal BST with minimum search cost.
    
    TODO: Weighted interval DP
    """
    print("--- Exercise 5: Optimal Binary Search Tree ---")
    
    def optimal_search_tree(keys, freq):
        """Min search cost for BST"""
        n = len(keys)
        dp = [[0] * n for _ in range(n)]
        
        # Prefix sums for frequency
        total = [[0] * n for _ in range(n)]
        for i in range(n):
            total[i][i] = freq[i]
            for j in range(i + 1, n):
                total[i][j] = total[i][j-1] + freq[j]
        
        # Single keys
        for i in range(n):
            dp[i][i] = freq[i]
        
        # Fill DP table
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                dp[i][j] = float('inf')
                
                # Try each key as root
                for r in range(i, j + 1):
                    left = dp[i][r-1] if r > i else 0
                    right = dp[r+1][j] if r < j else 0
                    cost = left + right + total[i][j]
                    dp[i][j] = min(dp[i][j], cost)
        
        return dp[0][n-1]
    
    keys = [10, 12, 20]
    freq = [34, 8, 50]
    
    print(f"Keys: {keys}")
    print(f"Frequencies: {freq}")
    
    min_cost = optimal_search_tree(keys, freq)
    print(f"\nMin search cost: {min_cost}")
    
    print()

# ============================================================
# EXERCISE 6: Remove Boxes
# ============================================================

def remove_boxes():
    """
    Maximum points from removing boxes.
    
    TODO: Complex interval DP
    """
    print("--- Exercise 6: Remove Boxes ---")
    
    def remove_boxes_max(boxes):
        """Max points from removing boxes"""
        n = len(boxes)
        memo = {}
        
        def dp(i, j, k):
            """Max points for boxes[i:j+1] with k boxes[i] before i"""
            if i > j:
                return 0
            if (i, j, k) in memo:
                return memo[(i, j, k)]
            
            # Optimize: merge consecutive same boxes
            while i < j and boxes[i] == boxes[i+1]:
                i += 1
                k += 1
            
            # Remove boxes[i] with k same boxes
            result = (k + 1) ** 2 + dp(i + 1, j, 0)
            
            # Try merging with later same boxes
            for m in range(i + 1, j + 1):
                if boxes[m] == boxes[i]:
                    result = max(
                        result,
                        dp(i + 1, m - 1, 0) + dp(m, j, k + 1)
                    )
            
            memo[(i, j, k)] = result
            return result
        
        return dp(0, n - 1, 0)
    
    test_cases = [
        [1, 3, 2, 2, 2, 3, 4, 3, 1],
        [1, 1, 1],
        [1, 2, 1]
    ]
    
    for boxes in test_cases:
        max_points = remove_boxes_max(boxes)
        print(f"Boxes: {boxes}")
        print(f"  Max points: {max_points}\n")
    
    print()

# ============================================================
# EXERCISE 7: Real-World Scenario - Optimal Cuts
# ============================================================

def optimal_cuts():
    """
    Minimum cost to cut a stick.
    
    TODO: Interval DP for cutting
    """
    print("--- Exercise 7: Optimal Cuts ---")
    
    def min_cost_cuts(n, cuts):
        """Minimum cost to make all cuts"""
        cuts = [0] + sorted(cuts) + [n]
        m = len(cuts)
        dp = [[0] * m for _ in range(m)]
        
        # length is interval length
        for length in range(2, m):
            for i in range(m - length):
                j = i + length
                dp[i][j] = float('inf')
                
                # Try each cut point
                for k in range(i + 1, j):
                    cost = cuts[j] - cuts[i] + dp[i][k] + dp[k][j]
                    dp[i][j] = min(dp[i][j], cost)
        
        return dp[0][m-1]
    
    test_cases = [
        (7, [1, 3, 4, 5]),
        (9, [5, 6, 1, 4, 2])
    ]
    
    for n, cuts in test_cases:
        cost = min_cost_cuts(n, cuts)
        print(f"Stick length: {n}, Cuts: {cuts}")
        print(f"  Min cost: {cost}\n")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Interval DP Complexity:
    
    Pattern:
    - Process intervals of increasing length
    - Try all split points within interval
    - Combine subproblem solutions
    
    Time Complexity:
    - Typically O(n³)
    - n² intervals × n split points
    
    Space Complexity:
    - O(n²) for DP table
    - Can't optimize easily (need all intervals)
    
    Key Characteristics:
    - Subproblems are intervals [i, j]
    - Optimal solution uses optimal subintervals
    - Process by increasing interval length
    
    Common Problems:
    - Matrix chain multiplication
    - Burst balloons
    - Palindrome partitioning
    - Optimal BST
    - Cutting problems
    
    Best Practices:
    - Start with small intervals
    - Try all split points
    - Combine subproblem costs
    - Add interval cost if needed
    
    Debugging Tips:
    - Draw interval tree
    - Check base cases
    - Verify split point logic
    - Test small examples
    
    Security Considerations:
    - Validate interval bounds
    - Check for integer overflow
    - Limit input sizes
    - Handle edge cases
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 8, Day 5: Matrix Chain & Interval DP")
    print("=" * 60)
    print()
    
    matrix_chain_multiplication()
    burst_balloons()
    merge_stones()
    palindrome_partitioning()
    optimal_bst()
    remove_boxes()
    optimal_cuts()
    
    print("=" * 60)
    print("✅ Day 5 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. Interval DP: Process by increasing length")
    print("2. Try all split points within interval")
    print("3. Typically O(n³) time, O(n²) space")
    print("4. Common pattern for optimization problems")


