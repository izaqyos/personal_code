class Solution {
public:
    int rob(vector<int>& nums) {
        vector<int> maxs(nums.size());
        for (int i=0; i<nums.size(); ++i)
        {
            if (i == 0) maxs[i] = nums[i];
            else if (i == 1) maxs[i] = max(nums[i], nums[i-1]);
            else maxs[i] = max(maxs[i-2] + nums[i], maxs[i-1]);
        }
        return maxs[nums.size()-1];
    }
};