# Arrays & Strings — Problem Bank

## Easy
- Two Sum (LC 1)
- Best Time to Buy and Sell Stock (LC 121)
- Contains Duplicate (LC 217)
- Valid Anagram (LC 242)
- Merge Sorted Array (LC 88)

## Medium
- Product of Array Except Self (LC 238)
- Container With Most Water (LC 11)
- Group Anagrams (LC 49)
- Longest Consecutive Sequence (LC 128)
- Top K Frequent Elements (LC 347)
- Encode and Decode Strings (LC 271)
- String to Integer (atoi) (LC 8)

## Hard
- Trapping Rain Water (LC 42)
- First Missing Positive (LC 41)
- Minimum Window Substring (LC 76)

## Solve Log

| Date | Problem | LC# | Difficulty | Result | Hints | Time-Space | Notes |
|------|---------|-----|------------|--------|-------|------------|-------|
| 2026-03-26 | Product of Array Except Self | 238 | Medium | PASS | 1 (layered) | O(n)/O(1) | prefix/suffix pattern; O(n) space first, then optimized to O(1) by reusing output array for suffix + running prefix variable |
| 2026-03-29 | Group Anagrams | 49 | Medium | PASS | 0 | O(n·k)/O(n·k) | prime product sieve approach (creative), then added sorted-key O(n·k log k) and char-count tuple O(n·k) alternatives |
| 2026-03-30 | Valid Anagram | 242 | Easy | PASS | 0 | O(n)/O(1) | char-count single array with increment/decrement; early exit on length mismatch |
| 2026-03-31 | Contains Duplicate | 217 | Easy | PASS | 0 | O(n)/O(n) | set with early return; also know sort+scan O(n log n)/O(1) and brute force O(n²)/O(1) |
| 2026-04-06 | Longest Consecutive Sequence | 128 | Medium | PASS | 1 | O(n)/O(n) | set + only start counting from sequence heads (n-1 not in set); 1 hint: nudge away from DP toward set approach |
| 2026-04-09 | Container With Most Water | 11 | Medium | PASS | 1 | O(n)/O(1) | two pointers from edges; always move shorter side — moving taller can never improve min(h[l],h[r]) |
| 2026-04-13 | Top K Frequent Elements | 347 | Medium | PASS | 0 | O(n)/O(n) | Counter + bucket sort (index=frequency); also know heap approach O(n log k)/O(k) — better when n is huge and k is small |
| 2026-04-14 | Best Time to Buy and Sell Stock | 121 | Easy | PASS | 0 | O(n)/O(1) | greedy: track min price so far, compute profit at each step |
| 2026-04-19 | Merge Sorted Array | 88 | Easy | PASS | 1 | O(m+n)/O(1) | back-merge: 3 pointers from the end — fill nums1 right-to-left to avoid overwriting unread data (prior solves used forward merge with O(m) copy) |
