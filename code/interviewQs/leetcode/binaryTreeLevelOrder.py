"""
LC 102 - Binary Tree Level Order Traversal (Medium)

Given the root of a binary tree, return the level order traversal of its
nodes' values (i.e., from left to right, level by level).

Example 1:
    Input: root = [3,9,20,null,null,15,7]
    Output: [[3],[9,20],[15,7]]

Example 2:
    Input: root = [1]
    Output: [[1]]

Example 3:
    Input: root = []
    Output: []

Constraints:
    The number of nodes in the tree is in the range [0, 2000].
    -1000 <= Node.val <= 1000
"""
from typing import List, Optional
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(values: List[Optional[int]]) -> Optional[TreeNode]:
    """Builds a tree from LeetCode's level-order list format (None = missing child)."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    q = deque([root])
    i = 1
    while q and i < len(values):
        node = q.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            q.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            q.append(node.right)
        i += 1
    return root


def level_order(root: Optional[TreeNode]) -> List[List[int]]:
    if not root:
        return []

    ret_list = []
    q = deque([root])
    while q:
        level_length = len(q)
        interim_list = []
        for _ in range(level_length):
            current_node = q.popleft()
            interim_list.append(current_node.val)
            if current_node.left:
                q.append(current_node.left)
            if current_node.right:
                q.append(current_node.right)
        ret_list.append(interim_list)
    return ret_list


if __name__ == "__main__":
    tree1 = build_tree([3,9,20,None,None,15,7])
    assert level_order(tree1) == [[3],[9,20],[15,7]]

    tree2 = build_tree([1])
    assert level_order(tree2) == [[1]]

    tree3 = build_tree([])
    assert level_order(tree3) == []

    tree4 = build_tree([1,2,3,4,None,None,5])
    assert level_order(tree4) == [[1],[2,3],[4,5]]

    print("All tests passed.")
