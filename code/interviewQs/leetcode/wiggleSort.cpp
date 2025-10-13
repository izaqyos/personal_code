class Solution {
public:
    void wiggleSort(vector<int>& nums) {
        //new approach, just make sure each even is < odd, each odd > even, try swap w/ closes elem, if equal check next.
        
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
        int lowIdx = nums.size()/2 -1 ;
        if  (nums.size()%2 == 1 ) lowIdx++  ;
        int highIdx = nums.size()-1;
     //   cout<<"lowIdx "<<lowIdx<<", highIdx "<<highIdx<<"\n";
        vector<int> vRes(nums.size());
        
        for (int i=0; i<nums.size(); ++i )
        {
            if (i%2 == 0)
            {
                vRes[i]=nums[lowIdx];
                lowIdx--;
            }
            else
            {
                vRes[i] = nums[highIdx];
                highIdx--;
            }
        }
        
        nums = vRes;
        
        return;
        
    }
};
