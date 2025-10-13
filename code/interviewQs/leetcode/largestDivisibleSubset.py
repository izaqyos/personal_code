from typing import List

"""
Given a set of distinct positive integers nums, return the largest subset answer such that every pair (answer[i], answer[j]) of elements in this subset satisfies:

answer[i] % answer[j] == 0, or
answer[j] % answer[i] == 0
If there are multiple solutions, return any of them.

 

Example 1:

Input: nums = [1,2,3]
Output: [1,2]
Explanation: [1,3] is also accepted.
Example 2:

Input: nums = [1,2,4,8]
Output: [1,2,4,8]
 

Constraints:

1 <= nums.length <= 1000
1 <= nums[i] <= 2 * 109
All the integers in nums are unique.


I'll use dynamic programming to solve this problem.
high level:
1.  **Sort `nums`:** Correct. `nums.sort()`.
2.  **DP State:** `DP[i] = (length, prev_index)`. This is a good state.
    *   `length`: The length of the **L**argest **D**ivisible **S**ubset *ending* at `nums[i]`.
    *   `prev_index`: The index `j` such that `nums[j]` is the element that comes *just before* `nums[i]` in that longest subset. This is crucial for rebuilding the subset later. Let's use `-1` to indicate no previous element (for subsets of size 1).
3.  **Initialization:**
    *   Every element `nums[i]` can form a divisible subset of at least size 1 (just itself).
    *   So, initialize `DP = [(1, -1)] * n` where `n = len(nums)`. Each `DP[i]` starts assuming the longest subset ending at `nums[i]` is just `[nums[i]]`.
4.  **Transition (Calculating `DP[i]`):**
    *   To calculate the correct value for `DP[i]` (where `i > 0`), you need to look back at all previous elements `nums[j]` (where `j < i`).
    *   Outer loop: `for i from 1 to n-1:` (You've already initialized `DP[0]`)
    *   Inner loop: `for j from 0 to i-1:`
        *   **Check:** `if nums[i] % nums[j] == 0:`
        *   **Compare:** If the divisibility holds, it means we *could* potentially extend the LDS that ends at `nums[j]`. The potential new length would be `DP[j][0] + 1`.
        *   **Update:** If this potential length (`DP[j][0] + 1`) is *greater* than the current length stored in `DP[i][0]`, it means we've found a longer divisible subset ending at `nums[i]` by appending `nums[i]` to the subset ending at `nums[j]`. So, update `DP[i]` to `(DP[j][0] + 1, j)`.
5.  **Finding the Result (After filling DP table):**
    *   The final LDS doesn't necessarily end at `nums[n-1]`. The largest subset might end anywhere in the array.
    *   You need to find the entry in `DP` that has the maximum *length*.
    *   Keep track of `max_len = 0` and `end_index = -1`.
    *   Iterate through `DP`: `for i from 0 to n-1:`
        *   `if DP[i][0] > max_len:`
            *   `max_len = DP[i][0]`
            *   `end_index = i`
6.  **Reconstructing the Subset:**
    *   Now you know the length (`max_len`) and the index of the *last* element (`end_index`) of the overall LDS.
    *   Start with `result = []`.
    *   Use a loop or recursion, starting from `curr_index = end_index`:
        *   Add `nums[curr_index]` to the front of `result`.
        *   Update `curr_index = DP[curr_index][1]` (get the index of the previous element).
        *   Repeat until `curr_index` becomes `-1`.

**Example Walkthrough (`nums = [1, 2, 4, 8]`):**

*   `nums = [1, 2, 4, 8]` (already sorted)
*   `n = 4`
*   `DP = [(1, -1), (1, -1), (1, -1), (1, -1)]`

*   **`i = 1` (`nums[1] = 2`):**
    *   `j = 0` (`nums[0] = 1`): `2 % 1 == 0`. Potential length `DP[0][0] + 1 = 1 + 1 = 2`. Current `DP[1][0]` is 1. Since 2 > 1, update `DP[1] = (2, 0)`.
*   **`i = 2` (`nums[2] = 4`):**
    *   `j = 0` (`nums[0] = 1`): `4 % 1 == 0`. Potential length `DP[0][0] + 1 = 2`. Current `DP[2][0]` is 1. Update `DP[2] = (2, 0)`.
    *   `j = 1` (`nums[1] = 2`): `4 % 2 == 0`. Potential length `DP[1][0] + 1 = 2 + 1 = 3`. Current `DP[2][0]` is 2. Since 3 > 2, update `DP[2] = (3, 1)`.
*   **`i = 3` (`nums[3] = 8`):**
    *   `j = 0` (`nums[0] = 1`): `8 % 1 == 0`. Potential length `DP[0][0] + 1 = 2`. Current `DP[3][0]` is 1. Update `DP[3] = (2, 0)`.
    *   `j = 1` (`nums[1] = 2`): `8 % 2 == 0`. Potential length `DP[1][0] + 1 = 2 + 1 = 3`. Current `DP[3][0]` is 2. Update `DP[3] = (3, 1)`.
    *   `j = 2` (`nums[2] = 4`): `8 % 4 == 0`. Potential length `DP[2][0] + 1 = 3 + 1 = 4`. Current `DP[3][0]` is 3. Update `DP[3] = (4, 2)`.

*   **Final DP:** `[(1, -1), (2, 0), (3, 1), (4, 2)]`
*   **Find Max:** Max length is 4, at `end_index = 3`.
*   **Reconstruct:**
    *   `curr = 3`. Add `nums[3]=8`. `result = [8]`. `curr = DP[3][1] = 2`.
    *   `curr = 2`. Add `nums[2]=4`. `result = [4, 8]`. `curr = DP[2][1] = 1`.
    *   `curr = 1`. Add `nums[1]=2`. `result = [2, 4, 8]`. `curr = DP[1][1] = 0`.
    *   `curr = 0`. Add `nums[0]=1`. `result = [1, 2, 4, 8]`. `curr = DP[0][1] = -1`. Stop.
*   **Return:** `[1, 2, 4, 8]`

This revised DP approach correctly captures the dependencies and allows for reconstruction. The time complexity will be O(n^2) due to the nested loops for filling the DP table, dominated by the O(n log n) sort. The space complexity is O(n) for the DP table.

"""

class Solution:
    def largestDivisibleSubset(self, nums: List[int]) -> List[int]:
        nums.sort()
        dp = [(1, -1) for _ in range(len(nums))] # dp contains the length of the largest divisible subset ending at nums[i] and the index of the previous element in the subset
        for i in range(1, len(nums)):
            for j in range(i):
                if nums[i] % nums[j] == 0:
                    if dp[j][0] + 1 > dp[i][0]:
                        dp[i] = (dp[j][0] + 1, j)
        max_len = 0
        end_index = -1
        for i in range(len(nums)):
            if dp[i][0] > max_len:
                max_len = dp[i][0]
                end_index = i
        result = []
        while end_index != -1:
            result.append(nums[end_index])
            end_index = dp[end_index][1]
        result.reverse()
        return result
        