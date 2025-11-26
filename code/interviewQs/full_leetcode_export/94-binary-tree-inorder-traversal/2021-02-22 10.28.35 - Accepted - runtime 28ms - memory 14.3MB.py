# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def inorderTraversal(self, root):
        ret = []
        return self.inorderTraversalRecursive(root, ret)

    def inorderTraversalRecursive(self, root, ret):
        if root:
            self.inorderTraversalRecursive(root.left, ret)
            ret.append(root.val)
            self.inorderTraversalRecursive(root.right, ret)
            return ret
