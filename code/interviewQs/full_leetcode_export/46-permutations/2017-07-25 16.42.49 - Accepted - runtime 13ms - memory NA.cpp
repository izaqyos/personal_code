class Solution {
public:
    /*
    void permuteR(int num, vector<int>& nums, vector<vector<int>> & vres;) {
        
        int n = nums.length();
        if (n == 1) 
        {
            vector<int> vint;
            vint.push_back(num);
            vint.push_back(nums[0]);
            vres.push_back(vint);
            return;
        }
        else 
        {
            //copy nums. work on copy. delete nu then pass it to permuteR
            for(auto nu : nums)
            {
                permuteR
            }
        }
    }
    */
    
    vector<vector<int>> permute(vector<int>& nums) {
        int n = nums.size();
        vector<vector<int>> vres;
        if (n == 0) return vres;
        
        if (n == 1) 
        {
            vector<int> vint(1,nums[0]);
            vres.push_back(vint);
            return vres;
        }
        
        vector<int> nums_copy;
        vector<vector<int>> inter_res;
        for (int i=0; i<nums.size();++i)
        {
            nums_copy=nums;
            nums_copy.erase(nums_copy.begin()+i);
            inter_res = permute(nums_copy);
            for (auto & v : inter_res)
            {
                v.push_back(nums[i]);
                vres.push_back(v);
            }
        }
        
        return vres;
    }
        
        
    
};