class Solution {
public:
    int findPeakElement(vector<int>& nums) {
        if (nums.empty()) return -1*(1<<32 -1 );
        
        int peak=-1*(1<<32 -1 );
        int peakIdx=-1;
        for (int i=0; i<nums.size(); ++i)
        {
            if (nums[i]>peak) 
            {
                peak=nums[i];
                peakIdx=i;
            }
        }
        
        return peakIdx;
    }
};