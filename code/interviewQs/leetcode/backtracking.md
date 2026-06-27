# Backtracking — Problem Bank & Study Notes

## Study Notes (offline reference)

### The universal template
```
def backtrack(state, choices):
    if goal(state): record copy of state; return
    for choice in valid(choices):
        apply(choice)            # choose
        backtrack(...)           # explore
        undo(choice)             # unchoose — the defining move
```
Backtracking = DFS over a decision tree where you UNDO on the way back up. Record results with a COPY (`path[:]`) — appending the live list is the classic bug.

### The combinatorial trio (drill all three)
- **Subsets (LC 78)** — at each index: include or skip. Or: for-loop from `start`, recurse with `i+1`, record EVERY node (not just leaves). 2ⁿ subsets.
- **Permutations (LC 46)** — order matters; loop over ALL unused elements (used-set or in-place swap). n! leaves.
- **Combinations (LC 77)** — like subsets but fixed length k; prune when remaining elements can't fill k.

### Dedup on sorted input (subsets II, permutations II, combo-sum II)
Sort first; at the SAME tree depth skip an element equal to its left sibling:
`if i > start and a[i] == a[i-1]: continue`. This kills duplicate branches while keeping duplicate USES along one path (depth direction stays legal).

### Other patterns
- **Combination Sum (LC 39)** — reuse allowed → recurse with `i` (not `i+1`); subtract from remaining target, prune when negative (sorted input lets you `break`).
- **Grid + visited unmark** — Word Search: DFS 4 directions, mark the cell (in-place `'#'`), recurse, RESTORE. The restore is the backtrack.
- **Constraint placement** — N-Queens: row-by-row; O(1) attack checks via sets of cols, diag (r−c), anti-diag (r+c). Sudoku: same idea with row/col/box sets.
- **Partitioning** — Palindrome Partitioning: choose where the next cut ends; precompute palindrome checks if needed.

### Complexity & pruning
Exponential by nature (2ⁿ, n!, k^n) — acceptable because constraints are tiny (n ≤ ~20). Pruning order: fail fast (check validity BEFORE recursing), sort to enable early `break`, prune by remaining-count arithmetic.

### Pitfalls
- `result.append(path)` instead of `path[:]` — all results end up identical/empty.
- Dedup guard `i > start` (same depth) vs `i > 0` (kills legal reuse) — know the difference.
- Forgetting to restore grid/visited state on ALL return paths (early returns included).

## Easy
- Binary Watch (LC 401)

## Medium
- Subsets (LC 78)
- Subsets II (LC 90)
- Permutations (LC 46)
- Permutations II (LC 47)
- Combinations (LC 77)
- Combination Sum (LC 39)
- Combination Sum II (LC 40)
- Letter Combinations of a Phone Number (LC 17)
- Word Search (LC 79)
- Palindrome Partitioning (LC 131)
- Generate Parentheses (LC 22)
- Restore IP Addresses (LC 93)

## Hard
- N-Queens (LC 51)
- Sudoku Solver (LC 37)
- Word Search II (LC 212) — better with a Trie; cross-listed in tries.md
- Expression Add Operators (LC 282)

## Solve Log

| Date | Problem | LC# | Difficulty | Result | Hints | Time-Space | Notes |
|------|---------|-----|------------|--------|-------|------------|-------|
