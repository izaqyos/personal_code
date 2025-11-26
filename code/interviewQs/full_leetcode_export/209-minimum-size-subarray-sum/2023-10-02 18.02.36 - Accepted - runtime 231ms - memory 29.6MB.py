class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        """
        first Solution sliding window
        """
        if not nums:
            return 0
        if len(nums) == 1:
            if nums[0] >= target:
                return 1
            else:
                return 0

        l,r=0,0
        window_sum = nums[0]
        min_len = float('inf')
        while l<=r and r< len(nums):
            #print(f"l={l}, r={r}, window_sum={window_sum}, target={target}, min_len={min_len}, nums={nums}")
            if window_sum >= target:
                min_len = min(r-l+1, min_len)
                l = l+1
                window_sum = window_sum - nums[l-1]
            else:
                r=r+1
                if r< len(nums):
                    if nums[r] >= target:
                        return 1
                    else:
                        window_sum += nums[r]
        if min_len< float('inf'):
            return min_len
        else:
            return 0
