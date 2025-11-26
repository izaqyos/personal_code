# Binary Trees - Complete Guide

## 📋 Pattern Recognition

**When to use Trees:**
- Hierarchical data
- "Parent", "child", "ancestor", "descendant"
- "Path from root to leaf"
- "Level order", "depth"

**Keywords:** tree, binary, BST, path, ancestor, traversal, level

---

## 🎯 Tree Basics

### TreeNode Definition
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

### Tree Properties
- **Height:** Longest path from root to leaf
- **Depth:** Distance from root to node
- **Balanced:** |height(left) - height(right)| ≤ 1
- **Complete:** All levels filled except last (filled left to right)
- **Perfect:** All internal nodes have 2 children, all leaves same level

---

## 🔧 Pattern 1: Tree Traversals

### DFS Traversals (Recursive)
```python
def inorder(root: TreeNode) -> list:
    """Left → Root → Right (BST gives sorted order!)"""
    result = []
    def dfs(node):
        if not node:
            return
        dfs(node.left)
        result.append(node.val)
        dfs(node.right)
    dfs(root)
    return result


def preorder(root: TreeNode) -> list:
    """Root → Left → Right (used to copy tree)"""
    result = []
    def dfs(node):
        if not node:
            return
        result.append(node.val)
        dfs(node.left)
        dfs(node.right)
    dfs(root)
    return result


def postorder(root: TreeNode) -> list:
    """Left → Right → Root (used to delete tree)"""
    result = []
    def dfs(node):
        if not node:
            return
        dfs(node.left)
        dfs(node.right)
        result.append(node.val)
    dfs(root)
    return result
```

### Iterative Traversals
```python
def inorder_iterative(root: TreeNode) -> list:
    """Inorder using stack"""
    result = []
    stack = []
    current = root
    
    while current or stack:
        # Go to leftmost node
        while current:
            stack.append(current)
            current = current.left
        
        # Process node
        current = stack.pop()
        result.append(current.val)
        
        # Go to right subtree
        current = current.right
    
    return result
```

### Level Order (BFS)
```python
from collections import deque

def levelOrder(root: TreeNode) -> list[list[int]]:
    """
    LeetCode #102 - THE BFS template
    Time: O(n), Space: O(n)
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(level)
    
    return result
```

---

## 🔧 Pattern 2: Path Problems

### Max Path Sum
```python
def maxPathSum(root: TreeNode) -> int:
    """
    LeetCode #124 - Path can start/end anywhere
    
    For each node, max path either:
    1. Goes through node (left + node + right)
    2. In left subtree
    3. In right subtree
    
    Time: O(n), Space: O(h)
    """
    max_sum = float('-inf')
    
    def dfs(node):
        nonlocal max_sum
        
        if not node:
            return 0
        
        # Max path sum ending at left/right child
        left = max(0, dfs(node.left))   # Ignore negative paths
        right = max(0, dfs(node.right))
        
        # Max path through this node
        max_sum = max(max_sum, left + node.val + right)
        
        # Return max path sum ending at this node
        return node.val + max(left, right)
    
    dfs(root)
    return max_sum
```

### Path Sum II
```python
def pathSum(root: TreeNode, targetSum: int) -> list[list[int]]:
    """
    LeetCode #113 - All root-to-leaf paths with sum
    
    Time: O(n²) worst case, Space: O(h)
    """
    result = []
    
    def dfs(node, path, remaining):
        if not node:
            return
        
        path.append(node.val)
        
        # Leaf node with target sum
        if not node.left and not node.right and remaining == node.val:
            result.append(path[:])
        
        dfs(node.left, path, remaining - node.val)
        dfs(node.right, path, remaining - node.val)
        
        path.pop()  # Backtrack
    
    dfs(root, [], targetSum)
    return result
```

---

## 🔧 Pattern 3: BST Problems

### Validate BST
```python
def isValidBST(root: TreeNode) -> bool:
    """
    LeetCode #98 🚨 VERY COMMON
    
    BST property: left < node < right (for ALL descendants)
    
    Time: O(n), Space: O(h)
    """
    def validate(node, min_val, max_val):
        if not node:
            return True
        
        if not (min_val < node.val < max_val):
            return False
        
        return (validate(node.left, min_val, node.val) and
                validate(node.right, node.val, max_val))
    
    return validate(root, float('-inf'), float('inf'))
```

### Kth Smallest in BST
```python
def kthSmallest(root: TreeNode, k: int) -> int:
    """
    LeetCode #230 - Inorder traversal of BST is sorted!
    
    Time: O(h + k), Space: O(h)
    """
    stack = []
    current = root
    count = 0
    
    while current or stack:
        while current:
            stack.append(current)
            current = current.left
        
        current = stack.pop()
        count += 1
        if count == k:
            return current.val
        
        current = current.right
```

---

## 🔧 Pattern 4: Tree Construction

### From Preorder + Inorder
```python
def buildTree(preorder: list[int], inorder: list[int]) -> TreeNode:
    """
    LeetCode #105
    
    Preorder: [root, left subtree, right subtree]
    Inorder: [left subtree, root, right subtree]
    
    Time: O(n), Space: O(n)
    """
    if not preorder:
        return None
    
    # Map value to index in inorder for O(1) lookup
    inorder_map = {val: i for i, val in enumerate(inorder)}
    pre_idx = 0
    
    def build(left, right):
        nonlocal pre_idx
        
        if left > right:
            return None
        
        # Root is next element in preorder
        root_val = preorder[pre_idx]
        root = TreeNode(root_val)
        pre_idx += 1
        
        # Split inorder by root
        root_idx = inorder_map[root_val]
        
        # Build left then right (order matters - preorder!)
        root.left = build(left, root_idx - 1)
        root.right = build(root_idx + 1, right)
        
        return root
    
    return build(0, len(inorder) - 1)
```

---

## 🔧 Pattern 5: Lowest Common Ancestor

### LCA in Binary Tree
```python
def lowestCommonAncestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """
    LeetCode #236 🚨 MUST DO
    
    Key insight: LCA is where paths to p and q diverge
    
    Time: O(n), Space: O(h)
    """
    if not root or root == p or root == q:
        return root
    
    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)
    
    # If both sides found nodes, root is LCA
    if left and right:
        return root
    
    # Return whichever side found a node
    return left if left else right
```

### LCA in BST
```python
def lowestCommonAncestor_BST(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """
    LeetCode #235 - Use BST property!
    
    Time: O(h), Space: O(1) iterative
    """
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root
```

---

## 🔧 Pattern 6: Serialization

### Serialize/Deserialize
```python
class Codec:
    """
    LeetCode #297 🚨 MUST DO
    
    Use preorder traversal
    Time: O(n), Space: O(n)
    """
    def serialize(self, root: TreeNode) -> str:
        """Encode tree to string"""
        result = []
        
        def dfs(node):
            if not node:
                result.append('null')
                return
            result.append(str(node.val))
            dfs(node.left)
            dfs(node.right)
        
        dfs(root)
        return ','.join(result)
    
    def deserialize(self, data: str) -> TreeNode:
        """Decode string to tree"""
        values = iter(data.split(','))
        
        def dfs():
            val = next(values)
            if val == 'null':
                return None
            node = TreeNode(int(val))
            node.left = dfs()
            node.right = dfs()
            return node
        
        return dfs()
```

---

## 💡 Common Patterns Summary

### Pattern Decision Tree
```
Tree Problem?
│
├─ Traversal? → DFS (recursive/iterative) or BFS
├─ Path from root to leaf? → DFS with path tracking
├─ BST property? → Use BST constraints
├─ Build tree? → Use traversal properties
├─ LCA? → Recursive search in both subtrees
└─ Serialize? → Preorder + null markers
```

---

## 🎓 Practice Problems

### Easy
1. #104 Maximum Depth
2. #100 Same Tree
3. #101 Symmetric Tree
4. #226 Invert Tree - VERY FAMOUS!

### Medium
1. **#102 Binary Tree Level Order** 🚨 BFS template
2. **#98 Validate BST** 🚨 Very common
3. **#105 Construct from Pre+In** 🚨
4. **#236 LCA Binary Tree** 🚨
5. #230 Kth Smallest in BST
6. #113 Path Sum II
7. #199 Right Side View
8. #114 Flatten to Linked List

### Hard
1. **#297 Serialize/Deserialize** 🚨 MUST DO
2. **#124 Binary Tree Max Path Sum** 🚨
3. #145 Postorder Iterative

---

## 🐛 Common Mistakes

### Mistake 1: Not Checking for None
```python
# ❌ WRONG
def dfs(node):
    result = node.val  # Crashes if node is None!

# ✅ CORRECT
def dfs(node):
    if not node:
        return
    result = node.val
```

### Mistake 2: BST Validation Only Checking Immediate Children
```python
# ❌ WRONG - Doesn't check ALL descendants
def isValidBST(root):
    if root.left and root.left.val >= root.val:
        return False
    if root.right and root.right.val <= root.val:
        return False

# ✅ CORRECT - Use min/max bounds
def isValidBST(root, min_val, max_val):
    if not (min_val < root.val < max_val):
        return False
```

### Mistake 3: Forgetting to Backtrack in Path Problems
```python
# ❌ WRONG
path.append(node.val)
dfs(node.left)
dfs(node.right)
# Forgot to path.pop()!

# ✅ CORRECT
path.append(node.val)
dfs(node.left)
dfs(node.right)
path.pop()  # Backtrack!
```

---

## 💡 Pro Tips

### Tip 1: Tree Recursion Template
```python
def dfs(node):
    # Base case
    if not node:
        return base_value
    
    # Recursive calls
    left = dfs(node.left)
    right = dfs(node.right)
    
    # Combine results
    return combine(node.val, left, right)
```

### Tip 2: When to Use BFS vs DFS
- **BFS (Level order):** Shortest path, level by level processing
- **DFS (Preorder/Inorder/Postorder):** Path finding, tree properties

### Tip 3: BST Inorder = Sorted
```python
# Inorder traversal of BST gives sorted order!
# Use for: kth smallest, validate BST
```

---

**Remember:** Trees are recursive by nature! Master the recursion pattern and you'll solve most tree problems!

