class Solution {
public:
    vector<int> intersection(vector<int>& nums1, vector<int>& nums2) {
        set<int> sInter;
        vector<int> vRet;
        
        for (auto n1 : nums1)
        {
            for (auto n2 : nums2)
            {
                if (n1==n2)
                {
                    sInter.insert(n1);
                }
            }
        }
        
        for (auto n : sInter)
        {
            vRet.push_back(n);
        }
        
        return vRet;
    }
};