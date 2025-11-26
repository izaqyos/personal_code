class Solution:
    def pathNumber(self, path):
        factor = 1
        ret = 0
        for d in  reversed(path):
            ret += d*factor
            factor *= 10
        return ret

    def sumNumbers(self, root: Optional[TreeNode]) -> int:
        """
        idea. DFS, build path along the way, on leafs use self.pathNumber() helper to return this path number
        then add it to total and return total
        """
        if not root:
            return 0
        path = []
        total = 0
        stack = [(root, path)]
        while stack:
            cur, path = stack.pop()
            #print(f"cur={cur}, path={path}")
            path.append(cur.val)
            if cur.left:
                left_path = path[:]
                stack.append((cur.left, left_path))
            if cur.right:
                right_path = path[:]
                stack.append((cur.right, right_path))
            if (not cur.left) and (not cur.right):
                total += self.pathNumber(path) 
        return total

