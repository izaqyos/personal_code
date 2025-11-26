class Solution {
public:
    vector<vector<int>> fourSum(vector<int>& nums, int target) {
        bool bDebug = false;
        
        vector<vector<int>> vRet;
        
        if (nums.size()<4) return vRet;
        
        int n = nums.size();
        sort(nums.begin(),nums.end());
        
        if (bDebug)
        {
        copy(nums.begin(),nums.end(), ostream_iterator<int>(cout,", "));
        cout<<endl;
        }
        
        for (int i=0; i < n-3; ++i)
        {
            if (bDebug)cout<<"outer loop. nums["<<i<<"]="<<nums[i]<<endl;
            
            //optimization, skip same
            if (i>1 && nums[i]==nums[i-1]) continue;
            //optimization, if 4 smallest bigger than target, impossible to find quad
            if (nums[i]+nums[i+1]+nums[i+2]+nums[i+3] > target) break;
            //optimization, if ith + 3 biggest are smaller than target, try i+1
            if (nums[i]+nums[n-1]+nums[n-2]+nums[n-3] < target) continue;
            
            //now that we have plausible i, do same for j
            for (int j=i+1; j < n-2; ++j)
            {
                if (bDebug) cout<<"inner loop. nums["<<j<<"]="<<nums[j]<<endl;
                
                //optimization, skip same
                if ( j>i+1 && nums[j-1]==nums[j]) 
                    {
                        cout<<"skip same j"<<endl;
                        continue;
                    }
                    
                //optimization, if 4 smallest bigger than target, impossible to find quad
                if (nums[i]+nums[j]+nums[j+2]+nums[j+1] > target) 
                {
                    if (bDebug) cout<<"4 smallest bigger than target, impossible to find quad"<<endl;
                    break;
                }
                //optimization, if ith + jth + 2 biggest are smaller than target, try j+1
                if (nums[i]+nums[j]+nums[n-1]+nums[n-2] < target) 
                {
                    if (bDebug) cout<<"ith + jth + 2 biggest are smaller than target"<<endl;
                    continue;
                }
                
                //now we have plausible ith and jth use Left and Right pointers to do the sum
                // move L,R according to < or > than target
                
                int l=j+1;
                int r=n-1;
                while (l<r)
                {
                    if (bDebug) cout<<"left: "<<l<<", right: "<<r<<endl;
                    if (nums[i]+nums[j]+nums[l]+nums[r] > target)  --r; //too big, try r-1
                    else if (nums[i]+nums[j]+nums[l]+nums[r] < target)  ++l; //too small, try l+1
                    else //finally, found quad
                    {
                        if (bDebug) cout<<"found quad: ["<<i<<", "<<j<<", "<<l<<", "<<r<<"]"<<endl;
                        vector<int> vTemp = { nums[i], nums[j], nums[l], nums[r] };
                        vRet.push_back(vTemp);
                        l++; while (nums[l] == nums[l-1]) l++;
                        r--; while (nums[r] == nums[r+1]) r--;
                    }
                }
             }
        }
        
        return vRet;
        
    }
};