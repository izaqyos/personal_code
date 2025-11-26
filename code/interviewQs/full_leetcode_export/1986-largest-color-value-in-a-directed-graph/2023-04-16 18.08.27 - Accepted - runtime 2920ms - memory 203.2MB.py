class Solution:
    def largestPathValue(self, colors: str, edges: List[List[int]]) -> int:

        if not edges: return 1

        adj_list = defaultdict(list)
        for a, b in edges:
            adj_list[a].append(b)
        

        def dfs(cur):
            if cur in cycle: return True
            if cur in visited: return False
                
            visited.add(cur)
            cycle.add(cur)

            for neigh in adj_list[cur]:
                if dfs(neigh):
                    return True
                for color in range(26):
                    dp[cur][color] = max(dp[cur][color], dp[neigh][color])
            

            cur_color = ord(colors[cur]) - ord("a")
            dp[cur][cur_color] += 1
            self.ans = max(self.ans, dp[cur][cur_color])

            cycle.remove(cur)
            return False


        visited = set()
        cycle = set()
        dp = [[0] * 26 for _ in range(len(colors))]
        self.ans = -1

        for node in range(len(colors)):
            if node not in visited:
                if dfs(node):
                    return -1
        
        return self.ans
