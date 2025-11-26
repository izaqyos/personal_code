class Solution {
public:
    int lengthOfLIS(vector<int>& nums) {
     
     vector< vector<int> > vMem(nums); // n=nums.size(), nXn matrix to save partial results
     
     if (nums.empty()) return 0;
     if (nums.size() == 1) return 0;
     struct rankLis
     {
        int lisLen;
        int highest;
        int lisIndex;
     };
     
     vMem[0].push_back(nums[0]);
     for (int i=1; i<nums.size();++i)
     {
         rankLis rank;
         rank.lisLen=0;
         rank.lisLen=0;
         for (int j=i-1; j<i;++j)
         {
         if ( (nums[i]) > vMem[j].back() ) 
         {
             vMem[i] = vMem[i-1];
             vMem[i].push_back(nums[i])
         }
         }
     }
    }
};