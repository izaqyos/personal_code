class Solution {
public:
    int maxArea(vector<int>& height) {
        
        int l = 0;
        int r = height.size()-1; // left and right indices
        
        int maxA = 0;
        
        while (l<r)
        {
            int minH = min(height[l], height[r]);// minH determins container height so Volume(l,r)= minH*(r-l) 
            maxA = max (maxA ,  minH*(r-l)); // either previous max or V(l,r) encountered is new max
            while ((l<r) && (height[l]<=minH) ) l++; // since looking for narrower containers must be higher than minH
                                                     // to have possibly more volume
                                                     
            while ((l<r) && (height[r]<=minH) ) r--;
        
        }
        return maxA;
    }
};