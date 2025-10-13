"""
Binary Tree Maximum Path Sum
Hard
A path in a binary tree is a sequence of nodes where each pair of adjacent nodes in the sequence has an edge connecting them. A node can only appear in the sequence at most once. Note that the path does not need to pass through the root.

The path sum of a path is the sum of the node's values in the path.

Given the root of a binary tree, return the maximum path sum of any non-empty path.
Example 1:

Input: root = [1,2,3]
Output: 6
Explanation: The optimal path is 2 -> 1 -> 3 with a path sum of 2 + 1 + 3 = 6.
Example 2:
Input: root = [-10,9,20,null,null,15,7]
Output: 42
Explanation: The optimal path is 15 -> 20 -> 7 with a path sum of 15 + 20 + 7 = 42.
 

Constraints:

The number of nodes in the tree is in the range [1, 3 * 104].
-1000 <= Node.val <= 1000
"""
from typing import Optional
import pdb
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def calc_BTMPS(self, root):
        if not root:
            return 0, float('-inf')  # return 2 values, max path from root and the answer (max path sum from this node taking into account both left and right sub trees)
        left_MPFR, left_MPS = self.calc_BTMPS(root.left)
        right_MPFR, right_MPS = self.calc_BTMPS(root.right)
        return root.val+max(left_MPFR, right_MPFR, 0), max(left_MPS, right_MPS, max(left_MPFR,0)+max(right_MPFR,0)+root.val)

    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        _, res = self.calc_BTMPS(root)
        return res

class Solution_sucks:
    def calc_paths(self, root, final_paths):
        #pdb.set_trace()
        if root == None:
            return []
        if root.left == None and root.right==None:
            return [ [ root.val ] ]
        ret_paths = list()
        left_paths = self.calc_paths(root.left)
        right_paths = self.calc_paths(root.right)
        ret_paths.extend(left_paths)
        ret_paths.extend(right_paths)
        for lpath in left_paths:
            for rpath in right_paths:
                lpath_set = set(lpath)
                rpath_set = set(rpath)
                full_path_set = lpath|rpath
                full_path.add( root.val )
                final_paths.add(list(full_path_set))
        return ret_paths

    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        final_paths = []
        paths = self.calc_paths(root, final_paths)
        print(f"paths: {paths}")
        max_path=float('-inf')
        for path in paths:
            max_path = max(max_path, sum(path))
        return max_path

def tc1_single_node():
    root = TreeNode()
    sol = Solution()
    maxpathsum = sol.maxPathSum(root)
    print(maxpathsum)


#ToDo, add test cases from leet
def tc2():
    root = TreeNode()
    sol = Solution()
    maxpathsum = sol.maxPathSum(root)
    print(maxpathsum)


def main():
    tc1_single_node()

if __name__ == "__main__":
    main()


"""
def maxPathSum(self, root):

    def double(root): # return (max_path_from_root(root), self.maxPathSum(root))
        if root is None:
            return 0, float("-inf")
        x, y = double(root.left)
        a, b = double(root.right)
        
        return root.val + max(x,a,0), max(y, b, (root.val + max(0, x) + max(0,a)))

    m, n = double(root)   
    return n 
The function "double" returns two values 1) maximum sum of path starting from the root node and going down(max_path_from_root(root)) 2) The answer (what we want: self.maxPathSum(root)). Then these two values have recursive relations:

max_path_from_root(root) = root.val + max(max_path_from_root(root.left), max_path_from_root(root.right), 0)
self.maxPathSum(root) = max(self.maxPathSum(root.left), self.maxPathSum(root.right), root.val + max(0, max_path_from_root(root.left)) + max(0, max_path_from_root(root.right))
Note that the first two terms are the case the maximum path does not go through the root node. The last case is when it goes through the root node.
"""
