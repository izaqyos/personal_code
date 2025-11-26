class Solution {
public:
    double myPow(double x, int n) {
        
        if (n == 0) return 1;
        
        
        if (n<0) 
        {
            n *=-1;
            x = 1/x; 
        }
        
        double res = 1;
        while (n>0) 
        {
            if (n&1) res *=x; //if ith bit is set multiply by x^(2^i)
            x*=x; //prepare for next bit 
            n>>=1; //proceed to next bit
        }
        
        return res ;
    }
};