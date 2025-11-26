"""
Week 7, Day 5: Dijkstra's Shortest Path Algorithm

Learning Objectives:
- Understand Dijkstra's algorithm
- Implement shortest path finding
- Learn priority queue usage
- Practice weighted graph algorithms
- Solve path-finding problems

Time: 10-15 minutes
"""

import heapq
from collections import defaultdict

# ============================================================
# EXERCISE 1: Dijkstra's Algorithm Implementation
# ============================================================

def dijkstra_implementation():
    """
    Implement Dijkstra's algorithm.
    
    Dijkstra: Find shortest path in weighted graph
    """
    print("--- Exercise 1: Dijkstra's Algorithm ---")
    
    def dijkstra(graph, start):
        """Find shortest distances from start to all vertices"""
        distances = {vertex: float('inf') for vertex in graph}
        distances[start] = 0
        
        # Priority queue: (distance, vertex)
        pq = [(0, start)]
        visited = set()
        
        while pq:
            current_dist, current = heapq.heappop(pq)
            
            if current in visited:
                continue
            
            visited.add(current)
            
            # Check neighbors
            for neighbor, weight in graph[current]:
                distance = current_dist + weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))
        
        return distances
    
    # Build weighted graph
    graph = {
        'A': [('B', 4), ('C', 2)],
        'B': [('A', 4), ('C', 1), ('D', 5)],
        'C': [('A', 2), ('B', 1), ('D', 8), ('E', 10)],
        'D': [('B', 5), ('C', 8), ('E', 2)],
        'E': [('C', 10), ('D', 2)]
    }
    
    start = 'A'
    distances = dijkstra(graph, start)
    
    print(f"Shortest distances from {start}:")
    for vertex in sorted(distances.keys()):
        print(f"  {start} -> {vertex}: {distances[vertex]}")
    
    print("\n💡 Dijkstra: O((V + E) log V) with min-heap")
    print("💡 Works only with non-negative weights")
    
    print()

# ============================================================
# EXERCISE 2: Dijkstra with Path Reconstruction
# ============================================================

def dijkstra_with_path():
    """
    Dijkstra with path reconstruction.
    
    TODO: Track predecessors to reconstruct path
    """
    print("--- Exercise 2: Path Reconstruction ---")
    
    def dijkstra(graph, start, end):
        """Find shortest path from start to end"""
        distances = {vertex: float('inf') for vertex in graph}
        distances[start] = 0
        predecessors = {vertex: None for vertex in graph}
        
        pq = [(0, start)]
        visited = set()
        
        while pq:
            current_dist, current = heapq.heappop(pq)
            
            if current in visited:
                continue
            
            if current == end:
                break
            
            visited.add(current)
            
            for neighbor, weight in graph[current]:
                distance = current_dist + weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current
                    heapq.heappush(pq, (distance, neighbor))
        
        # Reconstruct path
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = predecessors[current]
        path.reverse()
        
        return distances[end], path
    
    graph = {
        'A': [('B', 4), ('C', 2)],
        'B': [('A', 4), ('C', 1), ('D', 5)],
        'C': [('A', 2), ('B', 1), ('D', 8), ('E', 10)],
        'D': [('B', 5), ('C', 8), ('E', 2)],
        'E': [('C', 10), ('D', 2)]
    }
    
    start, end = 'A', 'E'
    distance, path = dijkstra(graph, start, end)
    
    print(f"Shortest path from {start} to {end}:")
    print(f"  Path: {' -> '.join(path)}")
    print(f"  Distance: {distance}")
    
    print()

# ============================================================
# EXERCISE 3: All Pairs Shortest Path
# ============================================================

def all_pairs_shortest():
    """
    Find shortest paths between all pairs.
    
    TODO: Run Dijkstra from each vertex
    """
    print("--- Exercise 3: All Pairs Shortest Path ---")
    
    def all_pairs_dijkstra(graph):
        """Find shortest distances between all pairs"""
        all_distances = {}
        
        for start in graph:
            distances = {vertex: float('inf') for vertex in graph}
            distances[start] = 0
            
            pq = [(0, start)]
            visited = set()
            
            while pq:
                current_dist, current = heapq.heappop(pq)
                
                if current in visited:
                    continue
                
                visited.add(current)
                
                for neighbor, weight in graph[current]:
                    distance = current_dist + weight
                    
                    if distance < distances[neighbor]:
                        distances[neighbor] = distance
                        heapq.heappush(pq, (distance, neighbor))
            
            all_distances[start] = distances
        
        return all_distances
    
    graph = {
        'A': [('B', 1), ('C', 4)],
        'B': [('A', 1), ('C', 2), ('D', 5)],
        'C': [('A', 4), ('B', 2), ('D', 1)],
        'D': [('B', 5), ('C', 1)]
    }
    
    all_dist = all_pairs_dijkstra(graph)
    
    print("All pairs shortest distances:")
    print(f"{'From':<6}", end='')
    for v in sorted(graph.keys()):
        print(f"{v:>6}", end='')
    print()
    
    for start in sorted(all_dist.keys()):
        print(f"{start:<6}", end='')
        for end in sorted(graph.keys()):
            dist = all_dist[start][end]
            dist_str = str(dist) if dist != float('inf') else '∞'
            print(f"{dist_str:>6}", end='')
        print()
    
    print()

# ============================================================
# EXERCISE 4: Real-World Scenario - GPS Navigation
# ============================================================

def gps_navigation():
    """
    Simulate GPS navigation.
    
    TODO: Find shortest route between cities
    """
    print("--- Exercise 4: GPS Navigation ---")
    
    def find_route(graph, start, end):
        """Find shortest route with path"""
        distances = {city: float('inf') for city in graph}
        distances[start] = 0
        predecessors = {city: None for city in graph}
        
        pq = [(0, start)]
        visited = set()
        
        while pq:
            current_dist, current = heapq.heappop(pq)
            
            if current in visited:
                continue
            
            if current == end:
                break
            
            visited.add(current)
            
            for neighbor, distance in graph[current]:
                new_dist = current_dist + distance
                
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    predecessors[neighbor] = current
                    heapq.heappush(pq, (new_dist, neighbor))
        
        # Reconstruct route
        route = []
        current = end
        while current:
            route.append(current)
            current = predecessors[current]
        route.reverse()
        
        return distances[end], route
    
    # City network (distances in km)
    cities = {
        'NYC': [('Boston', 215), ('Philadelphia', 95)],
        'Boston': [('NYC', 215)],
        'Philadelphia': [('NYC', 95), ('Washington', 140)],
        'Washington': [('Philadelphia', 140), ('Richmond', 110)],
        'Richmond': [('Washington', 110)]
    }
    
    start, end = 'NYC', 'Richmond'
    distance, route = find_route(cities, start, end)
    
    print(f"Route from {start} to {end}:")
    for i in range(len(route) - 1):
        print(f"  {route[i]} -> {route[i+1]}")
    print(f"\nTotal distance: {distance} km")
    
    print()

# ============================================================
# EXERCISE 5: Dijkstra vs BFS
# ============================================================

def dijkstra_vs_bfs():
    """
    Compare Dijkstra with BFS.
    
    TODO: Understand when to use each
    """
    print("--- Exercise 5: Dijkstra vs BFS ---")
    
    from collections import deque
    
    def bfs_shortest(graph, start, end):
        """BFS for unweighted graph"""
        queue = deque([(start, [start])])
        visited = {start}
        
        while queue:
            vertex, path = queue.popleft()
            
            if vertex == end:
                return len(path) - 1, path
            
            for neighbor, _ in graph[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return float('inf'), []
    
    # Unweighted graph (all weights = 1)
    graph = {
        'A': [('B', 1), ('C', 1)],
        'B': [('A', 1), ('D', 1)],
        'C': [('A', 1), ('D', 1)],
        'D': [('B', 1), ('C', 1), ('E', 1)],
        'E': [('D', 1)]
    }
    
    start, end = 'A', 'E'
    
    # BFS
    bfs_dist, bfs_path = bfs_shortest(graph, start, end)
    print(f"BFS path: {' -> '.join(bfs_path)} (distance: {bfs_dist})")
    
    # Dijkstra
    def dijkstra_path(graph, start, end):
        distances = {v: float('inf') for v in graph}
        distances[start] = 0
        predecessors = {v: None for v in graph}
        pq = [(0, start)]
        visited = set()
        
        while pq:
            dist, curr = heapq.heappop(pq)
            if curr in visited:
                continue
            if curr == end:
                break
            visited.add(curr)
            
            for neighbor, weight in graph[curr]:
                new_dist = dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    predecessors[neighbor] = curr
                    heapq.heappush(pq, (new_dist, neighbor))
        
        path = []
        curr = end
        while curr:
            path.append(curr)
            curr = predecessors[curr]
        return distances[end], path[::-1]
    
    dijk_dist, dijk_path = dijkstra_path(graph, start, end)
    print(f"Dijkstra path: {' -> '.join(dijk_path)} (distance: {dijk_dist})")
    
    print("\n💡 For unweighted graphs:")
    print("  • BFS: Simpler, O(V + E)")
    print("  • Dijkstra: More general, O((V + E) log V)")
    
    print("\n💡 For weighted graphs:")
    print("  • Must use Dijkstra (or Bellman-Ford for negative weights)")
    
    print()

# ============================================================
# EXERCISE 6: Modified Dijkstra - K Stops
# ============================================================

def dijkstra_k_stops():
    """
    Shortest path with at most k stops.
    
    TODO: Modified Dijkstra with stop limit
    """
    print("--- Exercise 6: Shortest Path with K Stops ---")
    
    def shortest_path_k_stops(graph, start, end, k):
        """Find shortest path with at most k stops"""
        # (cost, vertex, stops)
        pq = [(0, start, 0)]
        visited = {}
        
        while pq:
            cost, vertex, stops = heapq.heappop(pq)
            
            if vertex == end:
                return cost
            
            if stops > k:
                continue
            
            if vertex in visited and visited[vertex] <= stops:
                continue
            
            visited[vertex] = stops
            
            for neighbor, weight in graph[vertex]:
                heapq.heappush(pq, (cost + weight, neighbor, stops + 1))
        
        return -1
    
    graph = {
        'A': [('B', 100), ('C', 500)],
        'B': [('C', 100), ('D', 600)],
        'C': [('D', 200)],
        'D': []
    }
    
    start, end = 'A', 'D'
    
    for k in [0, 1, 2]:
        cost = shortest_path_k_stops(graph, start, end, k)
        print(f"Shortest path with ≤{k} stops: {cost if cost != -1 else 'No path'}")
    
    print()

# ============================================================
# BONUS CHALLENGE: A* Algorithm Preview
# ============================================================

def astar_preview():
    """
    Preview of A* algorithm.
    
    A*: Dijkstra + heuristic for faster pathfinding
    """
    print("--- Bonus Challenge: A* Preview ---")
    
    def astar(graph, start, end, heuristic):
        """A* algorithm with heuristic"""
        # (f_score, g_score, vertex)
        pq = [(heuristic[start], 0, start)]
        visited = set()
        predecessors = {start: None}
        g_scores = {vertex: float('inf') for vertex in graph}
        g_scores[start] = 0
        
        while pq:
            _, g_score, current = heapq.heappop(pq)
            
            if current in visited:
                continue
            
            if current == end:
                # Reconstruct path
                path = []
                while current:
                    path.append(current)
                    current = predecessors[current]
                return g_score, path[::-1]
            
            visited.add(current)
            
            for neighbor, weight in graph[current]:
                tentative_g = g_score + weight
                
                if tentative_g < g_scores[neighbor]:
                    g_scores[neighbor] = tentative_g
                    f_score = tentative_g + heuristic[neighbor]
                    predecessors[neighbor] = current
                    heapq.heappush(pq, (f_score, tentative_g, neighbor))
        
        return float('inf'), []
    
    graph = {
        'A': [('B', 1), ('C', 4)],
        'B': [('D', 2)],
        'C': [('D', 1)],
        'D': []
    }
    
    # Heuristic: estimated distance to goal
    heuristic = {'A': 3, 'B': 2, 'C': 1, 'D': 0}
    
    distance, path = astar(graph, 'A', 'D', heuristic)
    print(f"A* path: {' -> '.join(path)} (distance: {distance})")
    
    print("\n💡 A* = Dijkstra + heuristic")
    print("💡 Faster for pathfinding with good heuristic")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    Dijkstra's Algorithm:
    - Time: O((V + E) log V) with binary heap
    - Time: O(V²) with array
    - Space: O(V) for distances and priority queue
    
    Optimizations:
    - Use Fibonacci heap: O(E + V log V)
    - Early termination when target found
    - Bidirectional search
    
    Limitations:
    - Doesn't work with negative weights
    - Use Bellman-Ford for negative weights
    - Use Floyd-Warshall for all pairs
    
    Applications:
    - GPS navigation
    - Network routing
    - Game pathfinding
    - Resource allocation
    
    Best Practices:
    - Use priority queue (heapq)
    - Track visited vertices
    - Store predecessors for path reconstruction
    - Handle disconnected graphs
    
    Common Patterns:
    - Priority queue with (distance, vertex)
    - Update distances when shorter path found
    - Reconstruct path from predecessors
    - Early termination optimization
    
    Security Considerations:
    - Validate graph structure
    - Limit graph size
    - Handle negative weights carefully
    - Prevent infinite loops
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 7, Day 5: Dijkstra's Algorithm")
    print("=" * 60)
    print()
    
    dijkstra_implementation()
    dijkstra_with_path()
    all_pairs_shortest()
    gps_navigation()
    dijkstra_vs_bfs()
    dijkstra_k_stops()
    astar_preview()
    
    print("=" * 60)
    print("✅ Day 5 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. Dijkstra finds shortest paths in weighted graphs")
    print("2. Time: O((V + E) log V) with min-heap")
    print("3. Doesn't work with negative weights")
    print("4. Essential for GPS, routing, pathfinding")

