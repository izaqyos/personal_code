class Solution {
public:
    bool isMatch(string s, string p) {
        
        bool bD = true;
        
        int iStar = -1; //index to star
        int iS = 0; //index to current position in s
        int iP = 0; //index to current position in p
        int iSS = 0; //copy of index to current position in s
        while (iS< s.length() && iP<p.length()){
            //advancing both pointers when (both characters match) or ('?' found in pattern)
            //note that *p will not advance beyond its length 
            if ((p[iP]=='?')||(p[iP]==s[iS])){iS++;iP++;continue;} 

            // * found in pattern, track index of *, only advancing pattern pointer 
            //this way we may skip consecutive * but either way get to end of P or next non star...
            // iSS copy is for backtracking, we may have partial match so iS will advance but then fail
            // so we let the star eat the whole pattern starting from last match
            if (p[iP]=='*'){iStar=iP++; iSS=iS;continue;} 

            //current characters didn't match, last pattern pointer was *, current pattern pointer is not *
            //only advancing pattern pointer
            if (iStar>=0){ iP = iStar+1; iS=++iSS;continue;} 

           //current pattern pointer is not star, last patter pointer was not *
           //characters do not match
            return false;
        }

       //s exhausted. check for remaining characters in pattern to be * only
        while (iP<p.length() && p[iP]=='*'){iP++;}

        return iP==p.length(); 
    }
};