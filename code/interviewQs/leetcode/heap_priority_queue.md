# Heap / Priority Queue — Problem Bank & Study Notes

## Study Notes (offline reference)

### Fundamentals
A binary heap is a complete binary tree in an array: children of `i` at `2i+1, 2i+2`, parent at `(i-1)//2`. Push = append + sift-up; pop = swap root/last, sift-down. Push/pop O(log n); **heapify is O(n)** (not n log n) — sift-down from the last parent. Be able to write sift-up/sift-down from scratch once.

Python `heapq` is a MIN-heap, functions over a plain list: `heappush`, `heappop`, `heapify`, `heappushpop`, `nlargest/nsmallest`. Max-heap → negate values. Ties → push tuples `(key, tiebreak, payload)`; ensure the tiebreak is comparable (a counter beats hoping payloads compare).

### Core patterns
- **Top-K with a size-k heap** — kth LARGEST: keep a MIN-heap of size k (the root is the answer; anything bigger pushes the smallest out). O(n log k) — beats full sort when k ≪ n. Counterpart: quickselect gives average O(n) — know both and the trade-off (heap streams, quickselect needs the array).
- **K-way merge** — seed heap with each list's head `(val, list_idx, node)`; pop, push the popped element's successor. Merge-k-lists, kth smallest in sorted matrix, smallest range covering k lists.
- **Two heaps (streaming median)** — max-heap `lo` (lower half) + min-heap `hi` (upper half), rebalance so sizes differ ≤ 1; median is `lo`'s root (odd) or average of roots (even). The pattern for any "running middle/percentile".
- **Scheduling / simulation** — heap = "what frees up next": meeting rooms II (heap of end times), task scheduler, CPU intervals, single-threaded CPU. Often paired with a sort by start time.
- **Greedy + heap** — repeatedly take the current best when "best" changes dynamically: last stone weight, reorganize string (most frequent char first), IPO (two heaps: affordable-by-capital feed into max-profit).
- **Lazy deletion** — when arbitrary removal is needed, mark dead entries in a counter and discard them when they surface at the root (sliding-window median, design problems). Avoids O(n) removal.

### When NOT to use a heap
Need ALL elements ordered → sort. Need kth once with data in memory → quickselect. Need min AND max with deletions → two heaps with lazy deletion, or a sorted container.

### Pitfalls
- Forgetting to negate on BOTH push and pop for max-heap simulation.
- Pushing non-comparable tuples (dicts/nodes as second element) — add a counter field.
- Top-k: pushing everything (O(n log n)) instead of capping the heap at size k.

## Easy
- Kth Largest Element in a Stream (LC 703)
- Last Stone Weight (LC 1046)
- Relative Ranks (LC 506)

## Medium
- Kth Largest Element in an Array (LC 215)
- Top K Frequent Elements (LC 347)
- K Closest Points to Origin (LC 973)
- Task Scheduler (LC 621)
- Meeting Rooms II (LC 253)
- Kth Smallest Element in a Sorted Matrix (LC 378)
- Reorganize String (LC 767)
- Single-Threaded CPU (LC 1834)
- Design Twitter (LC 355)

## Hard
- Find Median from Data Stream (LC 295)
- Merge k Sorted Lists (LC 23)
- IPO (LC 502)
- Smallest Range Covering Elements from K Lists (LC 632)
- Sliding Window Median (LC 480)

## Solve Log

| Date | Problem | LC# | Difficulty | Result | Hints | Time-Space | Notes |
|------|---------|-----|------------|--------|-------|------------|-------|
