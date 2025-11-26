class Solution {
public:
    bool isValidSerialization(string preorder) {
        if (0 <= (preorder[0] -'0') <=9)
        {
            int idx = 1;  
            bool runningBranch = true;
            while (idx <= preorder.length())
            {
                if (preorder[idx] == ',') idx++;
                if (runningBranch)
                {
                    if (preorder[idx] == '#') runningBranch = false;
                }
                else
                {
                    if (preorder[idx] == '#') return false; //not valid # as root of sub branch
                    else runningBranch = true; // digit or , no need check
                }
                idx++;
            }
        }
        else
        {
            return false;
        }
        return true;
    }
};