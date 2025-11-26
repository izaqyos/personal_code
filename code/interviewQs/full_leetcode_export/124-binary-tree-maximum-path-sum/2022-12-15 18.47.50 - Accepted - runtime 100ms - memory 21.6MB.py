
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def calc_BTMPS(self, root):
        if not root:
            return 0, float('-inf')  # return 2 values, max path from root and the answer (max path sum from this node taking into account both left and right sub trees)
        left_MPFR, left_MPS = self.calc_BTMPS(root.left)
        right_MPFR, right_MPS = self.calc_BTMPS(root.right)
        return root.val+max(left_MPFR, right_MPFR, 0), max(left_MPS, right_MPS, max(left_MPFR,0)+max(right_MPFR,0)+root.val)

    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        _, res = self.calc_BTMPS(root)
        return res





