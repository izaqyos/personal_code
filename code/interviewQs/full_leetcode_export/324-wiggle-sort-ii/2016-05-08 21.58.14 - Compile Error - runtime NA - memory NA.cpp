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
        for (int i=0; i<nums.size(); ++i )
        {
            if ((i%2) == 0)//even index
            {
                if(i < (nums.size()-1) ) //only if not last elem
                {
                    if (nums[i] > nums [i+1])//swap
                    {
                        int temp = nums[i];
                        nums[i] = nums[i+1];
                        nums[i+1] = temp;
                    }
                    else if (nums[i] == nums [i+1]) // run till first >
                    {
                        /**
                        for (int j=i+2; j < nums.size(); ++j)
                        {
                            if (nums[i] > nums [j])//swap
                            {
                                int temp = nums[i];
                                nums[i] = nums[j];
                                nums[j] = temp;
                            }       
                        }
                        **/
                        
                        for (int j = nums.size()-1; --j)
                        {
                            if (nums[i] > nums [j])//swap
                            {
                                int temp = nums[i];
                                nums[i] = nums[i+1];
                                nums[i+1] = temp;
                            }
                    
                            
                        }
                    
                }
            }
            else //odd
            {
                if(i < (nums.size()-1) ) //only if not last elem
                {
                    if (nums[i] < nums [i+1])//swap
                    {
                        int temp = nums[i];
                        nums[i] = nums[i+1];
                        nums[i+1] = temp;
                    }
                    else if (nums[i] == nums [i+1]) // run till first <
                    {
                        /**
                        for (int j=i+2; j < nums.size(); ++j)
                        {
                            if (nums[i] < nums [j])//swap
                            {
                                int temp = nums[i];
                                nums[i] = nums[j];
                                nums[j] = temp;
                            }       
                        }
                        **/
                        
                        for (int j=0; j < i; j=j+2)
                        {
                            if (nums[i] < nums [j])//swap
                            {
                                int temp = nums[i];
                                nums[i] = nums[j];
                                nums[j] = temp;
                            }       
                        }
                        
                    }
                }
                
            }
        }
        
        /**
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
        **/
        return;
        
    }
};