/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
#include <queue>

class Solution {
public:
    bool isSameTree(TreeNode* p, TreeNode* q) {
        queue<TreeNode *> qp, qq;
        qp.push(p);
        qq.push(q);
        while ((! qp.empty()) && (! qq.empty()) ) {
            TreeNode* qp_cur = qp.front();
            TreeNode* qq_cur = qq.front();
            qp.pop();
            qq.pop();

            if ((qp_cur and !qq_cur) || (qq_cur and !qp_cur))
            {
                return false;
            }
            if (qp_cur && qq_cur)
            {
                if ( qp_cur->val != qq_cur->val ){
                    return false;
                }
                qp.push(qp_cur->right);
                qp.push(qp_cur->left);
                qq.push(qq_cur->right);
                qq.push(qq_cur->left);
            }
        }
        if (!qp.empty() || !qq.empty()) {
            return false;
        }
        return true;
    }
};

