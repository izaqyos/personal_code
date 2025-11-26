class Solution {
public:
    bool isPowerOfFour(int num) {
        if ((num & (num-1)) == 0 )
        {
            do
            {
                if (num == 4) return true;
                if (num < 4) return false;
            }
            while (num = num >>2);
        }
        else
        {
        return false;
        }
        return false;
    }
};