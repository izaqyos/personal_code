"""
Given the roots of two binary trees p and q, write a function to check if they are the same or not.

Two binary trees are considered the same if they are structurally identical, and the nodes have the same value.



Example 1:


Input: p = [1,2,3], q = [1,2,3]
Output: true
Example 2:


Input: p = [1,2], q = [1,null,2]
Output: false
Example 3:


Input: p = [1,2,1], q = [1,1,2]
Output: false


Constraints:

The number of nodes in both trees is in the range [0, 100].
-104 <= Node.val <= 104
"""

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


