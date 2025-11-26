class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        retSet = set()
        retSet.add(())
        
        for i,e in enumerate(nums):
            tnums = nums[:i]+nums[i+1:]
            subsets = self.subsetsWithDup(tnums)
            for s in subsets:
                tl=tuple(sorted(s))
                retSet.add(tl)
                s.append(e)
                tl=tuple(sorted(s))
                retSet.add(tl)
        ret =[]
        for s in retSet:
            ret.append(list(s))
        return ret
            
        