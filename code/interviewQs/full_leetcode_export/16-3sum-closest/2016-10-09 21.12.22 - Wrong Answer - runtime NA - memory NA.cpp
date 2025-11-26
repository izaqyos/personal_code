class Solution {
public:
    int threeSumClosest(vector<int>& nums, int target) {
        if (nums.size() <3) return 0;
        
        int l,r;
        int sum =0;
        int tmp_sum,diff;
        int min_diff = INT_MAX;
        
        sort(nums.begin(),nums.end());
       //std::copy(nums.begin(),nums.end(), std::ostream_iterator<int>(std::cout, ", "));
        //cout<<endl;
        
        for (int i=0;i<nums.size();++i)
        {
            l=i+1;
            r=nums.size()-1;
            
            while (l<r)
            {
            
                tmp_sum=nums[i]+nums[l]+nums[r];
                diff = abs(tmp_sum -target);
           // cout<<"i: "<<i<<", l: "<<l<<", r: "<<r<<", tsum: "<<tmp_sum<<", tdiff: "<<diff<<endl;
                if (sum == target) return sum;
                else 
                {
                    if (diff < min_diff )
                    {
                        min_diff = diff;
                        sum = tmp_sum;
                    }
                    if (tmp_sum< target) //try a bigger number, if we take smaller diff would increase
                    {
                        l++;
                        while (nums[l] == nums[l-1]) ++l;// skip same
                    }
                    else // (tmp_sum > target) //try a smaller number, if we take bigger diff would increase
                    {
                        --r;
                        while (nums[r] == nums[r+1]) r--; //skip same
                    }
                    
                }
            }
           
            
        }
        
        return sum;
    }
};