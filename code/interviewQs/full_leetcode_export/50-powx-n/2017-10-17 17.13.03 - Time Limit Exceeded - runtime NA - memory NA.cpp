class Solution {
public:
    double myPow(double x, int n) {
        
        if (n == 0) return 1;
        
        int sign = 1;
        if (n<0) sign =-1;
        
        n*=sign;
        
        
        double res = 1;
        while (n>0) 
        {
            res *=x;
            n--;
        }
        
        return (sign==1)? res : 1/res;
    }
};