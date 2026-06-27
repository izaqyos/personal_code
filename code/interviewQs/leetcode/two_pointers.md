# Two Pointers — Problem Bank & Study Notes

## Study Notes (offline reference)

### Core patterns
- **Converging pointers** (ends → middle) — requires sorted input or a symmetric property (palindrome). Pair sum: `sum < target → l += 1`, `sum > target → r -= 1`. Container/water variants: always move the *limiting* side; moving the taller side can never improve the min.
- **Read/write pointers** (in-place compaction) — `write` marks the next slot to fill, `read` scans everything. Keep elements that pass the filter: `if keep(a[read]): a[write] = a[read]; write += 1`. Covers remove-element, dedup, move-zeroes.
- **Anchor + scan** (kSum family) — fix one element with a for-loop, run a converging scan on the rest. Dedup at BOTH levels: skip repeated anchors at for-level, skip repeated l/r values after each hit. Generalizes recursively to kSum.
- **Partition / Dutch national flag** — three regions via `low`, `mid`, `high`: `0 → swap(low, mid), advance both; 1 → mid += 1; 2 → swap(mid, high), high -= 1` and do NOT advance mid (the swapped-in value is unexamined).
- **Fast/slow** — mostly a linked-list pattern (see linked_lists.md), but also: cycle in array (LC 287) treating values as next-indices.

### Template — converging
```
l, r = 0, n - 1
while l < r:
    evaluate(a[l], a[r])
    move exactly one pointer per iteration  # invariant: answer (if any) stays inside [l, r]
```

### Pitfalls
- The branch logic (`< target → l += 1`) is only valid on SORTED input — sort first or prove order.
- After recording a hit in kSum, advance both pointers BEFORE dedup-skip loops; bound the skips with `l < r`.
- Read/write: forgetting that everything before `write` is the answer; everything from `write` to `read` is garbage.
- Dutch flag: advancing `mid` after the high-swap inspects an element twice or skips one.

## Easy
- Valid Palindrome (LC 125)
- Merge Sorted Array (LC 88)
- Move Zeroes (LC 283)
- Squares of a Sorted Array (LC 977)
- Remove Duplicates from Sorted Array (LC 26)
- Remove Element (LC 27)
- Reverse String (LC 344)
- Is Subsequence (LC 392)

## Medium
- Two Sum II - Input Array Is Sorted (LC 167)
- 3Sum (LC 15)
- 3Sum Closest (LC 16)
- 4Sum (LC 18)
- Sort Colors (LC 75)
- Rotate Array (LC 189)
- Container With Most Water (LC 11)
- Boats to Save People (LC 881)
- Partition Labels (LC 763)
- Find the Duplicate Number (LC 287)

## Hard
- Trapping Rain Water (LC 42)
- Shortest Subarray to be Removed to Make Array Sorted (LC 1574)

## Solve Log

| Date | Problem | LC# | Difficulty | Result | Hints | Time-Space | Notes |
|------|---------|-----|------------|--------|-------|------------|-------|
