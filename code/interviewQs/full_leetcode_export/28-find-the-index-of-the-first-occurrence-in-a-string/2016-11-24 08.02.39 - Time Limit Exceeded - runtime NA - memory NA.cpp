class Solution {
public:
    int strStr(string haystack, string needle) {
     
     if ( (haystack.size() == 0) && (needle.size() == 0) ) return 0;
     if (needle.size() == 0) return 0;
     
     int i = 0;
     while (i<haystack.size())
     {
         
        for (int j=0; j<needle.size();++j)
        {
            //cout<<"i: "<<i<<", hay["<<i+j<<"]: "<<haystack[i+j]<<", j:"<<j<<", needle["<<j<<"]: "<<needle[j]<<endl;
            if (haystack[i+j] != needle[j]) break;
            if ( j == (needle.size()-1)) return i;
            
        }
         ++i;
    
     }
     
     return -1;
    }
};