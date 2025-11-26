class Solution:
    def sortColors2N(self, nums):
        """
        as leet mentioned, counting sort. 1 pass count. 2nd pass fill.
        """
        reds = 0
        whites = 0
        blues = 0
        #count
        for color in nums:
            if color == 0:
                reds+=1
            elif color == 1:
                whites+=1
            elif color == 2:
                blues+=1

        #sort
        index = 0
        while index < reds:
            nums[index] = 0
            index+=1

        i = 0
        while i < whites:
            nums[i+index] = 1
            i+=1
        index+=i

        i=0
        while i< blues:
            nums[i+index] = 2
            i+=1

        
    def sortColors1N(self, nums):
        """
        original idea:
        will have three dynamic regions in original array.
        red, white, blue regions.
        init lower&upper indices to -1 (meaning no elements of corresponding color)
        sweep array. move each color to its region, expand and move regions as needed
        so, say first element is blue. set its region indices to 0,0. 
        next element is red. set its indices to 0,0. shift blue region 1 to right
        swap red and lowst blue elements.
        next elem is white. set its indices after red and right shift blue.
        keep adding elements and shifting as needed.

        can be simplified a lot. like this. first region is lower end of array. second is middle,
        last is higher end of array, 
        If we do one sweep and swap each red to buttom region, each blue to upper the whites will stay
        in middle (since not moved explicitly)
        """

        l,h,i=0,len(nums) -1, 0
        while i<=h:
            if nums[i] == 0: #red
                nums[i], nums[l] = nums[l], nums[i] 
                l+=1
            elif nums[i] == 2: #blue 
                nums[i], nums[h] = nums[h], nums[i] 
                h-=1
            else:
                i+=1
                     

    def sortColors(self, nums):
        """
        Do not return anything, modify nums in-place instead.
        """
        self.sortColors1N(nums)
        #self.sortColors2N(nums)