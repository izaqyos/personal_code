class Solution:
    def genTreesR(self, left, right) -> List[Optional[TreeNode]]:
        """
        generate all subtrees from range left to right
        """
        if left>right:
            return [None]
        
        ret = []
        for root in range(left,right+1):
            left_trees = self.genTreesR(left, root-1)
            right_trees = self.genTreesR(root+1, right)
            for left_root in left_trees:
                for right_root in right_trees:
                    ans = TreeNode(root, left_root, right_root)
                    ret.append(ans)
        return ret



    def generateTrees(self, n: int) -> List[Optional[TreeNode]]:
        return self.genTreesR(1,n)
