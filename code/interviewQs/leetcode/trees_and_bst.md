# Trees & BST — Problem Bank & Study Notes

## Study Notes (offline reference)

### Core patterns
- **The recursion contract** — most tree problems are: "define what `f(node)` RETURNS, trust it on children, combine". Write the contract in one sentence before coding. Base case is almost always `if not node: return <identity>`.
- **Top-down vs bottom-up** — top-down passes accumulated state DOWN as parameters (path sum, validate-BST bounds); bottom-up computes from children's RETURNS (height, diameter, subtree sums). Diameter/max-path-sum need BOTH: return one thing (best single arm) while updating a nonlocal best with another (arm + node + arm).
- **Traversals** — preorder (node,L,R), inorder (L,node,R), postorder (L,R,node). Iterative inorder: push left spine, pop, go right — drill this one. BFS level-order: deque + `for _ in range(len(queue))` per level.
- **BST invariant** — inorder traversal of a BST is sorted ascending. Validate-BST: pass `(low, high)` bounds down — comparing only parent/child is the classic wrong answer. Kth smallest = inorder with a counter. Mode/two-sum-in-BST also exploit inorder order.
- **LCA** — general tree: recurse both sides; if both return non-null, current node is the LCA. BST shortcut: walk from root, the first node between p and q in value is the LCA.
- **Serialize/deserialize** — preorder with explicit null markers ('#') is unambiguous; rebuild with an iterator/index. BFS layout also works.
- **Construct from traversals** — preorder[0] is root; find it in inorder to split left/right subtrees; pass index ranges (or a hashmap of value→inorder index) instead of slicing lists.

### Complexity
Balanced: height O(log n); skewed: O(n) — recursion depth follows height (watch Python's ~1000 limit on big skewed inputs; convert to iterative if needed). Traversals are O(n) time.

### Pitfalls
- Mixing "update a global best" with "return value" — keep the two roles explicit (nonlocal/`self.best` vs return).
- Validate-BST with duplicate values: decide strict vs non-strict bounds up front.
- Level-order: snapshot `len(queue)` BEFORE the inner loop.

## Easy
- Maximum Depth of Binary Tree (LC 104)
- Invert Binary Tree (LC 226)
- Same Tree (LC 100)
- Symmetric Tree (LC 101)
- Subtree of Another Tree (LC 572)
- Diameter of Binary Tree (LC 543)
- Balanced Binary Tree (LC 110)
- Merge Two Binary Trees (LC 617)

## Medium
- Binary Tree Level Order Traversal (LC 102)
- Validate Binary Search Tree (LC 98)
- Kth Smallest Element in a BST (LC 230)
- Lowest Common Ancestor of a BST (LC 235)
- Lowest Common Ancestor of a Binary Tree (LC 236)
- Construct Binary Tree from Preorder and Inorder (LC 105)
- Binary Tree Right Side View (LC 199)
- Count Good Nodes in Binary Tree (LC 1448)
- Path Sum II (LC 113)
- Binary Tree Zigzag Level Order Traversal (LC 103)
- Delete Node in a BST (LC 450)

## Hard
- Binary Tree Maximum Path Sum (LC 124)
- Serialize and Deserialize Binary Tree (LC 297)
- Recover Binary Search Tree (LC 99)

## Solve Log

| Date | Problem | LC# | Difficulty | Result | Hints | Time-Space | Notes |
|------|---------|-----|------------|--------|-------|------------|-------|
