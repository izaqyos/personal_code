# Intervals — Problem Bank & Study Notes

## Study Notes (offline reference)

### The two sort keys (choosing one is half the problem)
- **Sort by START** → merging/combining overlaps (merge intervals, insert interval).
- **Sort by END** → greedy selection "keep the most" (non-overlapping intervals, burst balloons arrows): the earliest-ending interval leaves maximum room — exchange argument.

### Overlap test
Two intervals `[a, b]`, `[c, d]` overlap iff `a <= d and c <= b`. After sorting by start, the streaming version is just: `current.start <= prev.end`. Decide early whether touching endpoints ([1,2],[2,3]) count as overlap for THIS problem — it flips `<=` vs `<`.

### Core patterns
- **Merge sweep** — sort by start; keep a growing `last` interval: overlap → `last.end = max(last.end, cur.end)` (the max matters — contained intervals!), else push `cur` as the new `last`.
- **Insert interval (no re-sort needed)** — three phases over the already-sorted list: (1) copy intervals entirely before the new one, (2) absorb all overlapping ones into it (min start, max end), (3) copy the rest.
- **Min meeting rooms / max concurrent** — two equivalent tools:
  - *Heap*: sort by start; heap of end times; pop ends ≤ current start (room freed), push current end; answer = max heap size.
  - *Sweep line*: events (+1 at start, −1 at end), sort (ends before starts on ties if touching ≠ overlap), running sum's max = answer. Sweep line generalizes (skyline, employee free time, car pooling with weights).
- **Greedy removal/selection** — sort by END, count compatible intervals (start ≥ last kept end); removals = n − kept.
- **Intersections of two sorted lists (LC 986)** — two pointers; intersection = `[max(starts), min(ends)]` if non-empty; advance whichever interval ends first.

### Pitfalls
- Forgetting `max()` when extending the merged end — `[1,10],[2,3]` breaks naive assignment.
- Tie-handling at equal timestamps (meeting ends exactly when another starts) — derive from the problem statement, don't guess.
- Mutating the input list of lists while iterating; build the result fresh.

## Easy
- Meeting Rooms (LC 252)
- Summary Ranges (LC 228)

## Medium
- Merge Intervals (LC 56)
- Insert Interval (LC 57)
- Meeting Rooms II (LC 253)
- Non-overlapping Intervals (LC 435)
- Interval List Intersections (LC 986)
- Minimum Number of Arrows to Burst Balloons (LC 452)
- Remove Covered Intervals (LC 1288)
- Car Pooling (LC 1094)
- My Calendar I (LC 729)

## Hard
- The Skyline Problem (LC 218)
- Employee Free Time (LC 759)
- Data Stream as Disjoint Intervals (LC 352)

## Solve Log

| Date | Problem | LC# | Difficulty | Result | Hints | Time-Space | Notes |
|------|---------|-----|------------|--------|-------|------------|-------|
