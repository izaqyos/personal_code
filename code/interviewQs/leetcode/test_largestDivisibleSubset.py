from typing import List
import unittest
from largestDivisibleSubset import Solution

class TestLargestDivisibleSubset(unittest.TestCase):

    def setUp(self):
        self.solution = Solution()
        print("\n--- Running Test --- ") # Add separator

    def assertValidSubset(self, nums: list[int], subset: list[int]):
        """Helper assertion to check if a subset is valid and its elements are from nums."""
        if not subset:
            return # Empty subset is valid

        # Check if all elements are from the original list (optional but good practice)
        num_set = set(nums)
        for x in subset:
            self.assertIn(x, num_set, f"Element {x} in subset is not in original nums")

        # Sort the subset to check for divisibility easily
        subset_copy = subset[:] # Avoid modifying the original result list during validation
        subset_copy.sort()
        for i in range(len(subset_copy) - 1):
            self.assertTrue(subset_copy[i+1] % subset_copy[i] == 0,
                            f"Invalid subset: {subset_copy[i+1]} is not divisible by {subset_copy[i]} in {subset_copy}")

    def test_example1(self):
        nums = [1, 2, 3]
        print(f"Input nums: {nums}")
        result = self.solution.largestDivisibleSubset(nums)
        print(f"Returned result: {result}")
        # Expected length is 2. Valid subsets: [1, 2] or [1, 3]
        expected_len = 2
        print(f"Expected length: {expected_len}")
        self.assertEqual(len(result), expected_len)
        self.assertValidSubset(nums, result)
        # Check if it's one of the expected results
        result_sorted = sorted(result) # Use sorted() to not modify result
        self.assertTrue(result_sorted == [1, 2] or result_sorted == [1, 3])

    def test_example2(self):
        nums = [1, 2, 4, 8]
        print(f"Input nums: {nums}")
        result = self.solution.largestDivisibleSubset(nums)
        print(f"Returned result: {result}")
        # Expected: [1, 2, 4, 8]
        expected_len = 4
        print(f"Expected length: {expected_len}")
        self.assertEqual(len(result), expected_len)
        self.assertValidSubset(nums, result)
        result_sorted = sorted(result)
        self.assertEqual(result_sorted, [1, 2, 4, 8])

    def test_empty_list(self):
        nums = []
        print(f"Input nums: {nums}")
        result = self.solution.largestDivisibleSubset(nums)
        print(f"Returned result: {result}")
        expected_len = 0
        print(f"Expected length: {expected_len}")
        self.assertEqual(len(result), expected_len)
        self.assertEqual(result, [])

    def test_single_element(self):
        nums = [5]
        print(f"Input nums: {nums}")
        result = self.solution.largestDivisibleSubset(nums)
        print(f"Returned result: {result}")
        expected_len = 1
        print(f"Expected length: {expected_len}")
        self.assertEqual(len(result), expected_len)
        self.assertValidSubset(nums, result)
        self.assertEqual(result, [5])

    def test_no_divisible_pairs(self):
        nums = [2, 3, 5, 7, 11]
        print(f"Input nums: {nums}")
        result = self.solution.largestDivisibleSubset(nums)
        print(f"Returned result: {result}")
        # Expected length is 1 (any single element)
        expected_len = 1
        print(f"Expected length: {expected_len}")
        self.assertEqual(len(result), expected_len)
        self.assertValidSubset(nums, result)
        self.assertIn(result[0], nums)

    def test_multiple_solutions_same_length(self):
        nums = [4, 8, 10, 240]
        print(f"Input nums: {nums}")
        # Potential subsets of length 2: [4, 8], [10, 240], [4, 240], [8, 240]
        # Actually, the LDS is [4, 8, 240] with length 3
        result = self.solution.largestDivisibleSubset(nums)
        print(f"Returned result: {result}")
        expected_len = 3
        print(f"Expected length: {expected_len}")
        self.assertEqual(len(result), expected_len)
        self.assertValidSubset(nums, result)

    def test_complex_case(self):
        nums = [3, 4, 16, 8, 6, 12, 24]
        print(f"Input nums: {nums}")
        # Sorted: [3, 4, 6, 8, 12, 16, 24]
        # Possible LDS: [3, 6, 12, 24], [4, 8, 16], [4, 8, 24]
        # Longest have length 4
        result = self.solution.largestDivisibleSubset(nums)
        print(f"Returned result: {result}")
        expected_len = 4
        print(f"Expected length: {expected_len}")
        self.assertEqual(len(result), expected_len)
        self.assertValidSubset(nums, result)

    def test_already_sorted(self):
        nums = [1, 2, 4, 8, 16]
        print(f"Input nums: {nums}")
        result = self.solution.largestDivisibleSubset(nums)
        print(f"Returned result: {result}")
        expected_len = 5
        print(f"Expected length: {expected_len}")
        self.assertEqual(len(result), expected_len)
        self.assertValidSubset(nums, result)
        # Note: Original result might be reversed by implementation
        self.assertEqual(sorted(result), [1, 2, 4, 8, 16])

    def test_reverse_sorted(self):
        nums = [16, 8, 4, 2, 1]
        print(f"Input nums: {nums}")
        result = self.solution.largestDivisibleSubset(nums)
        print(f"Returned result: {result}")
        expected_len = 5
        print(f"Expected length: {expected_len}")
        self.assertEqual(len(result), expected_len)
        self.assertValidSubset(nums, result)
        result.sort() # Sort for comparison
        self.assertEqual(result, [1, 2, 4, 8, 16])

    def test_contains_duplicates_in_logic_but_unique_input(self):
        # Ensure logic handles numbers that divide each other multiple ways
        nums = [2, 4, 6, 12, 24]
        print(f"Input nums: {nums}")
        # LDS: [2, 4, 12, 24] or [2, 6, 12, 24]
        result = self.solution.largestDivisibleSubset(nums)
        print(f"Returned result: {result}")
        expected_len = 4
        print(f"Expected length: {expected_len}")
        self.assertEqual(len(result), expected_len)
        self.assertValidSubset(nums, result)

if __name__ == '__main__':
    unittest.main() 