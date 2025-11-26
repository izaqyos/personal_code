class Solution {
public:

    bool bdebug = false;

//Use 2 dicts. 1 word->count , how many times each word
//2nd, word->count how many times word encountered from position i
//if not found or > than expected cont to i++
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
            if (bdebug) cout<<"Added word: "<<w<<", to dictionary, freq: "<<expectedWords[w]<<endl;
        }
        
        for (int i=0; i<= slen-(wlen*words.size()); ++i)
        {
            
            if (bdebug) cout<<"crawling index: "<<i<<endl;
            foundWords.clear();
            
            int j=0;
            for(;j<words.size();++j)
            {
                if (bdebug) cout<<"inner index: "<<j<<endl;
                string cword = s.substr(i+(j*wlen),wlen);
                cit = expectedWords.find(cword);
                if ( cit != expectedWords.end()) 
                {
                    foundWords[cword]++;
                    if (foundWords[cword] > expectedWords[cword]) break;
                }
                else break;// current word not in expected list bail
            }
            
            if (j == words.size()) vret.push_back(i);
        }
                
        return vret;
    }
};