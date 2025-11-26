class Solution {
public:
    string &  trimRight(string & str)
    {
            str.erase(str.find_last_not_of(m_ws) +1);
            return str;
    }

    string &  trimLeft(string & str)
    {
            str.erase(0, str.find_first_not_of(m_ws));
            return str;
    }

    string & trim(string & str)
    {
            return trimLeft(trimRight(str));
    }

    //assumes str is trimmed. i.e. not starting w/ 1 or more delim
    vector<string>  split(string &str, string & delims)
    {
            if (m_bDebug) cout<<"Split str= "<<str<<", delimiters= "<<delims<<endl;
            vector<string>  vRet;
            unsigned int idx = 0;
            size_t found;
            while (idx < str.size()) //won't enter on empty str
            {

                found = str.find_first_of(delims,idx); //find first delim, so first token is substr(idx, found-idx) 
                if (found ==  string::npos ) //no delim, push substr from idx to end of str
                {
                        if (m_bDebug) cout<<"no delimeter found. adding substr from index "<<idx<<", token "<<str.substr(idx) <<endl;
                        vRet.push_back(str.substr(idx)) ;
                        return vRet;
                }
                else
                {
                    if (m_bDebug) cout<<"delimeter found. adding substr from index "<<idx<<", of length "<<found-idx<<", token "<<str.substr(idx, found-idx) <<endl;
                    vRet.push_back (str.substr(idx,found-idx ) ); //push_back substr from idx, length found -idx
                    idx=found; //increment idx to 1st delim
                    idx=str.find_first_not_of(delims,idx); // skip additional consequitive delims if any 
                    if (idx == string::npos) return vRet; // no more tokens, return
                }
            } //while
        return vRet;
    }

    int lengthOfLastWord(string s) {

        //return s.trim().split().back().length(); //would've been cool but alas, on empty vector back() crashes
        string sDelim(m_ws);
        vector<string> words = split(trim(s), sDelim);
        if (words.empty()) return 0 ;
        else  return words.back().length() ;
    }

private:
    const char* m_ws = " \t\n\r\f\v";
    bool m_bDebug = false;
};
