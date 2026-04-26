"""
121. Best Time to Buy and Sell Stock
https://leetcode.com/problems/best-time-to-buy-and-sell-stock/

You are given an array prices where prices[i] is the price of a given stock
on the ith day.

You want to maximize your profit by choosing a single day to buy and a single
day to sell in the future. Return the maximum profit you can achieve from this
transaction. If you cannot achieve any profit, return 0.

Constraints:
- 1 <= prices.length <= 10^5
- 0 <= prices[i] <= 10^4

Example 1: prices = [7,1,5,3,6,4] -> 5  (buy day 1 at 1, sell day 4 at 6)
Example 2: prices = [7,6,4,3,1]   -> 0  (prices only decrease, no profit)
"""


def max_profit(prices: list[int]) -> int:
    max_profit_val = 0
    if not prices or len(prices) == 1:
        return max_profit_val

    # Alternative (shorter, same logic):
    #   min_value = min(min_value, prices[i])
    #   max_profit_val = max(max_profit_val, prices[i] - min_value)
    min_value = prices[0]
    for i in range(1, len(prices)):
        cur_value = prices[i]
        if cur_value > min_value:
            max_profit_val = max(max_profit_val, cur_value-min_value)
        if cur_value<min_value:
            min_value = cur_value
    
    return max_profit_val
   


if __name__ == "__main__":
    tests = [
        ([7, 1, 5, 3, 6, 4], 5),
        ([7, 6, 4, 3, 1], 0),
        ([1], 0),                        # single day
        ([2, 1], 0),                     # only decreasing
        ([1, 2], 1),                     # minimal profit
        ([3, 3, 3, 3], 0),              # flat prices
        ([1, 2, 3, 4, 5], 4),           # monotone increasing
        ([2, 1, 4, 5, 2, 9, 7], 8),    # buy at 1, sell at 9
        ([10, 8, 2, 9], 7),             # dip then spike
    ]
    for i, (prices, expected) in enumerate(tests):
        result = max_profit(prices)
        status = "PASS" if result == expected else "FAIL"
        print(f"Test {i+1}: {status} | prices={prices}, expected={expected}, got={result}")
