# Arrays & Strings — Problem Bank & Study Notes

## Study Notes (offline reference)

### Core patterns
- **Prefix/suffix accumulation** — precompute running sums/products from left and right; answer at `i` combines `prefix[i-1]` and `suffix[i+1]`. Space-optimize by reusing the output array for one direction + a running scalar for the other.
- **Frequency counting** — fixed alphabet → `[0]*26` array; arbitrary chars/case-sensitive → dict/Counter. Increment one string, decrement the other, check all-zero.
- **Index-as-hash (in-place marking)** — when values are bounded by array length, the array itself is the hash table: flip sign at index `v-1`, or place `v` at slot `v-1` (cyclic sort). Gives O(1) space on problems that look like they need a set.
- **Kadane's algorithm** — max subarray sum: `cur = max(x, cur + x)`, `best = max(best, cur)`. Extends to max product (track min too, signs flip).
- **String building** — strings are immutable; repeated `+=` is O(n²). Collect parts in a list, `''.join(parts)` at the end.
- **Matrix tricks** — rotate 90° = transpose + reverse each row; spiral = four shrinking boundaries; set-zeroes in O(1) space = use row 0 / col 0 as marker arrays.

### Sorting fundamentals (drill these from scratch)
```
merge_sort(a):                      # O(n log n) time, O(n) space, stable
    if len(a) <= 1: return a
    L, R = merge_sort(left half), merge_sort(right half)
    merge: two pointers over L and R, take smaller, drain leftovers

quicksort partition (Lomuto):       # avg O(n log n), worst O(n²), in place
    pivot = a[hi]; i = lo
    for j in lo..hi-1: if a[j] < pivot: swap(a[i], a[j]); i += 1
    swap(a[i], a[hi]); return i
```
Know when sorting *is* the answer: dedup, anagram keys, meeting-style problems, two-pointer preconditions.

### Pitfalls
- Off-by-one at boundaries — write the loop invariant in a comment before coding.
- Mutating a list while iterating it — iterate a copy or build a new list.
- Python negative indexing silently "works" — a stray `-1` index reads the last element instead of crashing.
- `enumerate` yields `(i, val)` in that order.

## Easy
- Two Sum (LC 1)
- Best Time to Buy and Sell Stock (LC 121)
- Contains Duplicate (LC 217)
- Valid Anagram (LC 242)
- Merge Sorted Array (LC 88)
- Longest Common Prefix (LC 14)
- Plus One (LC 66)
- Remove Duplicates from Sorted Array (LC 26)
- Length of Last Word (LC 58)
- Merge Strings Alternately (LC 1768)

## Medium
- Product of Array Except Self (LC 238)
- Container With Most Water (LC 11)
- Group Anagrams (LC 49)
- Longest Consecutive Sequence (LC 128)
- Top K Frequent Elements (LC 347)
- Encode and Decode Strings (LC 271)
- String to Integer (atoi) (LC 8)
- 3Sum (LC 15)
- Maximum Subarray (LC 53)
- Maximum Product Subarray (LC 152)
- Rotate Array (LC 189)
- Rotate Image (LC 48)
- Spiral Matrix (LC 54)
- Set Matrix Zeroes (LC 73)
- String Compression (LC 443)
- Zigzag Conversion (LC 6)
- Sort Colors (LC 75)

## Hard
- Trapping Rain Water (LC 42)
- First Missing Positive (LC 41)
- Minimum Window Substring (LC 76)
- Text Justification (LC 68)
- Candy (LC 135)

## Solve Log

| Date | Problem | LC# | Difficulty | Result | Hints | Time-Space | Notes |
|------|---------|-----|------------|--------|-------|------------|-------|
