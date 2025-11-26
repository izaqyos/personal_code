class Solution:
    def part(self, partitions, i, j):
        #print(f"solve partition indices {i,j}")
        if i>j:
            return 0
        minimum_cost = float('inf')
        for ind in range(i,j+1):
            cost = partitions[j+1]-partitions[i-1] + self.part(partitions, i,ind-1)+self.part(partitions, ind+1,j)
            minimum_cost = min(minimum_cost, cost)
        return minimum_cost

    def minCost(self, n: int, cuts: List[int]) -> int:
        cuts.sort()
        partitions = [0]+cuts[:]+[n] #pad cuts with 0 and len(cuts) values for convenience
        #print(f"Claculate min cost of cutting stick of length {n} given cuts {cuts}. Created partitions array: {partitions}")
        return self.part(partitions, 1, len(cuts)) #solve partitions min cost problem. 
