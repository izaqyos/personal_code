class Solution {
public:
    bool isMatch(string s, string p) {
       // bool res = false;
        
        bool bD = false;
        if (s.empty())
        {
            if (p.empty()) return true;
            else
            {
                for(auto c : p)
                {
                    if( c != '*') return false;
                }
                return true;
            }
        }
        
       // int pi = 0;
        for(int i=0;i<s.length();++i)
        {
            if (bD) cout<<"pos: "<<i<<", compare "<<s[i]<<" to "<<p[i]<<endl;
            if ( i<p.length())
            {
                if (p[i] == '?') continue;
                else if (p[i] == s[i]) continue;
                else if (p[i] == '*')
                {
                    for(int j=i;j<s.length();++j) //try 0 or more matches as many as s allows
                    {
                        if ( isMatch ( s.substr(j, string::npos)  , p.substr(i+1, string::npos)  ) ) return true;
                    }
                }
                else return false;
                     
            }
            else
            {
                return false;
            }
        }
        return true;
    }
};