class Solution {
public:

    bool bD = false;
    
    int searchR(vector<int>& nums, int target, int l, int r)
    {
        if (bD) cout<<"searchR(), l="<<l<<", r="<<r<<endl;    
        if (r == l) return ( target == nums[l] ) ? l : -1;
        if (r-l == 1) return ( target == nums[l] ) ? l : -1;
        
        int m = l+(r-l )/2;
        
        if (target == nums[m]) return m;
        else if (target < nums[m])
        {
            if ( ( nums[l] <= target ) && (target <= nums[m-1])) // check before recursing
            {
                return searchR(nums, target, l, m);
            }
            else // we hit pivot search in opposite range
            {
                if (m +1<nums.size()) return searchR(nums, target, m+1, r);
                else return -1;
            }
        }
        else //(target >= nums[m])
        {
            
                if ( ( (m+1<nums.size()) && (nums[m+1] <= target) ) && (target <= nums[r-1])) // check before recursing
                {
                    return searchR(nums, target, m+1, r);
                }
                else // we hit pivot search in opposite range
                {
                    return searchR(nums, target, l, m);
                }
        
            
        }
    }
    
    int search(vector<int>& nums, int target) {
        
        //my idea. binary search w/ twist
        // compare target to nums[n/2] then in sorted array we would recurse on either half 
        // this time, since nums[n/2] may be pivot we need to check range first.
        int n = nums.size();
        
        if (n == 0 ) return -1;
        return searchR(nums, target, 0, n);   
    }
};