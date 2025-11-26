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
        
        
        for (int j=0;  j<nums.size();++j)
        {
           // cout<<"a. nums["<<j<<"]="<<nums[j]<<endl;
            //if ((nums[j]>0) && (nums[j] > nums.size()) ) nums.resize(nums[j], -1);
            while ( (nums[j]>0) && (nums[j] < nums.size()) && (nums[j] != nums[nums[j]-1]) ) swap(nums,j,nums[j]-1); //objective, for all j , j+1 -= nums[j]
        }
        
        
        int j=0;
        for (; j<nums.size();++j)
        {
         //  cout<<"b. nums["<<j<<"]="<<nums[j]<<endl;
            if ( (nums[j] != (j+1)) ) return j+1;
        }
        
        return j+1;
        
        
    }
};