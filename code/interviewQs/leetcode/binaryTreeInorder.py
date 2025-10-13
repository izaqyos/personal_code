"""
Given the root of a binary tree, return the inorder traversal of its nodes' values.

 

Example 1:


Input: root = [1,null,2,3]
Output: [1,3,2]
Example 2:

Input: root = []
Output: []
Example 3:

Input: root = [1]
Output: [1]
Example 4:


Input: root = [1,2]
Output: [2,1]
Example 5:


Input: root = [1,null,2]
Output: [1,2]
 

Constraints:

The number of nodes in the tree is in the range [0, 100].
-100 <= Node.val <= 100
 

Follow up:

Recursive solution is trivial, could you do it iteratively?
"""

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:

    def inorderTraversal(self, root):
        ret = []
        #return self.inorderTraversalRecursive(root, ret)
        ret = self.inorderTraversalIterative(root)
        return ret

    def inorderTraversalRecursive(self, root, ret):
        """
        recursion is trivial duh
        """
        if root:
            self.inorderTraversalRecursive(root.left, ret)
            ret.append(root)
            self.inorderTraversalRecursive(root.right, ret)
        return ret


    def inorderTraversalIterative(self, root):
        """
        iterative idea. use stack like DFS but after popping node 
        don't perform action(print/add to final list) instead check
        if it doesn't have left son. if so, perform action.
        Then if it has right son push to stack
        if it has left son, push current back then left son.
        """
        from collections import deque
        ret = []
        st = deque()
        st.append(root)
        visited = {root}
        while st:
            current = st.pop()
            if current.right and not current.right in visited:
                st.append(current.right)
                visited.add(current.right)
            if current.left and not current.left in visited:
                st.append(current)
                st.append(current.left)
                visited.add(current.left)
            else:
                ret.append(current.val)
        return ret
                

        
    def addNodeFromList(self, index, lst):
        if index>= len(lst):
            return None
        else:
            if lst[index]:
                node = TreeNode(lst[index])
                node.left = self.addNodeFromList(2*index+1, lst)
                node.right = self.addNodeFromList(2*index+2, lst)
                return node
            else:
                return None

    def buildTree(self, lst):
        """
        for each node at position i, it's sons are at 2*i+1,2*i+2 (left, right)
        """
        if not lst:
            return
        return self.addNodeFromList(0, lst)

    def traverse_tree(self, root, callback):
        callback(root)
        if root:
            self.traverse_tree(root.left, callback)
            self.traverse_tree(root.right, callback)
        


def main():
    inputs = [
            [1,None,2,3],
            #[1,2,3,4,5,6,7],
            ]
    sol = Solution()
    for inp in inputs:
        root = sol.buildTree(inp)
        sol.traverse_tree(root, lambda x: print(x.val) if x else print('None'))

if __name__ == "__main__":
    main()
