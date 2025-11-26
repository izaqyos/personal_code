class Solution:
    def partitionDisjoint(self, nums: List[int]) -> int:
        n = len(nums)
        minima = [[0 for i in range(n)] for _ in range(n)]
        maxima = [[0 for i in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i,n):
                if i == j:
                    minima[i][j] = nums[i]
                    maxima[i][j] = nums[i]
                else:        
                    minima[i][j] = min(nums[j], minima[i][j-1])
                    maxima[i][j] = max(nums[j], maxima[i][j-1])
            
        
        
        for i in range(n):
            if maxima[0][i] <= minima[i+1][n-1]:
                return i+1
        