class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        
        //vector<int> vLoLS(s.size(),1);
        
        if (s.empty()) return 0;
        
        int ret = 1;
        int highest = ret;
        string sUniq(1, s[0]);
        for (int i=1; i<s.size();++i)
        {
            size_t found = sUniq.find(s[i]);
            if (found == string::npos)
            {
                sUniq+=s[i];
                cout<<"uniq: "<<sUniq<<endl;
                ++ret;
                if (ret> highest ) highest = ret;
            }
            else
            {
                ret=1;
                sUniq=s[i];
            }
        }
        
        return highest;
    }
};