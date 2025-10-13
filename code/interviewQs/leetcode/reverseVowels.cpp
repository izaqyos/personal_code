class Solution {
public:
    string reverseVowels(string s) {
        string sVoewls;
        string sAux = "aAeEiIoOuU";
        
        for (string::const_iterator ci = s.begin(); ci!=s.end();++ci)
        if ( sAux.find(*ci) != string::npos ) 
        {
            sVoewls.push_back(*ci);
        }
        
        for (unsigned int i = 0; i < s.size(); ++i)
        {
            if ( sAux.find(s[i]) != string::npos  )
            {
                s[i] = sVoewls.back();
                sVoewls.pop_back();
            }
        }
        
        return s;
    }
};
