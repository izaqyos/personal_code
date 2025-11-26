class Solution {
public:
    double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
        if(nums1.size() > nums2.size()) nums1.swap(nums2);
        int itotalsize = nums1.size()+nums2.size(), imiddle = (itotalsize-1)/2;
        int ileft = 0, iright = nums1.size()-1;// indexes to left and right of search range
        while(ileft <= iright) {
            int imiddle1 = ileft+((iright-ileft)>>1), imiddle2 = imiddle-imiddle1;
            if(nums1[imiddle1] < nums2[imiddle2]) ileft = imiddle1+1;//take the higher (right) part of nums1 to search
            else iright = imiddle1-1;//take the lower (left) part of nums1 to search
        }
        int imedian1 = max(ileft>0? nums1[iright]:INT_MIN, imiddle-ileft<nums2.size()? nums2[imiddle-ileft]:INT_MIN);
        if(itotalsize&1) return imedian1;
        int imedian2 = min(ileft<nums1.size()? nums1[ileft]:INT_MAX, imiddle-ileft+1<nums2.size()? nums2[imiddle-iright]:INT_MAX);
        return (imedian1+imedian2)/2.0;
    }
};