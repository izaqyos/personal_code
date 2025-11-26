class Solution {
public:
    int strStr(string haystack, string needle) {
     
     if ( (haystack.size() == 0) && (needle.size() == 0) ) return 0;
     if (needle.size() == 0) return 0;
     
     int iPartial = 0;
     for (int i=0; i<haystack.size();++i)
     {
         
         if (haystack[i] == needle[iPartial])
         {
             if(iPartial == needle.size()-1) return true;
             else iPartial++;
         }
         else iPartial = 0;
     }
     
     return -1;
    }
};