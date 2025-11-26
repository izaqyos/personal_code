class Solution {
public:
    bool isValidSudoku(vector<vector<char>>& board) {
        
        //1st idea, scan once board. each character save in 3 sections of map.
        // 1st section represents rows. r1 = 0-9, r2 = 10-19,...,r9=80-89
        // 2nd section represents columns. c1 = 100-109, c2 = 110-119,...,c9=180-189
        // 3rd section represents 3X3 inner quads. q1 = 2000,2003,2006,2030,2033,2036,2060,2063,2066
        //                                         q2 = 2009,2012,2015,2039,2042,2045,2069,2072,2075
        //                                          ...
        //                                          q9= 2098,2101,2103,2228,2231,2234,2258,2261,2264
        // how to calculate key:
        // for rows: Kr = 10*i +j
        // for columns: Cr = 100 +10*i +j
        // for quads: Qr = 2000 +30*i +3*j , note could have used any other calc, like 1000+10*i+j etc...
        
        // so. check 9X9, check valid chars 1-9 and .
        // add to map
        
        //1st idea, too much work. 2nd.
        // set char -> vector<pair<int,int>> 
        // scan once and add to set all coordinates of char
        // then for each char loop over coordinates. If same row return false, if same colums return false,
        // if same quad (Ifirst -Jfirst < 3) and (Isecond - Jsecond < 3) return false,
        
        int m = board.size();
        if (m != 9 ) return false;
        for (auto r : board)
        {
            if ( r.size() != 9) return false;
        }
        int n = board[0].size();
        
        unordered_map<char, vector<pair<int,int> > > chars;
        unordered_map<char, vector<pair<int,int> > >::iterator it;
        
        for (int i=0;i<m;++i)
        {
            for (int j=0;j<n;++j)
            {
                char c = board[i][j];
                if (c == '.') continue;
                if ( ( ( c - '0') < 1)  || ( ( c - '0') > 9)  ) //illegal char 
                    return false;
                    
                    
                it = chars.find(c);
                if (it == chars.end())
                {
                    //vector<pair<int,int> > vec = vector<pair<int,int> >(1, make_pair(i,j)); //old syntax
                    vector<pair<int,int> > vec = {{i,j}}; //new syntax
                    chars[c] = vec;
                }
                else
                {
                    chars[c].push_back(make_pair(i,j));
                }
                
            }
        }
        
        //for (const auto& [ k, v ] : chars) //C++17 syntax, not working here :(
        for (const auto & kv : chars) //in C++14 iterate key_pairs e.g. for (const auto & kv : chars) {kv.first;kv.second; 
        {
            
            for (int i=0; i<kv.second.size(); ++i)
            {
                for (int j=i+1; j<kv.second.size(); ++j)    
                {
                    int ir = kv.second[i].first; //i raw
                    int jr = kv.second[j].first; //j raw 
                    int ic = kv.second[i].second; //i column
                    int jc = kv.second[j].second; //j column
                    
                    if (ir == jr) return false; // row has 1-9 more than once
                    if (ic == jc) return false; // column has 1-9 more than once
                   //too simplistic. doesn't work. check any same char in 3X3 sub-box
                   // if ( ( abs(kv.second[i].first - kv.second[j].first) < 3 ) && ( abs(kv.second[i].second - kv.second[j].second) < 3 ) ) return false; // same sub-box
                   //correct check. scan specifically 9 sub-boxes
                   for (int k=0;k<3;++k) //raw offset
                   {
                       for(int l=0;l<3;++l) //column offset
                       {
                           if ( ( k*3 <= ir ) && (  ir < (k+1)*3 ) &&
                                  ( k*3 <= jr ) && (  jr < (k+1)*3 ) &&
                                  ( l*3 <= ic ) && (  ic < (l+1)*3 ) &&
                                  ( l*3 <= jc ) && (  jc < (l+1)*3 ) 
                                  )
                                  return false;
                       }
                   }
                }
            }
        }
        
        return true;
        
    }
};