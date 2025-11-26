class Solution {
public:
    bool isMatch(string s, string p) {
        //dp solution
        
        vector< vector<bool> > match(s.length()+1, vector<bool>(p.length()+1, false));// s.len()+1 X p.len()+1 matrix, init to false
        // match(0,j) row and match (i,0) column all false since empty s match non empty p and vice versa
        // exception match(0,0) true since empty string match empty pattern
        match[0][0] = true;
        
        
        //Now match(i,j) value means s0...s(j-1) match p0...p(j-1) that's why match( s.length()+1, p.length()+1) is final result
        // match(i,j) can be calculated from match(i-1,j-1) if p(j-1) is char or '.' 
        //                       [non empty]  [ based on previos...]   [exact char match]    [. match all ]
        //then match(i,j) =   ( (i>0)   &&    match(i-1,j-1)     &&  ( (p[j-1] == s[i-1]) || (p[i-1] =='.')))
        //
        //                                              [ zero match]        [non empty]  [at least one match   or '.'   ]
        // else (p[j-1] == '*') then match = ( (j>1) && ( (match(i,j-2)) || ( (i>0) && ((s[i-1] == p[j-2]) ||(p[j-2]=='.'))   // )
        
        
        for (int i=0; i< s.length()+1; ++i)
        {
            for (int j=1; j< p.length()+1; ++j) // start from 2nd char but look back
            {
               // cout<<"i: "<<i<<", j:"<<j<<endl;
                if (p[j-1] == '*')
                {
                    //cout<<"prev is *"<<endl;
                   match[i][j] = ( (j>1) && ( (match[i][j-2]) || ( (i>0) && ( match[i-1][j]&& ((s[i-1] == p[j-2]) ||(p[j-2]=='.'))) ) ) ); 
                }
                else //. or char
                {
                   // cout<<"prev is . or char"<<endl;
                    match[i][j] =   ( (i>0) && ( match[i-1][j-1] &&  ( (p[j-1] == s[i-1]) || (p[j-1] =='.')) ) );
                }
                //cout<<"match: "<<match[i][j]<<endl;
            }
        }
        
        return match[ s.length()][p.length()];
    }
};