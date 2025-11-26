class Solution:
    ##naive Solution, o(nlogn). sort first.
    #def findKthLargest(self, nums: List[int], k: int) -> int:
    #    nums.sort()
    #    return nums[-k]

    #Solution, o(n). quick select : https://www.geeksforgeeks.org/quickselect-algorithm/, wors case o(n^2)
    def findKthLargest(self, nums: List[int], k: int) -> int:
        n = len(nums)
        def partition(l,r):
            pivot=nums[r]
            i=l #smaller than pivot section , left section
            for j in range(l,r):
                if nums[j] <= pivot:
                    nums[i], nums[j] = nums[j], nums[i] #move smaller than pivot to left section
                    i+=1
            nums[i], nums[r] = nums[r], nums[i] #move pivot to it's correct index i
            return i



        def quick_select(l,r,k): #for kth smallest
            #print(f"got k={k}, l={l}, r={r}") 
            if l == r:
                return nums[l]
            if  k>0 and k<=r-l+1:
                pivot_index = partition(l,r)
                #print(f"partition result pivot_index={pivot_index}, normalized pivot_index={pivot_index-l}, pivot={nums[pivot_index]}") 
                #print(f"nums={nums}") 

                if pivot_index-l == k:
                    return nums[pivot_index]
                if pivot_index-l > k: #if index is bigger than k than k is in the left part
                    return  quick_select(l, pivot_index-1, k)

                #if index is <= k than k would be in right part (bigger nums) and it would be (k-index)th element
                return quick_select(pivot_index+l , r, k-pivot_index+l)

            #print("invalid k")

        return quick_select(0, n-1, n-k)
