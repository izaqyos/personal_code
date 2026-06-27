# Dynamic Programming — Problem Bank & Study Notes

## Study Notes (offline reference)

### The 5-question framework (answer these before any code)
1. **State** — what does `dp[i]` (or `dp[i][j]`) MEAN, in one sentence?
2. **Transition** — how does a state derive from smaller states?
3. **Base cases** — which states are known directly?
4. **Order** — what fill order guarantees dependencies are ready?
5. **Answer** — which cell holds it (last? max over all? dp[0]?)

Memoization (top-down, `@cache` on recursion) and tabulation (bottom-up loops) are the same math; memoize when the state space is sparse or the recursion is natural, tabulate when you want space compression.

### Canonical families
- **1D linear** — climb stairs / house robber: `dp[i] = best(dp[i-1], dp[i-2] + gain)`. Usually compresses to two scalars. Decode-ways adds validity guards on 1- and 2-char reads.
- **2D grid paths** — unique paths / min path sum: `dp[r][c]` from top/left. Compresses to one row.
- **Two-sequence (alignment)** — edit distance / LCS / interleaving: `dp[i][j]` over prefixes of both strings. Match → diagonal; else 1 + best of (insert, delete, replace). Indexing trap: `dp[i][j]` describes prefixes of length i,j → chars are `s[i-1], t[j-1]`.
- **0/1 knapsack** — subset-sum / partition / target-sum: `dp[j] |= dp[j - item]`, iterating items outer, capacity INNER and BACKWARD (forward = unbounded knapsack = coin change permutations; direction IS the semantics).
- **Unbounded knapsack** — coin change: capacity forward. Min-coins vs count-ways differ only in the combine op.
- **Intervals on a string/array** — palindromic substrings (expand-around-center beats DP here), longest palindromic subsequence, burst balloons / cut stick: `dp[i][j]` over subranges, length-increasing fill order, pick the LAST operation in the range as the split.
- **LIS** — O(n²) `dp[i] = 1 + max(dp[j] for j<i, a[j]<a[i])`; better: patience sorting with bisect O(n log n) — keep `tails`, replace first ≥ element.
- **State machine** — stock problems with cooldown/fee/k-transactions: a small set of named states (holding, sold, rest) with transitions per day.
- **Kadane's** — max subarray is degenerate DP: `dp[i] = max(a[i], dp[i-1] + a[i])`.

### Pitfalls
- Compressed knapsack iterated forward silently reuses an item — the #1 DP bug.
- Off-by-one between "dp index = prefix length" and "string index".
- Memoization on mutable args (lists) — convert to tuples or indices.
- If greedy seems to work, find the counterexample before trusting it; if it survives an exchange argument, drop the DP.

## Easy
- Climbing Stairs (LC 70)
- Min Cost Climbing Stairs (LC 746)
- Maximum Subarray (LC 53)
- Pascal's Triangle (LC 118)

## Medium
- House Robber (LC 198)
- House Robber II (LC 213)
- Coin Change (LC 322)
- Longest Increasing Subsequence (LC 300)
- Unique Paths (LC 62)
- Minimum Path Sum (LC 64)
- Decode Ways (LC 91)
- Word Break (LC 139)
- Partition Equal Subset Sum (LC 416)
- Longest Palindromic Substring (LC 5)
- Palindromic Substrings (LC 647)
- Longest Common Subsequence (LC 1143)
- Target Sum (LC 494)
- Best Time to Buy and Sell Stock with Cooldown (LC 309)
- Maximum Product Subarray (LC 152)
- Jump Game (LC 55)

## Hard
- Edit Distance (LC 72)
- Burst Balloons (LC 312)
- Regular Expression Matching (LC 10)
- Longest Valid Parentheses (LC 32)
- Minimum Cost to Cut a Stick (LC 1547)
- Best Time to Buy and Sell Stock IV (LC 188)

## Solve Log

| Date | Problem | LC# | Difficulty | Result | Hints | Time-Space | Notes |
|------|---------|-----|------------|--------|-------|------------|-------|
