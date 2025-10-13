class disjointSetQuickFind:
    def __init__(self, N):
        """
        each node is parent of itself
        """
        self.parents = [_ for _ in range(N)]

    def find(self, node_val):
        #just return parent- assume that union does the heavy lifting of joining the subtrees. so find time complexity is O(1)
        return self.parents[node_val]

    def union(self, node_left, node_right):
        print(f"union of {node_left}-{node_right}")
        #union scans parents (O(n)) and joins all left subtree members to right tree 
        for i in range(len(self.parents)):
            if self.parents[i] == node_left:
                self.parents[i] = node_right

    def are_connected(self, node_left, node_right):
        return self.parents[node_left] == self.parents[node_right]

    def __str__(self):
        return f"UF parents: {self.parents}"

def test_case1():
    edges = [[0,1],[1,3], [2,4]]
    UF = disjointSetQuickFind(5)
    print(UF)
    for e in edges:
        UF.union(e[0], e[1])
        print(UF)
    print(f"find 0: {UF.find(0)}")
    print(f"find 1: {UF.find(1)}")
    print(f"find 2: {UF.find(2)}")
    print(f"find 3: {UF.find(3)}")
    print(f"find 4: {UF.find(4)}")

def main():
    test_case1()

if __name__ == '__main__':
    main()
