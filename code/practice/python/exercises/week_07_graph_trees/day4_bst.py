"""
Week 7, Day 4: Binary Search Trees (BST)

Learning Objectives:
- Understand BST properties
- Implement BST operations
- Learn search, insert, delete
- Practice BST validation
- Solve BST problems

Time: 10-15 minutes
"""

# ============================================================
# EXERCISE 1: BST Node and Basic Structure
# ============================================================

class BSTNode:
    """Binary Search Tree node"""
    
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

class BST:
    """
    Binary Search Tree.
    
    Property: Left < Root < Right for all nodes
    """
    
    def __init__(self):
        self.root = None
    
    def insert(self, val):
        """Insert value into BST"""
        if not self.root:
            self.root = BSTNode(val)
        else:
            self._insert_recursive(self.root, val)
    
    def _insert_recursive(self, node, val):
        """Recursive insert"""
        if val < node.val:
            if node.left:
                self._insert_recursive(node.left, val)
            else:
                node.left = BSTNode(val)
        else:
            if node.right:
                self._insert_recursive(node.right, val)
            else:
                node.right = BSTNode(val)
    
    def inorder(self):
        """Inorder traversal (sorted order)"""
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node, result):
        """Recursive inorder"""
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.val)
            self._inorder_recursive(node.right, result)

def test_bst_basics():
    """Test BST basics"""
    print("--- Exercise 1: BST Basics ---")
    
    bst = BST()
    values = [5, 3, 7, 1, 4, 6, 9]
    
    print(f"Inserting: {values}")
    for val in values:
        bst.insert(val)
    
    print(f"Inorder (sorted): {bst.inorder()}")
    
    print("\n💡 BST Property: Left < Root < Right")
    print("💡 Inorder traversal gives sorted order")
    
    print()

# ============================================================
# EXERCISE 2: BST Search
# ============================================================

def bst_search():
    """
    Search in BST.
    
    TODO: O(h) search where h = height
    """
    print("--- Exercise 2: BST Search ---")
    
    def search(root, val):
        """Search for value in BST"""
        if not root or root.val == val:
            return root
        
        if val < root.val:
            return search(root.left, val)
        return search(root.right, val)
    
    def search_iterative(root, val):
        """Iterative search"""
        current = root
        
        while current:
            if val == current.val:
                return current
            elif val < current.val:
                current = current.left
            else:
                current = current.right
        
        return None
    
    bst = BST()
    for val in [5, 3, 7, 1, 4, 6, 9]:
        bst.insert(val)
    
    test_values = [4, 8]
    for val in test_values:
        found = search(bst.root, val)
        print(f"Search {val}: {'Found' if found else 'Not found'}")
    
    print("\n💡 BST Search: O(h) time, O(1) space (iterative)")
    
    print()

# ============================================================
# EXERCISE 3: BST Delete
# ============================================================

def bst_delete():
    """
    Delete from BST.
    
    TODO: Handle 3 cases - leaf, one child, two children
    """
    print("--- Exercise 3: BST Delete ---")
    
    def delete(root, val):
        """Delete value from BST"""
        if not root:
            return None
        
        if val < root.val:
            root.left = delete(root.left, val)
        elif val > root.val:
            root.right = delete(root.right, val)
        else:
            # Found node to delete
            
            # Case 1: Leaf node
            if not root.left and not root.right:
                return None
            
            # Case 2: One child
            if not root.left:
                return root.right
            if not root.right:
                return root.left
            
            # Case 3: Two children
            # Find inorder successor (min in right subtree)
            min_node = find_min(root.right)
            root.val = min_node.val
            root.right = delete(root.right, min_node.val)
        
        return root
    
    def find_min(node):
        """Find minimum value node"""
        while node.left:
            node = node.left
        return node
    
    bst = BST()
    for val in [5, 3, 7, 1, 4, 6, 9]:
        bst.insert(val)
    
    print(f"Original: {bst.inorder()}")
    
    bst.root = delete(bst.root, 3)
    print(f"After deleting 3: {bst.inorder()}")
    
    print("\n💡 Delete cases:")
    print("  1. Leaf: Just remove")
    print("  2. One child: Replace with child")
    print("  3. Two children: Replace with inorder successor")
    
    print()

# ============================================================
# EXERCISE 4: Validate BST
# ============================================================

def validate_bst():
    """
    Check if tree is valid BST.
    
    TODO: Validate BST property
    """
    print("--- Exercise 4: Validate BST ---")
    
    def is_valid_bst(root, min_val=float('-inf'), max_val=float('inf')):
        """Check if tree is valid BST"""
        if not root:
            return True
        
        if root.val <= min_val or root.val >= max_val:
            return False
        
        return (is_valid_bst(root.left, min_val, root.val) and
                is_valid_bst(root.right, root.val, max_val))
    
    # Valid BST
    bst1 = BST()
    for val in [5, 3, 7, 1, 4, 6, 9]:
        bst1.insert(val)
    
    print(f"Tree 1: {bst1.inorder()}")
    print(f"Is valid BST: {is_valid_bst(bst1.root)}")
    
    # Invalid BST (manually constructed)
    invalid = BSTNode(5)
    invalid.left = BSTNode(3)
    invalid.right = BSTNode(7)
    invalid.left.right = BSTNode(6)  # Violates BST property
    
    print(f"\nTree 2 (invalid): Has 6 in left subtree of 5")
    print(f"Is valid BST: {is_valid_bst(invalid)}")
    
    print()

# ============================================================
# EXERCISE 5: BST from Sorted Array
# ============================================================

def bst_from_sorted():
    """
    Create balanced BST from sorted array.
    
    TODO: Use middle element as root
    """
    print("--- Exercise 5: BST from Sorted Array ---")
    
    def sorted_array_to_bst(arr):
        """Create balanced BST from sorted array"""
        if not arr:
            return None
        
        mid = len(arr) // 2
        root = BSTNode(arr[mid])
        
        root.left = sorted_array_to_bst(arr[:mid])
        root.right = sorted_array_to_bst(arr[mid + 1:])
        
        return root
    
    def height(root):
        """Calculate height"""
        if not root:
            return 0
        return 1 + max(height(root.left), height(root.right))
    
    def inorder(root, result=None):
        """Inorder traversal"""
        if result is None:
            result = []
        if root:
            inorder(root.left, result)
            result.append(root.val)
            inorder(root.right, result)
        return result
    
    arr = [1, 2, 3, 4, 5, 6, 7]
    print(f"Sorted array: {arr}")
    
    root = sorted_array_to_bst(arr)
    print(f"BST inorder: {inorder(root)}")
    print(f"BST height: {height(root)}")
    
    print("\n💡 Balanced BST: Height = O(log n)")
    
    print()

# ============================================================
# EXERCISE 6: Kth Smallest Element
# ============================================================

def kth_smallest():
    """
    Find kth smallest element in BST.
    
    TODO: Use inorder traversal
    """
    print("--- Exercise 6: Kth Smallest Element ---")
    
    def kth_smallest_element(root, k):
        """Find kth smallest (1-indexed)"""
        def inorder(node):
            if not node:
                return []
            return inorder(node.left) + [node.val] + inorder(node.right)
        
        sorted_vals = inorder(root)
        return sorted_vals[k - 1] if k <= len(sorted_vals) else None
    
    def kth_smallest_optimized(root, k):
        """Optimized: stop after k elements"""
        count = [0]
        result = [None]
        
        def inorder(node):
            if not node or result[0] is not None:
                return
            
            inorder(node.left)
            
            count[0] += 1
            if count[0] == k:
                result[0] = node.val
                return
            
            inorder(node.right)
        
        inorder(root)
        return result[0]
    
    bst = BST()
    for val in [5, 3, 7, 1, 4, 6, 9]:
        bst.insert(val)
    
    print(f"BST (sorted): {bst.inorder()}")
    
    for k in [1, 3, 5]:
        val = kth_smallest_optimized(bst.root, k)
        print(f"{k}th smallest: {val}")
    
    print()

# ============================================================
# EXERCISE 7: Real-World Scenario - Range Query
# ============================================================

def range_query():
    """
    Find all values in range [low, high].
    
    TODO: Efficient range search in BST
    """
    print("--- Exercise 7: Range Query ---")
    
    def range_search(root, low, high):
        """Find all values in [low, high]"""
        result = []
        
        def search(node):
            if not node:
                return
            
            # Search left if possible
            if node.val > low:
                search(node.left)
            
            # Add current if in range
            if low <= node.val <= high:
                result.append(node.val)
            
            # Search right if possible
            if node.val < high:
                search(node.right)
        
        search(root)
        return result
    
    bst = BST()
    for val in [5, 3, 7, 1, 4, 6, 9]:
        bst.insert(val)
    
    print(f"BST: {bst.inorder()}")
    
    ranges = [(3, 6), (1, 4), (7, 10)]
    for low, high in ranges:
        result = range_search(bst.root, low, high)
        print(f"Range [{low}, {high}]: {result}")
    
    print()

# ============================================================
# BONUS CHALLENGE: Lowest Common Ancestor in BST
# ============================================================

def lca_bst():
    """
    Find LCA in BST (optimized).
    
    TODO: Use BST property for efficient LCA
    """
    print("--- Bonus Challenge: LCA in BST ---")
    
    def lca(root, p, q):
        """Find LCA of p and q in BST"""
        if not root:
            return None
        
        # Both in left subtree
        if p < root.val and q < root.val:
            return lca(root.left, p, q)
        
        # Both in right subtree
        if p > root.val and q > root.val:
            return lca(root.right, p, q)
        
        # Split point (or one equals root)
        return root
    
    bst = BST()
    for val in [6, 2, 8, 0, 4, 7, 9, 3, 5]:
        bst.insert(val)
    
    print(f"BST: {bst.inorder()}")
    
    pairs = [(2, 8), (2, 4), (3, 5)]
    for p, q in pairs:
        ancestor = lca(bst.root, p, q)
        print(f"LCA({p}, {q}): {ancestor.val if ancestor else None}")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    BST Operations (average case):
    - Search: O(h) where h = height
    - Insert: O(h)
    - Delete: O(h)
    - Inorder: O(n)
    
    Balanced BST:
    - Height: O(log n)
    - All operations: O(log n)
    
    Unbalanced BST:
    - Height: O(n) worst case
    - Degenerates to linked list
    
    BST Properties:
    - Inorder gives sorted order
    - Left < Root < Right
    - No duplicates (typically)
    
    Advantages:
    - Fast search, insert, delete
    - Maintains sorted order
    - Range queries efficient
    
    Disadvantages:
    - Can become unbalanced
    - Worst case O(n)
    - Need balancing (AVL, Red-Black)
    
    Best Practices:
    - Keep tree balanced
    - Use iterative for space efficiency
    - Handle edge cases (null, single node)
    - Consider self-balancing trees
    
    Common Patterns:
    - Recursive divide and conquer
    - Inorder for sorted access
    - Range queries with pruning
    - LCA using BST property
    
    Security Considerations:
    - Validate input values
    - Limit tree depth
    - Prevent degenerate trees
    - Handle large datasets carefully
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 7, Day 4: Binary Search Trees")
    print("=" * 60)
    print()
    
    test_bst_basics()
    bst_search()
    bst_delete()
    validate_bst()
    bst_from_sorted()
    kth_smallest()
    range_query()
    lca_bst()
    
    print("=" * 60)
    print("✅ Day 4 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. BST property: Left < Root < Right")
    print("2. Operations: O(h) where h = height")
    print("3. Balanced BST: O(log n) operations")
    print("4. Inorder traversal gives sorted order")

