# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        if (not root) or (not root.left and not root.right) :
            return 0
        ldeep=0
        if root.left:
            ldeep = self.deepest(root.left)+1 
        rdeep=0
        if root.right:
            rdeep = self.deepest(root.right)+1
        return max(rdeep+ldeep, self.diameterOfBinaryTree(root.left), self.diameterOfBinaryTree(root.right))
        
    
    def deepest(self, root: Optional[TreeNode]) -> int:
        if (not root) or (not root.left and not root.right) :
            return 0
        return max(self.deepest(root.left), self.deepest(root.right)) +1
    
    