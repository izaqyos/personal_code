"""
Week 7, Day 3: Binary Trees

Learning Objectives:
- Understand binary tree structure
- Implement tree node and operations
- Learn tree traversals (inorder, preorder, postorder)
- Practice recursive tree algorithms
- Solve common tree problems

Time: 10-15 minutes
"""

from collections import deque

# ============================================================
# EXERCISE 1: Binary Tree Node
# ============================================================

class TreeNode:
    """
    Binary tree node.
    
    Each node has value, left child, right child
    """
    
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"TreeNode({self.val})"

def create_sample_tree():
    """Create sample binary tree"""
    #       1
    #      / \
    #     2   3
    #    / \
    #   4   5
    
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    
    return root

def test_tree_node():
    """Test tree node creation"""
    print("--- Exercise 1: Binary Tree Node ---")
    
    root = create_sample_tree()
    
    print("Tree structure:")
    print("       1")
    print("      / \\")
    print("     2   3")
    print("    / \\")
    print("   4   5")
    
    print(f"\nRoot: {root}")
    print(f"Left child: {root.left}")
    print(f"Right child: {root.right}")
    
    print()

# ============================================================
# EXERCISE 2: Inorder Traversal (Left-Root-Right)
# ============================================================

def inorder_traversal():
    """
    Inorder traversal: Left -> Root -> Right
    
    TODO: Recursive and iterative
    """
    print("--- Exercise 2: Inorder Traversal ---")
    
    def inorder_recursive(root, result=None):
        """Recursive inorder"""
        if result is None:
            result = []
        
        if root:
            inorder_recursive(root.left, result)
            result.append(root.val)
            inorder_recursive(root.right, result)
        
        return result
    
    def inorder_iterative(root):
        """Iterative inorder using stack"""
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
    
    root = create_sample_tree()
    
    print("Inorder (recursive):", inorder_recursive(root))
    print("Inorder (iterative):", inorder_iterative(root))
    
    print("\n💡 Inorder: Left -> Root -> Right")
    print("  • For BST: gives sorted order")
    
    print()

# ============================================================
# EXERCISE 3: Preorder Traversal (Root-Left-Right)
# ============================================================

def preorder_traversal():
    """
    Preorder traversal: Root -> Left -> Right
    
    TODO: Recursive and iterative
    """
    print("--- Exercise 3: Preorder Traversal ---")
    
    def preorder_recursive(root, result=None):
        """Recursive preorder"""
        if result is None:
            result = []
        
        if root:
            result.append(root.val)
            preorder_recursive(root.left, result)
            preorder_recursive(root.right, result)
        
        return result
    
    def preorder_iterative(root):
        """Iterative preorder using stack"""
        if not root:
            return []
        
        result = []
        stack = [root]
        
        while stack:
            node = stack.pop()
            result.append(node.val)
            
            # Push right first (so left is processed first)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
        
        return result
    
    root = create_sample_tree()
    
    print("Preorder (recursive):", preorder_recursive(root))
    print("Preorder (iterative):", preorder_iterative(root))
    
    print("\n💡 Preorder: Root -> Left -> Right")
    print("  • Used for: Tree copying, prefix expressions")
    
    print()

# ============================================================
# EXERCISE 4: Postorder Traversal (Left-Right-Root)
# ============================================================

def postorder_traversal():
    """
    Postorder traversal: Left -> Right -> Root
    
    TODO: Recursive and iterative
    """
    print("--- Exercise 4: Postorder Traversal ---")
    
    def postorder_recursive(root, result=None):
        """Recursive postorder"""
        if result is None:
            result = []
        
        if root:
            postorder_recursive(root.left, result)
            postorder_recursive(root.right, result)
            result.append(root.val)
        
        return result
    
    def postorder_iterative(root):
        """Iterative postorder using two stacks"""
        if not root:
            return []
        
        stack1 = [root]
        stack2 = []
        
        while stack1:
            node = stack1.pop()
            stack2.append(node)
            
            if node.left:
                stack1.append(node.left)
            if node.right:
                stack1.append(node.right)
        
        result = []
        while stack2:
            result.append(stack2.pop().val)
        
        return result
    
    root = create_sample_tree()
    
    print("Postorder (recursive):", postorder_recursive(root))
    print("Postorder (iterative):", postorder_iterative(root))
    
    print("\n💡 Postorder: Left -> Right -> Root")
    print("  • Used for: Tree deletion, postfix expressions")
    
    print()

# ============================================================
# EXERCISE 5: Level Order Traversal (BFS)
# ============================================================

def level_order_traversal():
    """
    Level order traversal using BFS.
    
    TODO: Traverse level by level
    """
    print("--- Exercise 5: Level Order Traversal ---")
    
    def level_order(root):
        """Level order traversal"""
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
    
    root = create_sample_tree()
    
    levels = level_order(root)
    print("Level order traversal:")
    for i, level in enumerate(levels):
        print(f"  Level {i}: {level}")
    
    print("\n💡 Level Order: BFS, level by level")
    
    print()

# ============================================================
# EXERCISE 6: Tree Properties
# ============================================================

def tree_properties():
    """
    Calculate tree properties.
    
    TODO: Height, size, leaf count
    """
    print("--- Exercise 6: Tree Properties ---")
    
    def height(root):
        """Calculate tree height"""
        if not root:
            return 0
        return 1 + max(height(root.left), height(root.right))
    
    def size(root):
        """Count total nodes"""
        if not root:
            return 0
        return 1 + size(root.left) + size(root.right)
    
    def count_leaves(root):
        """Count leaf nodes"""
        if not root:
            return 0
        if not root.left and not root.right:
            return 1
        return count_leaves(root.left) + count_leaves(root.right)
    
    def is_balanced(root):
        """Check if tree is height-balanced"""
        def check_height(node):
            if not node:
                return 0
            
            left_height = check_height(node.left)
            if left_height == -1:
                return -1
            
            right_height = check_height(node.right)
            if right_height == -1:
                return -1
            
            if abs(left_height - right_height) > 1:
                return -1
            
            return 1 + max(left_height, right_height)
        
        return check_height(root) != -1
    
    root = create_sample_tree()
    
    print(f"Height: {height(root)}")
    print(f"Size (total nodes): {size(root)}")
    print(f"Leaf nodes: {count_leaves(root)}")
    print(f"Is balanced: {is_balanced(root)}")
    
    print()

# ============================================================
# EXERCISE 7: Real-World Scenario - File System
# ============================================================

class FileNode:
    """
    File system node (file or directory).
    
    TODO: Represent file system as tree
    """
    
    def __init__(self, name, is_file=True, size=0):
        self.name = name
        self.is_file = is_file
        self.size = size
        self.children = [] if not is_file else None
    
    def add_child(self, child):
        """Add child (for directories)"""
        if not self.is_file:
            self.children.append(child)
    
    def get_total_size(self):
        """Calculate total size"""
        if self.is_file:
            return self.size
        return sum(child.get_total_size() for child in self.children)
    
    def print_tree(self, indent=0):
        """Print file system tree"""
        prefix = "  " * indent
        if self.is_file:
            print(f"{prefix}{self.name} ({self.size} KB)")
        else:
            print(f"{prefix}{self.name}/")
            for child in self.children:
                child.print_tree(indent + 1)

def test_file_system():
    """Test file system tree"""
    print("--- Exercise 7: File System ---")
    
    # Create file system
    root = FileNode("root", is_file=False)
    
    docs = FileNode("documents", is_file=False)
    docs.add_child(FileNode("resume.pdf", size=150))
    docs.add_child(FileNode("cover_letter.pdf", size=80))
    
    photos = FileNode("photos", is_file=False)
    photos.add_child(FileNode("vacation.jpg", size=2000))
    photos.add_child(FileNode("family.jpg", size=1500))
    
    root.add_child(docs)
    root.add_child(photos)
    root.add_child(FileNode("readme.txt", size=5))
    
    print("File system structure:")
    root.print_tree()
    
    print(f"\nTotal size: {root.get_total_size()} KB")
    
    print()

# ============================================================
# BONUS CHALLENGE: Lowest Common Ancestor
# ============================================================

def lowest_common_ancestor():
    """
    Find lowest common ancestor of two nodes.
    
    TODO: LCA in binary tree
    """
    print("--- Bonus Challenge: Lowest Common Ancestor ---")
    
    def lca(root, p, q):
        """Find LCA of nodes p and q"""
        if not root or root.val == p or root.val == q:
            return root
        
        left = lca(root.left, p, q)
        right = lca(root.right, p, q)
        
        if left and right:
            return root
        
        return left if left else right
    
    root = create_sample_tree()
    
    p, q = 4, 5
    ancestor = lca(root, p, q)
    print(f"LCA of {p} and {q}: {ancestor.val if ancestor else None}")
    
    p, q = 4, 3
    ancestor = lca(root, p, q)
    print(f"LCA of {p} and {q}: {ancestor.val if ancestor else None}")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    Traversals:
    - Time: O(n) - visit each node once
    - Space: O(h) for recursion, O(n) for iterative
    - h = height of tree
    
    Tree Properties:
    - Height: O(n) time, O(h) space
    - Size: O(n) time, O(h) space
    - Balanced check: O(n) time, O(h) space
    
    Traversal Types:
    - Inorder: Left-Root-Right (BST: sorted)
    - Preorder: Root-Left-Right (copy tree)
    - Postorder: Left-Right-Root (delete tree)
    - Level order: BFS (level by level)
    
    Best Practices:
    - Use recursion for simplicity
    - Use iteration to avoid stack overflow
    - Handle null nodes
    - Consider tree structure
    
    Common Patterns:
    - Divide and conquer
    - Recursion with base case
    - Level-order with queue
    - Path tracking with backtracking
    
    Security Considerations:
    - Limit tree depth
    - Validate tree structure
    - Handle large trees
    - Prevent stack overflow
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 7, Day 3: Binary Trees")
    print("=" * 60)
    print()
    
    test_tree_node()
    inorder_traversal()
    preorder_traversal()
    postorder_traversal()
    level_order_traversal()
    tree_properties()
    test_file_system()
    lowest_common_ancestor()
    
    print("=" * 60)
    print("✅ Day 3 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. Three main traversals: inorder, preorder, postorder")
    print("2. Level order uses BFS with queue")
    print("3. Recursion is natural for tree problems")
    print("4. All traversals are O(n) time")

