class Solution {
public:
    int divide(int dividend, int divisor) {
        if (divisor == 0 ) return INT_MAX;
        if (divisor == 1 ) return dividend;
        int ret =0;
        
        while ( dividend >= divisor)
        {
            dividend-=divisor;
            ret++;
        }
        
        return ret;
    }
};