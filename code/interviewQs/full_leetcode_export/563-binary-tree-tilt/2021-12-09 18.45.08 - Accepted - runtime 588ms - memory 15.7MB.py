class Solution:
    def sumTree(self, root):
        if not root:
            return 0
        sumTree = root.val + self.sumTree(root.left)+ self.sumTree(root.right)
        return sumTree

    def findTilt(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        return abs(self.sumTree(root.right) - self.sumTree(root.left)) + self.findTilt(root.left) + self.findTilt(root.right)
