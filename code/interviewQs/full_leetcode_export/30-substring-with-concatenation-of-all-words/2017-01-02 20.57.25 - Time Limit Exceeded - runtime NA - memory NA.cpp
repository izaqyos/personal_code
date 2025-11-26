class Solution {
public:

    bool bdebug = false;

//Use 2 dicts. 1 word->count , how many times each word
//2nd, word->count how many times word encountered from position i
//if not found or > expected cont to i++
            //params: substr to match, current (not matched) words, match indices vector, match to add when words has one word,  s - string to cont. matches. 
    
    vector<int> findSubstring(string s, vector<string>& words) {
        vector<int> vret;
        
        if (s.length() == 0 )
        {
            //if (words.empty() ) vret.push_back(0);
            return vret;
        }
        
        
        int slen = s.length();
        int wlen = words[0].length();
        
        if (words.empty()   || (wlen > slen )) return vret;
        
        unordered_map<string, int> expectedWords;
        unordered_map<string, int> foundWords;
        unordered_map<string, int>::const_iterator cit;
        
        for (auto w : words)
        {
            expectedWords[w]++;
        }
        
        for (int i=0; i<= slen-wlen; ++i)
        {
            foundWords = expectedWords;
            if (bdebug) cout<<"crawling index: "<<i<<endl;
            bool bCont = true;
            
            string cword = s.substr(i,wlen);
            int index = i;
            while (bCont )
            {
                if (foundWords.empty()) 
                {
                    vret.push_back(i);
                    bCont = false;
                }
                cit =   foundWords.find(cword);
                if ( cit == foundWords.end()) // current word not in expected list bail
                {
                    bCont = false;
                }
                else 
                {
                    foundWords[cword]--;
                    if (  foundWords[cword] == 0) 
                    {
                        foundWords.erase(cit);
                    }
                }
                if (index + wlen <= slen) 
                {
                    index+=wlen;
                    cword = s.substr(index,wlen);
                }
                else bCont = false;
            }
            
        }
        
        
        return vret;
    }
};