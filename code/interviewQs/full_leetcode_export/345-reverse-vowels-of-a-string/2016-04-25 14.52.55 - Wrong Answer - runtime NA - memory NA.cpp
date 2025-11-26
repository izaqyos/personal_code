class Solution {
public:
    string reverseVowels(string s) {
        string sVoels;
        
        for (string::const_iterator ci = s.begin(); ci!=s.end();++ci)
        if ( ((*ci) == 'a' ) || ((*ci) == 'e' ) || ((*ci) == 'i' ) || ((*ci) == 'o' ) || ((*ci) == 'u' ) ) 
        {
            sVoels.push_back(*ci);
        }
        
        for (unsigned int i = 0; i < s.size(); ++i)
        {
            if ( (s[i] == 'a' ) || (s[i] == 'e' ) || (s[i] == 'i' ) || (s[i] == 'o' ) || (s[i] == 'u' )  )
            {
                s[i] = sVoels.back();
                sVoels.pop_back();
            }
        }
        
        return s;
    }
};