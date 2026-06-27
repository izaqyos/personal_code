# Binary Search — Problem Bank & Study Notes

## Study Notes (offline reference)

### Core patterns
- **Exact match** — `while lo <= hi`, `mid = (lo + hi) // 2`, return on hit, else move past mid (`lo = mid + 1` / `hi = mid - 1`). Terminates because the range strictly shrinks.
- **Leftmost / boundary search (bisect_left)** — find the first index where a predicate becomes true. `while lo < hi: mid = (lo+hi)//2; if pred(mid): hi = mid else: lo = mid + 1`. Answer is `lo`. This ONE template solves first-bad-version, search-insert, find-first/last.
- **Search on the answer space** — when the array isn't sorted but the ANSWER is monotone (e.g., "can Koko finish at speed s?" — if yes at s, yes at s+1). Binary search over candidate answers, feasibility check as the predicate. Spot it by: "minimum X such that condition holds".
- **Rotated sorted array** — at every mid, ONE half is properly sorted (check `a[lo] <= a[mid]`). Decide if target is inside the sorted half; recurse to the other half otherwise.
- **2D matrix as flat array** — index `i ∈ [0, m*n)`, map `row = i // n, col = i % n`. One standard binary search.
- **Median of two sorted arrays** — partition the shorter array, derive the other partition, check cross conditions `maxLeftA <= minRightB`. O(log min(m,n)).

### Invariant discipline (where bugs live)
- Define what `lo` and `hi` MEAN before writing the loop (e.g., "answer is always in [lo, hi]") and keep every branch consistent with it.
- `while lo < hi` with `hi = mid` needs `mid` biased LOW (`(lo+hi)//2`); if a branch sets `lo = mid`, bias HIGH (`(lo+hi+1)//2`) or you infinite-loop on a 2-element range.
- Python ints don't overflow; in other languages use `lo + (hi-lo)//2`.
- Know `bisect.bisect_left/right` — and be able to reimplement them.

## Easy
- Binary Search (LC 704)
- Search Insert Position (LC 35)
- First Bad Version (LC 278)
- Sqrt(x) (LC 69)
- Guess Number Higher or Lower (LC 374)

## Medium
- Search in Rotated Sorted Array (LC 33)
- Find Minimum in Rotated Sorted Array (LC 153)
- Search a 2D Matrix (LC 74)
- Koko Eating Bananas (LC 875)
- Find Peak Element (LC 162)
- Find First and Last Position in Sorted Array (LC 34)
- Capacity to Ship Packages Within D Days (LC 1011)
- Time Based Key-Value Store (LC 981)
- Search in Rotated Sorted Array II (LC 81)

## Hard
- Median of Two Sorted Arrays (LC 4)
- Split Array Largest Sum (LC 410)
- Find in Mountain Array (LC 1095)

## Solve Log

| Date | Problem | LC# | Difficulty | Result | Hints | Time-Space | Notes |
|------|---------|-----|------------|--------|-------|------------|-------|
