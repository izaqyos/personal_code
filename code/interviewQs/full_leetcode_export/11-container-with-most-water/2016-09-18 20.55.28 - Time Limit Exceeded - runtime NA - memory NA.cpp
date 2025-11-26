class Solution {
public:
    int maxArea(vector<int>& height) {
        if ((height.empty()) || (height.size() == 1 )) return 0;
        
        int maxA=0;
        int tempA=0;
        for (int i=0;i<height.size(); ++i)
        {
            for (int j=i+1;j<height.size(); ++j)
            {
                tempA=(j-i)*(min(height[i],height[j])) ;
                if (tempA>maxA) maxA=tempA;
            }
        }
        return maxA;
    }
};