class Solution:

    def find_pile(self, piles, num):
        """
        simple binary search, since we want to insert to the left 
        we will return the biggest index where piles[index] <= num
        """
        # note, can use bisect_left(piles, num) but I'll implement myself
        l = 0
        h = len(piles)

        while l<h:
            mid = (l+h)//2
            if piles[mid] < num:
                l =mid+1 # if l>=h, either return past end or we are sure that <=piles[h]
            else:
                h = mid # num can't be inserted in mid pos since it <= piles[mid]
        return l

    def lengthOfLISPatienceSort(self, nums):
        """
        patience sort. instead of piles I'll use stacks (simple list will do)
        for finding where to put next card I'll binary search the top cards for
        the correct stack to add to (or create a new stack if needed)

        Note, if we were asked for the actual LIS we could add to the piles a
        class of val, back where back is a pointer to the top of the last pile.
        Then we talk the top of left most pile (piles[-1].top()) and follow the
        back pointers to retreive the list

        Note, since we don't need the full piles its possible to not use stack,
        just a list that would hold the top cards
        """
        if len(nums) == 0:
            return 0

        piles = []
        #piles.append([nums[0]])
        piles.append(nums[0])

        for n in nums[1:]:
            i = self.find_pile(piles, n)
            if i<len(piles):
                #piles[i].append(n)
                piles[i] = n
            else:
                #piles.append([n])
                piles.append(n)

    
        return len(piles)


    def lengthOfLISDP(self, nums):
        """
        recursion. 
        LIS(nums, n) = max(join(LIS(nums,j),j, nums[n]) (j in {0,..,n-1})
        join(lis, j, num):
            if num>nums[j]:
                return lis+1
            else:
                return lis
        complexity: each pass has n steps of calling LIS(0,..,n-1) , seems to
        me like o(n!)

        DP save LIS values instead of call recursion. o(n^2) 
        """
        if len(nums) == 0:
            return 0

        LISDP = [1 for i in nums]
        n = len(nums)
        LIS = 1
        for i in range(1,n):
            for j in range(0,i):
                if nums[i] > nums[j]:
                    LISDP[i] = max(LISDP[i], LISDP[j]+1)
                    LIS = max(LIS, LISDP[i])

        return LIS



    def lengthOfLIS(self, nums):
        #return self.lengthOfLISDP(nums)
        return self.lengthOfLISPatienceSort(nums)
