class Solution {
public:
    vector<int> largestDivisibleSubset(vector<int>& nums) {
        if (nums.empty() ||(nums.size()==1)) return nums;
        
        vector<int>  vLDS_biggest; // vLDS_biggest[i] will contain size of largestDivisibleSubset "ending" w/ nums[i]
        
        sort(nums.begin(), nums.end()); 
        
        vLDS_biggest.push_back(1); // size of largestDivisibleSubset "ending" w/ nums[0], which is smallest num
        int longest = 0;
        int longestIdx = 0;
        vector< vector <int> > longestSubsetPerIdx;
        longestSubsetPerIdx.push_back(vector<int>(1,nums[0]));//at 0 -> {nums[0]}
        
        for (int i=1; i < nums.size(); ++i)
        {
            //cout<<"calc i"<<i<<endl;
            longest =0;
            longestIdx = 0;
            
            for (int j=i-1; j>=0; --j)
            {
                //cout<<"calc j"<<j<<"Test mod "<<nums[i]<<"%"<<nums[j]<<endl;
                if ((nums[i] %  nums[j]) == 0)    
                {
                    if (vLDS_biggest[j] > longest)
                    {
                        longest = vLDS_biggest[j];
                        longestIdx = j;
                       // cout<<"longest: "<<longest<<", + index: "<<longestIdx<<endl;
                    }
                }
            }
            if (longest == 0 ) // nums [i] doesn't divide by any of nums[0...i-1]
            {
                vLDS_biggest[i] = 1; // just divide by himself
                longestSubsetPerIdx.push_back(vector<int>(1,nums[i]));
            }
            else
            {
                vLDS_biggest[i] = longest+1; //  divides a longer (the longest) seq...
                vector<int> set = longestSubsetPerIdx[longestIdx];
                set.push_back(nums[i]);
                longestSubsetPerIdx.push_back(set);
            }
            
        }
        
        return longestSubsetPerIdx[nums.size()-1];
        
    }
};