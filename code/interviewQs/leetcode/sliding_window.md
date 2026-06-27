# Sliding Window — Problem Bank & Study Notes

## Study Notes (offline reference)

### Core patterns
- **Fixed-size window** — compute window k once, then slide: `add a[i], remove a[i-k]`, update best. Never recompute from scratch inside the loop.
- **Variable-size window (grow/shrink)** — the workhorse. Right pointer expands every iteration; an inner while shrinks from the left while the window is invalid (or, for "shortest" problems, while it is VALID — record best before shrinking).
- **"At most K distinct" trick** — exactly-K = atMost(K) − atMost(K−1). Turns hard counting problems into two easy passes.
- **Satisfaction counter** — instead of comparing two freq maps every step (O(alphabet) per step), keep one scalar `formed` = number of chars whose count requirement is exactly met. Bump it only at exact threshold crossings (== after increment, < after decrement).
- **Monotonic deque (window max/min)** — deque holds indices, values decreasing. New element pops smaller tails; front is the max; pop front when it slides out of the window. O(n) total.

### Template — variable window (longest valid)
```
l = 0
for r in range(n):
    include a[r] in window state
    while window invalid:
        exclude a[l]; l += 1
    best = max(best, r - l + 1)
```
For SHORTEST-valid problems, invert: shrink while valid, record best inside the shrink loop.

### Pitfalls
- Choosing the wrong template direction: "longest" records after shrinking to valid; "shortest" records during the valid-shrink loop.
- Updating window state and pointer in the wrong order (classic off-by-one).
- Deque pattern: store indices (not values) or you can't tell when the front expires.
- A window only works when the predicate is monotone (growing the window never makes an invalid window valid again, or vice versa). If not monotone — different tool.

## Easy
- Best Time to Buy and Sell Stock (LC 121)
- Maximum Average Subarray I (LC 643)
- Contains Duplicate II (LC 219)

## Medium
- Longest Substring Without Repeating Characters (LC 3)
- Longest Repeating Character Replacement (LC 424)
- Permutation in String (LC 567)
- Fruit Into Baskets (LC 904)
- Maximum Number of Vowels in a Substring (LC 1456)
- Minimum Size Subarray Sum (LC 209)
- Max Consecutive Ones III (LC 1004)
- Subarrays with K Different Integers — try atMost trick (LC 992, listed Hard on LC)
- Find All Anagrams in a String (LC 438)

## Hard
- Minimum Window Substring (LC 76)
- Sliding Window Maximum (LC 239)
- Substring with Concatenation of All Words (LC 30)
- Longest Substring with At Most K Distinct Characters (LC 340)

## Solve Log

| Date | Problem | LC# | Difficulty | Result | Hints | Time-Space | Notes |
|------|---------|-----|------------|--------|-------|------------|-------|
