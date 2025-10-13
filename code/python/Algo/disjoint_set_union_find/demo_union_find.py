class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)
        if rootX != rootY:
            if self.rank[rootX] > self.rank[rootY]:
                self.parent[rootY] = rootX
            elif self.rank[rootX] < self.rank[rootY]:
                self.parent[rootX] = rootY
            else:
                self.parent[rootY] = rootX
                self.rank[rootX] += 1

def kruskal(n, edges):
    # Sort edges by weight
    edges.sort(key=lambda x: x[2])
    ds = DisjointSet(n)
    mst = []
    mst_weight = 0

    for u, v, weight in edges:
        if ds.find(u) != ds.find(v):  # Only add edge if it doesn't form a cycle
            ds.union(u, v)
            mst.append((u, v, weight))
            mst_weight += weight

    return mst, mst_weight


def test_mst():
    # Example usage
    n = 4
    edges = [
        (0, 1, 10),
        (0, 2, 6),
        (0, 3, 5),
        (1, 3, 15),
        (2, 3, 4)
    ]
    
    mst, total_weight = kruskal(n, edges)
    print("MST edges:", mst)
    print("Total weight of MST:", total_weight)


def connected_components(n, edges):
    ds = DisjointSet(n)
    for u, v in edges:
        ds.union(u, v)
    # Find unique representatives of each connected component
    components = {}
    for node in range(n):
        root = ds.find(node)
        if root not in components:
            components[root] = []
        components[root].append(node)
    return list(components.values())


def test_connected_components():
    # Example usage
    n = 6
    edges = [
        (0, 1),
        (1, 2),
        (3, 4)
    ]
    components = connected_components(n, edges)
    print("Connected components:", components)


def has_cycle(n, edges):
    ds = DisjointSet(n)
    for u, v in edges:
        if ds.find(u) == ds.find(v):
            return True  # Cycle found
        ds.union(u, v)
    return False  # No cycle found


def test_has_cycle():
    # Example usage
    n = 4
    edges_with_cycle = [
        (0, 1),
        (1, 2),
        (2, 0),
        (2, 3)
    ]
    edges_without_cycle = [
        (0, 1),
        (1, 2),
        (2, 3)
    ]
    print("Graph with cycle:", has_cycle(n, edges_with_cycle))
    print("Graph without cycle:", has_cycle(n, edges_without_cycle))


if __name__ == "__main__":
    test_mst()
    test_connected_components()
    test_has_cycle()
