"""
Best Time to Buy and Sell Stock II
You are given an integer array prices where prices[i] is the price of a given stock on the ith day.

On each day, you may decide to buy and/or sell the stock. You can only hold at most one share of the stock at any time. However, you can buy it then immediately sell it on the same day.

Find and return the maximum profit you can achieve.

 

Example 1:

Input: prices = [7,1,5,3,6,4]
Output: 7
Explanation: Buy on day 2 (price = 1) and sell on day 3 (price = 5), profit = 5-1 = 4.
Then buy on day 4 (price = 3) and sell on day 5 (price = 6), profit = 6-3 = 3.
Total profit is 4 + 3 = 7.
Example 2:

Input: prices = [1,2,3,4,5]
Output: 4
Explanation: Buy on day 1 (price = 1) and sell on day 5 (price = 5), profit = 5-1 = 4.
Total profit is 4.
Example 3:

Input: prices = [7,6,4,3,1]
Output: 0
Explanation: There is no way to make a positive profit, so we never buy the stock to achieve the maximum profit of 0.
 

Constraints:

1 <= prices.length <= 3 * 104
0 <= prices[i] <= 104
"""
# to test run: python3 -m unittest test_BestTimeToBuySellStocks2.py
from typing import List

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        profit = 0
        for i in range(1, len(prices)):
            profit += max(0, prices[i] - prices[i-1])
        return profit


if __name__ == "__main__":
    solution = Solution()
    
    # Test case 1: Multiple buy/sell opportunities
    prices1 = [7,1,5,3,6,4]
    result1 = solution.maxProfit(prices1)
    print(f"Test 1 - Multiple transactions: {prices1}")
    print(f"Expected: 7, Got: {result1}")
    print("Buy at 1, sell at 5 (profit=4) + Buy at 3, sell at 6 (profit=3) = 7\n")
    
    # Test case 2: Continuously increasing prices
    prices2 = [1,2,3,4,5]
    result2 = solution.maxProfit(prices2)
    print(f"Test 2 - Continuously increasing: {prices2}")
    print(f"Expected: 4, Got: {result2}")
    print("Buy at 1, sell at 5 (profit=4) OR capture each daily gain\n")
    
    # Test case 3: Continuously decreasing prices
    prices3 = [7,6,4,3,1]
    result3 = solution.maxProfit(prices3)
    print(f"Test 3 - Continuously decreasing: {prices3}")
    print(f"Expected: 0, Got: {result3}")
    print("No profitable transactions possible\n")

    print("To run full test suite: python3 -m unittest test_BestTimeToBuySellStocks2.py")