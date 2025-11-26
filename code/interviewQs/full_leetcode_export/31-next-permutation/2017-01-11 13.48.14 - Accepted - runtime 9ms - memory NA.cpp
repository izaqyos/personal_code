class Solution {
public:
    void nextPermutation(vector<int>& nums) {
        
        int temp;
        int len = nums.size();
        for (int i = len-1; i>0;--i)// n iters
        {
            
            if (nums[i] > nums[i-1]) // when we get here we have nums[i] >= nums[i+1]>=...nums[len-1]
            //so the smallest increase next permutation would require.
            //a. swap nums[i-1] and nums[len-1] if its bigger, otherwise use len-2 etc. (since its smallest)
            //b. sort nums nums[i]-nums[len-1] in acsending order
            {
                int j = len-1;
                for (; j>i-1;j--) 
                {
                    if (nums[j] > nums[i-1]) break;
                }
                
                temp = nums[i-1];
                nums[i-1]= nums[j];
                nums[j]=temp;
                //cout<<"sort range "<<i<<" to end"<<endl;
                sort(nums.begin()+i,nums.end());
                return;
            }
        }
        
        //if we got here it means permuation is in descending order - rearrange to acending
        //since we start we descending sorted most efficient is not use sort, this is O(n)
        
        for (int i=0; i< nums.size()/2;++i)
        {
            temp = nums[i];
            nums[i]=nums[nums.size() -i -1];
            nums[nums.size() -i -1] = temp;
        }
        return;
    }
};