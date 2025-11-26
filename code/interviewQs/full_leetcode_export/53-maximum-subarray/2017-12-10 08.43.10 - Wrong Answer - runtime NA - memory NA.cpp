class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        
        int b=0,sum=0,max = 0; //indices. begin of subarray, end and current
        
        for (b=0;b<nums.size()-1; ++b)
        {
            sum+=nums[b];
            sum = std::max(sum,0);
            max = std::max(sum,max); 
        }
        return max;
    }
};