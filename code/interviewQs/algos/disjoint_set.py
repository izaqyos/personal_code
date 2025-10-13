from collections import defaultdict
class DSU:
    def __init__(self, num_vertices):
        self.V = num_vertices
        self.graph = defaultdict(list)
        self.parent = [i for i in range(self.V)]
        print(self)
        

    def find(self, i): #find parent node
        print(f"find {i}")
        if self.parent[i] == i:
            return i
        else: 
            return self.find(self.parent[i])

    def union(self, i,j):
        self.parent[i] = j

    def addEdge(self, i, j):
        self.graph[i].append(j)

    def areConnected(self, i, j):
        return self.find(i) == self.find(j)

    def __str__(self):
        return f"{self.V} vertices. parent: {self.parent}, graph: {self.graph}"


def is_circle(n, edges):
    dsu = DSU(n)
    #build graph
    for edge in edges:
        dsu.addEdge(edge[0], edge[1])

    print(dsu)
    for i in dsu.graph: #iterate all nodes
        for j in dsu.graph[i]: #for each node all it's neighbors , so all edges are processed
            pi = dsu.find(i)
            pj = dsu.find(j)
            if pi==pj: #there are no self cycles so if both nodes are in same set there's a circle 
                return True
            dsu.union(i,j) #since connected union these nodes
            print(f"pi={pi}, pj={pj}, dsu={dsu}")
    return False

def valid_paths(n, edges, source, target):
    dsu = DSU(n)
    for edge in edges:
        dsu.addEdge(edge[0], edge[1])
    for edge in edges:
        dsu.union(edge[0], edge[1])
    print(f"dsu={dsu}")
    return False
    #return dsu.areConnected(source, target)


def test_is_circle():
    g1=[[0,1], [1,2], [2,0]]
    r1 = is_circle(len(g1), g1)
    print(f"{g1} graph is circle {r1}")

    g2=[[0,1], [1,2]]
    r2 = is_circle(3, g2)
    print(f"{g2} graph is circle {r2}")

    g3=[[0,1], [0,2], [2,1]]
    r3 = is_circle(len(g3), g3)
    print(f"{g3} graph is circle {r3}")

def test_is_path():
    input1=(  3, [[0,1],[1,2],[2,0]], 0, 2)
    r1 = valid_paths(*input1)

def main():
    test_is_circle()
    #test_is_path()

if __name__ == "__main__":
    main()
