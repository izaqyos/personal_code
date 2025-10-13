from collections import defaultdict

class Graph:
    def __init__(self, vertices):
        self.graph = defaultdict(list)
        self.V = vertices

    def add_edge(self, u, v):
        self.graph[u].append(v)

    def topological_sort_util(self, v, visited, stack):
        print(f"topological_sort_util exploring {v}")
        visited[v] = True

        for i in self.graph[v]:
            if not visited[i]:
                print(f"topological_sort_util dfsing from {v} to neighbor {i}")
                self.topological_sort_util(i, visited, stack)

        stack.insert(0, v)
        print(f"Added {v} to toposort stack {stack}")

    def topological_sort(self):
        visited = [False] * self.V
        stack = []

        for i in range(self.V):
            print("Checking node",i)
            if not visited[i]:
                self.topological_sort_util(i, visited, stack)

        return stack

# Example usage
g = Graph(6)
g.add_edge(5, 2)
g.add_edge(5, 0)
g.add_edge(4, 0)
g.add_edge(4, 1)
g.add_edge(2, 3)
g.add_edge(3, 1)

print(g.topological_sort())  # expected output: [5, 4, 2, 3, 1, 0]
"""
Checking node 0
topological_sort_util exploring 0
Added 0 to toposort stack [0]
Checking node 1
topological_sort_util exploring 1
Added 1 to toposort stack [1, 0]
Checking node 2
topological_sort_util exploring 2
topological_sort_util dfsing from 2 to neighbor 3
topological_sort_util exploring 3
Added 3 to toposort stack [3, 1, 0]
Added 2 to toposort stack [2, 3, 1, 0]
Checking node 3
Checking node 4
topological_sort_util exploring 4
Added 4 to toposort stack [4, 2, 3, 1, 0]
Checking node 5
topological_sort_util exploring 5
Added 5 to toposort stack [5, 4, 2, 3, 1, 0]
[5, 4, 2, 3, 1, 0]
"""

