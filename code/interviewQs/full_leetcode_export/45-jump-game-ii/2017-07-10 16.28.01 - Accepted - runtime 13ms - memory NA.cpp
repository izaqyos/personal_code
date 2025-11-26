class Solution {
public:
    int jump(vector<int>& nums) {
        
        // consider nums as a graph, elements are vertices
        // values dictate edges, e.g. a[0]=k, means a[0]<->a[j] where 1<=j<=k
        // now run BFS, start at a[0], calculate max jump (k), process all nodes 
        // that are immediate neighboughrs of a[0], calculate next max jump
        // - the furthest can jump from a[j] 
        // stop when either 0 neighboughrs or next jump > n
        
        bool bd = false;
        
        int i=0,depth=0,mj=0,nmj=0; //iterator, graph depth, Max Jump, Next Max Jump
        int n= nums.size();
        if (n<=1) return 0;
        
        while( mj-i >= 0) //mj reaches i, meaning at least one node in next depth
        {
            if (bd) cout<<"i="<<i<<", mj="<<mj<<", depth="<<depth<<endl;
            depth++;
            for( ; i<=mj;++i)
            {
                nmj = max(nmj, i+nums[i]);
                if (bd) cout<<"i="<<i<<", nmj="<<nmj<<endl;
                if (nmj >= n-1) return depth;
            }
            
            mj = nmj;
        }
        
        return depth;
    }
};