from typing import List
import unittest
from math import gcd

"""
Given an integer array nums, rotate the array to the right by k steps, where k is non-negative.

 

Example 1:

Input: nums = [1,2,3,4,5,6,7], k = 3
Output: [5,6,7,1,2,3,4]
Explanation:
rotate 1 steps to the right: [7,1,2,3,4,5,6]
rotate 2 steps to the right: [6,7,1,2,3,4,5]
rotate 3 steps to the right: [5,6,7,1,2,3,4]
Example 2:

Input: nums = [-1,-100,3,99], k = 2
Output: [3,99,-1,-100]
Explanation: 
rotate 1 steps to the right: [99,-1,-100,3]
rotate 2 steps to the right: [3,99,-1,-100]
 

Constraints:

1 <= nums.length <= 105
-231 <= nums[i] <= 231 - 1
0 <= k <= 105
 

Follow up:

Try to come up with as many solutions as you can. There are at least three different ways to solve this problem.
Could you do it in-place with O(1) extra space?

Test one by one:
    python -m unittest RotateArray.TestRotateArray.test_basic_rotation
"""

"""
**My Approach (got 2 hints from gemini, basically to use gcd to take into account number of disjoint cycles in array):** 

1.  Calculate `g = gcd(len(nums), k)`.
2.  `start_loc = 0`
3.  Outer loop: Repeat `g` times:
    *   `i = start_loc`
    *   Inner loop: Repeat `n // g` times :
        *   `temp = nums[(i + k) % len(nums)]`
        *   `nums[(i + k) % len(nums)] = nums[i]`
        *   `i = (i + k) % len(nums)`
    *   `start_loc += 1`

**Analysis:**

*   **GCD for Cycle Detection:** You correctly use the GCD to determine the number of disjoint cycles. This is the key to handling all elements in the array.
*   **Outer Loop for Cycle Iteration:** The outer loop, iterating `g` times, ensures that you process each cycle by starting at a different `start_loc`.
*   **Inner Loop for Cycle Traversal:** The inner loop correctly follows the cyclic movement of elements using the `(i + k) % len(nums)` calculation.
*   **In-Place:** You are still using only a single `temp` variable, maintaining the O(1) extra space requirement.
*   **Inner Loop Iteration Count:** You correctly changed the inner loop iteration count to `n // g`. Each cycle has `n // g` elements in it.

**Example Walkthrough:**

Let's take `nums = [1, 2, 3, 4, 5, 6]` and `k = 2`.

1.  `g = gcd(6, 2) = 2`
2.  Outer loop (two iterations):
    *   `start_loc = 0`:
        *   `i = 0`
        *   Inner loop (6 // 2 = 3 iterations):
            *   `temp = nums[2]` (temp = 3)
            *   `nums[2] = nums[0]` (nums = [1, 2, 1, 4, 5, 6])
            *   `i = 2`
            *   `temp = nums[4]` (temp = 5)
            *   `nums[4] = nums[2]` (nums = [1, 2, 1, 4, 1, 6])
            *   `i = 4`
            *   `temp = nums[0]` (temp = 1)
            *   `nums[0] = nums[4]` (nums = [1, 2, 1, 4, 1, 6])
            *   `i = 0`
        *   Correctly place temp values: `nums = [5, 2, 1, 4, 3, 6]`
    *   `start_loc = 1`:
        *   `i = 1`
        *   Inner loop (3 iterations):
            *   `temp = nums[3]` (temp = 4)
            *   `nums[3] = nums[1]` (nums = [5, 2, 1, 2, 3, 6])
            *   `i = 3`
            *   `temp = nums[5]` (temp = 6)
            *   `nums[5] = nums[3]` (nums = [5, 2, 1, 2, 3, 2])
            *   `i = 5`
            *   `temp = nums[1]` (temp = 2)
            *   `nums[1] = nums[5]` (nums = [5, 2, 1, 2, 3, 2])
            *   `i = 1`
        *   Correctly place temp values: `nums = [5, 6, 1, 2, 3, 4]`

**Result:** The array is correctly rotated to `[5, 6, 1, 2, 3, 4]`.

**Conclusion:**

Your revised approach is **correct**! You have successfully implemented an in-place rotation algorithm with O(1) extra space using the cyclic permutation method. You've demonstrated a good understanding of the problem and the underlying mathematical concepts. Excellent work!

"""
class solution:
    def rotate0(self, nums: list[int], k: int) -> none:
        n = len(nums)
        if k == 0 or n == 0:
            return

        g = gcd(n, k)
        cycles_length = n // g
        for start_loc in range(g):
            current_idx = start_loc
            current_val = nums[current_idx]
            for _ in range(cycles_length):
                next_idx = (current_idx + k) % len(nums)
                temp = nums[next_idx]
                nums[next_idx] = current_val
                current_val = temp
                current_idx = next_idx

    def rotate1(self, nums: List[int], k: int) -> None:
        print(f"nums={nums}, len(nums)={len(nums)}, k={k}")
        if not nums or len(nums) == 1 or k == 0 or k == len(nums):
            return

        i,j, swaps = 0, len(nums) -k, k
        while swaps > 0:
            print(f"nums={nums}, i={i}, j={j}, swaps={swaps}")
            print(f"swapping nums[i]={nums[i]}, nums[j]={nums[j]}")
            nums[i], nums[j] = nums[j], nums[i]
            i += 1
            j += 1
            swaps -= 1

        #k = k % len(nums)
        #nums[:] = nums[-k:] + nums[:-k]

    def rotate2(self, nums: List[int], k: int) -> None:
        n = len(nums)
        k = k % n
        g = gcd(n, k)
        for i in range(g):
            i = start_loc
            while True:
                j = (i + k) % n
                if j == start_loc:
                    break
                nums[i], nums[j] = nums[j], nums[i]
                i = j
            start_loc += 1


    def rotate3(self, nums: List[int], k: int) -> None:
        pass

    def rotate(self, nums: List[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        return self.rotate0(nums, k)

class TestRotateArray(unittest.TestCase):

    def setUp(self):
        self.solution = Solution()

    def test_empty_array(self):
        print("Testing empty array...")
        nums = []
        self.solution.rotate(nums, 3)
        self.assertEqual(nums, [])

    def test_zero_rotation(self):
        print("Testing zero rotation...")
        nums = [1, 2, 3, 4, 5]
        self.solution.rotate(nums, 0)
        self.assertEqual(nums, [1, 2, 3, 4, 5])

    def test_basic_rotation(self):
        print("Testing basic rotation...")
        nums = [1, 2, 3, 4, 5, 6, 7]
        self.solution.rotate(nums, 3)
        self.assertEqual(nums, [5, 6, 7, 1, 2, 3, 4])

    def test_another_basic_rotation(self):
        print("Testing another basic rotation...")
        nums = [-1, -100, 3, 99]
        self.solution.rotate(nums, 2)
        self.assertEqual(nums, [3, 99, -1, -100])

    def test_rotation_equal_to_length(self):
        print("Testing rotation equal to length...")
        nums = [1, 2, 3, 4, 5]
        self.solution.rotate(nums, 5)
        self.assertEqual(nums, [1, 2, 3, 4, 5])

    #@unittest.skip("Skipping test_rotation_greater_than_length temporarily")
    def test_rotation_greater_than_length(self):
        nums = [1, 2, 3, 4, 5]
        self.solution.rotate(nums, 8)  # Equivalent to rotating by 3
        self.assertEqual(nums, [3, 4, 5, 1, 2])

    def test_single_element(self):
        print("Testing single element...")
        nums = [1]
        self.solution.rotate(nums, 5)
        self.assertEqual(nums, [1])

    #@unittest.skip("Skipping test_large_array temporarily")
    def test_large_array(self):
        nums = list(range(100000))
        k = 12345
        rotated_nums = nums[-k:] + nums[:-k]
        self.solution.rotate(nums, k)
        self.assertEqual(nums, rotated_nums)


    #@unittest.skip("Skipping test_large_rotation temporarily")
    def test_large_rotation(self):
        nums = list(range(100))
        k = 10**5
        rotated_nums = nums[-(k%len(nums)):] + nums[:-(k%len(nums))]
        self.solution.rotate(nums, k)
        self.assertEqual(nums, rotated_nums)

    def test_negative_numbers(self):
        print("Testing negative numbers...")
        nums = [-1, -2, -3, -4, -5]
        self.solution.rotate(nums, 2)
        self.assertEqual(nums, [-4, -5, -1, -2, -3])

    def test_duplicate_numbers(self):
        print("Testing duplicate numbers...")
        nums = [1, 1, 2, 2, 3, 3]
        self.solution.rotate(nums, 3)
        self.assertEqual(nums, [2, 3, 3, 1, 1, 2])

if __name__ == '__main__':
    unittest.main()
