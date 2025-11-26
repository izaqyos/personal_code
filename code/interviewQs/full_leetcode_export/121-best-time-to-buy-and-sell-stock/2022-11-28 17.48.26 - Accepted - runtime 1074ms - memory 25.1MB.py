class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if not prices or len(prices)<2:
            return 0
        imin, vmin, profit = 0, prices[0], 0
        for j in range(1,len(prices)):
            if prices[j] < vmin:
                imin = j
                vmin = prices[j]
            elif prices[j] > vmin:
                profit = max(profit, prices[j]-vmin)
        return profit
