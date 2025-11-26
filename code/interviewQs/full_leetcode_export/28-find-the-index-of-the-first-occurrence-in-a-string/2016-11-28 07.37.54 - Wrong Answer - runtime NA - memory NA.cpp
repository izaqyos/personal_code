class Solution {
public:
    int strStr(string haystack, string needle) {
     
     bool bDebug = true;
     //Boyer-Moore
     if ( (haystack.size() == 0) && (needle.size() == 0) ) return 0;
     if ( haystack.size() < needle.size() > 0) return -1;
     if (needle.size() == 0) return 0;
     
     int m = needle.size();
     int n = haystack.size();
     int alphaBetSize = 256;
     int badCharTable[alphaBetSize]; //bad char match shift table
     for (int i=0; i< alphaBetSize; ++i )
     {
         badCharTable[i] = -1;
     }
     for (int i=0; i<m;++i)
     {
         badCharTable[needle[i]] = i;
     }
     
     int shift = 0; // shift of needle in haystack
     while (shift < n-m) 
     {
         if (bDebug) cout<<"shift: "<<shift<<endl;
         int j=m-1; //index of needle char to be matched
        while ( (j>=0) && (haystack[shift+j]  == needle[j] )) j--;
        
        if (bDebug) cout<<"matched "<<m-j-1<<" out of "<<m<<endl;
        if (j<0) //if full match j ends up as -1
        {
            return shift;
            // In real Boyer-Moore we keep looking so shift while still has chance to find needle
            //shift += (shift < n-m) ? m-badCharTable[haystack[shift+m]] :1
            
        }
         
         else //no match, so shift until bad char in haystack is aligned w/ its last occurense in needle
         //if shift is 0 or -1 (not in needle) we shift by 1
            shift+= max(1,   j - badCharTable[haystack[shift+j]]);
    
     }
     
     return shift;
    }
};