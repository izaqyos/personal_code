class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        
        int b=0,sum=0,max = 0; //indices. begin of subarray, end and current
        
        for (b=0;b<nums.size(); ++b)
        {
            sum+=nums[b];
            //cout<<"sum: "<<sum<<endl;
            sum = std::max(sum,0);
            //cout<<"sum: "<<sum<<endl;
            max = std::max(sum,max); 
        }
        return max;
    }
};