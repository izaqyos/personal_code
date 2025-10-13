#include <string>
#include <iostream>
#include <vector>

using namespace std;

class Solution {
public:

    bool bdebug = true;

            //params: substr to match, current (not matched) words, match indices vector, match to add when words has one word,  s - string to cont. matches. 
    bool checkMatch(string word, vector<string> & words, vector<int>& vret,int match_idx,string s) 
    {
        if (bdebug) cout<<"checkMatch() called to match "<<word<<endl<<"Remaining str: "<<s<<endl;
        
        if (words.empty() ) return false;
        
        int wlen = words[0].length();
        
        for (vector<string>::iterator it = words.begin(); it != words.end(); ++it)
        {
            if ( (*it) == word)
            {
                if (bdebug) cout<<"checkMatch() matched "<<word<<endl;
                words.erase(it);
                if (bdebug) cout<<"checkMatch() erased "<<word<<", words left "<<words.size()<<endl;
                if (words.empty() ) 
                {
                    if (bdebug) cout<<"checkMatch() found full match. returning"<<endl;
                    vret.push_back(match_idx);
                    cout<<"YYYY"<<endl;
                    return true;
                }
                
                
                if (s.size() >=wlen)
                {
                    checkMatch(s.substr(0,wlen), words, vret, match_idx, s.substr(wlen, s.size()));    
                }
                else return false;
                
                
            }
        }
        
        return false;
    }
    
    vector<int> findSubstring(string s, vector<string>& words) {
        vector<int> vret;
        
        if (s.length() == 0 )
        {
            if (words.empty() ) vret.push_back(0);
            return vret;
        }
        
        
        int slen = s.length();
        int wlen = words[0].length();
        
        if (words.empty()   || (wlen > slen )) return vret;
        
        for (int i=0; i<= slen-wlen; ++i)
        {
            if (bdebug) cout<<"crawling index: "<<i<<endl;
            vector<string> words_copy = words;
            if (! checkMatch(s.substr(i,wlen), words_copy, vret,i,s.substr(i+wlen, s.size())) ) 
            {
                if (bdebug) cout<<"no match at index: "<<i<<endl;
            }
            else 
            {
                if (bdebug) cout<<"found full match at index: "<<i<<endl;
            }
            
        }
        
        
        return vret;
    }
};

int main()
{

	string s("barfoothefoobarman");
	vector<string> words = {"foo","bar"};
	Solution sol;
	sol.findSubstring(s,words);
}

