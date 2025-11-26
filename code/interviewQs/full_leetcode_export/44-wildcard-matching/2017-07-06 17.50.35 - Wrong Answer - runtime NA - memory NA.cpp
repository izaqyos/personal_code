class Solution {
public:
    bool isMatch(string s, string p) {
       // bool res = false;
        
        bool bD = false;
        
        //DP solution
        //matches(n+1,m+1) matrix - matches(i,j) true IFF s(0..i) matches p(0..j)
        //at end return matches(s.length(),p.length())
        
        int n = s.length();
        int m = p.length();
        vector<vector<bool>> matches(n+1, vector<bool>(m+1, false) );
        
        if (bD) cout<<"Check match "<<s<<", of length "<<n<<", to "<<p<<", of length "<<m<<endl;
        matches[0][0] = true; //empty strings match
        
        for (int j=1;j<=m;++j) 
        {
            
            matches[0][j] = ( p[j-1] == '*'  && matches[0][j-1] ) ? true: false; // only consecutive * in pattern can match empty s 
            if (bD) cout<<"set value of matches["<<0<<"]["<<j<<"]="<<matches[0][j]<<endl;
        }
   //     for (int i=0;i<n;++i) matches(i,0) =  false; //empty pattern can't match non empty s... in comment since false is default val

        
        for (int i=0; i<=n;++i) // matches[i][j] corresponds to s[i-1] and p[j-1]...
        {
            for(int j=1;j<=m;++j) //start but always look back one char...  
            {
               // if (bD) cout<<"Determine value of matches["<<i<<"]["<<j<<"]"<<endl;
                if( p[j-1] != '*'  )
                {
                    
                    matches[i][j] = (i>0  &&   (matches[i-1][j-1]  &&( (p[j-1] == '?') || (p[j-1] == s[i-1] )) ) );
                    
                }
                else
                {
                    if ( i>0 )
                    {
                        if (j>1 && matches[i][j-1])
                        {
                            if (bD) cout<<"Found empty match at matches["<<i<<"]["<<j-1<<"]="<<matches[i][j-1]<<endl;
                            matches[i][j] =  matches[i][j-1] ;
                        }
                        
                        if ( (j==1) || matches[i-1][j-1]) //j=1 means P[0]=* 
                        {
                            if (bD) cout<<"Found * to 1 char match at matches["<<i-1<<"]["<<j-1<<"]="<<matches[i-1][j-1]<<endl;
                            matches[i][j] =  (j==1) || matches[i-1][j-1] ;
                        }
                    }
                    //matches[i][j] = ( (i>0) && (( j>1  && matches[i-1][j-2]) /* empty match * */ || ( matches[i-1][j-1] ) ) )/* * matches si-1*/;
                }    
                if (bD) cout<<"set value of matches["<<i<<"]["<<j<<"]="<<matches[i][j]<<endl;
                
            }
        }
        return matches[n][m];
        /*
        // recursive solution. too slow worst case O(n*m)
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
                    for(int j=i;j<=s.length();++j) //try 0 or more matches as many as s allows
                    {
                        if (bD) cout<<"recursive call to match "<< s.substr(j, string::npos) <<" with "<< p.substr(i+1, string::npos) <<endl;
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
        
        //s is exhausted. p should be as well, unless *
        for(auto c : p.substr(s.length(), string::npos))
        {
                    if( c != '*') return false;
        }
        return true;
        
        */
    }
};