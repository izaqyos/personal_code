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
