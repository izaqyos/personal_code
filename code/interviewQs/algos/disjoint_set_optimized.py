"""
optimized union-find. 2 improvements:
a.    union by rank 
keep track of tree length by keeping track of rank (init to 1)
Then on union use rank to attach shorter tree to root of longer

b. find path compression.
during find when attaching to new tree attach to grandparent instead of parent, thus halving length
"""

class disjointSetOptimized:
    def __init__(self, N):
        """
        each node is parent of itself
        """
        self.parents = [_ for _ in range(N)]
        self.ranks = [1 for _ in range(N)]

    """
    since the trees are balanced in both find and union they are both O(nlogn) time complexity
    """
    def find(self, node_val):
        while self.parents[node_val] != node_val: #root
            self.parents[node_val] = self.parents[self.parents[node_val]] #set to grandparent if there is, otherwise to parent
            node_val = self.parents[node_val]  #traverse up towards set root
        return node_val

    def union(self, node_left, node_right):
        print(f"union of {node_left}-{node_right}")
        rleft, rright = self.parents[node_left], self.parents[node_right]
        if rleft == rright:
            return
        if self.ranks[rleft] < self.ranks[rright]:
            self.parents[rleft] = rright
        elif self.ranks[rright] < self.ranks[rleft]: 
            self.parents[rright] = rleft
        else: #both left and right are same height
            self.parents[rleft] = rright # arbitrarily add left to right
            self.ranks[rright] +=1 

    def are_connected(self, node_left, node_right):
        return self.find(node_left) == self.find(node_right)

    def __str__(self):
        return f"UF parents: {self.parents}"

def test_case1():
    edges = [[0,1],[1,3], [2,4]]
    UF = disjointSetOptimized(5)
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


