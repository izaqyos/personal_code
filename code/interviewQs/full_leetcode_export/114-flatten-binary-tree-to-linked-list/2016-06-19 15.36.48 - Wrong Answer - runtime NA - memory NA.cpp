/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode(int x) : val(x), left(NULL), right(NULL) {}
 * };
 */
class Solution {
public:
    void flatten(TreeNode* root) {
        TreeNode* A = root;
          if ((A == NULL)    ) return ;
    if ( ((A->left) == NULL) && ((A->right) == NULL) ) return;
    
    bool prn = true;
    
    if (prn) cout<<"flatten "<<(A->val)<<endl;
    if (A->left == NULL) 
    {
        if (prn) cout<<"no left, flatten right..."<<endl;
        flatten(A->right);
    }
    
    TreeNode *pCur = NULL;
    TreeNode *pTmp = NULL;
    if (A->left) 
    {
       if (prn) cout<<"flatten left "<<(A->left->val)<<endl;
       pCur = A->left;
       flatten(A->left);
       pCur = A->left;
        while (pCur->right != NULL)
        {
            pCur = pCur->right;
        }
        if (prn) cout<<"set right most node of left tree ( "<<(pCur->val)<<") to point to right node ("<<(A->right ? (A->right->val):0)<<endl;
        pCur->right = A->right;
        A->left = NULL;
        A->right = pCur;
        //flatten(A->right);
    }
    
    
    }
};