# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def ispseudopali(self, path_digit_frequencies):
        odd = 0
        for v in path_digit_frequencies.values():
            if v%2!=0:
                odd+=1
        return odd<2

    def dfs (self, root: Optional[TreeNode]) -> int:
        paths = 0
        path_digit_frequencies =  {digit:0 for digit in range(1,10)}
        dfs_stack = [(root, path_digit_frequencies)] #each stack element is a tuple of, current node and path_digit_frequencies dictionary
        while dfs_stack:
            current_node, path_digit_frequencies = dfs_stack.pop()
            path_digit_frequencies[current_node.val]+=1
            if current_node.left or current_node.right:
                if current_node.left:
                    path_digit_frequencies_left = dict(path_digit_frequencies)
                    dfs_stack.append((current_node.left, path_digit_frequencies_left))
                if current_node.right:
                    path_digit_frequencies_right = dict(path_digit_frequencies)
                    dfs_stack.append((current_node.right, path_digit_frequencies_right))
            else: #leave
                if self.ispseudopali(path_digit_frequencies): #todo, impl, # of even digits >=8
                    paths+=1
        return paths
                

    def pseudoPalindromicPaths (self, root: Optional[TreeNode]) -> int:
        return self.dfs(root)
