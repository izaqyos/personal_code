class Solution {
public:
    string convert(string s, int numRows) {
        
        if (s.empty() || (numRows<=1) ) return s;
        
        vector<string> lines(numRows,"");
        
        int mi=0;//matrix indes
        
        
       for (int i=0; i<s.size(); i++,mi++)
       {
          // cout<<"s["<<i<<"]: "<<s[i]<<", mi: "<<mi<<endl;
           //fill even columns fully
           if ( (((mi/numRows)%2)&1)==0  )
           {
              // cout<<"fill even column"<<endl;
            lines[mi%numRows].push_back(s[i]);
           }
           else//fill odd columns only in odd rows
           {
               //cout<<"fill odd column"<<endl;
               if ( (mi%numRows)&1  )
               {
                   lines[mi%numRows].push_back(s[i]);
               }
               
               else //skip
               {
                   mi++;
                   lines[mi%numRows].push_back(s[i]);
               }
               
           }
           
       }
       
       
       ostream_iterator<string> sout(cout,"\n");
       std::copy(lines.begin(),lines.end(), sout);
       
       s.erase();
       for (auto str : lines)
       {
           s += str;
          // s += "\n";
       }
       return s;
       
       
    }
};