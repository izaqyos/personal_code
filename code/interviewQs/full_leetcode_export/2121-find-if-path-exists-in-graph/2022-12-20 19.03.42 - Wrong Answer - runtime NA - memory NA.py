from collections import deque
class Solution:


    def createGraph(self, edges: List[List[int]]):
        graph = dict()
        for edge in edges:
            u,v=edge[0], edge[1]
            if u in graph:
                graph[u].add(v)
            else:
                graph[u] = {v}
            if v in graph:
                graph[v].add(u)
            else:
                graph[v] = {u}
        return graph

    def validPath(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
        """
        idea, BFS. First convert 2d list to a dictionary k- source node to [v1,v2,...] target 
        then do plain old fashioned BFS if path found return True otherwise return False 
        """
        if not edges:
            return False
        #print(f"{edges}, {source}, {destination}")
        graph = self.createGraph(edges)
        #print(graph)
        visited = set()
        q = deque([source])
        while q:
            node = q.popleft()
            #print(f"poped {node}")
            for t in graph[node]:
                if t == destination:
                    return True
                if not t in visited:
                    visited.add(t)
                    q.append(t)
        return False

