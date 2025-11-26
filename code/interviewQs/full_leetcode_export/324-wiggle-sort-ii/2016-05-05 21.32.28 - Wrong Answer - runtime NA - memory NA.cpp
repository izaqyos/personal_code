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
        int lowIdx = 1;
        int highIdx = nums.size()/2;
        
        while (lowIdx<highIdx )
        {
                int temp = nums[lowIdx];
                nums[lowIdx] = nums[highIdx];
                nums[highIdx] = temp;
                lowIdx+=2;
                highIdx++;
        }
        
        return;
        
    }
};