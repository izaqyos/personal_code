class Solution {
public:
    string longestCommonPrefix(vector<string>& strs) {
        
        string sret="";
        char c;
        int i=0;
        //bool end=false;//one of strs is exhausted
        bool stop=false;//found longest common prefix
        
        if (strs.empty()) return sret;
        while (!stop)
        {
            
            for (int j=0; j<strs.size();++j)
            {
               cout<<"j: "<<j<<", i:"<<i<<endl;
               if (i< strs[j].size())
               {
                   if (j==0) c = strs[j][i];
                   else if (c != strs[j][i] ) stop=true;
                
               }
               else
               {
                   stop = true;
               }
               
            }
            ++i;
            if (stop) break;
            else sret+=c;
            cout<<"sret: "<<sret<<endl;

            
        }
        
        return sret;
        
    }
};