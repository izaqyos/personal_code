# Union Find — Problem Bank & Study Notes

## Study Notes (offline reference)

### The structure (drill from scratch — it's ~15 lines)
```
parent = list(range(n)); rank = [0]*n          # or size = [1]*n

find(x):                                        # with path compression
    while parent[x] != x:
        parent[x] = parent[parent[x]]           # halving: point to grandparent
        x = parent[x]
    return x

union(a, b):                                    # by rank (or size)
    ra, rb = find(a), find(b)
    if ra == rb: return False                   # already connected — useful signal!
    attach lower-rank root under higher; equal ranks → either, rank += 1
    return True
```
With both optimizations, ops are amortized O(α(n)) — inverse Ackermann, effectively constant. Either optimization alone is already near-log; both is the standard recital.

### When Union Find beats BFS/DFS
- **Dynamic connectivity** — edges arrive over time and you ask "connected yet?" between additions (earliest moment everyone is friends, number of islands II). BFS would re-traverse per query.
- **Cycle detection in an undirected edge list** — `union` returning False = this edge closes a cycle (Redundant Connection). One pass, no graph build.
- **Offline grouping by equivalence** — accounts-merge (emails), equality equations, similar string groups: union everything equivalent, then bucket by root.
- **Kruskal's MST** — sort edges by weight, add unless it cycles (union returns False). The classic UF application; know the name.
- Static graph, single pass, need paths/distances → plain BFS/DFS is simpler. UF gives connectivity only, no paths.

### Patterns & bookkeeping
- Component COUNT: start at n, decrement on each successful union.
- Component sizes: maintain `size[]`, merge small into large; answer "largest component" instantly.
- Non-integer items (emails, strings): dict-based parent map, or pre-index to ints.
- Grid problems: flatten cell (r, c) → r*cols + c.

### Pitfalls
- Forgetting path compression → quietly O(n) per find on adversarial chains.
- Comparing `parent[x]` instead of `find(x)` for connectivity — stale parents lie.
- Union by rank: rank increments ONLY on equal-rank merges.

## Easy
- Find if Path Exists in Graph (LC 1971)
- Number of Provinces (LC 547)

## Medium
- Redundant Connection (LC 684)
- Number of Connected Components in an Undirected Graph (LC 323)
- Graph Valid Tree (LC 261)
- Accounts Merge (LC 721)
- Satisfiability of Equality Equations (LC 990)
- Most Stones Removed with Same Row or Column (LC 947)
- Longest Consecutive Sequence (LC 128) — alt UF solve; set approach is simpler
- Number of Islands (LC 200) — alt UF solve; DFS is simpler

## Hard
- Number of Islands II (LC 305)
- Similar String Groups (LC 839)
- Swim in Rising Water (LC 778) — UF or binary-search+BFS
- Smallest String With Swaps (LC 1202) — medium-hard bridge

## Solve Log

| Date | Problem | LC# | Difficulty | Result | Hints | Time-Space | Notes |
|------|---------|-----|------------|--------|-------|------------|-------|
