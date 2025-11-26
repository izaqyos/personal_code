class Solution {



public:
class Node
{
    public:
    int val;
    vector<Node *> vNeigh;
};

class Tree
{
    public:
    vector<Node *> vNodes;
    void addEdge(pair<int,int> & edge)
    {
        Node * p1st = NULL;
        Node * p2nd = NULL;
        
        cout<<"addEdge() adding pair <"<<edge.first<<","<<edge.second<<">\n";
        bool isEdgeInTree = false;
        for ( vector<Node *>::iterator it1st = vNodes.begin(); it1st != vNodes.end(); ++it1st)
        {
            if ( ((*it1st)->val == edge.first ) )
            {
                cout<<"addEdge() found node "<<edge.first<<"\n";
                p1st = *it1st;
                for(vector<Node *>::iterator it = ((*it1st)->vNeigh).begin(); it != ((*it1st)->vNeigh).end(); ++it )
                {
                    if ( ((*it)->val == edge.second ) )
                    {
                        isEdgeInTree = true;    
                        break;
                    }
                }
            }
            
            if ( ((*it1st)->val == edge.second ) )
            {
                cout<<"addEdge() found node "<<edge.second <<"\n";
                p2nd = *it1st;
                for(vector<Node *>::iterator it = ((*it1st)->vNeigh).begin(); it != ((*it1st)->vNeigh).end(); ++it )
                {
                    if ( ((*it)->val == edge.first ) )
                    {
                        isEdgeInTree = true;           
                        break;
                    }
                }
            }
        }
        
        if (! isEdgeInTree)
        {
            cout<<"addEdge() adding new edge\n";
            if (! p1st) 
            {
                p1st = new Node();
                p1st->val = edge.first;
                vNodes.push_back(p1st);
            }
            
            if (! p2nd) 
            {
                p2nd = new Node();
                p2nd->val = edge.second;
                vNodes.push_back(p2nd);
            }
            
            vector<Node *>::iterator it = find(p1st->vNeigh.begin(), p1st->vNeigh.end(), p2nd);
            if (it == p1st->vNeigh.end())
            {
                cout<<"addEdge() adding link "<<(p1st->val)<<"-->"<<(p2nd->val)<<"\n";
                p1st->vNeigh.push_back(p2nd);
            }
            
            
            it = find(p2nd->vNeigh.begin(), p2nd->vNeigh.end(), p1st);
            if (it == p2nd->vNeigh.end())
            {
                cout<<"addEdge() adding link "<<p2nd->val<<"-->"<<p1st->val<<"\n";
                p2nd->vNeigh.push_back(p1st);
            }
        }
    }
    
    void buildTree(vector<pair<int, int>>& edges)
    {
        for (vector<pair<int, int>>::iterator it = edges.begin(); it!=edges.end();++it)
        {
            addEdge(*it);
        }
    }
    
    int calcMHT(Node * pEntryNode, Node * pParent)
    {
        cout<<"calcMHT() for "<<pEntryNode->val<<"\n";
        int maxMHT = 0;
        int MHT = 0;
        for(vector<Node *>::iterator it = pEntryNode->vNeigh.begin(); it != pEntryNode->vNeigh.end();++it )
        {
            if ( (*it) != pParent)
            {
            MHT = calcMHT(*it, pEntryNode);
            if (MHT>maxMHT) maxMHT=MHT;    
            }
            
        }
        cout<<"calcMHT() MHT for "<<pEntryNode->val<<"is "<<maxMHT+1<<"\n";
        return maxMHT+1;
    }
};

static bool myComp(pair<int, int> p1, pair<int, int> p2)
{
    return (p1.second < p2.second);
}

    vector<int> findMinHeightTrees(int n, vector<pair<int, int>>& edges) {
        //build tree
        Tree tree;
        tree.buildTree(edges);
        
        vector < pair<int,int> > vRes;
        //loop nodes
        for(vector<Node *>::iterator it = tree.vNodes.begin(); it !=tree.vNodes.end();++it )
        {
            int iCurr = (*it)->val;
            cout<<"scanning node "<<iCurr<<"\n";
            //for each node call recursive function, MHT. if lead ret. 0 otherwhise Max(MHT(sons))
            int iHeight = tree.calcMHT(*it, NULL);
            vRes.push_back( make_pair(iCurr, iHeight));
        }
        
        //Add to vector of pairs node val and MHT, then sort w/ special comp (use MHT)
        sort(vRes.begin(), vRes.end(), myComp);
        
        vector<int> vFinalRes;
        int i = 0;
        vFinalRes.push_back(vRes[i].first);
        ++i;
        while (i<vRes.size() && (vRes[i].second == vRes[0].second) ) vFinalRes.push_back(vRes[i].first);
        
        return vFinalRes;
    }
};