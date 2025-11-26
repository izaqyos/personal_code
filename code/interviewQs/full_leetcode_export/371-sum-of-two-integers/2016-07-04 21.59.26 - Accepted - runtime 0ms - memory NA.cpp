class Solution {
public:
    int getSum(int a, int b) {
        
        int iC=0;//carry over
        int iRet = 0;
        
        if  (a==0) return b;
        if  (b==0) return a;
        
        while (b !=0)
        {
            
            iRet = a^b; // handle 0,1 1,0 and 0,0 bit addition
            iC = (a&b)<<1; // handle 1,1 bit addition so 0 and 1 carry over;
            b = iC;
            a = iRet;
        }
        
        return iRet;
    }
};