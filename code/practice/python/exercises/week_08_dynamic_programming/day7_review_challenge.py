"""
Week 8, Day 7: Review & Challenge - Dynamic Programming Problems

Learning Objectives:
- Review all Week 8 concepts
- Apply DP techniques to complex problems
- Practice problem identification
- Master optimization strategies
- Build complete DP solutions

Challenge: Solve advanced DP problems

Time: 15-20 minutes
"""

from functools import lru_cache

# ============================================================
# REVIEW: Week 8 Concepts
# ============================================================

def week8_review():
    """Quick review of all Week 8 concepts"""
    print("=" * 60)
    print("WEEK 8 REVIEW")
    print("=" * 60)
    
    print("\nDay 1: Memoization (Top-Down)")
    print("  • Recursion + caching")
    print("  • functools.lru_cache")
    print("  • Exponential → Polynomial")
    
    print("\nDay 2: Tabulation (Bottom-Up)")
    print("  • Iterative DP with table")
    print("  • No recursion overhead")
    print("  • Space optimization")
    
    print("\nDay 3: Knapsack Problems")
    print("  • 0/1 vs Unbounded")
    print("  • Subset sum variations")
    print("  • Pseudo-polynomial time")
    
    print("\nDay 4: String DP")
    print("  • LCS, LIS, Edit distance")
    print("  • Palindromes")
    print("  • Pattern matching")
    
    print("\nDay 5: Interval DP")
    print("  • Matrix chain multiplication")
    print("  • Burst balloons")
    print("  • O(n³) complexity")
    
    print("\nDay 6: State Machine DP")
    print("  • Stock trading problems")
    print("  • State transitions")
    print("  • Constraint encoding")
    
    print("\n" + "=" * 60)
    print()

# ============================================================
# CHALLENGE 1: Unique Paths II (with Obstacles)
# ============================================================

def unique_paths_obstacles():
    """
    Count paths in grid with obstacles.
    
    TODO: DP with constraints
    """
    print("--- Challenge 1: Unique Paths with Obstacles ---")
    
    def unique_paths(grid):
        """Count unique paths from top-left to bottom-right"""
        if not grid or grid[0][0] == 1:
            return 0
        
        m, n = len(grid), len(grid[0])
        dp = [[0] * n for _ in range(m)]
        dp[0][0] = 1
        
        # Fill first row
        for j in range(1, n):
            dp[0][j] = dp[0][j-1] if grid[0][j] == 0 else 0
        
        # Fill first column
        for i in range(1, m):
            dp[i][0] = dp[i-1][0] if grid[i][0] == 0 else 0
        
        # Fill rest
        for i in range(1, m):
            for j in range(1, n):
                if grid[i][j] == 0:
                    dp[i][j] = dp[i-1][j] + dp[i][j-1]
        
        return dp[m-1][n-1]
    
    grid = [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ]
    
    print("Grid (0=free, 1=obstacle):")
    for row in grid:
        print(f"  {row}")
    
    paths = unique_paths(grid)
    print(f"\nUnique paths: {paths}")
    
    print()

# ============================================================
# CHALLENGE 2: Maximum Product Subarray
# ============================================================

def max_product_subarray():
    """
    Find maximum product of contiguous subarray.
    
    TODO: Track both max and min (for negatives)
    """
    print("--- Challenge 2: Maximum Product Subarray ---")
    
    def max_product(nums):
        """Maximum product subarray"""
        if not nums:
            return 0
        
        max_prod = min_prod = result = nums[0]
        
        for i in range(1, len(nums)):
            if nums[i] < 0:
                max_prod, min_prod = min_prod, max_prod
            
            max_prod = max(nums[i], max_prod * nums[i])
            min_prod = min(nums[i], min_prod * nums[i])
            
            result = max(result, max_prod)
        
        return result
    
    test_cases = [
        [2, 3, -2, 4],
        [-2, 0, -1],
        [-2, 3, -4]
    ]
    
    for nums in test_cases:
        max_val = max_product(nums)
        print(f"Array: {nums}")
        print(f"  Max product: {max_val}\n")
    
    print()

# ============================================================
# CHALLENGE 3: Word Break II
# ============================================================

def word_break_ii():
    """
    Return all possible word break sentences.
    
    TODO: DP + backtracking
    """
    print("--- Challenge 3: Word Break II ---")
    
    def word_break(s, word_dict):
        """Return all possible sentences"""
        word_set = set(word_dict)
        
        @lru_cache(maxsize=None)
        def backtrack(start):
            """Find all sentences from start"""
            if start == len(s):
                return [[]]
            
            sentences = []
            for end in range(start + 1, len(s) + 1):
                word = s[start:end]
                if word in word_set:
                    for rest in backtrack(end):
                        sentences.append([word] + rest)
            
            return sentences
        
        result = backtrack(0)
        return [' '.join(sentence) for sentence in result]
    
    s = "catsanddog"
    word_dict = ["cat", "cats", "and", "sand", "dog"]
    
    print(f"String: '{s}'")
    print(f"Dictionary: {word_dict}")
    
    sentences = word_break(s, word_dict)
    print("\nPossible sentences:")
    for sentence in sentences:
        print(f"  '{sentence}'")
    
    print()

# ============================================================
# CHALLENGE 4: Russian Doll Envelopes
# ============================================================

def russian_doll_envelopes():
    """
    Maximum envelopes that can be nested.
    
    TODO: 2D LIS problem
    """
    print("--- Challenge 4: Russian Doll Envelopes ---")
    
    def max_envelopes(envelopes):
        """Max envelopes that can be nested"""
        if not envelopes:
            return 0
        
        # Sort by width asc, height desc
        envelopes.sort(key=lambda x: (x[0], -x[1]))
        
        # LIS on heights
        def lis_length(nums):
            from bisect import bisect_left
            dp = []
            for num in nums:
                pos = bisect_left(dp, num)
                if pos == len(dp):
                    dp.append(num)
                else:
                    dp[pos] = num
            return len(dp)
        
        heights = [h for _, h in envelopes]
        return lis_length(heights)
    
    envelopes = [[5, 4], [6, 4], [6, 7], [2, 3]]
    
    print(f"Envelopes (width, height): {envelopes}")
    max_count = max_envelopes(envelopes)
    print(f"  Max nested: {max_count}")
    
    print()

# ============================================================
# CHALLENGE 5: Maximal Rectangle
# ============================================================

def maximal_rectangle():
    """
    Largest rectangle in binary matrix.
    
    TODO: DP + stack for histogram
    """
    print("--- Challenge 5: Maximal Rectangle ---")
    
    def max_rectangle(matrix):
        """Largest rectangle area"""
        if not matrix or not matrix[0]:
            return 0
        
        def largest_rectangle_histogram(heights):
            """Largest rectangle in histogram"""
            stack = []
            max_area = 0
            heights = heights + [0]
            
            for i, h in enumerate(heights):
                while stack and heights[stack[-1]] > h:
                    height = heights[stack.pop()]
                    width = i if not stack else i - stack[-1] - 1
                    max_area = max(max_area, height * width)
                stack.append(i)
            
            return max_area
        
        m, n = len(matrix), len(matrix[0])
        heights = [0] * n
        max_area = 0
        
        for i in range(m):
            for j in range(n):
                heights[j] = heights[j] + 1 if matrix[i][j] == '1' else 0
            max_area = max(max_area, largest_rectangle_histogram(heights))
        
        return max_area
    
    matrix = [
        ["1", "0", "1", "0", "0"],
        ["1", "0", "1", "1", "1"],
        ["1", "1", "1", "1", "1"],
        ["1", "0", "0", "1", "0"]
    ]
    
    print("Matrix:")
    for row in matrix:
        print(f"  {row}")
    
    max_area = max_rectangle(matrix)
    print(f"\nMaximal rectangle area: {max_area}")
    
    print()

# ============================================================
# CHALLENGE 6: Scramble String
# ============================================================

def scramble_string():
    """
    Check if s2 is scrambled version of s1.
    
    TODO: Interval DP with recursion
    """
    print("--- Challenge 6: Scramble String ---")
    
    def is_scramble(s1, s2):
        """Check if s2 is scramble of s1"""
        if s1 == s2:
            return True
        if sorted(s1) != sorted(s2):
            return False
        
        @lru_cache(maxsize=None)
        def helper(s1, s2):
            if s1 == s2:
                return True
            if sorted(s1) != sorted(s2):
                return False
            
            n = len(s1)
            for i in range(1, n):
                # No swap
                if helper(s1[:i], s2[:i]) and helper(s1[i:], s2[i:]):
                    return True
                # Swap
                if helper(s1[:i], s2[n-i:]) and helper(s1[i:], s2[:n-i]):
                    return True
            
            return False
        
        return helper(s1, s2)
    
    test_cases = [
        ("great", "rgeat"),
        ("abcde", "caebd"),
        ("a", "a")
    ]
    
    for s1, s2 in test_cases:
        result = is_scramble(s1, s2)
        print(f"S1: '{s1}', S2: '{s2}'")
        print(f"  Is scramble: {result}\n")
    
    print()

# ============================================================
# CHALLENGE 7: Frog Jump
# ============================================================

def frog_jump():
    """
    Check if frog can cross river.
    
    TODO: DP with state = (position, last_jump)
    """
    print("--- Challenge 7: Frog Jump ---")
    
    def can_cross(stones):
        """Check if frog can cross"""
        stone_set = set(stones)
        memo = {}
        
        def jump(pos, k):
            """Can reach end from pos with last jump k"""
            if pos == stones[-1]:
                return True
            if (pos, k) in memo:
                return memo[(pos, k)]
            
            # Try jumps of k-1, k, k+1
            for next_k in [k - 1, k, k + 1]:
                if next_k > 0:
                    next_pos = pos + next_k
                    if next_pos in stone_set:
                        if jump(next_pos, next_k):
                            memo[(pos, k)] = True
                            return True
            
            memo[(pos, k)] = False
            return False
        
        return jump(0, 0)
    
    test_cases = [
        [0, 1, 3, 5, 6, 8, 12, 17],
        [0, 1, 2, 3, 4, 8, 9, 11]
    ]
    
    for stones in test_cases:
        can = can_cross(stones)
        print(f"Stones: {stones}")
        print(f"  Can cross: {can}\n")
    
    print()

# ============================================================
# SELF-ASSESSMENT
# ============================================================

def self_assessment():
    """Self-assessment checklist for Week 8"""
    print("=" * 60)
    print("WEEK 8 SELF-ASSESSMENT")
    print("=" * 60)
    
    checklist = [
        ("Memoization", "Can you add caching to recursive solutions?"),
        ("Tabulation", "Can you build DP tables iteratively?"),
        ("Knapsack", "Do you understand 0/1 vs unbounded?"),
        ("String DP", "Can you solve LCS, edit distance?"),
        ("Interval DP", "Can you process intervals optimally?"),
        ("State Machine", "Can you model states and transitions?"),
        ("Problem ID", "Can you identify DP problems?"),
    ]
    
    print("\nRate yourself (1-5) on these concepts:\n")
    for i, (topic, question) in enumerate(checklist, 1):
        print(f"{i}. {topic}")
        print(f"   {question}")
        print()
    
    print("=" * 60)
    print()

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 8, Day 7: Review & Challenge")
    print("=" * 60)
    print()
    
    week8_review()
    
    print("\n" + "=" * 60)
    print("CHALLENGES")
    print("=" * 60 + "\n")
    
    unique_paths_obstacles()
    max_product_subarray()
    word_break_ii()
    russian_doll_envelopes()
    maximal_rectangle()
    scramble_string()
    frog_jump()
    
    self_assessment()
    
    print("=" * 60)
    print("✅ Week 8 Complete!")
    print("=" * 60)
    print("\n🎉 Congratulations! You've mastered Dynamic Programming!")
    print("\n📚 Next: Week 9 - Standard Library (Text & Data)")
    print("\n💡 DP is one of the most powerful techniques!")


