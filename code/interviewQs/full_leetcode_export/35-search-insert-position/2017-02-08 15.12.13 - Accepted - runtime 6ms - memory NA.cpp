class Solution {
public:
    int searchInsert(vector<int>& nums, int target) {
        
        if (nums.empty()) return 0;
        if ( (nums.size() == 1) ) // optimization
        {
           if  ( (nums[0] == target ) || (nums[0] > target )) return 0;
           else return 1;
        }
        
        int n = nums.size();
        int l=0,m=0, h=n-1, li=0,hi=0;
        
        /*
        
        idea, binary search, if target found return index, if not use li and hi to mark lower than index and upper than index
        
        */
        while (l<=h)
        {
            m=(l+h)/2;
            
            if(nums[m] == target) return m;
            else if (nums[m] > target )
            {
                hi=m;
                h=m-1;
            }
            else
            {
                li=m;
                l=m+1;
            }
            
        }
        
        if (li == n-1) return n;
        else if (hi == 0 ) return 0;
        else return hi;
        
    }
};