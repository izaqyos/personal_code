class Solution {
public:
    bool isPowerOfFour(int num) {
        int masks[16];
        masks[0]=1;
        for (int i =1; i<16;++i)
        {
            masks[i] = masks[i-1] << 2;
        }
        
        for (int i =0; i<16;++i)
        {
            if (num == masks[i]) return true;
        }
        return false;
    }
};
