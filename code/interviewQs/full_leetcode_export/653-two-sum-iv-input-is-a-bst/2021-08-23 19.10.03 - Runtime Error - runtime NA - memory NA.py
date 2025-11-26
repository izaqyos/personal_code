# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def findTarget(self, root: Optional[TreeNode], k: int) -> bool:
        """
        idea. BFS and set of seen elements. Since its BST no need 4 visited set
        """

        if not root:
            return False

        from collections import deque
        q = deque() 
        q.append(root)
        s = set()

        while q:
            c = q.popleft()
            if c.val in s:
                if 2*c.val == k:
                    return True
            else:
                s.add(c.val)
                if k-c.val in s:
                    return True
            q.append(c.left)
            q.append(c.right)

        return False

