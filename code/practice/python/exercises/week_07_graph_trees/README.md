# Week 7: Graph & Tree Algorithms

Master essential graph and tree data structures and algorithms.

## Overview

This week focuses on graphs and trees - fundamental data structures for representing relationships and hierarchies. Learn traversal algorithms, shortest path finding, and tree operations essential for solving complex problems.

## Daily Breakdown

### Day 1: Graph Representation
**File:** `day1_graph_representation.py`

Learn different ways to represent graphs:
- Adjacency list (most common)
- Adjacency matrix (dense graphs)
- Edge list (edge-focused algorithms)
- Directed vs undirected graphs
- Weighted vs unweighted graphs

**Key Concepts:**
- Adjacency list: O(V + E) space
- Adjacency matrix: O(V²) space
- Choose based on graph density and operations

---

### Day 2: BFS and DFS Traversal
**File:** `day2_bfs_dfs.py`

Master graph traversal algorithms:
- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- Shortest path with BFS
- Connected components
- Cycle detection
- Topological sort

**Complexity:**
- Both: O(V + E) time
- BFS: Queue-based, level-order
- DFS: Stack/recursion-based, deep exploration

---

### Day 3: Binary Trees
**File:** `day3_binary_trees.py`

Learn binary tree operations:
- Tree node structure
- Inorder traversal (Left-Root-Right)
- Preorder traversal (Root-Left-Right)
- Postorder traversal (Left-Right-Root)
- Level-order traversal (BFS)
- Tree properties (height, size, leaves)

**Key Operations:**
- All traversals: O(n) time
- Recursion natural for trees
- Level-order uses queue

---

### Day 4: Binary Search Trees (BST)
**File:** `day4_bst.py`

Master BST operations:
- BST property: Left < Root < Right
- Search, insert, delete
- Validate BST
- Kth smallest element
- Range queries
- Lowest common ancestor

**Complexity:**
- Balanced BST: O(log n) operations
- Unbalanced: O(n) worst case
- Inorder gives sorted order

---

### Day 5: Dijkstra's Algorithm
**File:** `day5_dijkstra.py`

Learn shortest path algorithms:
- Dijkstra's algorithm
- Path reconstruction
- All pairs shortest path
- GPS navigation
- Priority queue usage
- A* algorithm preview

**Key Points:**
- Time: O((V + E) log V) with heap
- Works only with non-negative weights
- Essential for routing and pathfinding

---

### Day 6: Trie (Prefix Tree)
**File:** `day6_trie.py`

Master trie data structure:
- Trie node structure
- Insert, search, prefix matching
- Autocomplete
- Spell checker
- Word search with wildcards
- Frequency tracking

**Complexity:**
- Insert/Search: O(m) where m = word length
- Perfect for prefix operations
- Trade space for speed

---

### Day 7: Review & Challenge
**File:** `day7_review_challenge.py`

Apply all concepts:
- **Challenge 1:** Course schedule (cycle detection)
- **Challenge 2:** Clone graph
- **Challenge 3:** Word ladder (BFS)
- **Challenge 4:** Serialize/deserialize tree
- **Challenge 5:** Network delay time (Dijkstra)
- **Challenge 6:** Trie with prefix count
- **Challenge 7:** Maximum path sum

---

## Quick Reference

### Graph Traversal

```python
from collections import deque, defaultdict

# BFS
def bfs(graph, start):
    visited = set([start])
    queue = deque([start])
    
    while queue:
        vertex = queue.popleft()
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

# DFS (recursive)
def dfs(graph, vertex, visited=None):
    if visited is None:
        visited = set()
    visited.add(vertex)
    
    for neighbor in graph[vertex]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
```

### Binary Tree Traversals

```python
# Inorder (Left-Root-Right)
def inorder(root):
    if root:
        inorder(root.left)
        print(root.val)
        inorder(root.right)

# Preorder (Root-Left-Right)
def preorder(root):
    if root:
        print(root.val)
        preorder(root.left)
        preorder(root.right)

# Postorder (Left-Right-Root)
def postorder(root):
    if root:
        postorder(root.left)
        postorder(root.right)
        print(root.val)

# Level-order (BFS)
def level_order(root):
    if not root:
        return
    queue = deque([root])
    while queue:
        node = queue.popleft()
        print(node.val)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
```

### BST Operations

```python
class BST:
    def insert(self, root, val):
        if not root:
            return TreeNode(val)
        if val < root.val:
            root.left = self.insert(root.left, val)
        else:
            root.right = self.insert(root.right, val)
        return root
    
    def search(self, root, val):
        if not root or root.val == val:
            return root
        if val < root.val:
            return self.search(root.left, val)
        return self.search(root.right, val)
```

### Dijkstra's Algorithm

```python
import heapq

def dijkstra(graph, start):
    distances = {v: float('inf') for v in graph}
    distances[start] = 0
    pq = [(0, start)]
    visited = set()
    
    while pq:
        dist, vertex = heapq.heappop(pq)
        if vertex in visited:
            continue
        visited.add(vertex)
        
        for neighbor, weight in graph[vertex]:
            new_dist = dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor))
    
    return distances
```

### Trie

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end
```

---

## Algorithm Complexity Summary

| Algorithm | Time | Space | Use Case |
|-----------|------|-------|----------|
| **BFS** | O(V + E) | O(V) | Shortest path, level-order |
| **DFS** | O(V + E) | O(V) | Cycle detection, topological sort |
| **Tree Traversal** | O(n) | O(h) | Process all nodes |
| **BST Search** | O(log n)* | O(1) | Find in sorted data |
| **Dijkstra** | O((V+E) log V) | O(V) | Shortest path (weighted) |
| **Trie Insert/Search** | O(m) | O(ALPHABET × N × M) | Prefix operations |

*O(log n) for balanced BST, O(n) worst case

---

## Common Patterns

### Finding Shortest Path
```python
# Unweighted: Use BFS
# Weighted (non-negative): Use Dijkstra
# Weighted (negative): Use Bellman-Ford
```

### Tree Problems
```python
# Most tree problems: Use recursion
# Level-order: Use BFS with queue
# Path problems: Track path in recursion
```

### Graph Problems
```python
# Connected components: DFS/BFS
# Cycle detection: DFS with parent/color tracking
# Topological sort: DFS with post-order
```

---

## When to Use Each

| Problem Type | Best Algorithm |
|--------------|----------------|
| Shortest path (unweighted) | BFS |
| Shortest path (weighted) | Dijkstra |
| Cycle detection | DFS |
| Topological sort | DFS |
| Tree traversal | Recursion (DFS) |
| Level-order | BFS |
| BST operations | Recursion |
| Autocomplete | Trie |
| Spell check | Trie |

---

## Learning Outcomes

After completing Week 7, you should be able to:

✅ Represent graphs using different structures  
✅ Implement BFS and DFS traversals  
✅ Perform all binary tree traversals  
✅ Implement BST operations  
✅ Find shortest paths with Dijkstra  
✅ Use tries for prefix operations  
✅ Choose appropriate algorithms for problems  
✅ Solve complex graph and tree problems  

---

## Running the Exercises

```bash
# Run individual days
python day1_graph_representation.py
python day2_bfs_dfs.py
python day3_binary_trees.py
python day4_bst.py
python day5_dijkstra.py
python day6_trie.py
python day7_review_challenge.py

# Run all
for day in day*.py; do python "$day"; done
```

---

## Additional Resources

**Official Documentation:**
- [collections.deque](https://docs.python.org/3/library/collections.html#collections.deque)
- [heapq module](https://docs.python.org/3/library/heapq.html)

**Further Reading:**
- [Graph Algorithms](https://realpython.com/python-graph-data-structures/)
- [Binary Trees](https://realpython.com/binary-search-tree-python/)

---

## Next Steps

🎯 **Week 8:** Dynamic Programming  
Learn to solve optimization problems with memoization and tabulation.

---

## Notes

- Graphs and trees are everywhere in CS
- Master traversals - they're fundamental
- Dijkstra is essential for routing
- Tries are perfect for autocomplete
- Practice, practice, practice!

**Time Investment:** ~10-15 minutes per day, 15-20 minutes for Day 7  
**Total:** ~90 minutes for the week

---

*Happy graph and tree traversing! 🐍*

