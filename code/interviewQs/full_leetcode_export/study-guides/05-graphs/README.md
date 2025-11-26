# Graphs - Complete Guide

## 📋 Pattern Recognition

**When to use Graphs:**
- Problems mention "nodes", "edges", "connections", "paths"
- "Network", "islands", "courses with prerequisites"
- "Shortest path", "connected components"
- Social networks, dependency resolution, map navigation

**Common Keywords:**
- Connected, reachable, path, cycle, component
- Shortest, neighbors, edges, vertices
- Prerequisite, dependency, order

---

## 🎯 Graph Basics

### Graph Representation

#### 1. Adjacency List (Most Common)
```python
# Using dictionary (handles any node type)
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D'],
    'C': ['A', 'D'],
    'D': ['B', 'C']
}

# Using list of lists (for numbered nodes 0...n-1)
n = 5
graph = [[] for _ in range(n)]
# Add edge: 0 -> 1
graph[0].append(1)

# For weighted graphs
graph = {
    'A': [('B', 5), ('C', 3)],  # (neighbor, weight)
    'B': [('A', 5), ('D', 2)],
}
```

**Space: O(V + E)** where V = vertices, E = edges

#### 2. Adjacency Matrix
```python
# For n nodes
n = 5
graph = [[0] * n for _ in range(n)]

# Add edge: 0 -> 1
graph[0][1] = 1  # or weight for weighted graphs

# Undirected: add both directions
graph[0][1] = graph[1][0] = 1
```

**Space: O(V²)** - Use when graph is dense or need O(1) edge lookup

#### 3. Edge List
```python
edges = [
    (0, 1),      # edge from 0 to 1
    (1, 2),
    (2, 3)
]

# For weighted graphs
edges = [
    (0, 1, 5),   # (from, to, weight)
    (1, 2, 3),
]
```

**Space: O(E)** - Use for Union-Find, MST algorithms

---

## 🔧 Core Algorithm 1: Depth-First Search (DFS)

### DFS Concept
- Explore as far as possible along each branch before backtracking
- Uses stack (explicit or recursion call stack)
- Good for: cycle detection, topological sort, path finding

### DFS Template - Recursive

```python
def dfs_recursive(graph, start, visited=None):
    """
    Standard DFS template
    
    Time: O(V + E), Space: O(V) for recursion stack
    """
    if visited is None:
        visited = set()
    
    # Mark current node as visited
    visited.add(start)
    print(start)  # Process node
    
    # Visit all neighbors
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited)
    
    return visited
```

### DFS Template - Iterative

```python
def dfs_iterative(graph, start):
    """
    Iterative DFS using explicit stack
    
    Time: O(V + E), Space: O(V)
    """
    visited = set()
    stack = [start]
    
    while stack:
        node = stack.pop()
        
        if node in visited:
            continue
        
        visited.add(node)
        print(node)  # Process node
        
        # Add neighbors to stack
        for neighbor in graph[node]:
            if neighbor not in visited:
                stack.append(neighbor)
    
    return visited
```

### Problem 1: Number of Islands (DFS)

```python
def numIslands(grid: list[list[str]]) -> int:
    """
    LeetCode #200 - Count islands in 2D grid
    
    Key insight: Each DFS explores one complete island
    
    Time: O(rows * cols), Space: O(rows * cols) worst case stack
    """
    if not grid or not grid[0]:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    def dfs(r, c):
        # Boundary check and water check
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == '0':
            return
        
        # Mark as visited by changing to '0'
        grid[r][c] = '0'
        
        # Explore 4 directions
        dfs(r + 1, c)  # down
        dfs(r - 1, c)  # up
        dfs(r, c + 1)  # right
        dfs(r, c - 1)  # left
    
    # Try starting DFS from each cell
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                dfs(r, c)  # Explore entire island
                count += 1  # Found one complete island
    
    return count
```

### Problem 2: Clone Graph

```python
class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors else []

def cloneGraph(node: Node) -> Node:
    """
    LeetCode #133 - Deep copy of graph
    
    Time: O(V + E), Space: O(V)
    """
    if not node:
        return None
    
    # Map old node -> new node
    clones = {}
    
    def dfs(node):
        if node in clones:
            return clones[node]
        
        # Create clone
        clone = Node(node.val)
        clones[node] = clone
        
        # Clone neighbors
        for neighbor in node.neighbors:
            clone.neighbors.append(dfs(neighbor))
        
        return clone
    
    return dfs(node)
```

---

## 🔧 Core Algorithm 2: Breadth-First Search (BFS)

### BFS Concept
- Explore level by level (closest nodes first)
- Uses queue
- Good for: shortest path (unweighted), level-order traversal

### BFS Template

```python
from collections import deque

def bfs(graph, start):
    """
    Standard BFS template
    
    Time: O(V + E), Space: O(V)
    """
    visited = set([start])
    queue = deque([start])
    
    while queue:
        node = queue.popleft()
        print(node)  # Process node
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return visited
```

### BFS with Level Tracking

```python
def bfs_with_levels(graph, start):
    """
    BFS that tracks distance/level from start
    """
    visited = {start: 0}  # node -> distance
    queue = deque([start])
    
    while queue:
        node = queue.popleft()
        current_dist = visited[node]
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited[neighbor] = current_dist + 1
                queue.append(neighbor)
    
    return visited
```

### Problem 3: Shortest Path in Binary Matrix

```python
def shortestPathBinaryMatrix(grid: list[list[int]]) -> int:
    """
    LeetCode #1091 - Shortest path from (0,0) to (n-1,n-1)
    Can move in 8 directions
    
    Time: O(n²), Space: O(n²)
    """
    n = len(grid)
    
    if grid[0][0] == 1 or grid[n-1][n-1] == 1:
        return -1
    
    # 8 directions
    directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    
    queue = deque([(0, 0, 1)])  # (row, col, distance)
    visited = {(0, 0)}
    
    while queue:
        r, c, dist = queue.popleft()
        
        # Reached end
        if r == n-1 and c == n-1:
            return dist
        
        # Explore neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            if (0 <= nr < n and 0 <= nc < n and 
                grid[nr][nc] == 0 and (nr, nc) not in visited):
                visited.add((nr, nc))
                queue.append((nr, nc, dist + 1))
    
    return -1
```

### Problem 4: Word Ladder

```python
def ladderLength(beginWord: str, endWord: str, wordList: list[str]) -> int:
    """
    LeetCode #127 - Shortest transformation sequence
    
    BFS on word graph (words differ by 1 letter are connected)
    
    Time: O(M² * N) where M = word length, N = number of words
    Space: O(M² * N)
    """
    word_set = set(wordList)
    if endWord not in word_set:
        return 0
    
    queue = deque([(beginWord, 1)])  # (word, level)
    
    while queue:
        word, level = queue.popleft()
        
        if word == endWord:
            return level
        
        # Try changing each character
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                next_word = word[:i] + c + word[i+1:]
                
                if next_word in word_set:
                    word_set.remove(next_word)  # Mark as visited
                    queue.append((next_word, level + 1))
    
    return 0
```

---

## 🔧 Core Algorithm 3: Union-Find (Disjoint Set) 🚨 CRITICAL

### Union-Find Concept
- Track connected components efficiently
- Two operations: **find** (which set?), **union** (merge sets)
- Uses **path compression** and **union by rank** for O(α(n)) ≈ O(1)

### Union-Find Implementation

```python
class UnionFind:
    """
    Optimized Union-Find with path compression and union by rank
    
    All operations: O(α(n)) ≈ O(1) amortized
    """
    def __init__(self, n):
        self.parent = list(range(n))  # Each node is its own parent initially
        self.rank = [0] * n           # Height of tree
        self.count = n                # Number of components
    
    def find(self, x):
        """
        Find root of x with path compression
        Path compression: make every node point directly to root
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]
    
    def union(self, x, y):
        """
        Union by rank: attach smaller tree under larger tree
        Returns True if union happened, False if already connected
        """
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False  # Already in same set
        
        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        
        self.count -= 1
        return True
    
    def connected(self, x, y):
        """Check if x and y are in same set"""
        return self.find(x) == self.find(y)
    
    def get_count(self):
        """Get number of disjoint sets"""
        return self.count
```

### Problem 5: Number of Provinces (Union-Find)

```python
def findCircleNum(isConnected: list[list[int]]) -> int:
    """
    LeetCode #547 - Count connected components
    
    Time: O(n² * α(n)), Space: O(n)
    """
    n = len(isConnected)
    uf = UnionFind(n)
    
    # Union directly connected cities
    for i in range(n):
        for j in range(i + 1, n):
            if isConnected[i][j] == 1:
                uf.union(i, j)
    
    return uf.get_count()
```

### Problem 6: Redundant Connection

```python
def findRedundantConnection(edges: list[list[int]]) -> list[int]:
    """
    LeetCode #684 - Find edge that creates cycle
    
    Key insight: Union-Find detects cycles!
    When union returns False, we found the edge that creates cycle
    
    Time: O(n * α(n)), Space: O(n)
    """
    n = len(edges)
    uf = UnionFind(n + 1)  # Nodes are 1-indexed
    
    for u, v in edges:
        if not uf.union(u, v):
            return [u, v]  # This edge creates cycle
    
    return []
```

### Problem 7: Accounts Merge

```python
def accountsMerge(accounts: list[list[str]]) -> list[list[str]]:
    """
    LeetCode #721 - Merge accounts with common emails
    
    Time: O(n * k * α(n)), Space: O(n * k)
    where n = accounts, k = emails per account
    """
    uf = UnionFind(len(accounts))
    email_to_id = {}  # email -> account index
    
    # Union accounts with same email
    for i, account in enumerate(accounts):
        for email in account[1:]:
            if email in email_to_id:
                uf.union(i, email_to_id[email])
            else:
                email_to_id[email] = i
    
    # Group emails by root account
    root_to_emails = {}
    for email, acc_id in email_to_id.items():
        root = uf.find(acc_id)
        if root not in root_to_emails:
            root_to_emails[root] = []
        root_to_emails[root].append(email)
    
    # Build result
    result = []
    for root, emails in root_to_emails.items():
        name = accounts[root][0]
        result.append([name] + sorted(emails))
    
    return result
```

---

## 🔧 Core Algorithm 4: Topological Sort

### Topological Sort Concept
- Linear ordering of vertices in DAG (Directed Acyclic Graph)
- If edge u → v, then u appears before v in ordering
- Applications: course prerequisites, build dependencies

### Method 1: DFS-based (Post-order)

```python
def topological_sort_dfs(n, edges):
    """
    DFS-based topological sort
    
    Time: O(V + E), Space: O(V)
    """
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
    
    visited = set()
    result = []
    
    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)
        result.append(node)  # Add after visiting all descendants
    
    for i in range(n):
        if i not in visited:
            dfs(i)
    
    return result[::-1]  # Reverse to get correct order
```

### Method 2: Kahn's Algorithm (BFS-based) ⭐ RECOMMENDED

```python
from collections import deque

def topological_sort_kahn(n, edges):
    """
    Kahn's algorithm - BFS with indegree
    Also detects cycles!
    
    Time: O(V + E), Space: O(V)
    """
    graph = [[] for _ in range(n)]
    indegree = [0] * n
    
    # Build graph and count indegrees
    for u, v in edges:
        graph[u].append(v)
        indegree[v] += 1
    
    # Start with nodes having no prerequisites (indegree = 0)
    queue = deque([i for i in range(n) if indegree[i] == 0])
    result = []
    
    while queue:
        node = queue.popleft()
        result.append(node)
        
        # Remove this node from graph
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    
    # If result has all nodes, no cycle. Otherwise, cycle exists!
    return result if len(result) == n else []
```

### Problem 8: Course Schedule

```python
def canFinish(numCourses: int, prerequisites: list[list[int]]) -> bool:
    """
    LeetCode #207 - Detect cycle in directed graph
    
    Time: O(V + E), Space: O(V + E)
    """
    graph = [[] for _ in range(numCourses)]
    indegree = [0] * numCourses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        indegree[course] += 1
    
    # Kahn's algorithm
    queue = deque([i for i in range(numCourses) if indegree[i] == 0])
    completed = 0
    
    while queue:
        course = queue.popleft()
        completed += 1
        
        for next_course in graph[course]:
            indegree[next_course] -= 1
            if indegree[next_course] == 0:
                queue.append(next_course)
    
    return completed == numCourses
```

### Problem 9: Course Schedule II

```python
def findOrder(numCourses: int, prerequisites: list[list[int]]) -> list[int]:
    """
    LeetCode #210 - Return topological order
    
    Time: O(V + E), Space: O(V + E)
    """
    graph = [[] for _ in range(numCourses)]
    indegree = [0] * numCourses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        indegree[course] += 1
    
    queue = deque([i for i in range(numCourses) if indegree[i] == 0])
    order = []
    
    while queue:
        course = queue.popleft()
        order.append(course)
        
        for next_course in graph[course]:
            indegree[next_course] -= 1
            if indegree[next_course] == 0:
                queue.append(next_course)
    
    return order if len(order) == numCourses else []
```

---

## 🔧 Advanced: Dijkstra's Algorithm (Shortest Path)

### Dijkstra Concept
- Shortest path in **weighted graph** (non-negative weights)
- Greedy approach: always expand closest unvisited node
- Uses priority queue (min-heap)

### Dijkstra Implementation

```python
import heapq

def dijkstra(graph, start, n):
    """
    Find shortest path from start to all nodes
    
    graph: adjacency list with weights [(neighbor, weight), ...]
    
    Time: O((V + E) log V), Space: O(V)
    """
    # Distance to all nodes (initialize to infinity)
    dist = [float('inf')] * n
    dist[start] = 0
    
    # Min-heap: (distance, node)
    heap = [(0, start)]
    visited = set()
    
    while heap:
        d, node = heapq.heappop(heap)
        
        if node in visited:
            continue
        
        visited.add(node)
        
        # Update distances to neighbors
        for neighbor, weight in graph[node]:
            new_dist = d + weight
            
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))
    
    return dist
```

### Problem 10: Network Delay Time

```python
def networkDelayTime(times: list[list[int]], n: int, k: int) -> int:
    """
    LeetCode #743 - Time for signal to reach all nodes
    
    Time: O((V + E) log V), Space: O(V + E)
    """
    # Build graph
    graph = [[] for _ in range(n + 1)]
    for u, v, w in times:
        graph[u].append((v, w))
    
    # Dijkstra from node k
    dist = [float('inf')] * (n + 1)
    dist[k] = 0
    heap = [(0, k)]
    
    while heap:
        d, node = heapq.heappop(heap)
        
        if d > dist[node]:
            continue
        
        for neighbor, weight in graph[node]:
            new_dist = d + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))
    
    # Find max distance (ignore node 0)
    max_dist = max(dist[1:])
    return max_dist if max_dist != float('inf') else -1
```

---

## 💡 Problem Patterns Summary

### Pattern 1: Counting Connected Components
**Use:** DFS, BFS, or Union-Find
- #200 Number of Islands
- #547 Number of Provinces
- #323 Number of Connected Components (Premium)

### Pattern 2: Cycle Detection
**Use:** DFS (3 colors) or Union-Find
- #207 Course Schedule
- #684 Redundant Connection

### Pattern 3: Shortest Path (Unweighted)
**Use:** BFS
- #1091 Shortest Path in Binary Matrix
- #127 Word Ladder
- #994 Rotting Oranges

### Pattern 4: Shortest Path (Weighted)
**Use:** Dijkstra
- #743 Network Delay Time
- #787 Cheapest Flights K Stops

### Pattern 5: Topological Sort
**Use:** Kahn's Algorithm (BFS + indegree)
- #207 Course Schedule
- #210 Course Schedule II
- #269 Alien Dictionary (Premium)

### Pattern 6: Graph Coloring
**Use:** BFS/DFS with 2 colors
- #785 Is Graph Bipartite?
- #886 Possible Bipartition

---

## 🎓 Practice Problems by Difficulty

### Easy
1. **#733 Flood Fill** - DFS/BFS basics
2. **#997 Find the Town Judge** - Graph representation
3. **#1971 Find if Path Exists** - Basic connectivity

### Medium  
1. **#200 Number of Islands** 🚨 **MUST DO**
2. **#207 Course Schedule** 🚨 **MUST DO**
3. **#547 Number of Provinces** - Union-Find template
4. **#133 Clone Graph** - DFS with hash map
5. **#684 Redundant Connection** - Union-Find cycle detection
6. **#785 Is Graph Bipartite?** - Graph coloring
7. **#1091 Shortest Path in Binary Matrix** - BFS shortest path
8. **#994 Rotting Oranges** - Multi-source BFS
9. **#721 Accounts Merge** - Union-Find grouping
10. **#743 Network Delay Time** - Dijkstra

### Hard
1. **#127 Word Ladder** - BFS on implicit graph
2. **#1192 Critical Connections** - Tarjan's algorithm
3. **#269 Alien Dictionary** (Premium) - Topological sort

---

## 🐛 Common Mistakes

### Mistake 1: Not Checking Visited in Graph
```python
# ❌ WRONG - Infinite loop on cyclic graphs!
def dfs(node):
    for neighbor in graph[node]:
        dfs(neighbor)

# ✅ CORRECT
def dfs(node, visited):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor, visited)
```

### Mistake 2: Modifying Matrix While Iterating
```python
# ❌ WRONG - Don't modify what you're iterating over
for r in range(rows):
    for c in range(cols):
        if grid[r][c] == '1':
            grid[r][c] = '0'  # Modifying during iteration

# ✅ CORRECT - Use visited set or mark differently
visited = set()
# OR mark as visited during DFS
```

### Mistake 3: Forgetting Path Compression in Union-Find
```python
# ❌ SLOW - O(n) find operation
def find(self, x):
    while self.parent[x] != x:
        x = self.parent[x]
    return x

# ✅ FAST - O(α(n)) ≈ O(1) with path compression
def find(self, x):
    if self.parent[x] != x:
        self.parent[x] = self.find(self.parent[x])
    return self.parent[x]
```

### Mistake 4: Wrong Direction in Topological Sort
```python
# For prerequisites[i] = [a, b]:
# b is prerequisite of a (b → a)

# ❌ WRONG direction
graph[a].append(b)

# ✅ CORRECT
graph[b].append(a)
```

---

## 💡 Pro Tips

### Tip 1: Choose the Right Algorithm

| Problem Type | Algorithm | Time |
|--------------|-----------|------|
| Connected components | DFS/BFS/Union-Find | O(V+E) |
| Shortest path (unweighted) | BFS | O(V+E) |
| Shortest path (weighted) | Dijkstra | O((V+E)logV) |
| Cycle detection | DFS/Union-Find | O(V+E) |
| Topological sort | Kahn's Algorithm | O(V+E) |

### Tip 2: DFS vs BFS Decision
- **Use DFS when:** Path finding, cycle detection, exploring all paths
- **Use BFS when:** Shortest path (unweighted), level-order

### Tip 3: Union-Find When
- Multiple "merge" operations
- Need to track connected components
- Cycle detection in undirected graphs
- Dynamic connectivity queries

### Tip 4: Grid as Graph
```python
# 4-directional movement
directions = [(0,1), (1,0), (0,-1), (-1,0)]

# 8-directional movement
directions = [(0,1), (1,0), (0,-1), (-1,0), 
              (1,1), (1,-1), (-1,1), (-1,-1)]

# Boundary check template
def is_valid(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols
```

### Tip 5: Multi-source BFS
```python
# Start BFS from multiple sources simultaneously
queue = deque()
for r in range(rows):
    for c in range(cols):
        if grid[r][c] == initial_condition:
            queue.append((r, c, 0))
            visited.add((r, c))

# Then run standard BFS
```

---

## 📊 Algorithm Complexity Cheatsheet

| Algorithm | Time | Space | Notes |
|-----------|------|-------|-------|
| DFS | O(V+E) | O(V) | Recursion stack |
| BFS | O(V+E) | O(V) | Queue storage |
| Union-Find (optimized) | O(α(n)) per op | O(V) | Amortized |
| Topological Sort | O(V+E) | O(V) | Only for DAG |
| Dijkstra | O((V+E)logV) | O(V) | Non-negative weights |
| Bellman-Ford | O(VE) | O(V) | Handles negative weights |

---

## 🎯 Interview Strategy

### Step 1: Identify Graph Type (30 seconds)
- Directed or undirected?
- Weighted or unweighted?
- Sparse or dense?
- Explicit edges or implicit (like grid)?

### Step 2: Choose Representation
- **Adjacency list:** Most common, sparse graphs
- **Adjacency matrix:** Dense graphs, need O(1) edge lookup
- **Edge list:** Union-Find, MST problems

### Step 3: Select Algorithm
- Connectivity? → DFS/BFS/Union-Find
- Shortest path? → BFS (unweighted) or Dijkstra (weighted)
- Order/dependencies? → Topological sort
- Cycle detection? → DFS with 3 colors or Union-Find

### Step 4: Handle Edge Cases
```python
# Always check:
1. Empty graph (no nodes)
2. Single node
3. Disconnected components
4. Cycles
5. Self-loops
6. Duplicate edges
```

---

**Remember:** Graphs are about relationships! Draw the graph first, then choose the right algorithm for the question being asked.

