class Solution:
    def part(self,memo, partitions, i, j):
        #print(f"solve partition indices {i,j}")
        if i>j:
            return 0
        minimum_cost = float('inf')
        for ind in range(i,j+1):
            lower_cost, upper_cost = float('inf'), float('inf')
            if memo[i][ind-1] == -1:
                memo[i][ind-1] = self.part(memo, partitions, i,ind-1)
            lower_cost = memo[i][ind-1]
            if memo[ind+1][j] == -1:
                memo[ind+1][j] = self.part(memo, partitions, ind+1, j)
            upper_cost = memo[ind+1][j]

            cost = partitions[j+1]-partitions[i-1] + lower_cost + upper_cost
            minimum_cost = min(minimum_cost, cost)
        return minimum_cost

    def minCost(self, n: int, cuts: List[int]) -> int:
        cuts.sort()
        partitions = [0]+cuts[:]+[n] #pad cuts with 0 and len(cuts) values for convenience
        memo =[ [-1 for _ in range(len(partitions)+1)] for _ in range(len(partitions)+1)]
        #print(f"Claculate min cost of cutting stick of length {n} given cuts {cuts}. Created partitions array: {partitions}")
        return self.part(memo, partitions, 1, len(cuts)) #solve partitions min cost problem. 

