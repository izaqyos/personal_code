class Solution(object):
    def canJump(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """
        if (nums is None):
            return False;
        
        if len(nums) == 0:
            return True;
        
        jL = nums[0]
       # if (jL < 0) and (len(nums) ==1): 
        #    return False;
        
        dpJumps = [jL]
        for i,elem in enumerate(nums):
            if i==0:
                continue
            if jL < 0:
                return False;
            jL-=1
            jL = max(jL, elem)
            if ( jL <= 0 ) and (i<(len(nums)-1)):
                return False;
            
        return True
        