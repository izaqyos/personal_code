
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        """
        idea. do any graph traversal algorithm. at any point of diff return false. after dual traversal is complete return true
        I'll do BFS. No need for visited since it's a tree
        """
        from collections import deque
        qp, qq  = deque([p]), deque([q])
        while qp and qq:
            p_cur, q_cur = qp.popleft(), qq.popleft() 
            if (p_cur and not q_cur) or (q_cur and not p_cur):
                return False
            if p_cur and q_cur:
                if p_cur.val != q_cur.val:
                    return False
                qp.append(p_cur.left)
                qp.append(p_cur.right)
                qq.append(q_cur.left)
                qq.append(q_cur.right)
        if qq or qp:
            return False
        return True
