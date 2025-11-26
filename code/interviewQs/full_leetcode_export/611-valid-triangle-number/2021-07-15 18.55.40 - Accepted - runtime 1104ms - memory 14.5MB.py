class Solution:
    def triangleNumber(self, nums: List[int]) -> int:
        def isTriangle(a,b,c):
            if (a+b>c) and (a+c>b) and (c+b>a):
                return True
            else:
                return False
            
        n = len(nums)
        if n<3:
            return 0
        ret=0
        nums=sorted(nums)
        for i in range(2,n):
            s,e=0,i-1
            
            while s<e:
                if nums[s]+nums[e]>nums[i]:
                    ret+=e-s
                    e-=1
                else:
                    s+=1
        return ret
                        
            
        
        # o(n^3) TLE
        #ntriangles = 0
        #for i in range(n):
        #    j=i+1
        #    while j<n:
        #        k=j+1
        #        while k<n:           
        #            if isTriangle(nums[i], nums[j], nums[k]):
        #                ntriangles+=1
        #            k+=1
        #        j+=1
        #return ntriangles
        