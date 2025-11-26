class Solution {
 public:
  vector<int> findMinHeightTrees(int n, vector<pair<int, int>>& edges) {
    
    vector <unordered_set <int> > vsGraph(n);
    for (auto edge : edges)
    {
        vsGraph[edge.first].insert(edge.second);
        vsGraph[edge.second].insert(edge.first);
    }
    vector<int> vRet;
    if (n == 1) 
    {
        vRet.push_back(0);
        return vRet;
    }
    
    //BFS buttom up, MHTs are "inner most root" nodes
    for (int i =0; i < vsGraph.size(); ++i)
    {
        if (vsGraph[i].size() == 1) vRet.push_back(i);
    }
    
    while (true)
    {
        vector<int> vQueue;
        for (auto node : vRet )
        {
            for(auto adjacent : vsGraph[node] )
            {
                vsGraph[adjacent].erase(node);
                if (vsGraph[adjacent].size() == 1) vQueue.push_back(adjacent);//we processed all adjacent neighbors so add it to Q
                
            }
        }
        if (vQueue.empty()) return vRet; // all nodes processed
        vRet = vQueue ; // next "distance level" to search
    }
  }
};