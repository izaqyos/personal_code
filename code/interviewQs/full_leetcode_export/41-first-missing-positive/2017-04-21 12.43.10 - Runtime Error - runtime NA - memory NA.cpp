class Solution {
public:
    void swap(vector<int>& nums, int s, int d)
    {
        if (s!=d)
        {
        int t = nums[s];
        nums[s] = nums[d];
        nums[d] = t;
        }
    }
    
    int firstMissingPositive(vector<int>& nums) {
        
        for (int j=0; j<nums.size();++j)
        {
            swap(nums,j,nums[j]-1);
        }
        
        for (int j=0; j<nums.size();++j)
        {
            if (nums[j] != (j+1) ) return j+1;
        }
        
        return nums.size()+1;
        
    }
};