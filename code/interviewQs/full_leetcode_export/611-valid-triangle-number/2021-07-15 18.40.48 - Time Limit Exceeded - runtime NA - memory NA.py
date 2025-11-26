class Solution:
    def triangleNumber(self, nums: List[int]) -> int:
        def isTriangle(a,b,c):
            if (a+b>c) and (a+c>b) and (c+b>a):
                return True
            else:
                return False
            
        n = len(nums)
        
        ntriangles = 0
        for i in range(n):
            j=i+1
            while j<n:
                k=j+1
                while k<n:
                    
                    if isTriangle(nums[i], nums[j], nums[k]):
                        ntriangles+=1
                    k+=1
                j+=1
        return ntriangles
        