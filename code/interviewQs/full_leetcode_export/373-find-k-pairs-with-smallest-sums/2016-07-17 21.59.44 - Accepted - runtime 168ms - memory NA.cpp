   //could just be bool comp (const pair<int, int>& l, const pair<int, int>& r) but I wanted to play w/ auto ret type
   //Note that in C++ 14 no need for decltype part as auto deduce ret type works 
    auto comp (const pair<int, int>& l, const pair<int, int>& r) -> decltype ((l.first+l.second) > (r.first+r.second))
    {
        return ((l.first+l.second) > (r.first+r.second));
    }


class Solution {
public:
    
    vector<pair<int, int>> kSmallestPairs(vector<int>& nums1, vector<int>& nums2, int k) {
        
        // use min_heap iterate all pairs and push to heap, copy K min elems from heap to res...
         vector<pair<int, int>> vRes;
         vector<pair<int, int>> vHeap;
         
         unsigned int n1idx = 0;
         unsigned int n2idx = 0;
         vRes.clear();
         vHeap.clear();
         make_heap(vHeap.begin(), vHeap.end(), comp);
         
         if ( (nums1.empty()) || (nums2.empty()) || (k <= 0)  ) return vRes;
         
         for (unsigned int i =0; i<nums1.size(); ++i)
         {
             for (unsigned int j =0; j<nums2.size(); ++j)
             {
                vHeap.push_back( make_pair(nums1[i], nums2[j]));
                push_heap(vHeap.begin(), vHeap.end(), comp);
             }
         }
         for (unsigned int i=0;(i<k && (i<(nums1.size()*nums2.size())) ) ;++i)
         {
             vRes.push_back(vHeap.front());
             pop_heap(vHeap.begin(), vHeap.end(), comp);
             vHeap.pop_back();
         }
         return vRes;
    }
};