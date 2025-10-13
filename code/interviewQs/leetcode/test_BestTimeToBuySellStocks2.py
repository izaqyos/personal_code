import unittest
from typing import List
from BestTimeToBuySellStocks2 import Solution

class TestMaxProfit(unittest.TestCase):
    def setUp(self):
        """Set up a new Solution instance for each test."""
        self.solution = Solution()

    def test_example_1(self):
        """Test the first example from the problem description."""
        prices = [7, 1, 5, 3, 6, 4]
        self.assertEqual(self.solution.maxProfit(prices), 7)

    def test_example_2(self):
        """Test the second example: continuously increasing prices."""
        prices = [1, 2, 3, 4, 5]
        self.assertEqual(self.solution.maxProfit(prices), 4)

    def test_example_3(self):
        """Test the third example: continuously decreasing prices."""
        prices = [7, 6, 4, 3, 1]
        self.assertEqual(self.solution.maxProfit(prices), 0)

    def test_no_profit(self):
        """Test a case where no profit can be made."""
        prices = [5, 4, 3, 2, 1]
        self.assertEqual(self.solution.maxProfit(prices), 0)

    def test_single_day(self):
        """Test with only one price, no transaction possible."""
        prices = [10]
        self.assertEqual(self.solution.maxProfit(prices), 0)

    def test_two_days_profit(self):
        """Test a simple two-day profitable transaction."""
        prices = [2, 10]
        self.assertEqual(self.solution.maxProfit(prices), 8)

    def test_two_days_loss(self):
        """Test a simple two-day losing transaction."""
        prices = [10, 2]
        self.assertEqual(self.solution.maxProfit(prices), 0)

    def test_empty_list(self):
        """Test with an empty list of prices."""
        # According to constraints, prices.length >= 1, but good to be robust.
        prices: List[int] = []
        self.assertEqual(self.solution.maxProfit(prices), 0)
        
    def test_up_and_down(self):
        """Test a fluctuating price list."""
        prices = [1, 5, 2, 8, 3, 9]
        # (5-1) + (8-2) + (9-3) = 4 + 6 + 6 = 16
        self.assertEqual(self.solution.maxProfit(prices), 16)

if __name__ == '__main__':
    unittest.main() 