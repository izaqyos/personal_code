class disjointSetQuickUnion:

    def __init__(self, N):
        """
        each node is parent of itself
        """
        self.parents = [_ for _ in range(N)]

    def find(self, node_val):
        if self.parents[node_val] == node_val: #root
            return self.parents[node_val]
        #the recursion makes find complexity O(n) 
        return self.find(self.parents[node_val])

    def union(self, node_left, node_right):
        print(f"union of {node_left}-{node_right}")
        rleft, rright = self.parents[node_left], self.parents[node_right]
        #since we attach rleft tree ti rright w/o optimization union time complexity is O(1)
        self.parents[rleft] = rright #attach rleft tree to rright

    def are_connected(self, node_left, node_right):
        return self.find(node_left) == self.find(node_right)

    def __str__(self):
        return f"UF parents: {self.parents}"

def test_case1():
    edges = [[0,1],[1,3], [2,4]]
    UF = disjointSetQuickUnion(5)
    print(UF)
    for e in edges:
        UF.union(e[0], e[1])
        print(UF)
    print(f"find 0: {UF.find(0)}")
    print(f"find 1: {UF.find(1)}")
    print(f"find 2: {UF.find(2)}")
    print(f"find 3: {UF.find(3)}")
    print(f"find 4: {UF.find(4)}")
    print(f"Are 0-1 connected? {UF.are_connected(0,1)}")
    print(f"Are 0-2 connected? {UF.are_connected(0,2)}")

def main():
    test_case1()

if __name__ == '__main__':
    main()

