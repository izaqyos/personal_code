class Solution {
public:
    bool isMatch(string s, string p) {
        bool bMatch = false;
        
        int i=0;//s idx
        
        int j=0;//p idx
        
        //cout<<"i: "<<i<<", s["<<i<<"]: "<<s[i]<<", j: "<<j<<", p["<<j<<"]: "<<p[j]<<endl;
        while (true)
        {
         //   cout<<"i: "<<i<<", s["<<i<<"]: "<<s[i]<<", j: "<<j<<", p["<<j<<"]: "<<p[j]<<endl;
                if (p[j] == '*' )
                {
                   // cout<<"found *"<<endl;
                    if (j==0) //illegal
                    {
                        return bMatch;
                    }
                    else 
                    {
                        char prev = p[j-1];
                        while (prev == s[i]) ++i; //greedy match - eat as much as you can or nothing (* - 0 or more matches)
                        if (i== s.size()   && (j == p.size()) ) return true;
                        else ++j;
                    }
                }
                else if (p[j] == '.' )
                {
                    //cout<<"found ."<<endl;
                    ++j;
                    ++i;
                }
                else
                {
                   // cout<<"found regular char"<<endl;
                    if ( (j == p.size() - 1)  )
                    {
                     //   cout<<"j at last pos"<<endl;
                        if (s[i] == p[j])
                        {
                            if (i == s.size()-1) return true;
                            else return false;
                        }
                        else j =0;
                        
                    }
                    else if ( (p[j+1]) == '*'  ) ++j; // a* could be 0 or more - will be handled in next iteration
                    else if (s[i] == p[j])
                    {
                        //cout<<"Found literal match, i: "<<i<<", s["<<i<<"]: "<<s[i]<<", j: "<<j<<", p["<<j<<"]: "<<p[j]<<endl;
                        ++j;
                        ++i;
                    }
                    else
                    {
                      //  cout<<"Didn't find literal match, i: "<<i<<", s["<<i<<"]: "<<s[i]<<", j: "<<j<<", p["<<j<<"]: "<<p[j]<<endl;
                        ++i;
                        j=0;
                    }
                }
              //  ++j;
              if (i == s.size())
              {
                  if (j == p.size()) return true;
              }
              else
              {
                  if (j == p.size()) return false;
              }
              
               if (j == p.size())
              {
                  if (i == s.size()) return true;
              }
              else
              {
                  if (i == s.size()) return false;
              }
            }
        
        
        
        return bMatch;
    }
};