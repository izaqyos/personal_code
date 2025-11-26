class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        
        //vector<int> vLoLS(s.size(),1);
        
        if (s.empty()) return 0;
        
        
        
        string sUniq(1, s[0]);
        int highest = sUniq.length();
        
        for (int i=1; i<s.size();++i)
        {
            size_t found = sUniq.find(s[i]);
            if (found == string::npos)
            {
                sUniq+=s[i];
               // cout<<"uniq: "<<sUniq<<endl;
                
                if (sUniq.length()> highest ) highest = sUniq.length();
            }
            else
            {
                //if found char delete prefix up to char (inclusive) - size of sUniq is current length 
                sUniq=sUniq.substr(found+1);
                sUniq+=s[i];
                
              //  cout<<"uniq: "<<sUniq<<endl;
            }
        }
        
        return highest;
    }
};