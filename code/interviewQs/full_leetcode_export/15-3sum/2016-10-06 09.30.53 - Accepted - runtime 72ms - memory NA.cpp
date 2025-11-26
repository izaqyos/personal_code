class Solution {
public:
    vector<vector<int>> threeSum(vector<int>& nums) {
        vector<vector<int>> vRet;
        if (nums.size() < 3) return vRet;
        
        int l,r;
        
        
        sort(nums.begin(), nums.end());
      // std::copy(nums.begin(), nums.end(),std::ostream_iterator<int> (std::cout,", "));
    //    cout<<endl;
        
        for (int i=0; i<nums.size()-2; ++i)
        {
            
            l=i+1;
            r=nums.size()-1;
            while (l<r)
            if ( nums[i] + nums[l] +nums[r] < 0) l++; //need bigger num so l++
            else if ( nums[i] + nums[l] +nums[r] > 0) r--; //need smaller num so r--
            else //( nums[i] + nums[l] +nums[r] == 0)
            {
                    //   cout<<"Adding triplet: ["<<i<<","<<l<<","<<r<<"]"<<endl;
                        vector<int> vec = {nums[l] ,nums[i] , nums[r]};
                        vRet.push_back(vec );//make uniqu use set
                        l++;
                       // while ((nums [l-1] == nums[l]) ||(nums[i] == nums[l])) l++; 
                       while(nums[i] == nums[i+1]) i++;//avoid dups
                       while(nums[l] == nums[l-1]) l++;//avoid dups
                        r--;
                    
            }
            
        
        }
        return vRet;
    }
};