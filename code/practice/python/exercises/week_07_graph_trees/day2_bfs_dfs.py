"""
Week 7, Day 2: BFS and DFS Traversal

Learning Objectives:
- Master Breadth-First Search (BFS)
- Master Depth-First Search (DFS)
- Understand traversal applications
- Practice recursive and iterative approaches
- Solve graph problems with traversal

Time: 10-15 minutes
"""

from collections import deque, defaultdict

# ============================================================
# EXERCISE 1: BFS Implementation
# ============================================================

def bfs_implementation():
    """
    Implement Breadth-First Search.
    
    BFS: Explore level by level using queue
    """
    print("--- Exercise 1: BFS Implementation ---")
    
    def bfs(graph, start):
        """BFS traversal from start vertex"""
        visited = set()
        queue = deque([start])
        visited.add(start)
        result = []
        
        while queue:
            vertex = queue.popleft()
            result.append(vertex)
            
            for neighbor, _ in graph[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return result
    
    # Build graph
    graph = defaultdict(list)
    edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('B', 'E'), ('C', 'F')]
    for u, v in edges:
        graph[u].append((v, 1))
        graph[v].append((u, 1))
    
    print("Graph edges:", edges)
    result = bfs(graph, 'A')
    print(f"BFS from A: {' -> '.join(result)}")
    
    print("\n💡 BFS:")
    print("  • Time: O(V + E)")
    print("  • Space: O(V) for queue")
    print("  • Finds shortest path (unweighted)")
    print("  • Level-order traversal")
    
    print()

# ============================================================
# EXERCISE 2: DFS Implementation (Recursive)
# ============================================================

def dfs_recursive():
    """
    Implement DFS recursively.
    
    DFS: Explore as deep as possible before backtracking
    """
    print("--- Exercise 2: DFS (Recursive) ---")
    
    def dfs(graph, vertex, visited, result):
        """DFS traversal from vertex"""
        visited.add(vertex)
        result.append(vertex)
        
        for neighbor, _ in graph[vertex]:
            if neighbor not in visited:
                dfs(graph, neighbor, visited, result)
    
    def dfs_traversal(graph, start):
        """Start DFS from start vertex"""
        visited = set()
        result = []
        dfs(graph, start, visited, result)
        return result
    
    # Build graph
    graph = defaultdict(list)
    edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('B', 'E'), ('C', 'F')]
    for u, v in edges:
        graph[u].append((v, 1))
        graph[v].append((u, 1))
    
    print("Graph edges:", edges)
    result = dfs_traversal(graph, 'A')
    print(f"DFS from A: {' -> '.join(result)}")
    
    print("\n💡 DFS (Recursive):")
    print("  • Time: O(V + E)")
    print("  • Space: O(V) for call stack")
    print("  • Simple and elegant")
    
    print()

# ============================================================
# EXERCISE 3: DFS Implementation (Iterative)
# ============================================================

def dfs_iterative():
    """
    Implement DFS iteratively.
    
    DFS: Use stack instead of recursion
    """
    print("--- Exercise 3: DFS (Iterative) ---")
    
    def dfs(graph, start):
        """DFS traversal using stack"""
        visited = set()
        stack = [start]
        result = []
        
        while stack:
            vertex = stack.pop()
            
            if vertex not in visited:
                visited.add(vertex)
                result.append(vertex)
                
                # Add neighbors in reverse for same order as recursive
                for neighbor, _ in reversed(graph[vertex]):
                    if neighbor not in visited:
                        stack.append(neighbor)
        
        return result
    
    # Build graph
    graph = defaultdict(list)
    edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('B', 'E'), ('C', 'F')]
    for u, v in edges:
        graph[u].append((v, 1))
        graph[v].append((u, 1))
    
    print("Graph edges:", edges)
    result = dfs(graph, 'A')
    print(f"DFS from A: {' -> '.join(result)}")
    
    print("\n💡 DFS (Iterative):")
    print("  • Time: O(V + E)")
    print("  • Space: O(V) for stack")
    print("  • Avoids recursion limit")
    
    print()

# ============================================================
# EXERCISE 4: Shortest Path (BFS)
# ============================================================

def shortest_path_bfs():
    """
    Find shortest path using BFS.
    
    TODO: BFS finds shortest path in unweighted graph
    """
    print("--- Exercise 4: Shortest Path (BFS) ---")
    
    def shortest_path(graph, start, end):
        """Find shortest path from start to end"""
        if start == end:
            return [start]
        
        visited = {start}
        queue = deque([(start, [start])])
        
        while queue:
            vertex, path = queue.popleft()
            
            for neighbor, _ in graph[vertex]:
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    
                    if neighbor == end:
                        return new_path
                    
                    visited.add(neighbor)
                    queue.append((neighbor, new_path))
        
        return None
    
    # Build graph
    graph = defaultdict(list)
    edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D'), ('D', 'E')]
    for u, v in edges:
        graph[u].append((v, 1))
        graph[v].append((u, 1))
    
    print("Graph edges:", edges)
    path = shortest_path(graph, 'A', 'E')
    print(f"Shortest path A -> E: {' -> '.join(path)}")
    
    print()

# ============================================================
# EXERCISE 5: Connected Components
# ============================================================

def connected_components():
    """
    Find connected components using DFS.
    
    TODO: Use DFS to find all components
    """
    print("--- Exercise 5: Connected Components ---")
    
    def find_components(graph):
        """Find all connected components"""
        visited = set()
        components = []
        
        def dfs(vertex, component):
            """DFS to explore component"""
            visited.add(vertex)
            component.append(vertex)
            
            for neighbor, _ in graph[vertex]:
                if neighbor not in visited:
                    dfs(neighbor, component)
        
        # Try each vertex
        for vertex in graph:
            if vertex not in visited:
                component = []
                dfs(vertex, component)
                components.append(sorted(component))
        
        return components
    
    # Build graph with multiple components
    graph = defaultdict(list)
    edges = [
        ('A', 'B'), ('B', 'C'),  # Component 1
        ('D', 'E'),              # Component 2
        ('F', 'G'), ('G', 'H')   # Component 3
    ]
    for u, v in edges:
        graph[u].append((v, 1))
        graph[v].append((u, 1))
    
    # Add isolated vertices
    for v in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
        if v not in graph:
            graph[v] = []
    
    print("Graph edges:", edges)
    components = find_components(graph)
    print(f"Connected components: {components}")
    
    print()

# ============================================================
# EXERCISE 6: Cycle Detection
# ============================================================

def cycle_detection():
    """
    Detect cycles using DFS.
    
    TODO: Use DFS with parent tracking
    """
    print("--- Exercise 6: Cycle Detection ---")
    
    def has_cycle_undirected(graph):
        """Detect cycle in undirected graph"""
        visited = set()
        
        def dfs(vertex, parent):
            """DFS with parent tracking"""
            visited.add(vertex)
            
            for neighbor, _ in graph[vertex]:
                if neighbor not in visited:
                    if dfs(neighbor, vertex):
                        return True
                elif neighbor != parent:
                    # Visited and not parent = cycle
                    return True
            
            return False
        
        # Check each component
        for vertex in graph:
            if vertex not in visited:
                if dfs(vertex, None):
                    return True
        
        return False
    
    # Graph without cycle
    graph1 = defaultdict(list)
    edges1 = [('A', 'B'), ('B', 'C'), ('C', 'D')]
    for u, v in edges1:
        graph1[u].append((v, 1))
        graph1[v].append((u, 1))
    
    print("Graph 1 (no cycle):", edges1)
    print(f"Has cycle: {has_cycle_undirected(graph1)}")
    
    # Graph with cycle
    graph2 = defaultdict(list)
    edges2 = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A')]
    for u, v in edges2:
        graph2[u].append((v, 1))
        graph2[v].append((u, 1))
    
    print(f"\nGraph 2 (with cycle): {edges2}")
    print(f"Has cycle: {has_cycle_undirected(graph2)}")
    
    print()

# ============================================================
# EXERCISE 7: Real-World Scenario - Web Crawler
# ============================================================

def web_crawler():
    """
    Simulate web crawler using BFS.
    
    TODO: BFS to crawl web pages
    """
    print("--- Exercise 7: Web Crawler ---")
    
    def crawl(start_url, max_depth=2):
        """Crawl web pages up to max_depth"""
        # Simulated web graph
        web = {
            'home.html': ['about.html', 'products.html'],
            'about.html': ['team.html', 'contact.html'],
            'products.html': ['product1.html', 'product2.html'],
            'team.html': [],
            'contact.html': [],
            'product1.html': ['reviews.html'],
            'product2.html': [],
            'reviews.html': []
        }
        
        visited = set()
        queue = deque([(start_url, 0)])
        visited.add(start_url)
        crawled = []
        
        while queue:
            url, depth = queue.popleft()
            crawled.append((url, depth))
            
            if depth < max_depth:
                for link in web.get(url, []):
                    if link not in visited:
                        visited.add(link)
                        queue.append((link, depth + 1))
        
        return crawled
    
    result = crawl('home.html', max_depth=2)
    
    print("Crawled pages (max depth 2):")
    for url, depth in result:
        print(f"  {'  ' * depth}{url} (depth {depth})")
    
    print()

# ============================================================
# BONUS CHALLENGE: Topological Sort
# ============================================================

def topological_sort():
    """
    Topological sort using DFS.
    
    TODO: Order vertices in directed acyclic graph
    """
    print("--- Bonus Challenge: Topological Sort ---")
    
    def topo_sort(graph):
        """Topological sort of DAG"""
        visited = set()
        stack = []
        
        def dfs(vertex):
            """DFS to build topological order"""
            visited.add(vertex)
            
            for neighbor, _ in graph[vertex]:
                if neighbor not in visited:
                    dfs(neighbor)
            
            stack.append(vertex)
        
        # Process all vertices
        for vertex in graph:
            if vertex not in visited:
                dfs(vertex)
        
        return stack[::-1]
    
    # Course prerequisites (directed graph)
    graph = defaultdict(list)
    prereqs = [
        ('Math', 'Physics'),
        ('Math', 'CS'),
        ('Physics', 'Engineering'),
        ('CS', 'AI'),
        ('CS', 'Engineering')
    ]
    
    for u, v in prereqs:
        graph[u].append((v, 1))
    
    # Ensure all vertices in graph
    for u, v in prereqs:
        if u not in graph:
            graph[u] = []
        if v not in graph:
            graph[v] = []
    
    print("Course prerequisites:")
    for u, v in prereqs:
        print(f"  {u} -> {v}")
    
    order = topo_sort(graph)
    print(f"\nCourse order: {' -> '.join(order)}")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    BFS:
    - Time: O(V + E)
    - Space: O(V) for queue
    - Uses queue (FIFO)
    - Level-order traversal
    
    DFS:
    - Time: O(V + E)
    - Space: O(V) for stack/recursion
    - Uses stack (LIFO)
    - Goes deep first
    
    Applications:
    - BFS: Shortest path, level-order, web crawling
    - DFS: Topological sort, cycle detection, maze solving
    
    BFS vs DFS:
    - BFS: Better for shortest path
    - DFS: Better for exploring all paths
    - BFS: More memory for wide graphs
    - DFS: Risk of deep recursion
    
    Best Practices:
    - Track visited vertices
    - Handle disconnected components
    - Choose based on problem requirements
    - Consider iterative vs recursive
    
    Common Patterns:
    - Shortest path: BFS
    - Cycle detection: DFS
    - Connected components: DFS
    - Topological sort: DFS
    
    Security Considerations:
    - Limit traversal depth
    - Prevent infinite loops
    - Validate graph structure
    - Handle large graphs carefully
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 7, Day 2: BFS and DFS Traversal")
    print("=" * 60)
    print()
    
    bfs_implementation()
    dfs_recursive()
    dfs_iterative()
    shortest_path_bfs()
    connected_components()
    cycle_detection()
    web_crawler()
    topological_sort()
    
    print("=" * 60)
    print("✅ Day 2 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. BFS: Level-order, shortest path")
    print("2. DFS: Deep exploration, topological sort")
    print("3. Both: O(V + E) time complexity")
    print("4. Choose based on problem requirements")

