from typing import TypeVar

Location = TypeVar('Location')
T = TypeVar('T')

class Graph():
    def neighbours(self, id: Location) -> list[Location]:
        pass 

class SimpleGraph:
    def __init__(self) -> None:
        self.edges: dict[Location: list[Location]] = {}

    def neighbors(self, id: Location) -> list[Location]:
        return self.edges[id]


import collections
class Queue():
    def __init__(self):
        self.q = collections.deque()

    def is_empty(self) -> bool:
        return not self.q

    def put(self, elem: T):
        self.q.append(elem)

    def get(self) -> T:
        return self.q.popleft()

def bfs(graph: Graph, start: Location):
    q: Queue = Queue()
    visited: dict[Location, bool] = {}
    visited[start] = True
    q.put(start)

    while not q.is_empty():
        cur = q.get()
        print(f"Currently visiting node {cur}, neighbors={graph.neighbors(cur)}")
        for neighbor in graph.neighbors(cur):
            if not neighbor in visited or not visited[neighbor]:
                visited[neighbor] = True
                q.put(neighbor)

def test():
    example_graph = SimpleGraph()
    example_graph.edges = {
        'A': ['B'],
        'B': ['C'],
        'C': ['B', 'D', 'F'],
        'D': ['C', 'E'],
        'E': ['F'],
        'F': [],
    }
    print('Reachable from A:')
    bfs(example_graph, 'A')
    print('Reachable from E:')
    bfs(example_graph, 'E')

if __name__ == '__main__':
    test()


