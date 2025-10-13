"""
There is a bi-directional graph with n vertices, where each vertex is labeled from 0 to n - 1 (inclusive). The edges in the graph are represented as a 2D integer array edges, where each edges[i] = [ui, vi] denotes a bi-directional edge between vertex ui and vertex vi. Every vertex pair is connected by at most one edge, and no vertex has an edge to itself.

You want to determine if there is a valid path that exists from vertex source to vertex destination.

Given edges and the integers n, source, and destination, return true if there is a valid path from source to destination, or false otherwise.

 

Example 1:


Input: n = 3, edges = [[0,1],[1,2],[2,0]], source = 0, destination = 2
Output: true
Explanation: There are two paths from vertex 0 to vertex 2:
- 0 → 1 → 2
- 0 → 2
Example 2:


Input: n = 6, edges = [[0,1],[0,2],[3,5],[5,4],[4,3]], source = 0, destination = 5
Output: false
Explanation: There is no path from vertex 0 to vertex 5.
 

Constraints:

1 <= n <= 2 * 105
0 <= edges.length <= 2 * 105
edges[i].length == 2
0 <= ui, vi <= n - 1
ui != vi
0 <= source, destination <= n - 1
There are no duplicate edges.
There are no self edges.
"""

# disjoint set 
class dsu:
        def __init__(self, vertices):
            self.v = vertices
            self.parent = [i for i in range(self.v)]

        def areconnected(self, i,j):
            return self.find(i) == self.find(j)

        def union(self, i,j):
            if i!=j:
                pi = self.find(i)
                pj = self.find(j)
                self.parent[pi] =  pj
            

        def find(self, i):
            parent = i
            while parent != self.parent[parent]:
                parent = self.parent[ parent ]
            self.parent[i] = parent
            return parent

    



# BFS, 
from collections import deque
class Solution:


    def createGraph(self, edges: List[List[int]]):
        graph = dict()
        for edge in edges:
            u,v=edge[0], edge[1]
            if u in graph:
                graph[u].add(v)
            else:
                graph[u] = {v}
            if v in graph:
                graph[v].add(u)
            else:
                graph[v] = {u}
        return graph

    def validPathDSU(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
        dsu = DSU(n)
        for edge in edges:
            dsu.union(edge[0], edge[1])
        return dsu.areConnected(source, destination)

    def validPath(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
        """
        idea, BFS. First convert 2d list to a dictionary k- source node to [v1,v2,...] target 
        then do plain old fashioned BFS if path found return True otherwise return False 
        """
        if not edges:
            if source == destination == 0:
                return True
            else:
                return False
        #print(f"{edges}, {source}, {destination}")
        graph = self.createGraph(edges)
        #print(graph)
        visited = set()
        q = deque([source])
        while q:
            node = q.popleft()
            #print(f"poped {node}")
            for t in graph[node]:
                if t == destination:
                    return True
                if not t in visited:
                    visited.add(t)
                    q.append(t)
        return False

