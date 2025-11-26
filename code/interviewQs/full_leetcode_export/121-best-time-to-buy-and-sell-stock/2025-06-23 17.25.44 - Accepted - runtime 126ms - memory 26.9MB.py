class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if not prices or len(prices)<2: 
            return 0
        imin, imax, idx,  profit = 0,  0, 0, 0
        while idx < len(prices):
            cur, minimum, maximum = prices[idx], prices[imin], prices[imax]
            if cur > maximum:
                imax = idx
                maximum = cur
            if cur < minimum:
                imin = idx
                imax = idx
                minimum = cur
                maximum = cur
            profit = max(profit, maximum - minimum)
            idx += 1
        return profit