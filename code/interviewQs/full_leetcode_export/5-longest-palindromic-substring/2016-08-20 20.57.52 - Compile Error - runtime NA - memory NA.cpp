class Solution {
public:
    string longestPalindrome(string s) {
        if (s.empty()|| s.size()==1) return s;
        
        // DP solution, keet matrix s.size()Xs.size() where (i,j) holds True/False whether s[i]..[j] is palindrom
        // so, compare s[i] to s[j] if not equal mark False
        // if equal check s[i-1][j-1] and set same value
        // do two first runs on i==j (diagonal ) all True
        // also j=i=1 and i=j=1 (length two)
        
        int len=1;
        int max_len=1;
        string sret= s.substr(0,1);  //hold longest palindrom
        vector< vector<bool> > PaliMatrix(s.size(), vector<bool>(s.size(),false));
        for (int i=0; i < s.size();++i)
        {
            PaliMatrix[i][i] = true; //len string is pali
            if (i+1< s.size())
            {
                if (s[i] == s[i+1])
                {
                    PaliMatrix[i][i+1] = true; //len 2 string found 2 be pali
                    if (max_len<2) sret=s.substr(i,2);
                }
                else PaliMatrix[i][i+1] = false;
            }
            
            int j=i;
            len =1;
            while (j+1<s.size() && (s[j]==s[j+1])) //eat same chars substring
            {
                len++;
                if (len>max_len) 
                {
                //    cout<<"same char len "<<len<<endl;
                    max_len=len;
                    PaliMatrix[i][j+1] = true; //same char string from i to j+1 is pali
                    sret=s.substr(i,j+1);
              //      cout<<"longest pali: "<<sret<<endl;
                    
                }
                ++j;
            }
        }
        
        len=max_len;
        while (len<=s.size())
        {
            //cout<<"checking substrs of len "<<len<<endl;
            for (int i=0; i+len <= s.size();++i)
            {
                if (s[i] == s[i+len-1]) 
                {
                    if (PaliMatrix[i+1][i+len-2] )
                    {
                        PaliMatrix[i][i+len-1] = true;//edges are pali + inner substr is pali
                        sret=s.substr(i,len);
                    }
                    else
                    {
                        PaliMatrix[i][i+len-1] = false;
                    }
                }
                else
                {
                    PaliMatrix[i][i+len-1] = false;
                }
            }
            ++len;
        }
        
        return sret;
    }
};