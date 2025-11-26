# Backtracking - Complete Guide

## 📋 Pattern Recognition

**When to use Backtracking:**
- "Generate all possible..."
- "Find all combinations/permutations"
- "Place N items with constraints"
- "Explore all paths in decision tree"

**Keywords:** all, combinations, permutations, subsets, generate

---

## 🎯 Backtracking Template

```python
def backtrack(path, choices):
    """
    Universal backtracking template
    """
    # Base case - found valid solution
    if is_valid_solution(path):
        result.append(path[:])  # Make copy!
        return
    
    # Explore all choices
    for choice in choices:
        # Make choice
        path.append(choice)
        
        # Recurse
        backtrack(path, get_next_choices())
        
        # Undo choice (backtrack)
        path.pop()
```

---

## 🔧 Pattern 1: Subsets (Power Set)

```python
def subsets(nums: list[int]) -> list[list[int]]:
    """
    LeetCode #78
    Generate all subsets (2^n subsets)
    
    Time: O(n * 2^n), Space: O(n) recursion depth
    """
    result = []
    
    def backtrack(start, path):
        # Every path is valid - add to result
        result.append(path[:])  # MUST copy!
        
        # Try adding each remaining element
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)  # Move to next index
            path.pop()
    
    backtrack(0, [])
    return result

# Example: [1,2,3]
# Result: [[], [1], [1,2], [1,2,3], [1,3], [2], [2,3], [3]]
```

### With Duplicates
```python
def subsetsWithDup(nums: list[int]) -> list[list[int]]:
    """
    LeetCode #90
    Handle duplicates by sorting + skipping
    """
    nums.sort()  # CRITICAL: sort first!
    result = []
    
    def backtrack(start, path):
        result.append(path[:])
        
        for i in range(start, len(nums)):
            # Skip duplicates at same level
            if i > start and nums[i] == nums[i-1]:
                continue
            
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()
    
    backtrack(0, [])
    return result
```

---

## 🔧 Pattern 2: Combinations

```python
def combine(n: int, k: int) -> list[list[int]]:
    """
    LeetCode #77
    Generate all k-length combinations from [1..n]
    
    Example: n=4, k=2 → [[1,2], [1,3], [1,4], [2,3], [2,4], [3,4]]
    """
    result = []
    
    def backtrack(start, path):
        # Base case: path has k elements
        if len(path) == k:
            result.append(path[:])
            return
        
        # Optimization: prune if can't reach k elements
        need = k - len(path)
        remain = n - start + 1
        if remain < need:
            return
        
        for i in range(start, n + 1):
            path.append(i)
            backtrack(i + 1, path)
            path.pop()
    
    backtrack(1, [])
    return result
```

### Combination Sum (Elements can be reused)
```python
def combinationSum(candidates: list[int], target: int) -> list[list[int]]:
    """
    LeetCode #39
    Unlimited reuse of elements
    """
    result = []
    
    def backtrack(start, path, total):
        if total == target:
            result.append(path[:])
            return
        
        if total > target:  # Prune
            return
        
        for i in range(start, len(candidates)):
            path.append(candidates[i])
            # Note: i (not i+1) allows reuse
            backtrack(i, path, total + candidates[i])
            path.pop()
    
    backtrack(0, [], 0)
    return result
```

---

## 🔧 Pattern 3: Permutations

```python
def permute(nums: list[int]) -> list[list[int]]:
    """
    LeetCode #46
    Generate all permutations (n! permutations)
    
    Time: O(n! * n), Space: O(n)
    """
    result = []
    
    def backtrack(path):
        # Base case: all elements used
        if len(path) == len(nums):
            result.append(path[:])
            return
        
        for num in nums:
            if num in path:  # Already used
                continue
            
            path.append(num)
            backtrack(path)
            path.pop()
    
    backtrack([])
    return result
```

### Optimized with Visited Set
```python
def permute_optimized(nums: list[int]) -> list[list[int]]:
    """
    Use set for O(1) lookup instead of O(n) 'in' check
    """
    result = []
    
    def backtrack(path, used):
        if len(path) == len(nums):
            result.append(path[:])
            return
        
        for i, num in enumerate(nums):
            if i in used:
                continue
            
            path.append(num)
            used.add(i)
            
            backtrack(path, used)
            
            path.pop()
            used.remove(i)
    
    backtrack([], set())
    return result
```

---

## 🔧 Pattern 4: N-Queens 👑

```python
def solveNQueens(n: int) -> list[list[str]]:
    """
    LeetCode #51 - Classic backtracking
    Place N queens on N×N board (no attacks)
    
    Time: O(n!), Space: O(n²)
    """
    result = []
    board = [['.'] * n for _ in range(n)]
    
    # Track attacked positions
    cols = set()
    diag1 = set()  # row - col constant
    diag2 = set()  # row + col constant
    
    def backtrack(row):
        if row == n:
            # Found valid solution
            result.append([''.join(row) for row in board])
            return
        
        for col in range(n):
            # Check if position is attacked
            if (col in cols or 
                (row - col) in diag1 or 
                (row + col) in diag2):
                continue
            
            # Place queen
            board[row][col] = 'Q'
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            
            backtrack(row + 1)
            
            # Remove queen (backtrack)
            board[row][col] = '.'
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)
    
    backtrack(0)
    return result
```

---

## 🔧 Pattern 5: Word Search

```python
def exist(board: list[list[str]], word: str) -> bool:
    """
    LeetCode #79
    Find word in 2D grid (can move up/down/left/right)
    
    Time: O(m*n*4^L) where L = len(word)
    """
    rows, cols = len(board), len(board[0])
    
    def backtrack(r, c, index):
        # Found complete word
        if index == len(word):
            return True
        
        # Out of bounds or wrong char
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            board[r][c] != word[index]):
            return False
        
        # Mark as visited
        temp = board[r][c]
        board[r][c] = '#'
        
        # Explore 4 directions
        found = (backtrack(r+1, c, index+1) or
                backtrack(r-1, c, index+1) or
                backtrack(r, c+1, index+1) or
                backtrack(r, c-1, index+1))
        
        # Restore (backtrack)
        board[r][c] = temp
        
        return found
    
    # Try starting from each cell
    for r in range(rows):
        for c in range(cols):
            if backtrack(r, c, 0):
                return True
    
    return False
```

---

## 🎓 Key Problems by Pattern

**Subsets:**
- #78 Subsets
- #90 Subsets II (with duplicates)

**Combinations:**
- #77 Combinations
- #39 Combination Sum
- #40 Combination Sum II
- #216 Combination Sum III

**Permutations:**
- #46 Permutations
- #47 Permutations II
- #60 Permutation Sequence

**Board/Grid:**
- #51 N-Queens
- #79 Word Search
- #36 Valid Sudoku

---

## 🚨 Common Mistakes

1. **Forgetting to copy result:**
   ```python
   # WRONG
   result.append(path)
   
   # CORRECT
   result.append(path[:])  # or list(path)
   ```

2. **Not sorting for duplicates:**
   ```python
   # For duplicates handling
   nums.sort()  # MUST sort first!
   ```

3. **Wrong pruning condition:**
   ```python
   # Check i > start, NOT i > 0
   if i > start and nums[i] == nums[i-1]:
       continue
   ```

---

## 💡 Pro Tips

**Time Complexity:**
- Subsets: O(2^n)
- Combinations: O(C(n,k))
- Permutations: O(n!)

**Optimization strategies:**
1. Prune early (check constraints before recursing)
2. Sort input for duplicate handling
3. Use sets for O(1) lookup instead of lists

**Template decision:**
- Need ALL solutions → Backtracking
- Need OPTIMAL solution → DP or Greedy
- Need ANY solution → DFS with early return

---

**Master the template, then customize for each problem!**

