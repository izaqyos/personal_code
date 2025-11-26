class Solution:
    def numberOfGoodPathsBFS(self, vals: List[int], edges: List[List[int]]) -> int:
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

    def numberOfGoodPaths(self, vals: List[int], edges: List[List[int]]) -> int:
        return self.numberOfGoodPathsBFS(vals, edges)
