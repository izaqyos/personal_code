from collections import deque
import sys

class Graph:
    """
    graph member is a dictonary. k - node. v - set of (target node, weight) touple
    """
    def __init__(self):
        self.graph = dict()
        self.weights = dict()
        #self.graph = defaultdict(set)
    
    def addEdge(self, v, u, weight):
        if v in self.graph:
            if not (u in self.graph[v]):
                self.graph[v].add(u)
        else:
            self.graph[v] = {u}
        if u in self.graph:
            if not (v in self.graph[u]):
                self.graph[u].add(v)
        else:
            self.graph[u] = {v}
        self.weights[(u,v)] = weight
        self.weights[(v,u)] = weight

def build_graph():
    g = Graph()
    g.addEdge('a', 'b', 5)
    g.addEdge('b', 'c', 3)
    g.addEdge('a', 'e', 6)
    g.addEdge('a', 'd', 2)
    g.addEdge('d', 'e', 3)
    g.addEdge('d', 'f', 1)
    g.addEdge('e', 'f', 3)
    g.addEdge('e', 'c', 1)
    return g


def dijkstra(graph, root):
    def getMinDistNode(spt_set, distances):
        min_dist = sys.maxsize
        for node in spt_set:
            dist = distances[node]
            if dist<min_dist:
                min_dist = dist
                min_node = node
        return min_node


    nodes = list(graph.graph.keys())
    distances = dict()
    previous = dict()
    spt_set = set()
    for n in nodes:
        distances[n] = sys.maxsize
        previous[n] = None
        spt_set.add(n)

    distances[root] = 0
    while spt_set:
        min_node = getMinDistNode(spt_set, distances)
        spt_set.discard(min_node)
        for neighbor in graph.graph[min_node]:
            if distances[neighbor] > distances[min_node]+graph.weights[(min_node, neighbor)]:
                distances[neighbor] = distances[min_node]+graph.weights[(min_node, neighbor)]
                previous[neighbor] = min_node
    return distances, previous 

def test():
    graph = build_graph()
    nodes = list(graph.graph.keys())
    root = nodes[0]
    distances, previous = dijkstra(graph, root) 
    print('For root {} these are dijkstra calculated distances  and previous dictionaries'.format(root))
    print(distances)
    print(previous)

if __name__ == "__main__":
    test()

