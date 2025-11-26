"""
Week 7, Day 1: Graph Representation

Learning Objectives:
- Learn different graph representations
- Understand adjacency list vs matrix
- Implement graph data structures
- Practice graph construction
- Compare representation trade-offs

Time: 10-15 minutes
"""

from collections import defaultdict, deque

# ============================================================
# EXERCISE 1: Adjacency List
# ============================================================

class GraphAdjList:
    """
    Graph using adjacency list representation.
    
    Adjacency list: Dict of vertex -> list of neighbors
    """
    
    def __init__(self, directed=False):
        self.graph = defaultdict(list)
        self.directed = directed
    
    def add_edge(self, u, v, weight=1):
        """Add edge from u to v"""
        self.graph[u].append((v, weight))
        if not self.directed:
            self.graph[v].append((u, weight))
    
    def get_neighbors(self, v):
        """Get neighbors of vertex v"""
        return self.graph[v]
    
    def get_vertices(self):
        """Get all vertices"""
        return list(self.graph.keys())
    
    def __str__(self):
        """String representation"""
        result = []
        for vertex in sorted(self.graph.keys()):
            neighbors = ', '.join(f"{n}(w={w})" for n, w in self.graph[vertex])
            result.append(f"{vertex} -> {neighbors}")
        return '\n'.join(result)

def test_adjacency_list():
    """Test adjacency list"""
    print("--- Exercise 1: Adjacency List ---")
    
    # Create undirected graph
    g = GraphAdjList(directed=False)
    g.add_edge('A', 'B', 5)
    g.add_edge('A', 'C', 3)
    g.add_edge('B', 'C', 2)
    g.add_edge('B', 'D', 1)
    
    print("Undirected Graph:")
    print(g)
    
    print("\n💡 Adjacency List:")
    print("  • Space: O(V + E)")
    print("  • Add edge: O(1)")
    print("  • Check edge: O(degree)")
    print("  • Good for: Sparse graphs")
    
    print()

# ============================================================
# EXERCISE 2: Adjacency Matrix
# ============================================================

class GraphAdjMatrix:
    """
    Graph using adjacency matrix representation.
    
    Adjacency matrix: 2D array where matrix[i][j] = weight
    """
    
    def __init__(self, vertices, directed=False):
        self.vertices = vertices
        self.directed = directed
        self.vertex_to_idx = {v: i for i, v in enumerate(vertices)}
        n = len(vertices)
        self.matrix = [[0] * n for _ in range(n)]
    
    def add_edge(self, u, v, weight=1):
        """Add edge from u to v"""
        i, j = self.vertex_to_idx[u], self.vertex_to_idx[v]
        self.matrix[i][j] = weight
        if not self.directed:
            self.matrix[j][i] = weight
    
    def has_edge(self, u, v):
        """Check if edge exists"""
        i, j = self.vertex_to_idx[u], self.vertex_to_idx[v]
        return self.matrix[i][j] != 0
    
    def get_neighbors(self, v):
        """Get neighbors of vertex v"""
        i = self.vertex_to_idx[v]
        neighbors = []
        for j, weight in enumerate(self.matrix[i]):
            if weight != 0:
                neighbors.append((self.vertices[j], weight))
        return neighbors
    
    def __str__(self):
        """String representation"""
        result = ["    " + " ".join(f"{v:3}" for v in self.vertices)]
        for i, v in enumerate(self.vertices):
            row = f"{v:3} " + " ".join(f"{self.matrix[i][j]:3}" for j in range(len(self.vertices)))
            result.append(row)
        return '\n'.join(result)

def test_adjacency_matrix():
    """Test adjacency matrix"""
    print("--- Exercise 2: Adjacency Matrix ---")
    
    vertices = ['A', 'B', 'C', 'D']
    g = GraphAdjMatrix(vertices, directed=False)
    g.add_edge('A', 'B', 5)
    g.add_edge('A', 'C', 3)
    g.add_edge('B', 'C', 2)
    g.add_edge('B', 'D', 1)
    
    print("Adjacency Matrix:")
    print(g)
    
    print("\n💡 Adjacency Matrix:")
    print("  • Space: O(V²)")
    print("  • Add edge: O(1)")
    print("  • Check edge: O(1)")
    print("  • Good for: Dense graphs, quick edge lookup")
    
    print()

# ============================================================
# EXERCISE 3: Edge List
# ============================================================

class GraphEdgeList:
    """
    Graph using edge list representation.
    
    Edge list: List of (u, v, weight) tuples
    """
    
    def __init__(self, directed=False):
        self.edges = []
        self.directed = directed
        self.vertices = set()
    
    def add_edge(self, u, v, weight=1):
        """Add edge from u to v"""
        self.edges.append((u, v, weight))
        self.vertices.add(u)
        self.vertices.add(v)
        if not self.directed:
            self.edges.append((v, u, weight))
    
    def get_edges(self):
        """Get all edges"""
        return self.edges
    
    def get_vertices(self):
        """Get all vertices"""
        return list(self.vertices)
    
    def __str__(self):
        """String representation"""
        result = ["Edges:"]
        seen = set()
        for u, v, w in self.edges:
            if self.directed or (u, v) not in seen and (v, u) not in seen:
                result.append(f"  {u} -- {v} (weight: {w})")
                seen.add((u, v))
        return '\n'.join(result)

def test_edge_list():
    """Test edge list"""
    print("--- Exercise 3: Edge List ---")
    
    g = GraphEdgeList(directed=False)
    g.add_edge('A', 'B', 5)
    g.add_edge('A', 'C', 3)
    g.add_edge('B', 'C', 2)
    g.add_edge('B', 'D', 1)
    
    print(g)
    
    print("\n💡 Edge List:")
    print("  • Space: O(E)")
    print("  • Good for: Algorithms that iterate over edges")
    print("  • Used in: Kruskal's MST, edge-based algorithms")
    
    print()

# ============================================================
# EXERCISE 4: Directed vs Undirected
# ============================================================

def directed_vs_undirected():
    """
    Compare directed and undirected graphs.
    
    TODO: Understand differences
    """
    print("--- Exercise 4: Directed vs Undirected ---")
    
    # Undirected graph
    undirected = GraphAdjList(directed=False)
    undirected.add_edge('A', 'B')
    undirected.add_edge('B', 'C')
    
    print("Undirected Graph:")
    print(undirected)
    
    # Directed graph
    directed = GraphAdjList(directed=True)
    directed.add_edge('A', 'B')
    directed.add_edge('B', 'C')
    directed.add_edge('C', 'A')
    
    print("\nDirected Graph:")
    print(directed)
    
    print("\n💡 Directed:")
    print("  • Edges have direction: A → B")
    print("  • Examples: Web links, dependencies, Twitter follows")
    
    print("\n💡 Undirected:")
    print("  • Edges are bidirectional: A ↔ B")
    print("  • Examples: Friendships, roads, networks")
    
    print()

# ============================================================
# EXERCISE 5: Weighted vs Unweighted
# ============================================================

def weighted_vs_unweighted():
    """
    Compare weighted and unweighted graphs.
    
    TODO: Understand use cases
    """
    print("--- Exercise 5: Weighted vs Unweighted ---")
    
    # Unweighted
    unweighted = GraphAdjList()
    unweighted.add_edge('A', 'B')
    unweighted.add_edge('B', 'C')
    
    print("Unweighted Graph:")
    print(unweighted)
    
    # Weighted
    weighted = GraphAdjList()
    weighted.add_edge('A', 'B', 10)
    weighted.add_edge('B', 'C', 5)
    weighted.add_edge('A', 'C', 20)
    
    print("\nWeighted Graph:")
    print(weighted)
    
    print("\n💡 Weighted:")
    print("  • Edges have costs/distances")
    print("  • Examples: Road networks, flight costs")
    
    print("\n💡 Unweighted:")
    print("  • All edges equal (or weight = 1)")
    print("  • Examples: Social networks, simple connections")
    
    print()

# ============================================================
# EXERCISE 6: Real-World Scenario - Social Network
# ============================================================

class SocialNetwork:
    """
    Social network using graph.
    
    TODO: Implement friend connections
    """
    
    def __init__(self):
        self.graph = defaultdict(set)
    
    def add_friendship(self, person1, person2):
        """Add bidirectional friendship"""
        self.graph[person1].add(person2)
        self.graph[person2].add(person1)
    
    def get_friends(self, person):
        """Get all friends"""
        return list(self.graph[person])
    
    def are_friends(self, person1, person2):
        """Check if two people are friends"""
        return person2 in self.graph[person1]
    
    def common_friends(self, person1, person2):
        """Find common friends"""
        return list(self.graph[person1] & self.graph[person2])
    
    def friend_suggestions(self, person):
        """Suggest friends (friends of friends)"""
        friends = self.graph[person]
        suggestions = set()
        
        for friend in friends:
            for friend_of_friend in self.graph[friend]:
                if friend_of_friend != person and friend_of_friend not in friends:
                    suggestions.add(friend_of_friend)
        
        return list(suggestions)

def test_social_network():
    """Test social network"""
    print("--- Exercise 6: Social Network ---")
    
    sn = SocialNetwork()
    sn.add_friendship("Alice", "Bob")
    sn.add_friendship("Alice", "Charlie")
    sn.add_friendship("Bob", "David")
    sn.add_friendship("Charlie", "David")
    sn.add_friendship("David", "Eve")
    
    print("Alice's friends:", sn.get_friends("Alice"))
    print("Bob's friends:", sn.get_friends("Bob"))
    
    print("\nCommon friends (Alice & Bob):", sn.common_friends("Alice", "Bob"))
    print("Friend suggestions for Alice:", sn.friend_suggestions("Alice"))
    
    print()

# ============================================================
# EXERCISE 7: Representation Comparison
# ============================================================

def representation_comparison():
    """
    Compare different representations.
    """
    print("--- Exercise 7: Representation Comparison ---")
    
    print("=" * 60)
    print("GRAPH REPRESENTATION COMPARISON")
    print("=" * 60)
    
    comparisons = [
        ("Operation", "Adj List", "Adj Matrix", "Edge List"),
        ("Space", "O(V + E)", "O(V²)", "O(E)"),
        ("Add vertex", "O(1)", "O(V²)", "O(1)"),
        ("Add edge", "O(1)", "O(1)", "O(1)"),
        ("Remove vertex", "O(E)", "O(V²)", "O(E)"),
        ("Remove edge", "O(E)", "O(1)", "O(E)"),
        ("Check edge", "O(degree)", "O(1)", "O(E)"),
        ("Get neighbors", "O(1)", "O(V)", "O(E)"),
        ("Iterate edges", "O(E)", "O(V²)", "O(E)"),
    ]
    
    print()
    for row in comparisons:
        print(f"{row[0]:<15} {row[1]:<15} {row[2]:<15} {row[3]:<15}")
    
    print("\n" + "=" * 60)
    
    print("\n💡 Choose based on:")
    print("  • Sparse graph (E << V²): Adjacency List")
    print("  • Dense graph (E ≈ V²): Adjacency Matrix")
    print("  • Edge-focused algorithms: Edge List")
    print("  • Need quick edge lookup: Adjacency Matrix")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Complexity analysis for graph representations.
    
    Adjacency List:
    - Best for: Sparse graphs
    - Space: O(V + E)
    - Iterate neighbors: O(degree)
    - Most common in practice
    
    Adjacency Matrix:
    - Best for: Dense graphs, quick edge lookup
    - Space: O(V²)
    - Check edge: O(1)
    - Wastes space for sparse graphs
    
    Edge List:
    - Best for: Edge-based algorithms
    - Space: O(E)
    - Simple representation
    - Slow for neighbor queries
    
    Graph Types:
    - Directed: Edges have direction
    - Undirected: Edges are bidirectional
    - Weighted: Edges have costs
    - Unweighted: All edges equal
    
    Common Graphs:
    - Social networks: Undirected, unweighted
    - Road networks: Undirected, weighted
    - Web pages: Directed, unweighted
    - Flight routes: Directed, weighted
    
    Best Practices:
    - Use adjacency list by default
    - Use matrix for dense graphs
    - Consider memory constraints
    - Choose based on operations needed
    
    Security Considerations:
    - Validate vertex/edge inputs
    - Check for cycles in directed graphs
    - Prevent graph exhaustion attacks
    - Limit graph size
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 7, Day 1: Graph Representation")
    print("=" * 60)
    print()
    
    test_adjacency_list()
    test_adjacency_matrix()
    test_edge_list()
    directed_vs_undirected()
    weighted_vs_unweighted()
    test_social_network()
    representation_comparison()
    
    print("=" * 60)
    print("✅ Day 1 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. Adjacency list: Best for sparse graphs")
    print("2. Adjacency matrix: Best for dense graphs")
    print("3. Edge list: Best for edge-based algorithms")
    print("4. Choose representation based on use case")

