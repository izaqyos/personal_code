#!/opt/homebrew/Caskroom/miniconda/base/bin/python
"""
Best time to buy and sell stocks

You are given an array prices where prices[i] is the price of a given stock on the ith day.
You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.
Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.
 
Example 1:
Input: prices = [7,1,5,3,6,4]
Output: 5
Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.
Note that buying on day 2 and selling on day 1 is not allowed because you must buy before you sell.
Example 2:
Input: prices = [7,6,4,3,1]
Output: 0
Explanation: In this case, no transactions are done and the max profit = 0.
 
Constraints:
* 1 <= prices.length <= 105
* 0 <= prices[i] <= 104

"""

from typing import List
# 18/06/25 13:43:51  solution, I'll try rolling window
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

def test1():
    prices = [7,1,5,3,6,4]
    expected = 5
    print(f"Test 1: Regular case - prices={prices}, expected={expected}")
    sol = Solution()
    profit = sol.maxProfit(prices)
    print(f"Test 1: profit={profit}")
    assert sol.maxProfit(prices) == expected

def test2():
    prices = [7,6,4,3,1]
    expected = 0
    print(f"Test 2: Descending case - prices={prices}, expected={expected}")
    sol = Solution()
    profit = sol.maxProfit(prices)
    print(f"Test 2: profit={profit}")
    assert sol.maxProfit(prices) == expected

def test3():
    prices = []
    expected = 0
    print(f"Test 3: Empty array - prices={prices}, expected={expected}")
    sol = Solution()
    assert sol.maxProfit(prices) == expected

def test4():
    prices = [1]
    expected = 0
    print(f"Test 4: Single element - prices={prices}, expected={expected}")
    sol = Solution()
    assert sol.maxProfit(prices) == expected

def test5():
    prices = [1, 2]
    expected = 1
    print(f"Test 5: Two elements with profit - prices={prices}, expected={expected}")
    sol = Solution()
    assert sol.maxProfit(prices) == expected

def test6():
    prices = [2, 1]
    expected = 0
    print(f"Test 6: Two elements no profit - prices={prices}, expected={expected}")
    sol = Solution()
    assert sol.maxProfit(prices) == expected

def test7():
    prices = [3, 3, 3, 3]
    expected = 0
    print(f"Test 7: All same values - prices={prices}, expected={expected}")
    sol = Solution()
    assert sol.maxProfit(prices) == expected

def test8():
    prices = [9, 7, 1, 5, 3, 6, 4]
    expected = 5
    print(f"Test 8: Multiple peaks and valleys - prices={prices}, expected={expected}")
    sol = Solution()
    assert sol.maxProfit(prices) == expected

def test9():
    prices = [3, 2, 1, 5, 6, 7]
    expected = 6
    print(f"Test 9: V-shaped then ascending - prices={prices}, expected={expected}")
    sol = Solution()
    assert sol.maxProfit(prices) == expected

def test10():
    # Testing with constraint boundary values
    prices = [10000] + [0] * 99999 + [10000]  # Max length array with max possible values
    expected = 10000
    print(f"Test 10: Constraint boundary test - array length={len(prices)}, expected={expected}")
    sol = Solution()
    assert sol.maxProfit(prices) == expected

def test11():
    prices = [2, 2, 5, 2, 4]
    expected = 3
    print(f"Test 11: Repeated values - prices={prices}, expected={expected}")
    sol = Solution()
    assert sol.maxProfit(prices) == expected

def tests():
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    test7()
    test8()
    test9()
    test10()
    test11()
    print("All tests passed!")

if __name__ == "__main__":
    tests()
