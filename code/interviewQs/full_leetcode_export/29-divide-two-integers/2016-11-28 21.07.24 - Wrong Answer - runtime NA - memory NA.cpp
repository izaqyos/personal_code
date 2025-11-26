class Solution {
public:
    int divide(int dividend, int divisor) {
        if (divisor == 0 ) return INT_MAX;
        if (divisor == 1 ) return dividend;
        int ret =0;
        
        int abs_div = ( (divisor<0)?-1:1) *divisor; 
        int abs_dend = ( (dividend<0)?-1:1) *dividend; 
        
        while ( abs_dend >= abs_div)
        {
            abs_dend-=abs_div;
            ret++;
        }
        
        return ret*( (divisor<0)?-1:1)*( (dividend<0)?-1:1);
    }
};