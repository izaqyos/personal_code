class Solution {
public:

    bool bD = false;
    
    int search(vector<int>& nums, int target) {
        
        //my idea. binary search w/ twist
        // so sorted array a1<=a2<=a3...<=an was rotated to something like
        //                 a(n-r+1)<=a(n-r+2)<=...<=a(r-1)<=a(r)<=... where r is rotation degree, ex, for degree 2 we have
        //                 a(n-1)<=a(n)<=a1<=a2<=...<=a(n-3)
        // once this is established we can find lowest element and binary search 
        // with a twist. The middle element index should be shifted the same as smallest element position -1
        
        int n = nums.size();
        
        if (n == 0 ) return -1;
        
        int m=0,l=0,h=n-1;
        while (l<h)
        {
            
            m = l+ (h-l)/2;
            if (bD) cout<<"m: "<<m<<endl;
            if (nums[l] <= nums[h])
            {
                h=m;
            }
            else
            {
                if (m +1 < n) l=m+1;
            }
        }
        
        if (bD) cout<<"Smallest nums["<<l<<"]="<<nums[l]<<endl;
        
        int shift = l;
        l=0;
        h=n-1;
        int rm=0;
        
        
        while ( l <= h)
        {
            
            m = l +(h-l)/2;
            rm = (m+shift-1)%n;
            if (bD) cout<<"l="<<l<<", h="<<h<<", m="<<m<<", rm="<<rm<<", nums["<<rm<<"]="<<nums[rm]<<endl;
            
            if (nums[rm] == target) return rm;
            else if (nums[rm] < target)
            {
                l = m+1;
            }
            else
            {
                h = m-1;
            }
            
        }
        return -1;
    }
};