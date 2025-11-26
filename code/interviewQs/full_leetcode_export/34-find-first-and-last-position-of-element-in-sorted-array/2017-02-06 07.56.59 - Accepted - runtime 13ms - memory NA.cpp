class Solution {
public:

    
    vector<int> searchRange(vector<int>& nums, int target) {
    
            
        int l=0,m=0, h=nums.size()-1;
        vector<int> vRange = {-1,-1};
        
        if (nums.empty()) return vRange;
        
        //search low target
        while (l<=h)
        {
            m = (l+h)/2;
            if (nums[m] == target) 
            {
                if (vRange[0] == -1)
                {
                    vRange[1] = m;    
                }
                vRange[0] = m;
                
                h=m-1;
            }
            else if (nums[m] > target) //search in lower part
            {
                h = m-1;
            }
            else
            {
                l=m+1;
            }
        }
        
        l=0;
        h=nums.size()-1;
        
        //search high target
        while (l<=h)
        {
            m = (l+h)/2;
            
            if (nums[m] == target) 
            {
                if ( vRange[1] < m) vRange[1] = m;
                
                l=m+1;
            }
            else if (nums[m] > target) //search in lower part
            {
                h = m-1;
            }
            else
            {
                l=m+1;
            }
        }
        
        return vRange;
    }
};