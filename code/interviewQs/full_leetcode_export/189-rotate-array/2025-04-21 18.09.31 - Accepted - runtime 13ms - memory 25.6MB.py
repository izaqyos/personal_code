class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
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
