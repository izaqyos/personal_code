class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        
        vector<int> vRet(2);
        
        // space efficient double loop o(n^2), space o(1)
        for (int i=0;i<nums.size();++i)
        {
            for (int j=i+1;j<nums.size();++j)
            {
                if (nums[i]+nums[j] == target)
                {
                    vRet[0]= i;
                    vRet[1]=j;
                    return vRet;
                }
            }
        }
        
        return vRet;
    }
};