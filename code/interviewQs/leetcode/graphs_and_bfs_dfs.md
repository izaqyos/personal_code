# Graphs & BFS/DFS — Problem Bank & Study Notes

## Study Notes (offline reference)

### Representations
Adjacency list (`defaultdict(list)`) is the default. Grids are IMPLICIT graphs: cell = node, 4-neighbors via `for dr, dc in ((1,0),(-1,0),(0,1),(0,-1))`. Build adj list from edge lists; remember to add both directions for undirected.

### Core algorithms (drill from scratch)
```
BFS — shortest path in UNWEIGHTED graphs, level-by-level:
    queue = deque([start]); visited = {start}     # mark when ENQUEUING, not dequeuing
    while queue:
        node = queue.popleft()
        for nb in neighbors(node):
            if nb not in visited: visited.add(nb); queue.append(nb)

DFS — reachability, components, exhaustive exploration:
    recursive: visit, mark, recurse on unvisited neighbors
    iterative: explicit stack (needed when depth can exceed ~1000 in Python)

Topological sort (DAG ordering — course schedule family):
    Kahn's: compute indegrees; queue of indegree-0 nodes; pop, append to order,
    decrement neighbors, enqueue new zeros. If order shorter than n → cycle.
    (alt: DFS postorder reversed, with 3-color cycle detection)
```

### Core patterns
- **Connected components / flood fill** — loop all nodes/cells, launch BFS/DFS from each unvisited one, count launches. Islands, provinces, area counting. Marking visited in-place (sink the island) saves the set.
- **Multi-source BFS** — seed the queue with ALL sources at distance 0 (rotting oranges, walls-and-gates, 01-matrix). Same algorithm, multiple starting points.
- **Cycle detection** — directed: 3 colors (white/gray/black); a gray→gray edge is a cycle. Undirected: DFS, a visited neighbor that isn't the parent is a cycle. Or Union Find.
- **BFS with state** — sometimes the node is (cell, extra-state), e.g., obstacles-eliminated count (LC 1293). Visited keys on the FULL state.
- **Bipartite check** — 2-color with BFS/DFS; an edge between same-colored nodes fails.
- **Dijkstra (weighted shortest path)** — heap of (dist, node); pop, skip stale entries, relax. Know it exists at this level (network delay time LC 743); deeper study belongs to system rounds.

### Pitfalls
- Marking visited at dequeue instead of enqueue → duplicate enqueues blow up the queue.
- Grid: bounds-check BEFORE indexing; don't forget to mark the START.
- Clone-graph: map old→new BEFORE recursing on neighbors, or cycles recurse forever.
- Recursion depth on big grids — Python: iterative DFS or `sys.setrecursionlimit`.

## Easy
- Find if Path Exists in Graph (LC 1971)
- Flood Fill (LC 733)
- Number of Provinces (LC 547)

## Medium
- Number of Islands (LC 200)
- Max Area of Island (LC 695)
- Clone Graph (LC 133)
- Rotting Oranges (LC 994)
- Course Schedule (LC 207)
- Course Schedule II (LC 210)
- Pacific Atlantic Water Flow (LC 417)
- Surrounded Regions (LC 130)
- Graph Valid Tree (LC 261)
- Shortest Path in Binary Matrix (LC 1091)
- Is Graph Bipartite? (LC 785)
- Network Delay Time (LC 743)
- Walls and Gates (LC 286)

## Hard
- Word Ladder (LC 127)
- Alien Dictionary (LC 269)
- Shortest Path in a Grid with Obstacles Elimination (LC 1293)
- Bus Routes (LC 815)

## Solve Log

| Date | Problem | LC# | Difficulty | Result | Hints | Time-Space | Notes |
|------|---------|-----|------------|--------|-------|------------|-------|
