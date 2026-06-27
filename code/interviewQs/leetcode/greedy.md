# Greedy — Problem Bank & Study Notes

## Study Notes (offline reference)

### What makes greedy valid
A greedy algorithm commits to the locally best choice and never revisits. It's correct only when the problem has the **exchange property**: any optimal solution can be transformed into the greedy one without getting worse. You can't prove this in an interview, but you should be able to SAY why swapping toward the greedy choice never hurts — and to hunt for a counterexample before trusting it. Greedy fails → usually the problem is DP.

### Core patterns
- **Sort, then sweep** — most greedy problems start with "sort by the right key". Choosing the KEY is the whole problem: intervals by end time (scheduling), people by weight (boats), jobs by ratio/deadline.
- **Interval scheduling** — max non-overlapping intervals: sort by END, take every interval that starts after the last taken end. (Equivalently: min removals = n − max kept.)
- **Reach / coverage** — Jump Game: track `furthest = max(furthest, i + a[i])`; fail if `i > furthest`. Jump Game II: greedy BFS-like layers — `jumps += 1` when `i` passes the current layer's edge.
- **Running-total feasibility** — Gas Station: if total gas ≥ total cost a solution exists; restart the candidate start whenever the running tank goes negative (the skipped prefix can't help any later start).
- **Two-pass constraints** — Candy: left-to-right pass enforces the left constraint, right-to-left pass enforces the right with `max()`. Pattern for any "must beat both neighbors" rule.
- **Counting / frequency greedy** — Task Scheduler: schedule around the most frequent task; formula `(maxFreq - 1) * (n + 1) + #tasks-with-maxFreq`, floor at total tasks.
- **Greedy + heap** — when "best current choice" changes dynamically, a heap supplies it: IPO (LC 502), reorganize string (LC 767). Bridges to the heap topic.
- **Local digit/char decisions** — remove-k-digits / monotonic-stack greedy: drop a bigger char when a smaller one follows. Bridges to monotonic stack.

### Pitfalls
- Plausible-but-wrong sort key — test small counterexamples (size 3 inputs break most wrong greedy ideas).
- Forgetting the feasibility precheck (gas station total) before the greedy sweep.
- Jump Game: `i > furthest` must be checked BEFORE extending furthest.

## Easy
- Assign Cookies (LC 455)
- Best Time to Buy and Sell Stock II (LC 122)
- Lemonade Change (LC 860)
- Can Place Flowers (LC 605)

## Medium
- Jump Game (LC 55)
- Jump Game II (LC 45)
- Gas Station (LC 134)
- Partition Labels (LC 763)
- Boats to Save People (LC 881)
- Task Scheduler (LC 621)
- Hand of Straights (LC 846)
- Merge Triplets to Form Target Triplet (LC 1899)
- Non-overlapping Intervals (LC 435)
- Reorganize String (LC 767)
- Remove K Digits (LC 402)

## Hard
- Candy (LC 135)
- Patching Array (LC 330)
- Minimum Number of Taps to Open to Water a Garden (LC 1326)

## Solve Log

| Date | Problem | LC# | Difficulty | Result | Hints | Time-Space | Notes |
|------|---------|-----|------------|--------|-------|------------|-------|
