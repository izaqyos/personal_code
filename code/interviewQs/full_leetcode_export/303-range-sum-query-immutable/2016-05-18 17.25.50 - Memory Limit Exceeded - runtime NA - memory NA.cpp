class NumArray {
public:
    NumArray(vector<int> &nums) {
        m_vNums=nums;
        for (int i=0; i<m_vNums.size(); ++i)
        {
            m_vPartRes.push_back( vector<int>(m_vNums.size()) );
        }
    }

    int sumRange(int i, int j) {
        if (i==j) {
            m_vPartRes[i][j] = m_vNums[i];
            return m_vNums[i];
        }
        else if ( (j-i) == 1){
          m_vPartRes[i][j] = m_vNums[i]+m_vNums[j];
          m_vPartRes[j][i] = m_vNums[i]+m_vNums[j];
          return (m_vNums[i]+m_vNums[j]);  
        } 
        else {
            
            return sumRange(i,(i+j)/2)+sumRange( ((i+j)/2)+1, j);
        }
    }
    
    vector<int> m_vNums;
    vector< vector<int> > m_vPartRes;
};


// Your NumArray object will be instantiated and called as such:
// NumArray numArray(nums);
// numArray.sumRange(0, 1);
// numArray.sumRange(1, 2);