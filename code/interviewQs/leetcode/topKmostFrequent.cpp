class Solution {
public:
    vector<int> topKFrequent(vector<int>& nums, int k) {
        
        struct pairComp{
            bool operator() (const pair<int,int>& a, const pair<int,int>& b) const
            {
                return a.second < b.second;
              
            }
        };
        
        vector<int> vRet(k);
        vector< pair<int, int> > vHeap(nums.size()); // Freq, Num pairs
        map<int,int> mFreqs; //map num to freq
        make_heap(vHeap.begin(), vHeap.end(),pairComp());
        
        for (auto n : nums) //o(n)
        {
            mFreqs[n]++;
        }
        
        for (auto const & n : mFreqs) //(Ulog(n)) , where U is # of unique nums, worst case all unique U==n
        {
            pair<int, int> tPair(n.first, n.second );
            vHeap.push_back(tPair);
            push_heap(vHeap.begin(), vHeap.end(),pairComp());
        }
        
        for (int i=0; i<k;++i) //o(klog(n))
        {
            //cout<<"k "<<k<<", heap size"<<vHeap.size()<<endl;
            if (k<=vHeap.size())
            {
            vRet[i] = vHeap.front().first;
            //cout<<"The "<<i<<" most frequent num is "<<vRet[i]<<endl;
            pop_heap(vHeap.begin(), vHeap.end(),pairComp());
            vHeap.pop_back();
            }
        }
        return vRet;
    }
};
