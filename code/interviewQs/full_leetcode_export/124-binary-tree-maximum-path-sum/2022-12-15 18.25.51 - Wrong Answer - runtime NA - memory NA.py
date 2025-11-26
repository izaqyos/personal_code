
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right


class Solution:
    def calc_BTMPS(self, root):
        if not root:
            return -9999
        if not root.left and not root.right:
            return root.val
        BTMPS_L = self.calc_BTMPS(root.left)
        BTMPS_R = self.calc_BTMPS(root.right)
        return max(BTMPS_L, BTMPS_R, root.val, BTMPS_L+BTMPS_R+root.val, BTMPS_L+root.val, BTMPS_R+root.val)

    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        return self.calc_BTMPS(root)
