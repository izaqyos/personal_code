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


    def numberOfGoodPaths(self, vals: List[int], edges: List[List[int]]) -> int:
        return self.numberOfGoodPathsUF(vals, edges)
