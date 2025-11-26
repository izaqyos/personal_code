class Solution {
public:
    void wiggleSort(vector<int>& nums) {
        
        
        if ( (nums.size()==0 ) || (nums.size()==1 ) ) return ; //already wiggle sorted
        if  (nums.size()==2 )
        {
            if (nums[0] > nums[1])
            {
                int temp = nums[0];
                nums[0] = nums[1];
                nums[1] = temp;
            }
            
            return;
        }
        
        sort(nums.begin(), nums.end());
        int lowIdx = 0;
        int highIdx = nums.size()/2;
        vector<int> vRes(nums.size());
        
        for (int i=0; i<nums.size()-1; i+=2 )
        {
            vRes[i]= nums[lowIdx];
            vRes[i+1]=nums[highIdx];
            lowIdx++;
            highIdx++;
        }
        
        nums = vRes;
        return;
        
    }
};