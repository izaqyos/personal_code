class Solution {
public:
    int removeDuplicates(vector<int>& nums) {
     
     if (nums.empty() || (nums.size()==1)) return nums.size();
    
     
     int j=1; //index to next cell of return array and size at end
     
    for (int i=1;i<nums.size();++i)
    {
        if (nums[i]!=nums[i-1]) // found unique element. add it
        {
            nums[j] = nums[i];
            ++j;
        }
        
    }
    return j;
    }
};