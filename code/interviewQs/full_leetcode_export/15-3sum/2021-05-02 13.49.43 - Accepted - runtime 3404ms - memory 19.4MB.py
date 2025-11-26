class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        return self.threeSumON2(nums)

    def threeSumON3(self, nums: list[int]) -> list[list[int]]:
        """
        time complexity: O(N^3)
        memory complexity: O(1)
        """
        ret = []
        triplets = set()
        for i in range(len(nums)):
            for j in range(i+1, len(nums)):
                for k in range(j+1, len(nums)):
                    if nums[i]+nums[j]+nums[k] == 0:
                        triplet = [nums[i], nums[j], nums[k]]
                        triplet.sort()
                        triplets.add((triplet[0],triplet[1], triplet[2]))
        ret.extend(list(triplets))
        return list(ret)
                    
    def threeSumON2(self, nums: list[int]) -> list[list[int]]:
        """
        time complexity: O(N^2)
        memory complexity: O(N)
        idea, save in set seen vals, then run double loop for each i,j check if 0-(i+j) == -i-j is in set. if so add triplet
        """
        ret = []
        triplets = set()
        seen = set()
        if nums:
            seen.add(nums[0])
        for i in range(1, len(nums)):
            for j in range(i+1, len(nums)):
                if -(nums[i]+nums[j]) in seen: 
                    triplet = [nums[i], nums[j], -(nums[i]+nums[j])]
                    triplet.sort()
                    triplets.add((triplet[0],triplet[1], triplet[2]))
            seen.add(nums[i])
        ret = [ list(_) for _ in triplets]
        return list(ret)
