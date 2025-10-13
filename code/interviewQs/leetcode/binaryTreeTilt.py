# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def sumTree(self, root):
        if not root:
            return 0
        sumTree = root.val + self.sumTree(root.left)+ self.sumTree(root.right)
        return sumTree

    def findTiltRec(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        return abs(self.sumTree(root.right) - self.sumTree(root.left)) + self.findTilt(root.left) + self.findTilt(root.right)

    
    sums = dict()
    tilts = dict()
    def sumTreeMem(self, root):
        if not root:
            return 0
        if root in self.sums:
            print(f"sum memo used for {root.val}")
            return self.sums[root]

        sumTree = root.val + self.sumTree(root.left)+ self.sumTree(root.right)
        self.sums[root] = sumTree
        return sumTree

    # memorization
    def findTilt(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        if root in self.tilts:
            print(f"tilt memo used for {root.val}")
            return self.tilts[root]

        tilt = abs(self.sumTreeMem(root.right) - self.sumTreeMem(root.left)) + self.findTilt(root.left) + self.findTilt(root.right)
        self.tilts[root] = tilt
        return tilt 






class Solution:
    def isLeaf(self, node):
        return not node or((not node.left) and (not node.right))
    
    def getLeafVal(self, node):
        if not node:
            return 0
        else:
            return node.val
        
    def findTilt(self, root: Optional[TreeNode]) -> int:
        print(f"at {root.val}")
        if not root or self.isLeaf(root):
            print("ret 0")
            return 0
        if self.isLeaf(root.left) and self.isLeaf(root.right):
            print("ret", abs(self.getLeafVal(root.left) - self.getLeafVal(root.right)))
            return abs(self.getLeafVal(root.left) - self.getLeafVal(root.right))
        if self.isLeaf(root.left):
            print("ret", abs(self.getLeafVal(root.left) - self.findTilt(root.right)))
            return abs(self.getLeafVal(root.left) - self.findTilt(root.right))
        if self.isLeaf(root.right):
            print("ret", abs(self.getLeafVal(root.right) - self.findTilt(root.left)))
            return abs(self.getLeafVal(root.right) - self.findTilt(root.left))
        print("ret", abs(self.findTilt(root.left)-self.findTilt(root.left)))
        return abs(self.findTilt(root.left)-self.findTilt(root.right))

        
