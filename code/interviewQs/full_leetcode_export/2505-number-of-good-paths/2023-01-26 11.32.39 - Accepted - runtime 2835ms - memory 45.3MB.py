"""
here is a tree (i.e. a connected, undirected graph with no cycles) consisting of n nodes numbered from 0 to n - 1 and exactly n - 1 edges.
You are given a 0-indexed integer array vals of length n where vals[i] denotes the value of the ith node. You are also given a 2D integer array edges where edges[i] = [ai, bi] denotes that there exists an undirected edge connecting nodes ai and bi.
A good path is a simple path that satisfies the following conditions:
* 		The starting node and the ending node have the same value.
* 		All nodes between the starting node and the ending node have values less than or equal to the starting node (i.e. the starting node's value should be the maximum value along the path).
Return the number of distinct good paths.
Note that a path and its reverse are counted as the same path. For example, 0 -> 1 is considered to be the same as 1 -> 0. A single node is also considered as a valid path.

I'll provide two solutions.
First using BFS on all nodes. space complexity O(1), time complexity O(n^2)
idea: just iterate all nodes. for each node do BFS. don't cont. to nodes who break good path condition (val>root val), for each val==root val +1 to good paths. add all nodes as single node good path
second union-find bases solution. space complexity O(n), time complexity O(nlog(n))
idea. sort nodes ascending then iterate over all nodes. 
we need a dictionary that maps values to nodes
for each value and it;s list of nodes try to add to disjoint-set (union-find) . if there's only one node skip since can't be start of good path (requires at least another node w/ same value).
    examine adjacent nodes. can they be added to UF?- only iff their val < current node val
    now if at the end they are connected add to good paths number of nodes with value -1
"""

"""
optimized union-find. 2 improvements:
a.    union by rank
keep track of tree length by keeping track of rank (init to 1)
Then on union use rank to attach shorter tree to root of longer

b. find path compression.
during find when attaching to new tree attach to grandparent instead of parent, thus halving length
"""

from collections import defaultdict
class disjointSet:
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
        #print(f"union of {node_left}-{node_right}")
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

class Solution:
    def numberOfGoodPathsBFS(self, vals: List[int], edges: List[List[int]]) -> int:
        """
        demo O(n^2) solution. It fails on TLE (time limit exceeded). 
        """
        from collections import defaultdict, deque
        adjacent = defaultdict(set)
        num_good_paths= 0
        for edge in edges:
            adjacent[edge[0]].add(edge[1])
            adjacent[edge[1]].add(edge[0])

        #print(f"Got vals={vals}")
        #print(f"Got edges={edges}")
        #print(f"Built adjacent={adjacent}")

        for i in range(len(vals)):
            #print(f"BFS starting at node {i}")
            bfsq = deque([i])
            visited = set()
            max_val= vals[i]
            while bfsq:
                cur = bfsq.popleft()
                visited.add(cur)
                #print(f"BFS process node {cur}. Q={bfsq}, visited={visited}, adjacent={adjacent[cur]}")
                for n in adjacent[cur]:
                    if not n in visited:
                        if vals[n] < max_val:
                            bfsq.append(n)
                        elif vals[n] == max_val:
                            num_good_paths+=1
                            bfsq.append(n)
        num_good_paths //=2  #each path was found twice
        num_good_paths += len(vals) #each node is by definition a good path
        return num_good_paths

    def numberOfGoodPathsUF(self, vals: List[int], edges: List[List[int]]) -> int:
        """
        use union-find to reduce complexity to O(nlog(n))
        This implementation passes 84/140 tests but has some kind of bug.
        """
        num_good_paths = 0
        UF = disjointSet(len(vals)) 
        vals_to_nodes = defaultdict(set)
        for i in range(len(vals)):
            vals_to_nodes[vals[i]].add(i)
        graph = defaultdict(set)
        for edge in edges:
            graph[edge[0]].add(edge[1])
            graph[edge[1]].add(edge[0])

        # perform a greedy traversal starting from the smallest values nodes 
        for node_val in sorted(vals_to_nodes.keys()):
            for node in vals_to_nodes[node_val]:
                for neighbor in graph[node]:
                    if vals[neighbor]<=vals[node]:
                        UF.union(node,neighbor)
            #determine how many node_val nodes are in the UF. if 1 => 1 good path (to itself), 2 => 3 (1 connecting + 1 for each to itself), 3=>6 so arithmetic series 
            count_connected = defaultdict(int)
            for node in vals_to_nodes[node_val]:
                root = UF.find(node)
                count_connected[root]+=1
                num_good_paths += count_connected[root] #increment by n-1 (arithmetic series)

        return num_good_paths 

    def numberOfGoodPathsUF_Simple(self, vals: List[int], edges: List[List[int]]) -> int:
        edges.sort(key=lambda x: max(vals[x[0]], vals[x[1]])) #sort edges asc by max val in edge
        n = len(vals)
        parents = list(range(n)); size = [1]*n #UF parents, size - num of good paths in parent
        def find(i): #naive find, no compression
            if parents[i] != i:
                parents[i] = find(parents[i])
            return parents[i]
        goodPaths = n #n nodes, each good path to itself
        for a,b in edges:
            parent_a, parent_b = find(a), find(b)
            if vals[parent_a] == vals[parent_b]: #add goodpaths the multiplication of good paths in each disjoint-set since connecting via parents 
                goodPaths += size[parent_a] * size[parent_b]
                parents[parent_a] = parent_b
                size[parent_b] += size[parent_a] #a root is attached to b root so update b root good paths by adding a root good paths
            elif vals[parent_a] > vals[parent_b]: #no good path between parents but they are connected, so connect them to smaller root: b
                parents[parent_b] = parent_a
            else:#no good path between parents but they are connected, so connect them to smaller root: a
                parents[parent_a] = parent_b
        return goodPaths

    def numberOfGoodPaths(self, vals: List[int], edges: List[List[int]]) -> int:
        return self.numberOfGoodPathsUF_Simple(vals, edges)
