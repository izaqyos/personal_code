"""
 Sum Root to Leaf Numbers
You are given the root of a binary tree containing digits from 0 to 9 only.

Each root-to-leaf path in the tree represents a number.

For example, the root-to-leaf path 1 -> 2 -> 3 represents the number 123.
Return the total sum of all root-to-leaf numbers. Test cases are generated so that the answer will fit in a 32-bit integer.

A leaf node is a node with no children.


Constraints:

The number of nodes in the tree is in the range [1, 1000].
0 <= Node.val <= 9
The depth of the tree will not exceed 10.
"""

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
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


            


