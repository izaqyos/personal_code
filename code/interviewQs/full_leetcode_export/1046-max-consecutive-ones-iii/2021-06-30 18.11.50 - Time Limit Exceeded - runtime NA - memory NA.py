import math
class Solution:
    """
    I chose a sliding window algo. just fill 0 as long as kleft > 0
    perform 2 scans left to right and right to left
    right to left is required for cases like
    1110001111 , k=2 if only do l to r we get 5 as result
    r to l allows us to capture the last segment 001111
    another solution is to step back k-1 times after each window is concluded but this has possible issues. large k would hurt performance
    """
    def longestOnes(self, nums: List[int], k: int) -> int:
        maxones = -math.inf
        wlen=0
        for i in range(len(nums)):
            j=i
            kleft=k
            wones=0
            while j<len(nums):
                if nums[j] == 1:
                    wones+=1
                else:
                    if kleft>0:
                        wones+=1
                        kleft-=1
                    else: #close this window
                        maxones = max(maxones, wones) 
                        break
                j+=1
            if j==len(nums):
                maxones = max(maxones, wones) 
                break



        return maxones