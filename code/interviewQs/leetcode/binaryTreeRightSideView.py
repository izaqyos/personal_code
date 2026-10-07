"""
LC 199 - Binary Tree Right Side View (Medium)

Given the root of a binary tree, imagine yourself standing on the right
side of it. Return the values of the nodes you can see, ordered from
top to bottom.

Example 1:
    Input: root = [1,2,3,None,5,None,4]
    Output: [1,3,4]

Example 2:
    Input: root = [1,None,3]
    Output: [1,3]

Example 3:
    Input: root = []
    Output: []

Constraints:
    The number of nodes in the tree is in the range [0, 100].
    -100 <= Node.val <= 100
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


def right_side_view(root: Optional[TreeNode]) -> List[int]:
    if not root: return []
    ret_val_list = []
    q = deque([root])
    while q:
        rhs_val = q[-1].val
        ret_val_list.append(rhs_val)
        for _ in range(len(q)): #process this whole level to BFS nxt lvl
            node = q.popleft()
            if node.left: q.append(node.left)
            if node.right: q.append(node.right)
    return ret_val_list



if __name__ == "__main__":
    tree1 = build_tree([1,2,3,None,5,None,4])
    assert right_side_view(tree1) == [1,3,4]

    tree2 = build_tree([1,None,3])
    assert right_side_view(tree2) == [1,3]

    tree3 = build_tree([])
    assert right_side_view(tree3) == []

    tree4 = build_tree([1,2,None,5])
    assert right_side_view(tree4) == [1,2,5]

    print("All tests passed.")
