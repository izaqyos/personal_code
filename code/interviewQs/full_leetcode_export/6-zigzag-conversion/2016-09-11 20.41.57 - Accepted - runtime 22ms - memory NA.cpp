class Solution {
public:
/**
 * 
 pattern:
         0   1       2      3 ..         n = numRows
 0       s1                         S2n-1        
 1       s2                 S2n-2   S2n            
 2
 .
 .                  Sn+2
 .           Sn+1
 n       Sn
 * 
 * */
    string convert(string s, int numRows) {
        if( numRows<=1 ) return s;
        vector<string> lines(numRows);
        int row=0; //row - which string to add to 
        int inc=-1; 
        for(int i=0; i<s.size(); ++i){
            // Start adding to string row by row
            // When i is multiplication of (numRows-1) change direction - so 1st decreasing
            // row to get zigzag effect every time at turning point
            // Then increasing and vice versa 
            if(i%(numRows-1)==0) inc *= -1;
            lines[row].push_back(s[i]);
            row += inc;
        }
        string ret;
        for(const auto& line:lines){
            ret += line;
        }
        return ret;
    }
};