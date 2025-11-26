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
        if ( (root == NULL) || ((root->right == NULL)  && (root->left == NULL) ) ) return;
        
        //idea, flatten left set root->right=leftpr
        // then point last left node to first right node, then flatten right
        
        //TreeNode * leftptr = root->left;
        TreeNode * rightptr = root->right;
        if (root->left != NULL)
        {
            flatten(root->left);
            TreeNode * ptr = root->left;
            while  (ptr->right !=NULL ) ptr = ptr->right;
            ptr->right = root->right;
            root->right = root->left;
            root->left = NULL;    
        }
        
        flatten(rightptr);
        
    }
};