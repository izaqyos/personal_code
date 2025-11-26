"""
Week 7, Day 7: Review & Challenge - Graph and Tree Problems

Learning Objectives:
- Review all Week 7 concepts
- Apply graph and tree algorithms
- Solve complex problems
- Practice algorithm selection
- Build complete solutions

Challenge: Solve real-world graph and tree problems

Time: 15-20 minutes
"""

from collections import defaultdict, deque
import heapq

# ============================================================
# REVIEW: Week 7 Concepts
# ============================================================

def week7_review():
    """Quick review of all Week 7 concepts"""
    print("=" * 60)
    print("WEEK 7 REVIEW")
    print("=" * 60)
    
    print("\nDay 1: Graph Representation")
    print("  • Adjacency list, matrix, edge list")
    print("  • Directed vs undirected")
    print("  • Weighted vs unweighted")
    
    print("\nDay 2: BFS and DFS")
    print("  • BFS: Level-order, shortest path")
    print("  • DFS: Deep exploration, topological sort")
    print("  • Both: O(V + E)")
    
    print("\nDay 3: Binary Trees")
    print("  • Inorder, preorder, postorder")
    print("  • Level-order traversal")
    print("  • Tree properties")
    
    print("\nDay 4: Binary Search Trees")
    print("  • BST property: Left < Root < Right")
    print("  • Search, insert, delete: O(h)")
    print("  • Inorder gives sorted order")
    
    print("\nDay 5: Dijkstra's Algorithm")
    print("  • Shortest path in weighted graphs")
    print("  • O((V + E) log V) with heap")
    print("  • No negative weights")
    
    print("\nDay 6: Trie")
    print("  • Prefix tree for strings")
    print("  • Autocomplete, spell check")
    print("  • O(m) operations")
    
    print("\n" + "=" * 60)
    print()

# ============================================================
# CHALLENGE 1: Course Schedule (Topological Sort)
# ============================================================

def course_schedule():
    """
    Determine if courses can be completed.
    
    TODO: Detect cycle in directed graph
    """
    print("--- Challenge 1: Course Schedule ---")
    
    def can_finish(num_courses, prerequisites):
        """Check if all courses can be completed"""
        # Build graph
        graph = defaultdict(list)
        for course, prereq in prerequisites:
            graph[prereq].append(course)
        
        # Track visit states: 0=unvisited, 1=visiting, 2=visited
        state = [0] * num_courses
        
        def has_cycle(course):
            """DFS to detect cycle"""
            if state[course] == 1:
                return True  # Cycle detected
            if state[course] == 2:
                return False  # Already processed
            
            state[course] = 1  # Mark as visiting
            
            for next_course in graph[course]:
                if has_cycle(next_course):
                    return True
            
            state[course] = 2  # Mark as visited
            return False
        
        # Check each course
        for course in range(num_courses):
            if state[course] == 0:
                if has_cycle(course):
                    return False
        
        return True
    
    test_cases = [
        (2, [[1, 0]]),
        (2, [[1, 0], [0, 1]]),
        (4, [[1, 0], [2, 0], [3, 1], [3, 2]])
    ]
    
    for num_courses, prereqs in test_cases:
        result = can_finish(num_courses, prereqs)
        print(f"Courses: {num_courses}, Prerequisites: {prereqs}")
        print(f"  Can finish: {result}\n")
    
    print()

# ============================================================
# CHALLENGE 2: Clone Graph
# ============================================================

def clone_graph():
    """
    Deep clone a graph.
    
    TODO: Clone graph with DFS/BFS
    """
    print("--- Challenge 2: Clone Graph ---")
    
    class Node:
        def __init__(self, val=0, neighbors=None):
            self.val = val
            self.neighbors = neighbors if neighbors else []
    
    def clone_graph_dfs(node):
        """Clone graph using DFS"""
        if not node:
            return None
        
        clones = {}
        
        def dfs(node):
            if node in clones:
                return clones[node]
            
            clone = Node(node.val)
            clones[node] = clone
            
            for neighbor in node.neighbors:
                clone.neighbors.append(dfs(neighbor))
            
            return clone
        
        return dfs(node)
    
    # Create sample graph
    node1 = Node(1)
    node2 = Node(2)
    node3 = Node(3)
    node1.neighbors = [node2, node3]
    node2.neighbors = [node1, node3]
    node3.neighbors = [node1, node2]
    
    print("Original graph:")
    print(f"  Node 1 neighbors: {[n.val for n in node1.neighbors]}")
    
    cloned = clone_graph_dfs(node1)
    print(f"\nCloned graph:")
    print(f"  Node 1 neighbors: {[n.val for n in cloned.neighbors]}")
    print(f"  Different objects: {cloned is not node1}")
    
    print()

# ============================================================
# CHALLENGE 3: Word Ladder
# ============================================================

def word_ladder():
    """
    Find shortest transformation sequence.
    
    TODO: BFS on word graph
    """
    print("--- Challenge 3: Word Ladder ---")
    
    def ladder_length(begin_word, end_word, word_list):
        """Find shortest transformation length"""
        if end_word not in word_list:
            return 0
        
        word_set = set(word_list)
        queue = deque([(begin_word, 1)])
        visited = {begin_word}
        
        while queue:
            word, length = queue.popleft()
            
            if word == end_word:
                return length
            
            # Try all one-letter changes
            for i in range(len(word)):
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    next_word = word[:i] + c + word[i+1:]
                    
                    if next_word in word_set and next_word not in visited:
                        visited.add(next_word)
                        queue.append((next_word, length + 1))
        
        return 0
    
    begin = "hit"
    end = "cog"
    word_list = ["hot", "dot", "dog", "lot", "log", "cog"]
    
    print(f"Begin: '{begin}'")
    print(f"End: '{end}'")
    print(f"Word list: {word_list}")
    
    length = ladder_length(begin, end, word_list)
    print(f"\nShortest transformation: {length} steps")
    
    print()

# ============================================================
# CHALLENGE 4: Serialize and Deserialize Binary Tree
# ============================================================

def serialize_deserialize():
    """
    Serialize and deserialize binary tree.
    
    TODO: Convert tree to/from string
    """
    print("--- Challenge 4: Serialize/Deserialize Tree ---")
    
    class TreeNode:
        def __init__(self, val=0, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right
    
    class Codec:
        """Codec for tree serialization"""
        
        def serialize(self, root):
            """Serialize tree to string"""
            if not root:
                return "null"
            
            left = self.serialize(root.left)
            right = self.serialize(root.right)
            return f"{root.val},{left},{right}"
        
        def deserialize(self, data):
            """Deserialize string to tree"""
            def helper(values):
                val = next(values)
                if val == "null":
                    return None
                
                node = TreeNode(int(val))
                node.left = helper(values)
                node.right = helper(values)
                return node
            
            return helper(iter(data.split(',')))
    
    # Create tree
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.right.left = TreeNode(4)
    root.right.right = TreeNode(5)
    
    codec = Codec()
    serialized = codec.serialize(root)
    print(f"Serialized: {serialized}")
    
    deserialized = codec.deserialize(serialized)
    reserialized = codec.serialize(deserialized)
    print(f"Reserialized: {reserialized}")
    print(f"Match: {serialized == reserialized}")
    
    print()

# ============================================================
# CHALLENGE 5: Network Delay Time
# ============================================================

def network_delay():
    """
    Find time for signal to reach all nodes.
    
    TODO: Dijkstra to find max distance
    """
    print("--- Challenge 5: Network Delay Time ---")
    
    def network_delay_time(times, n, k):
        """Find time for signal to reach all nodes"""
        # Build graph
        graph = defaultdict(list)
        for u, v, w in times:
            graph[u].append((v, w))
        
        # Dijkstra
        distances = {i: float('inf') for i in range(1, n + 1)}
        distances[k] = 0
        pq = [(0, k)]
        visited = set()
        
        while pq:
            time, node = heapq.heappop(pq)
            
            if node in visited:
                continue
            
            visited.add(node)
            
            for neighbor, weight in graph[node]:
                new_time = time + weight
                if new_time < distances[neighbor]:
                    distances[neighbor] = new_time
                    heapq.heappush(pq, (new_time, neighbor))
        
        max_time = max(distances.values())
        return max_time if max_time != float('inf') else -1
    
    times = [[2, 1, 1], [2, 3, 1], [3, 4, 1]]
    n = 4
    k = 2
    
    print(f"Network: {n} nodes")
    print(f"Times: {times}")
    print(f"Start: node {k}")
    
    delay = network_delay_time(times, n, k)
    print(f"\nDelay time: {delay}")
    
    print()

# ============================================================
# CHALLENGE 6: Implement Trie with Prefix Count
# ============================================================

def trie_prefix_count():
    """
    Trie that counts words with prefix.
    
    TODO: Track prefix counts
    """
    print("--- Challenge 6: Trie with Prefix Count ---")
    
    class PrefixTrie:
        """Trie with prefix counting"""
        
        def __init__(self):
            self.root = {'count': 0, 'end': 0}
        
        def insert(self, word):
            """Insert word"""
            node = self.root
            for char in word:
                if char not in node:
                    node[char] = {'count': 0, 'end': 0}
                node = node[char]
                node['count'] += 1
            node['end'] += 1
        
        def count_words_equal_to(self, word):
            """Count words equal to word"""
            node = self.root
            for char in word:
                if char not in node:
                    return 0
                node = node[char]
            return node['end']
        
        def count_words_starting_with(self, prefix):
            """Count words starting with prefix"""
            node = self.root
            for char in prefix:
                if char not in node:
                    return 0
                node = node[char]
            return node['count']
    
    trie = PrefixTrie()
    words = ["apple", "apple", "app", "apricot", "application"]
    
    print(f"Words: {words}")
    for word in words:
        trie.insert(word)
    
    print(f"\nCount 'apple': {trie.count_words_equal_to('apple')}")
    print(f"Count 'app': {trie.count_words_equal_to('app')}")
    print(f"Count starting with 'app': {trie.count_words_starting_with('app')}")
    print(f"Count starting with 'apr': {trie.count_words_starting_with('apr')}")
    
    print()

# ============================================================
# CHALLENGE 7: Binary Tree Maximum Path Sum
# ============================================================

def max_path_sum():
    """
    Find maximum path sum in binary tree.
    
    TODO: Use DFS with global maximum
    """
    print("--- Challenge 7: Maximum Path Sum ---")
    
    class TreeNode:
        def __init__(self, val=0, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right
    
    def max_path_sum_tree(root):
        """Find maximum path sum"""
        max_sum = [float('-inf')]
        
        def max_gain(node):
            """Max gain from node"""
            if not node:
                return 0
            
            # Max gain from left and right (ignore negative)
            left_gain = max(max_gain(node.left), 0)
            right_gain = max(max_gain(node.right), 0)
            
            # Path through node
            path_sum = node.val + left_gain + right_gain
            max_sum[0] = max(max_sum[0], path_sum)
            
            # Return max gain if continuing path
            return node.val + max(left_gain, right_gain)
        
        max_gain(root)
        return max_sum[0]
    
    # Create tree: -10, 9, 20, null, null, 15, 7
    root = TreeNode(-10)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    
    print("Tree structure:")
    print("      -10")
    print("      /  \\")
    print("     9    20")
    print("         /  \\")
    print("        15   7")
    
    max_sum_val = max_path_sum_tree(root)
    print(f"\nMaximum path sum: {max_sum_val}")
    print("(Path: 15 -> 20 -> 7)")
    
    print()

# ============================================================
# SELF-ASSESSMENT
# ============================================================

def self_assessment():
    """Self-assessment checklist for Week 7"""
    print("=" * 60)
    print("WEEK 7 SELF-ASSESSMENT")
    print("=" * 60)
    
    checklist = [
        ("Graphs", "Can you represent and traverse graphs?"),
        ("BFS/DFS", "Do you understand when to use each?"),
        ("Trees", "Can you implement tree traversals?"),
        ("BST", "Do you understand BST operations?"),
        ("Dijkstra", "Can you find shortest paths?"),
        ("Trie", "Can you implement prefix operations?"),
        ("Problem Solving", "Can you choose the right algorithm?"),
    ]
    
    print("\nRate yourself (1-5) on these concepts:\n")
    for i, (topic, question) in enumerate(checklist, 1):
        print(f"{i}. {topic}")
        print(f"   {question}")
        print()
    
    print("=" * 60)
    print()

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 7, Day 7: Review & Challenge")
    print("=" * 60)
    print()
    
    week7_review()
    
    print("\n" + "=" * 60)
    print("CHALLENGES")
    print("=" * 60 + "\n")
    
    course_schedule()
    clone_graph()
    word_ladder()
    serialize_deserialize()
    network_delay()
    trie_prefix_count()
    max_path_sum()
    
    self_assessment()
    
    print("=" * 60)
    print("✅ Week 7 Complete!")
    print("=" * 60)
    print("\n🎉 Congratulations! You've mastered graphs and trees!")
    print("\n📚 Next: Week 8 - Dynamic Programming")
    print("\n💡 Keep practicing these fundamental data structures!")

