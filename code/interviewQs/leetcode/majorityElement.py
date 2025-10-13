from typing import List
import random
import unittest

"""
Given an array nums of size n, return the majority element.

The majority element is the element that appears more than ⌊n / 2⌋ times. You may assume that the majority element always exists in the array.

 

Example 1:

Input: nums = [3,2,3]
Output: 3
Example 2:

Input: nums = [2,2,1,1,1,2,2]
Output: 2
 

Constraints:

n == nums.length
1 <= n <= 5 * 104
-109 <= nums[i] <= 109
 

Follow-up: Could you solve the problem in linear time and in O(1) space?

idea: using array of size 218  is considered O(1) space. Init it to 0.
pass over nums. For each number increment its corresponding index. If a number is greater than n/2, return it.
ok, when I copy pasted instructions to vim the range change from -10^9 - 10^9 to -109 - 109
So a constant space array will not work!
The solution is boyer moore's voting algorithm.
e.g.
Initialization:

candidate: Stores the current candidate for the majority element. Initialize it with the first element of the array.
count: Stores the count of the current candidate. Initialize it to 1.
Iteration: Iterate through the rest of the array:

If the current element is the same as the candidate, increment count.
If the current element is different from the candidate, decrement count.
If count becomes 0, set the candidate to the current element and reset count to 1.
Verification (Optional but Recommended): After the first pass, you have a potential majority element in candidate. You need to verify if it's actually the majority by counting its occurrences in the original array. This is necessary because the algorithm guarantees finding a candidate if a majority element exists, but it doesn't prove that the candidate is the majority element.
"""
class Solution:
    
    def majorityElement(self, nums: List[int]) -> int:
       candidate: int = nums[0]  # Initialize with the first element
        count: int = 0
        n = len(nums)
        half_n = n // 2

        for num in nums:
            if count == 0:
                candidate = num
            
            if num == candidate:
                count += 1
            else:
                count -= 1
            
            if count > half_n:
                return candidate

        return candidate

    def majorityElementFullBoyerMoore(self, nums: List[int]) -> int:
        """
        Boyer-Moore Voting Algorithm BoyerMooreVoting(sequence):
  Input: A sequence (array, list, etc.) of elements called 'sequence'
  Output: The majority element in the sequence, if it exists; otherwise, an arbitrary element.

  // Initialization
  candidate = null  // Initialize a variable to store the potential majority element (candidate)
  count = 0         // Initialize a counter to 0

  // First Pass: Find a potential candidate
  For each element in sequence:
    If count == 0:
      candidate = element   // If the counter is 0, set the current element as the new candidate
      count = 1             // and set the counter to 1
    Else if element == candidate:
      count = count + 1   // If the current element is the same as the candidate, increment the counter
    Else:
      count = count - 1   // If the current element is different from the candidate, decrement the counter

  // Second Pass: Verify the candidate (Optional but recommended for correctness)
  count = 0
  For each element in sequence:
      If element == candidate:
          count = count + 1

  // Check if the candidate is the true majority element
  If count > (length of sequence) / 2:
    Return candidate
  Else:
    Return "No majority element found"  // Or return null, or raise an exception, depending on the desired behavior
  End If

End Algorithm
        """
        majority = None
        count = 0
        for num in nums:
            if count == 0:
                majority = num
                count = 1
            elif num == majority:
                count += 1
            else:
                count -= 1

        count = 0
        for num in nums:
            if num == majority:
                count += 1
        if count > len(nums)//2:
            return majority
        else:
            return None

    #def normalizeIndex(self, num_val: int) -> int:
    #    """
    #    normalize num_val which is between -109 and 109. 
    #    to an index between 0 and 218
    #    """
    #    return num_val + 10**9

    #def majorityElement(self, nums: List[int]) -> int:
    #    n = len(nums)
    #    if n == 1:
    #        return nums[0]
    #    count = [0] * 219
    #    for num in nums:
    #        #print(f"num={num}, count={count}")
    #        count[self.normalizeIndex(num)] += 1
    #        if count[self.normalizeIndex(num)] > n//2:
    #            return num


"""
Explanation of Test Cases:

test_basic_cases: Tests with simple examples where a majority element clearly exists.
test_no_majority: Tests cases where no majority element is present, including an empty list.
test_single_element: Tests lists with only one element.
test_all_same: Tests cases where all elements are identical.
test_negative_numbers: Tests with negative numbers to ensure they are handled correctly.
test_large_input:
Tests with a list of 100,000 elements, one with a majority and one without, to check for performance on larger inputs.
Includes an optional test with a very large list (1 million elements) that you can uncomment if your system has enough memory.
test_randomized_inputs: Generates 100 random test cases with varying lengths and elements, some with a majority element and some without. This helps ensure the algorithm works correctly in a wide range of scenarios.

"""
class TestMajorityElement(unittest.TestCase):

    def setUp(self):
        self.solution = Solution()

    def test_basic_cases(self):
        self.assertEqual(self.solution.majorityElement([3, 2, 3]), 3)
        self.assertEqual(self.solution.majorityElement([2, 2, 1, 1, 1, 2, 2]), 2)
        self.assertEqual(self.solution.majorityElement([1, 1, 1, 2, 2]), 1)
        self.assertEqual(self.solution.majorityElement([1, 2, 2, 1, 1]), 1)

    def test_no_majority(self):
        self.assertIsNone(self.solution.majorityElement([1, 2, 3]))
        self.assertIsNone(self.solution.majorityElement([1, 2, 3, 4]))
        self.assertIsNone(self.solution.majorityElement([]))  # Empty list
        self.assertIsNone(self.solution.majorityElement([1, 2, 1, 2, 3]))

    def test_single_element(self):
        self.assertEqual(self.solution.majorityElement([1]), 1)
        self.assertEqual(self.solution.majorityElement([5]), 5)

    def test_all_same(self):
        self.assertEqual(self.solution.majorityElement([1, 1, 1, 1]), 1)
        self.assertEqual(self.solution.majorityElement([7, 7, 7, 7, 7]), 7)

    def test_negative_numbers(self):
        self.assertEqual(self.solution.majorityElement([-1, -1, -1, 2, 2]), -1)
        self.assertEqual(self.solution.majorityElement([-1, -2, -2]), -2)
        self.assertIsNone(self.solution.majorityElement([-1, -2, -3]))

    def test_large_input(self):
        # Test with a list of 100,000 elements
        large_list_majority = [1] * 50001 + [2] * 49999
        random.shuffle(large_list_majority)  # Shuffle to make it less predictable
        self.assertEqual(self.solution.majorityElement(large_list_majority), 1)

        large_list_no_majority = list(range(100000))
        random.shuffle(large_list_no_majority)
        self.assertIsNone(self.solution.majorityElement(large_list_no_majority))

        # Test with a very large list (1 million elements), if memory permits
        try:
          very_large_list_majority = [3] * 500001 + [4] * 499999
          random.shuffle(very_large_list_majority)
          self.assertEqual(self.solution.majorityElement(very_large_list_majority), 3)
        except MemoryError:
          print("MemoryError encountered during very large list test.")

    def test_randomized_inputs(self):
        # Generate 100 random test cases
        for _ in range(100):
            list_length = random.randint(1, 1000)
            has_majority = random.choice([True, False])

            if has_majority:
                majority_element = random.randint(1, 100)
                majority_count = random.randint(list_length // 2 + 1, list_length)
                other_elements_count = list_length - majority_count
                test_list = [majority_element] * majority_count + [random.randint(1, 100) for _ in range(other_elements_count)]
                random.shuffle(test_list)
                self.assertEqual(self.solution.majorityElement(test_list), majority_element)
            else:
                # Corrected logic to ensure no majority element
                test_list = []
                element_counts = {}
                while len(test_list) < list_length:
                    new_element = random.randint(1, 100)
                    if new_element not in element_counts:
                        element_counts[new_element] = 0

                    # Ensure no element becomes a majority
                    if element_counts[new_element] + 1 <= list_length // 2:
                        test_list.append(new_element)
                        element_counts[new_element] += 1

                random.shuffle(test_list)
                self.assertIsNone(self.solution.majorityElement(test_list))



if __name__ == '__main__':
    unittest.main()

#"""
#Add following test cases:
#1:
#Input: nums = [3,2,3]
#Output: 3
#
#2:
#Input: nums = [2,2,1,1,1,2,2]
#Output: 2
#
#3:
#Input: nums = [2]
#Output: 2
#
#4:
#Input: nums = [-109, -109, -108, 5, 5, -109, -109, 109, 7, 10, -109, -109, -109]
#Output: -109
#"""
##def tests():
##    assert Solution().majorityElement([3,2,3]) == 3
##    assert Solution().majorityElement([2,2,1,1,1,2,2]) == 2
##    assert Solution().majorityElement([2]) == 2
##    assert Solution().majorityElement([-109, -109, -108, 5, 5, -109, -109, 109, 7, 10, -109, -109, -109]) == -109
#
#def generate_test_case(length, majority_element):
#    """Generates a test case with a guaranteed majority element."""
#    nums = [majority_element] * (length // 2 + 1)
#    remaining = length - len(nums)
#    for _ in range(remaining):
#        while True:
#            rand_num = random.randint(-109, 109)
#            if rand_num != majority_element:
#                nums.append(rand_num)
#                break
#    random.shuffle(nums)
#    return nums, majority_element
#
#def tests():
#    test_cases = [
#        ([3, 2, 3], 3),
#        ([2, 2, 1, 1, 1, 2, 2], 2),
#        ([2], 2),
#        ([-109, -109, -108, 5, 5, -109, -109, 109, 7, 10, -109, -109, -109], -109),
#        ([1,2,3],None),
#        ([], None),
#        ([1, 1, 1, 2, 2], 1),
#        ([1, 2, 2, 2, 1], 2),
#        ([1]*10000 + [2]*10001, 2)
#    ]
#
#    # Generate random test cases with values within the constraints
#    for _ in range(10):
#        length = random.randint(1, 5 * 10**4)
#        majority = random.randint(-109, 109) #Majority is in range
#        nums, expected = generate_test_case(length, majority)
#        test_cases.append((nums, expected))
#
#    # Test cases where there is no majority element but values are in range:
#    for _ in range(5):
#        length = random.randint(1, 5 * 10**4)
#        nums = []
#        for i in range(length):
#            nums.append(random.randint(-109, 109))
#        test_cases.append((nums, None))
#
#    for nums, expected in test_cases:
#        result = Solution().majorityElement(nums)
#        print(f"Testing input: {nums[:10]}... (length: {len(nums)})" if len(nums) > 10 else f"Testing input: {nums}")
#        print(f"Expected output: {expected}")
#        print(f"Actual output: {result}")
#        assert result == expected, f"Test failed for input: {nums}. Expected: {expected}, Got: {result}"
#        print("Test passed\n")
#
#if __name__ == "__main__":
#    tests()
#    print("All tests finished")
