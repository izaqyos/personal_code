class Solution {
public:
    bool canJump(vector<int>& nums) {
        
        int n = nums.size();
        if (n== 0) return true; //arbitrery
       // if (nums[0]<=0) return false;
        
        //DP solution jumpLens[i], how much jump "left" offset left after i. Maximum from all possible previous values. including self
        // 0 value means unreachable.
        //If at any i, we get 0 offset we mark until n-1 as 0. 
        // return (jumpLens[n-1] >0 ) 
        vector <int> jumpLens(n,0);
        int jumpLeft = 0;
        jumpLens[0] = nums[0];
        jumpLeft = nums[0];
       // if (jumpLeft <=0 ) return false;
        for (int i=1;i<n;++i)
        {
            if (jumpLeft <=0) return false;
            jumpLeft--; //since we advanced by 1
            jumpLeft=max( jumpLeft, nums[i]);
            if ((jumpLeft <=0) && (i<n-1) ) return false;
        }
        
        return true;
    }
};