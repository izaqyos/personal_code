class Solution {
public:
    int removeElement(vector<int>& nums, int val) {
        if (nums.size()<1) return nums.size();
        
        int n = nums.size();
        int n2=0; //new size
        
        for (int i=0;i<n;++i)
        {
            if (nums[i] != val)
            {
                if (nums[n2] != nums[i]) nums[n2] = nums[i];
                n2++;
            }
            
        }
        
        return n2;
    }
};