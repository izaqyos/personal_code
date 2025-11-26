class Solution {
public:
    bool isPowerOfFour(int num) {
        while ((num & (num-1)) == 0 )
        {
            num = num >>2;
            if (num & 1) return true; 
        }
        
        return false;
        
    }
};