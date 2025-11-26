 class Solution {
public:
    int trap(vector<int>& height) {
        
        
        //3rd idea
        //scan from right and left simuletanously 
        //keep values of max left and right indices
        // water will accumulate up to min of the two
        // after taking water amount from given side move it index +1
        int res = 0;
        if (height.empty()) return res;
        
        int n=height.size();
        int li=0,ri=n-1,lmax=0,rmax=0; // left and right indices
        
        
        while(li<=ri) //iterate until left index passes right
        {
            if(height[li]<=height[ri]) //left is minimum
            {
                if (height[li] > lmax) lmax = height[li];
                else res+=lmax - height[li];
                li++; // we summed this columns water. move on
            }
            else //right is minimum
            {
                if (height[ri] > rmax) rmax = height[ri];
                else res+=rmax - height[ri];
                ri--; // we summed this columns water. move on
            }
        }
        
        
        
        

        return res;

    }
};