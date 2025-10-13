class NumArray {
public:
    NumArray(vector<int> &nums) {
        unsigned int sum = 0;
        m_vSums.reserve(nums.size());
        for (int i=0; i<nums.size(); ++i)
        {
            sum+=nums[i];
            m_vSums[i]= sum;
            //cout<<"sum untill "<<i<<" is "<<m_vSums[i]<<endl;
        }
        
    }

    int sumRange(int k, int l) {
        
        if (k == 0) return m_vSums[l];
        else return (m_vSums[l] - m_vSums[k-1]);
    }
    
    vector<int> m_vSums;
    
};
