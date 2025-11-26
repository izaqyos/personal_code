class NumArray {
public:
    NumArray(vector<int> &nums) {
        unsigned int sum = 0;
        for (int i=0; i<nums.size(); ++i)
        {
            m_vSums[i]= (sum+=nums[i] );
        }
    }

    int sumRange(int k, int l) {
        
        if (k == 0) return m_vSums[k];
        else return (m_vSums[k] - m_vSums[l-1]);
    }
    
    vector<int> m_vSums;
    
};


// Your NumArray object will be instantiated and called as such:
// NumArray numArray(nums);
// numArray.sumRange(0, 1);
// numArray.sumRange(1, 2);