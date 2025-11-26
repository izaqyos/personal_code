bool operator == (const vector<int> & v1, const vector<int> & v2)
        {
            if (v1.size() == v2.size())
            {
                for (int i=0; i<v1.size(); ++i)
                {
                    if (v1[i] != v2[i]) return false;
                }
            }
            else return false;
            
            return true;
        }


class Solution {
public:
        
    vector<vector<int>> permuteUnique(vector<int>& nums) {
        
        //use unordered_set<vector<int> > to save intermidate results
        // add to set first (so duplicated will not be added)
        //the from set add back to vres. need to pass hash function to set CTOR
        // the hash should run on vector<int> and used for =check
        //since anyway it is O(n), n being vec len its same complexity 
        
        int n = nums.size();
        vector<vector<int>> vres;
        
        if (n == 0) return vres;
        
        if (n == 1) 
        {
            vector<int> vint(1,nums[0]);
            vres.push_back(vint);
            return vres;
        }
        
        
        vector<int> nums_copy;
        vector<vector<int>> inter_res;
        
        struct hashF{
            size_t operator ()(const vector<int> & vec) const
            {
                size_t res = 0;
                /*
                for (i : vec)
                {
                    res+=i;
                }
                */
                for (int i=0; i<vec.size(); ++i)
                {
                    res+=(i+1)*vec[i];
                }
                return res;
            }
        };
        

        
        unordered_set<vector<int>, hashF> vecSet;
        
        for (int i=0; i<nums.size();++i)
        {
            nums_copy=nums;
            nums_copy.erase(nums_copy.begin()+i);
            inter_res = permuteUnique(nums_copy);
            for (auto & v : inter_res)
            {
                v.push_back(nums[i]);
                if ( vecSet.find(v) == vecSet.end())
                {
                    vecSet.insert(v);
                    vres.push_back(v);
                }
            }
        }
        
        return vres;
    }
};