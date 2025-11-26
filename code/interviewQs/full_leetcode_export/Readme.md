# LeetCode Solutions & Backup Guide

A comprehensive collection of solved LeetCode problems with detailed classifications, interview recommendations, and a guide for backing up your solutions using `leetcode-export`.

> ⚠️ **Note:** LeetCode problem statements are copyrighted. Keep this backup **private** and don't publish it publicly.

---

## Table of Contents

- [Problems Solved - Classification \& Analysis](#problems-solved---classification--analysis)
  - [Summary Statistics](#summary-statistics)
  - [Classification by Topic](#classification-by-topic)
    - [Arrays \& Strings](#arrays--strings)
    - [Linked Lists](#linked-lists)
    - [Binary Trees \& BST](#binary-trees--bst)
    - [Dynamic Programming](#dynamic-programming)
    - [Graph \& BFS/DFS](#graph--bfsdfs)
    - [Backtracking \& Recursion](#backtracking--recursion)
    - [Math \& Bit Manipulation](#math--bit-manipulation)
    - [Stack \& Queue](#stack--queue)
    - [Heap \& Priority Queue](#heap--priority-queue)
    - [Binary Search](#binary-search)
    - [Trie](#trie)
    - [Design \& Data Structures](#design--data-structures)
    - [Greedy](#greedy)
    - [Game Theory \& Minimax](#game-theory--minimax)
    - [String Matching](#string-matching)
    - [JavaScript/TypeScript Specific](#javascripttypescript-specific)
    - [Miscellaneous](#miscellaneous)
- [Recommended Future Problems](#recommended-future-problems)
  - [Top 20 Must-Do Problems](#-top-20-must-do-problems-you-havent-solved)
  - [By Pattern/Topic](#-by-patterntopic-filling-your-gaps)
  - [Easy Problems](#-easy-problems-quick-wins---fundamental-skills)
  - [Medium Problems](#-medium-problems-core-interview-problems)
  - [Hard Problems](#-hard-problems-seniorstaff-level)
  - [Study Plan Recommendation](#-study-plan-recommendation)
- [Focused Study Plans by Subject](#-focused-study-plans-by-subject)
  - [1. Linked Lists](#1️⃣-linked-lists-5-7-days)
  - [2. Arrays \& Strings](#2️⃣-arrays--strings-10-14-days)
  - [3. Dynamic Programming](#3️⃣-dynamic-programming-12-15-days)
  - [4. Memoization \& Optimization](#4️⃣-memoization--optimization-techniques-3-4-days)
  - [5. Binary Trees \& BST](#5️⃣-binary-trees--bst-8-10-days)
  - [6. Graphs](#6️⃣-graphs-10-12-days)
  - [7. Heaps \& Priority Queues](#7️⃣-heaps--priority-queues-4-5-days)
  - [8. Hash Tables](#8️⃣-hash-tables--hash-maps-3-4-days)
  - [9. Stack \& Queue](#9️⃣-stack--queue-4-5-days)
  - [10. Binary Search](#-binary-search-5-6-days)
  - [11. Tries](#1️⃣1️⃣-tries-4-5-days)
  - [12. Backtracking](#1️⃣2️⃣-backtracking-5-6-days)
  - [13. Greedy Algorithms](#1️⃣3️⃣-greedy-algorithms-4-5-days)
  - [14. Design Problems](#1️⃣4️⃣-design-problems-5-6-days)
  - [15. Bit Manipulation](#1️⃣5️⃣-bit-manipulation-3-4-days)
  - [Suggested Learning Order](#-suggested-learning-order-overall-priority)
  - [Progress Tracking Template](#-progress-tracking-template)
- [Interview Problems for Candidates](#interview-problems-for-candidates)
  - [Easy Level Problems](#easy-level-problems-3-problems)
    - [Problem 1: Two Sum](#problem-1-two-sum-1)
    - [Problem 2: Valid Parentheses](#problem-2-valid-parentheses-20)
    - [Problem 3: Merge Two Sorted Lists](#problem-3-merge-two-sorted-lists-21)
  - [Medium Level Problems](#medium-level-problems-3-problems)
    - [Problem 1: LRU Cache](#problem-1-lru-cache-146)
    - [Problem 2: Course Schedule](#problem-2-course-schedule-207)
    - [Problem 3: Longest Consecutive Sequence](#problem-3-longest-consecutive-sequence-128)
- [Complexity Analysis Summary](#complexity-analysis-summary)
  - [Time Complexity Hierarchy](#time-complexity-hierarchy-best-to-worst)
  - [Space Complexity Considerations](#space-complexity-considerations)
  - [Common Trade-offs](#common-trade-offs)
- [Interview Tips](#interview-tips)
  - [For Interviewers](#for-interviewers-evaluating-candidates)
  - [Problem Difficulty Guidelines](#problem-difficulty-guidelines)
  - [Red Flags \& Green Flags](#red-flags--green-flags)
- [Backup Instructions](#backup-instructions)
  - [Prerequisites](#prerequisites)
  - [Setup \& Installation](#setup--installation)
  - [Export Your Solutions](#export-your-solutions)
  - [Advanced Options](#advanced-options)
  - [Troubleshooting](#troubleshooting)

---

## Problems Solved - Classification & Analysis

### Summary Statistics
- **Total Problems Solved:** 197
- **Easy:** ~60 problems
- **Medium:** ~110 problems
- **Hard:** ~27 problems

### Classification by Topic

#### Arrays & Strings (48 problems)
**Easy:**
- #1 Two Sum
- #26 Remove Duplicates from Sorted Array
- #27 Remove Element
- #58 Length of Last Word
- #66 Plus One
- #67 Add Binary
- #88 Merge Sorted Array
- #169 Majority Element
- #189 Rotate Array
- #349 Intersection of Two Arrays

**Medium:**
- #3 Longest Substring Without Repeating Characters
- #11 Container With Most Water
- #15 3Sum
- #16 3Sum Closest
- #18 4Sum
- #48 Rotate Image
- #49 Group Anagrams
- #54 Spiral Matrix
- #56 Merge Intervals
- #57 Insert Interval
- #59 Spiral Matrix II
- #73 Set Matrix Zeroes
- #75 Sort Colors
- #151 Reverse Words in a String
- #189 Rotate Array
- #209 Minimum Size Subarray Sum
- #443 String Compression
- #807 Custom Sort String
- #1046 Max Consecutive Ones III
- #1464 Reduce Array Size to The Half

**Hard:**
- #4 Median of Two Sorted Arrays
- #30 Substring with Concatenation of All Words
- #41 First Missing Positive
- #42 Trapping Rain Water
- #76 Minimum Window Substring
- #84 Largest Rectangle in Histogram
- #85 Maximal Rectangle

#### Linked Lists (13 problems)
**Easy:**
- #21 Merge Two Sorted Lists
- #83 Remove Duplicates from Sorted List
- #141 Linked List Cycle

**Medium:**
- #2 Add Two Numbers
- #19 Remove Nth Node From End of List
- #24 Swap Nodes in Pairs
- #61 Rotate List
- #82 Remove Duplicates from Sorted List II
- #86 Partition List
- #92 Reverse Linked List II
- #148 Sort List

**Hard:**
- #23 Merge k Sorted Lists
- #25 Reverse Nodes in k-Group

#### Binary Trees & BST (22 problems)
**Easy:**
- #100 Same Tree
- #101 Symmetric Tree
- #235 Lowest Common Ancestor of a Binary Search Tree
- #501 Find Mode in Binary Search Tree
- #543 Diameter of Binary Tree
- #563 Binary Tree Tilt
- #653 Two Sum IV - Input is a BST

**Medium:**
- #94 Binary Tree Inorder Traversal
- #113 Path Sum II
- #114 Flatten Binary Tree to Linked List
- #129 Sum Root to Leaf Numbers
- #1050 Construct Binary Search Tree from Preorder Traversal
- #1568 Pseudo-Palindromic Paths in a Binary Tree

**Hard:**
- #124 Binary Tree Maximum Path Sum

#### Dynamic Programming (28 problems)
**Easy:**
- #70 Climbing Stairs
- #121 Best Time to Buy and Sell Stock
- #198 House Robber
- #303 Range Sum Query - Immutable
- #338 Counting Bits
- #740 Delete and Earn
- #747 Min Cost Climbing Stairs
- #1013 Fibonacci Number
- #1236 N-th Tribonacci Number

**Medium:**
- #5 Longest Palindromic Substring
- #62 Unique Paths
- #63 Unique Paths II
- #64 Minimum Path Sum
- #91 Decode Ways
- #120 Triangle
- #122 Best Time to Buy and Sell Stock II
- #139 Word Break
- #221 Maximal Square
- #300 Longest Increasing Subsequence
- #343 Integer Break
- #368 Largest Divisible Subset
- #416 Partition Equal Subset Sum
- #718 Maximum Length of Repeated Subarray
- #962 Flip String to Monotone Increasing
- #967 Minimum Falling Path Sum

**Hard:**
- #72 Edit Distance
- #1669 Minimum Cost to Cut a Stick

#### Graph & BFS/DFS (8 problems)
**Easy:**
- #2121 Find if Path Exists in Graph

**Medium:**
- #1171 Shortest Path in Binary Matrix
- #310 Minimum Height Trees

**Hard:**
- #1414 Shortest Path in a Grid with Obstacles Elimination
- #1986 Largest Color Value in a Directed Graph
- #2505 Number of Good Paths

#### Backtracking & Recursion (12 problems)
**Medium:**
- #17 Letter Combinations of a Phone Number
- #22 Generate Parentheses
- #39 Combination Sum
- #40 Combination Sum II
- #46 Permutations
- #47 Permutations II
- #77 Combinations
- #78 Subsets
- #79 Word Search
- #90 Subsets II

**Hard:**
- #51 N-Queens
- #52 N-Queens II

#### Math & Bit Manipulation (15 problems)
**Easy:**
- #7 Reverse Integer
- #9 Palindrome Number
- #13 Roman to Integer
- #66 Plus One
- #69 Sqrt(x)
- #191 Number of 1 Bits
- #202 Happy Number
- #342 Power of Four

**Medium:**
- #6 Zigzag Conversion
- #8 String to Integer (atoi)
- #12 Integer to Roman
- #29 Divide Two Integers
- #43 Multiply Strings
- #50 Pow(x, n)
- #371 Sum of Two Integers
- #372 Super Pow

#### Stack & Queue (7 problems)
**Easy:**
- #20 Valid Parentheses

**Medium:**
- #71 Simplify Path
- #227 Basic Calculator II
- #739 Daily Temperatures
- #886 Score of Parentheses
- #1128 Remove All Adjacent Duplicates In String

#### Heap & Priority Queue (5 problems)
**Medium:**
- #215 Kth Largest Element in an Array
- #347 Top K Frequent Elements
- #373 Find K Pairs with Smallest Sums
- #378 Kth Smallest Element in a Sorted Matrix

**Hard:**
- #218 The Skyline Problem

#### Binary Search (8 problems)
**Easy:**
- #35 Search Insert Position
- #69 Sqrt(x)

**Medium:**
- #33 Search in Rotated Sorted Array
- #34 Find First and Last Position of Element in Sorted Array
- #74 Search a 2D Matrix
- #162 Find Peak Element
- #167 Two Sum II - Input Array Is Sorted

#### Trie (1 problem)
**Medium:**
- #208 Implement Trie (Prefix Tree)

#### Design & Data Structures (3 problems)
**Medium:**
- #307 Range Sum Query - Mutable
- #341 Flatten Nested List Iterator

#### Greedy (5 problems)
**Medium:**
- #45 Jump Game II
- #55 Jump Game
- #611 Valid Triangle Number
- #917 Boats to Save People

#### Game Theory & Minimax (2 problems)
**Medium:**
- #375 Guess Number Higher or Lower II
- #909 Stone Game

#### String Matching (6 problems)
**Easy:**
- #14 Longest Common Prefix
- #28 Find the Index of the First Occurrence in a String
- #205 Isomorphic Strings

**Medium:**
- #299 Bulls and Cows

**Hard:**
- #10 Regular Expression Matching
- #44 Wildcard Matching
- #68 Text Justification

#### JavaScript/TypeScript Specific (30 problems)
- #2731 Memoize
- #2732 Counter
- #2733 Sleep
- #2734 Array Prototype Last
- #2741 Function Composition
- #2742 Group By
- #2743 Debounce
- #2746 Filter Elements from Array
- #2747 Apply Transform Over Each Element in Array
- #2749 Promise Time Limit
- #2759 Flatten Deeply Nested Array
- #2761 Array Reduce Transformation
- #2762 Cache with Time Limit
- #2789 Counter II
- #2796 Allow One Function Call
- #2797 Event Emitter
- #2798 Chunk Array
- #2804 Compact Object
- #2805 Array Wrapper
- #2807 Execute Asynchronous Functions in Parallel
- #2813 To Be Or Not To Be
- #2820 Return Length of Arguments Passed
- #2821 Timeout Cancellation
- #2858 Join Two Arrays by ID
- #2859 Add Two Promises
- #2860 Sort By
- #2862 Interval Cancellation
- #2864 Is Object Empty

#### Miscellaneous (8 problems)
**Easy:**
- #36 Valid Sudoku
- #1297 Maximum Number of Balloons
- #1584 Average Salary Excluding the Minimum and Maximum Salary

**Medium:**
- #31 Next Permutation
- #38 Count and Say
- #60 Permutation Sequence
- #331 Verify Preorder Serialization of a Binary Tree
- #1534 Minimum Number of Frogs Croaking

**Concurrency (2 problems):**
- #1187 Print FooBar Alternately
- #1203 Print in Order

---

## Recommended Future Problems

Based on your 197 solved problems, here are strategic recommendations to fill gaps and strengthen interview preparation:

### 🎯 Top 20 Must-Do Problems (You Haven't Solved)

These are extremely common in FAANG interviews:

1. **#206 Reverse Linked List** (Easy) - Fundamental, asked in 60% of interviews
2. **#200 Number of Islands** (Medium) - Classic DFS/BFS, matrix traversal
3. **#146 LRU Cache** (Medium) - System design favorite, tests multiple concepts
4. **#102 Binary Tree Level Order Traversal** (Medium) - BFS fundamentals
5. **#98 Validate Binary Search Tree** (Medium) - Tree properties, very common
6. **#236 Lowest Common Ancestor of Binary Tree** (Medium) - Advanced tree traversal
7. **#297 Serialize/Deserialize Binary Tree** (Hard) - Tree design, DFS/BFS
8. **#138 Copy List with Random Pointer** (Medium) - Linked list + hash map
9. **#322 Coin Change** (Medium) - DP classic, unbounded knapsack
10. **#152 Maximum Product Subarray** (Medium) - DP variant, tricky edge cases
11. **#295 Find Median from Data Stream** (Hard) - Two heaps pattern
12. **#85 Maximal Rectangle** (Hard) - You solved #221, this is the harder version
13. **#105 Construct Binary Tree from Preorder/Inorder** (Medium) - Tree construction
14. **#239 Sliding Window Maximum** (Hard) - Monotonic deque
15. **#212 Word Search II** (Hard) - Trie + backtracking (you solved #79)
16. **#128 Longest Consecutive Sequence** (Medium) - O(n) optimization
17. **#621 Task Scheduler** (Medium) - Greedy/heap problem
18. **#253 Meeting Rooms II** (Medium) - Interval scheduling (Premium but worth it)
19. **#301 Remove Invalid Parentheses** (Hard) - BFS/backtracking
20. **#127 Word Ladder** (Hard) - BFS in graph of words

---

### 📊 By Pattern/Topic (Filling Your Gaps)

#### Sliding Window (Critical Pattern - You Need More Practice)
You solved: #3, #76, #209, #1046
**Recommended:**
- **#424 Longest Repeating Character Replacement** (Medium) - Variable window
- **#438 Find All Anagrams in String** (Medium) - Fixed window with hash map
- **#76 Minimum Window Substring** (Hard) - You solved this! ✓
- **#3 Longest Substring Without Repeating Characters** (Medium) - You solved this! ✓
- **#567 Permutation in String** (Medium) - Similar to #438
- **#992 Subarrays with K Different Integers** (Hard) - Advanced sliding window

#### Two Pointers (Need More)
You solved: #15, #16, #18, #167
**Recommended:**
- **#11 Container With Most Water** (Medium) - You solved this! ✓
- **#283 Move Zeroes** (Easy) - In-place array manipulation
- **#26 Remove Duplicates** (Easy) - You solved this! ✓
- **#142 Linked List Cycle II** (Medium) - Floyd's algorithm advanced
- **#287 Find the Duplicate Number** (Medium) - Floyd's in array
- **#75 Sort Colors** (Medium) - You solved this! (Dutch National Flag) ✓

#### Union-Find / Disjoint Set (Major Gap)
You solved: #2121, #2505
**Recommended:**
- **#200 Number of Islands** (Medium) - Can solve with Union-Find
- **#547 Number of Provinces** (Medium) - Classic Union-Find
- **#684 Redundant Connection** (Medium) - Cycle detection in undirected graph
- **#721 Accounts Merge** (Medium) - String grouping with Union-Find
- **#323 Number of Connected Components** (Medium, Premium) - Fundamental
- **#1584 Min Cost to Connect All Points** (Medium) - MST with Union-Find

#### Advanced Tree Problems
You solved many tree problems! Here are challenging ones:
- **#297 Serialize/Deserialize Binary Tree** (Hard) - Design
- **#236 Lowest Common Ancestor** (Medium) - More general than #235
- **#102 Binary Tree Level Order Traversal** (Medium) - BFS basics
- **#199 Binary Tree Right Side View** (Medium) - BFS variant
- **#105 Construct Tree from Preorder/Inorder** (Medium) - Tree construction
- **#450 Delete Node in BST** (Medium) - BST modification
- **#230 Kth Smallest in BST** (Medium) - Inorder traversal

#### Advanced DP (You're Strong Here, But Missing Classics)
You solved 28 DP problems! Add these:
- **#322 Coin Change** (Medium) - Unbounded knapsack
- **#518 Coin Change II** (Medium) - Counting variant
- **#152 Maximum Product Subarray** (Medium) - Track min and max
- **#354 Russian Doll Envelopes** (Hard) - 2D LIS
- **#312 Burst Balloons** (Hard) - Interval DP
- **#115 Distinct Subsequences** (Hard) - String DP
- **#1143 Longest Common Subsequence** (Medium) - Classic LCS

#### Graph Algorithms (Need More Advanced)
You solved: #1171, #310, #1414, #1986, #2121, #2505
**Recommended:**
- **#200 Number of Islands** (Medium) - Must know!
- **#207 Course Schedule** (Medium) - You need this for topological sort
- **#210 Course Schedule II** (Medium) - Returns the ordering
- **#133 Clone Graph** (Medium) - Graph traversal + cloning
- **#399 Evaluate Division** (Medium) - Graph with weighted edges
- **#785 Is Graph Bipartite?** (Medium) - BFS/DFS with coloring
- **#743 Network Delay Time** (Medium) - Dijkstra's algorithm
- **#787 Cheapest Flights Within K Stops** (Medium) - BFS with constraints

#### Heap / Priority Queue (Light Coverage)
You solved: #215, #218, #347, #373, #378
**Recommended:**
- **#295 Find Median from Data Stream** (Hard) - Two heaps (max + min)
- **#23 Merge k Sorted Lists** (Hard) - You solved this! ✓
- **#621 Task Scheduler** (Medium) - Greedy with heap
- **#355 Design Twitter** (Medium) - Design with heap for feed
- **#767 Reorganize String** (Medium) - Greedy with heap
- **#1094 Car Pooling** (Medium) - Interval with heap/sweep line

#### Monotonic Stack/Queue (Major Gap)
You solved: #739, #84, #85
**Recommended:**
- **#239 Sliding Window Maximum** (Hard) - Monotonic deque
- **#739 Daily Temperatures** (Medium) - You solved this! ✓
- **#84 Largest Rectangle in Histogram** (Hard) - You solved this! ✓
- **#42 Trapping Rain Water** (Hard) - You solved this! ✓
- **#496 Next Greater Element I** (Easy) - Introduction to pattern
- **#503 Next Greater Element II** (Medium) - Circular array
- **#901 Online Stock Span** (Medium) - Monotonic stack application

#### Trie (Only 1 Solved!)
You solved: #208
**Recommended:**
- **#212 Word Search II** (Hard) - Trie + backtracking
- **#211 Design Add and Search Words** (Medium) - Trie with wildcard
- **#648 Replace Words** (Medium) - Trie for prefix matching
- **#677 Map Sum Pairs** (Medium) - Trie with values
- **#336 Palindrome Pairs** (Hard) - Advanced trie

#### Binary Search (You Have Good Coverage)
You solved: #33, #34, #35, #69, #74, #162, #167
**Recommended:**
- **#410 Split Array Largest Sum** (Hard) - Binary search on answer
- **#875 Koko Eating Bananas** (Medium) - Binary search pattern
- **#1011 Capacity To Ship Packages Within D Days** (Medium) - Similar to #410
- **#4 Median of Two Sorted Arrays** (Hard) - You solved this! ✓

#### Design Problems (Critical for Interviews)
You solved: #208, #307, #341, #2762, #2797
**Recommended:**
- **#146 LRU Cache** (Medium) - Most important design problem
- **#380 Insert Delete GetRandom O(1)** (Medium) - Array + hash map
- **#295 Find Median from Data Stream** (Hard) - Two heaps
- **#353 Design Snake Game** (Medium, Premium) - Queue + set
- **#362 Design Hit Counter** (Medium, Premium) - Time-based design
- **#1797 Design Authentication Manager** (Medium) - Hash map with expiry

---

### 🎯 Easy Problems (Quick Wins - Fundamental Skills)
1. **#206 Reverse Linked List** - Most asked easy problem
2. **#226 Invert Binary Tree** - Classic tree recursion
3. **#104 Maximum Depth of Binary Tree** - Tree basics
4. **#283 Move Zeroes** - Two pointers in-place
5. **#242 Valid Anagram** - Hash map basics
6. **#217 Contains Duplicate** - Hash set
7. **#268 Missing Number** - Math/XOR trick
8. **#136 Single Number** - XOR bit manipulation
9. **#108 Convert Sorted Array to BST** - Tree construction
10. **#110 Balanced Binary Tree** - Tree property checking

---

### 🔥 Medium Problems (Core Interview Problems)
1. **#200 Number of Islands** - #1 most asked medium
2. **#146 LRU Cache** - Design + data structures
3. **#102 Binary Tree Level Order Traversal** - BFS template
4. **#98 Validate Binary Search Tree** - Tree properties
5. **#322 Coin Change** - DP classic
6. **#236 Lowest Common Ancestor of Binary Tree** - Tree recursion
7. **#207 Course Schedule** - Topological sort
8. **#138 Copy List with Random Pointer** - Linked list + cloning
9. **#105 Construct Binary Tree from Preorder/Inorder** - Tree construction
10. **#152 Maximum Product Subarray** - DP variant
11. **#560 Subarray Sum Equals K** - Prefix sum
12. **#438 Find All Anagrams in String** - Sliding window
13. **#394 Decode String** - Stack recursion
14. **#200 Rotate Array** - Array manipulation (you solved #189) ✓
15. **#128 Longest Consecutive Sequence** - O(n) hash set

---

### 💀 Hard Problems (Senior/Staff Level)
1. **#297 Serialize/Deserialize Binary Tree** - Most important hard
2. **#295 Find Median from Data Stream** - Two heaps
3. **#239 Sliding Window Maximum** - Monotonic deque
4. **#212 Word Search II** - Trie + backtracking
5. **#127 Word Ladder** - BFS shortest path
6. **#124 Binary Tree Maximum Path Sum** - You solved this! ✓
7. **#329 Longest Increasing Path in Matrix** - DFS + memoization
8. **#301 Remove Invalid Parentheses** - BFS/DFS
9. **#312 Burst Balloons** - Interval DP
10. **#354 Russian Doll Envelopes** - 2D LIS

---

### 📈 Study Plan Recommendation

**Week 1-2: Fill Critical Gaps**
- Day 1-2: #206, #226, #104 (Easy tree/linked list fundamentals)
- Day 3-4: #200, #102 (BFS/DFS patterns)
- Day 5-7: #146, #138 (Design + cloning)

**Week 3-4: Core Mediums**
- Day 8-10: #98, #236, #105 (Advanced tree problems)
- Day 11-13: #322, #152, #560 (DP + prefix sum)
- Day 14: #207 (Topological sort)

**Week 5-6: Advanced Patterns**
- Day 15-17: #438, #567, #424 (Sliding window mastery)
- Day 18-20: #547, #684, #721 (Union-Find)
- Day 21: #295 (Two heaps)

**Week 7-8: Hard Problems**
- Day 22-24: #297, #212 (Tree design + trie)
- Day 25-27: #239, #295 (Advanced data structures)
- Day 28: Review and practice

---

## 📚 Focused Study Plans by Subject

Master one topic at a time with these structured learning paths. Each plan includes key concepts, progression from fundamentals to advanced, and estimated time.

Legend: ✅ = Solved | 🎯 = Priority | ⏰ = Time estimate

---

### 1️⃣ Linked Lists (5-7 days)

**Your Progress:** 13/20 Core Problems ✅ Good foundation!

**Key Concepts:**
- Pointer manipulation (next, prev)
- Dummy node technique
- Two pointers (fast/slow, runner technique)
- Reversing techniques
- Cycle detection (Floyd's algorithm)

**Study Order:**

**Day 1: Fundamentals (2-3 hours)**
- ✅ #21 Merge Two Sorted Lists (Easy) - Pointer basics
- 🎯 #206 Reverse Linked List (Easy) - **MUST DO**
- 🎯 #234 Palindrome Linked List (Easy) - Reverse + two pointers
- Practice: Write reversal from memory 3 times

**Day 2: Two Pointers Pattern (2-3 hours)**
- ✅ #141 Linked List Cycle (Easy) - Floyd's slow/fast
- 🎯 #142 Linked List Cycle II (Medium) - Find cycle start
- ✅ #19 Remove Nth Node From End (Medium)
- 🎯 #876 Middle of the Linked List (Easy)

**Day 3: Manipulation & Sorting (2-3 hours)**
- ✅ #24 Swap Nodes in Pairs (Medium)
- ✅ #82 Remove Duplicates from Sorted List II (Medium)
- ✅ #86 Partition List (Medium)
- ✅ #148 Sort List (Medium) - Merge sort on linked list

**Day 4: Advanced Techniques (3-4 hours)**
- ✅ #92 Reverse Linked List II (Medium) - Partial reversal
- 🎯 #138 Copy List with Random Pointer (Medium) - **Key problem**
- 🎯 #143 Reorder List (Medium) - Find mid + reverse + merge
- ✅ #61 Rotate List (Medium)

**Day 5: Hard Problems (3-4 hours)**
- ✅ #23 Merge k Sorted Lists (Hard) - Heap or divide & conquer
- ✅ #25 Reverse Nodes in k-Group (Hard) - Advanced reversal
- 🎯 #460 LFU Cache (Hard) - Design with doubly linked lists

**Practice Project:** Implement your own LinkedList class with all operations

---

### 2️⃣ Arrays & Strings (10-14 days)

**Your Progress:** 48/60 Core Problems ✅ Strong coverage!

**Key Concepts:**
- Two pointers
- Sliding window
- Prefix sum
- Kadane's algorithm
- Boyer-Moore (majority element)
- KMP (string matching)

#### Part A: Two Pointers (3 days)

**Day 1: Basic Two Pointers (2 hours)**
- ✅ #167 Two Sum II (Easy)
- 🎯 #283 Move Zeroes (Easy)
- ✅ #26 Remove Duplicates (Easy)
- 🎯 #344 Reverse String (Easy)

**Day 2: Meet in Middle (2-3 hours)**
- ✅ #15 3Sum (Medium) - Sort + two pointers
- ✅ #16 3Sum Closest (Medium)
- ✅ #18 4Sum (Medium)
- 🎯 #259 3Sum Smaller (Medium, Premium)

**Day 3: Advanced Applications (3 hours)**
- ✅ #11 Container With Most Water (Medium)
- 🎯 #42 Trapping Rain Water (Hard) - ✅ You solved this!
- 🎯 #287 Find Duplicate Number (Medium) - Floyd's in array

#### Part B: Sliding Window (4 days) **🚨 Critical Pattern**

**Day 4: Fixed Window (2-3 hours)**
- 🎯 #643 Maximum Average Subarray I (Easy)
- ✅ #1046 Max Consecutive Ones III (Medium)
- 🎯 #1456 Maximum Vowels in Substring (Medium)

**Day 5: Variable Window - Basic (3 hours)**
- ✅ #3 Longest Substring Without Repeating Characters (Medium)
- ✅ #209 Minimum Size Subarray Sum (Medium)
- 🎯 #904 Fruit Into Baskets (Medium)

**Day 6: Variable Window - Advanced (3-4 hours)**
- ✅ #76 Minimum Window Substring (Hard) - **Template problem**
- 🎯 #438 Find All Anagrams in String (Medium) - **Key pattern**
- 🎯 #567 Permutation in String (Medium)

**Day 7: Master Level (4 hours)**
- 🎯 #424 Longest Repeating Character Replacement (Medium)
- 🎯 #992 Subarrays with K Different Integers (Hard)
- 🎯 #1004 Max Consecutive Ones III (Medium)

#### Part C: Prefix Sum & Kadane (2 days)

**Day 8: Prefix Sum (2-3 hours)**
- ✅ #303 Range Sum Query (Easy)
- 🎯 #560 Subarray Sum Equals K (Medium) - **Very common**
- 🎯 #525 Contiguous Array (Medium)
- ✅ #307 Range Sum Query Mutable (Medium)

**Day 9: Kadane's Algorithm (2-3 hours)**
- ✅ #53 Maximum Subarray (Easy)
- 🎯 #152 Maximum Product Subarray (Medium) - **Must know**
- 🎯 #918 Maximum Sum Circular Subarray (Medium)

#### Part D: Advanced String (2 days)

**Day 10-11: Pattern Matching & Manipulation (3-4 hours)**
- ✅ #10 Regular Expression Matching (Hard)
- ✅ #44 Wildcard Matching (Hard)
- 🎯 #1044 Longest Duplicate Substring (Hard) - Rolling hash
- 🎯 #214 Shortest Palindrome (Hard) - KMP

---

### 3️⃣ Dynamic Programming (12-15 days)

**Your Progress:** 28/45 Core Problems ✅ Strong foundation, need advanced patterns!

**Key Concepts:**
- State definition & transitions
- Memoization (top-down) vs tabulation (bottom-up)
- Space optimization
- Common patterns: Knapsack, LIS, LCS, Palindrome, Tree DP

#### Part A: Fundamentals (2 days)

**Day 1: 1D DP Basics (2-3 hours)**
- ✅ #70 Climbing Stairs (Easy) - Basic recurrence
- ✅ #746 Min Cost Climbing Stairs (Easy)
- ✅ #198 House Robber (Easy)
- ✅ #740 Delete and Earn (Medium)

**Day 2: Fibonacci Variants (2 hours)**
- ✅ #1013 Fibonacci Number (Easy)
- ✅ #1236 Tribonacci Number (Easy)
- 🎯 #509 Fibonacci Number (Easy)
- Practice: Implement with and without memoization

#### Part B: Knapsack Pattern (3 days) **🚨 Critical**

**Day 3: 0/1 Knapsack (3 hours)**
- ✅ #416 Partition Equal Subset Sum (Medium) - **Template**
- 🎯 #494 Target Sum (Medium)
- 🎯 #1049 Last Stone Weight II (Medium)

**Day 4: Unbounded Knapsack (3 hours)**
- 🎯 #322 Coin Change (Medium) - **MUST DO**
- 🎯 #518 Coin Change II (Medium) - Counting combinations
- 🎯 #279 Perfect Squares (Medium)
- 🎯 #377 Combination Sum IV (Medium)

**Day 5: Multi-dimensional Knapsack (3-4 hours)**
- 🎯 #474 Ones and Zeroes (Medium)
- 🎯 #879 Profitable Schemes (Hard)

#### Part C: Sequences (3 days)

**Day 6: Longest Increasing Subsequence (3 hours)**
- ✅ #300 Longest Increasing Subsequence (Medium) - **Template**
- 🎯 #673 Number of LIS (Medium)
- 🎯 #354 Russian Doll Envelopes (Hard) - 2D LIS

**Day 7: Longest Common Subsequence (3 hours)**
- 🎯 #1143 Longest Common Subsequence (Medium) - **Classic**
- 🎯 #1092 Shortest Common Supersequence (Hard)
- 🎯 #583 Delete Operation for Two Strings (Medium)

**Day 8: Edit Distance (3 hours)**
- ✅ #72 Edit Distance (Hard) - **Interview favorite**
- 🎯 #712 Minimum ASCII Delete Sum (Medium)
- 🎯 #115 Distinct Subsequences (Hard)

#### Part D: Grid/2D DP (2 days)

**Day 9: Path Problems (2-3 hours)**
- ✅ #62 Unique Paths (Medium)
- ✅ #63 Unique Paths II (Medium)
- ✅ #64 Minimum Path Sum (Medium)
- ✅ #120 Triangle (Medium)

**Day 10: Grid Advanced (3 hours)**
- ✅ #221 Maximal Square (Medium)
- 🎯 #85 Maximal Rectangle (Hard) - ✅ You solved!
- 🎯 #1277 Count Square Submatrices (Medium)

#### Part E: Advanced Patterns (3 days)

**Day 11: Palindrome DP (3 hours)**
- ✅ #5 Longest Palindromic Substring (Medium)
- 🎯 #516 Longest Palindromic Subsequence (Medium)
- 🎯 #647 Palindromic Substrings (Medium)
- 🎯 #131 Palindrome Partitioning (Medium)

**Day 12: String DP (3 hours)**
- ✅ #139 Word Break (Medium)
- 🎯 #140 Word Break II (Hard)
- ✅ #91 Decode Ways (Medium)

**Day 13: Interval/Game DP (4 hours)**
- 🎯 #312 Burst Balloons (Hard) - **Classic interval DP**
- ✅ #1669 Minimum Cost to Cut a Stick (Hard)
- 🎯 #1000 Minimum Cost to Merge Stones (Hard)
- ✅ #375 Guess Number Higher or Lower II (Medium)

---

### 4️⃣ Memoization & Optimization Techniques (3-4 days)

**Key Concepts:**
- Top-down DP (recursion + cache)
- LRU cache for function results
- Space optimization (rolling array)
- State compression

**Day 1: Recursion to Memoization (2-3 hours)**
- Practice: Fibonacci naive → memoized → tabulated
- 🎯 #509 Fibonacci Number (Easy) - All 3 approaches
- ✅ #139 Word Break (Medium) - Add memoization
- 🎯 #329 Longest Increasing Path in Matrix (Hard) - **DFS + memo**

**Day 2: Memoization Patterns (3 hours)**
- 🎯 #140 Word Break II (Hard) - String memoization
- 🎯 #87 Scramble String (Hard) - 3D memoization
- ✅ JavaScript #2731 Memoize (Medium)

**Day 3: Space Optimization (2-3 hours)**
- ✅ #70 Climbing Stairs - Optimize O(n) → O(1)
- ✅ #198 House Robber - Optimize space
- 🎯 #123 Best Time to Buy/Sell Stock III (Hard) - State machine

**Day 4: Advanced Caching (3 hours)**
- ✅ #146 LRU Cache (Medium) - You need this!
- 🎯 #460 LFU Cache (Hard)
- ✅ JavaScript #2762 Cache with Time Limit (Medium)

**Practice Project:** Implement a generic memoization decorator/wrapper

---

### 5️⃣ Binary Trees & BST (8-10 days)

**Your Progress:** 22/35 Core Problems ✅ Good foundation, need advanced!

**Key Concepts:**
- Traversals (inorder, preorder, postorder, level-order)
- Recursion patterns
- BST properties
- Tree construction
- Lowest common ancestor
- Serialization

#### Part A: Traversals (2 days)

**Day 1: DFS Traversals (2-3 hours)**
- ✅ #94 Binary Tree Inorder Traversal (Easy)
- 🎯 #144 Binary Tree Preorder Traversal (Easy)
- 🎯 #145 Binary Tree Postorder Traversal (Easy)
- Practice: Iterative versions with stack

**Day 2: BFS & Level Order (2-3 hours)**
- 🎯 #102 Binary Tree Level Order Traversal (Medium) - **Template**
- 🎯 #107 Binary Tree Level Order Traversal II (Medium)
- 🎯 #103 Binary Tree Zigzag Level Order (Medium)
- 🎯 #199 Binary Tree Right Side View (Medium)

#### Part B: Tree Properties (2 days)

**Day 3: Basic Properties (2 hours)**
- ✅ #100 Same Tree (Easy)
- ✅ #101 Symmetric Tree (Easy)
- 🎯 #104 Maximum Depth (Easy)
- 🎯 #110 Balanced Binary Tree (Easy)
- ✅ #543 Diameter of Binary Tree (Easy)

**Day 4: BST Properties (3 hours)**
- 🎯 #98 Validate BST (Medium) - **Very common**
- ✅ #235 LCA of BST (Easy)
- 🎯 #230 Kth Smallest in BST (Medium)
- 🎯 #450 Delete Node in BST (Medium)

#### Part C: Tree Construction (2 days)

**Day 5: From Arrays (3 hours)**
- 🎯 #108 Convert Sorted Array to BST (Easy)
- 🎯 #105 Construct from Preorder/Inorder (Medium) - **Key problem**
- 🎯 #106 Construct from Inorder/Postorder (Medium)
- ✅ #1050 Construct BST from Preorder (Medium)

**Day 6: Serialization (3-4 hours)**
- 🎯 #297 Serialize/Deserialize Binary Tree (Hard) - **Must know**
- 🎯 #449 Serialize/Deserialize BST (Medium)
- ✅ #331 Verify Preorder Serialization (Medium)

#### Part D: Advanced Problems (3 days)

**Day 7: Path Problems (3 hours)**
- ✅ #113 Path Sum II (Medium)
- ✅ #129 Sum Root to Leaf (Medium)
- ✅ #124 Binary Tree Maximum Path Sum (Hard) - **Interview favorite**
- 🎯 #687 Longest Univalue Path (Medium)

**Day 8: LCA & Relationships (3 hours)**
- ✅ #235 LCA of BST (Easy)
- 🎯 #236 LCA of Binary Tree (Medium) - **Must know**
- 🎯 #1650 LCA of Binary Tree III (Medium, Premium)
- 🎯 #1123 LCA of Deepest Leaves (Medium)

**Day 9: Modification (3 hours)**
- ✅ #114 Flatten Binary Tree to Linked List (Medium)
- 🎯 #116 Populating Next Right Pointers (Medium)
- 🎯 #117 Populating Next Right Pointers II (Medium)

---

### 6️⃣ Graphs (10-12 days) **🚨 Major Focus Area**

**Your Progress:** 8/40 Core Problems ⚠️ Need significant work!

**Key Concepts:**
- Graph representations (adjacency list, matrix)
- DFS, BFS
- Topological sort (Kahn's algorithm)
- Union-Find
- Shortest path (Dijkstra, Bellman-Ford)
- Minimum spanning tree

#### Part A: Graph Fundamentals (2 days)

**Day 1: DFS Basics (2-3 hours)**
- 🎯 #200 Number of Islands (Medium) - **#1 most common**
- 🎯 #695 Max Area of Island (Medium)
- 🎯 #733 Flood Fill (Easy)
- ✅ #2121 Find if Path Exists (Easy)

**Day 2: BFS Basics (2-3 hours)**
- ✅ #1171 Shortest Path in Binary Matrix (Medium)
- 🎯 #994 Rotting Oranges (Medium)
- 🎯 #542 01 Matrix (Medium)
- 🎯 #1091 Shortest Path in Binary Matrix (Medium)

#### Part B: Union-Find (3 days) **🚨 Critical Gap**

**Day 3: Union-Find Basics (3 hours)**
- 🎯 #547 Number of Provinces (Medium) - **Template**
- 🎯 #684 Redundant Connection (Medium)
- 🎯 #323 Number of Connected Components (Medium, Premium)

**Day 4: Union-Find Applications (3 hours)**
- 🎯 #721 Accounts Merge (Medium)
- 🎯 #128 Longest Consecutive Sequence (Medium) - Union-Find solution
- 🎯 #952 Largest Component Size (Hard)

**Day 5: MST & Advanced (3-4 hours)**
- 🎯 #1584 Min Cost to Connect All Points (Medium) - Kruskal's
- 🎯 #1135 Connecting Cities (Medium, Premium)
- ✅ #2505 Number of Good Paths (Hard)

#### Part C: Topological Sort (2 days)

**Day 6: Topological Basics (3 hours)**
- 🎯 #207 Course Schedule (Medium) - **Must know**
- 🎯 #210 Course Schedule II (Medium)
- 🎯 #802 Find Eventual Safe States (Medium)

**Day 7: Advanced Topological (3 hours)**
- 🎯 #269 Alien Dictionary (Hard, Premium)
- 🎯 #310 Minimum Height Trees (Medium) - ✅ You solved!
- 🎯 #1136 Parallel Courses (Medium, Premium)

#### Part D: Shortest Path (3 days)

**Day 8: BFS Shortest Path (2-3 hours)**
- 🎯 #127 Word Ladder (Hard) - **Classic**
- 🎯 #126 Word Ladder II (Hard)
- 🎯 #433 Minimum Genetic Mutation (Medium)

**Day 9: Dijkstra's Algorithm (3-4 hours)**
- 🎯 #743 Network Delay Time (Medium) - **Template**
- 🎯 #787 Cheapest Flights Within K Stops (Medium)
- 🎯 #1514 Path with Maximum Probability (Medium)

**Day 10: Advanced Graph (4 hours)**
- ✅ #1414 Shortest Path with Obstacles Elimination (Hard)
- 🎯 #1293 Shortest Path in Grid with Obstacles (Hard)
- 🎯 #847 Shortest Path Visiting All Nodes (Hard)

---

### 7️⃣ Heaps & Priority Queues (4-5 days)

**Your Progress:** 5/20 Core Problems ⚠️ Need more practice!

**Key Concepts:**
- Min heap / Max heap
- Two heaps pattern (median maintenance)
- K-way merge
- Top K problems
- Heap as scheduling tool

**Day 1: Heap Basics (2-3 hours)**
- ✅ #215 Kth Largest Element (Medium)
- ✅ #347 Top K Frequent Elements (Medium)
- 🎯 #703 Kth Largest in Stream (Easy)
- 🎯 #1046 Last Stone Weight (Easy)

**Day 2: K-way Merge (3 hours)**
- ✅ #23 Merge k Sorted Lists (Hard)
- ✅ #373 Find K Pairs with Smallest Sums (Medium)
- ✅ #378 Kth Smallest in Sorted Matrix (Medium)

**Day 3: Two Heaps Pattern (3-4 hours)**
- 🎯 #295 Find Median from Data Stream (Hard) - **Must know**
- 🎯 #480 Sliding Window Median (Hard)
- 🎯 #502 IPO (Hard)

**Day 4: Scheduling & Intervals (3 hours)**
- 🎯 #253 Meeting Rooms II (Medium, Premium) - **Very common**
- 🎯 #621 Task Scheduler (Medium)
- 🎯 #1094 Car Pooling (Medium)

**Day 5: Advanced Heap (3-4 hours)**
- ✅ #218 The Skyline Problem (Hard)
- 🎯 #767 Reorganize String (Medium)
- 🎯 #358 Rearrange String k Distance Apart (Hard, Premium)

---

### 8️⃣ Hash Tables & Hash Maps (3-4 days)

**Your Progress:** Strong usage across all problems! Focus on advanced patterns.

**Key Concepts:**
- O(1) lookups
- Collision handling
- Hash functions
- Use cases vs arrays

**Day 1: Basic Patterns (2 hours)**
- ✅ #1 Two Sum (Easy)
- 🎯 #242 Valid Anagram (Easy)
- 🎯 #217 Contains Duplicate (Easy)
- 🎯 #383 Ransom Note (Easy)

**Day 2: Frequency & Counting (2-3 hours)**
- ✅ #169 Majority Element (Easy)
- ✅ #347 Top K Frequent Elements (Medium)
- 🎯 #451 Sort Characters By Frequency (Medium)
- ✅ #1464 Reduce Array Size to Half (Medium)

**Day 3: Advanced Mapping (3 hours)**
- ✅ #49 Group Anagrams (Medium)
- 🎯 #138 Copy List with Random Pointer (Medium)
- 🎯 #380 Insert Delete GetRandom O(1) (Medium)
- 🎯 #381 Insert Delete GetRandom with Duplicates (Hard)

**Day 4: Prefix Sum + Hash Map (3 hours)**
- 🎯 #560 Subarray Sum Equals K (Medium) - **Very common**
- 🎯 #523 Continuous Subarray Sum (Medium)
- 🎯 #525 Contiguous Array (Medium)
- 🎯 #974 Subarray Sums Divisible by K (Medium)

---

### 9️⃣ Stack & Queue (4-5 days)

**Your Progress:** 7/25 Core Problems ⚠️ Need monotonic stack!

**Key Concepts:**
- LIFO (stack) vs FIFO (queue)
- Monotonic stack/queue
- Expression evaluation
- Parentheses matching

#### Part A: Stack Basics (1 day)

**Day 1: Fundamentals (2-3 hours)**
- ✅ #20 Valid Parentheses (Easy)
- 🎯 #155 Min Stack (Medium) - **Design pattern**
- 🎯 #225 Implement Stack using Queues (Easy)
- ✅ #71 Simplify Path (Medium)

#### Part B: Monotonic Stack (2 days) **🚨 Critical Pattern**

**Day 2: Next Greater Element (3 hours)**
- 🎯 #496 Next Greater Element I (Easy) - **Template**
- 🎯 #503 Next Greater Element II (Medium)
- ✅ #739 Daily Temperatures (Medium)
- 🎯 #556 Next Greater Element III (Medium)

**Day 3: Advanced Monotonic Stack (3-4 hours)**
- ✅ #84 Largest Rectangle in Histogram (Hard) - **Classic**
- ✅ #85 Maximal Rectangle (Hard)
- ✅ #42 Trapping Rain Water (Hard)
- 🎯 #907 Sum of Subarray Minimums (Medium)

#### Part C: Expression Evaluation (1 day)

**Day 4: Calculators (3 hours)**
- ✅ #227 Basic Calculator II (Medium)
- 🎯 #224 Basic Calculator (Hard)
- 🎯 #772 Basic Calculator III (Hard, Premium)

#### Part D: Monotonic Queue (1 day)

**Day 5: Sliding Window Max (3-4 hours)**
- 🎯 #239 Sliding Window Maximum (Hard) - **Must know**
- 🎯 #862 Shortest Subarray with Sum at Least K (Hard)
- 🎯 #1438 Longest Continuous Subarray (Medium)

---

### 🔟 Binary Search (5-6 days)

**Your Progress:** 8/25 Core Problems ✅ Good foundation!

**Key Concepts:**
- Search space reduction
- Binary search on answer
- Lower bound / upper bound
- Rotated arrays
- Search in 2D

#### Part A: Classic Binary Search (1 day)

**Day 1: Templates (2-3 hours)**
- ✅ #35 Search Insert Position (Easy) - **Template**
- 🎯 #278 First Bad Version (Easy)
- 🎯 #374 Guess Number (Easy)
- Practice: Write template from memory

#### Part B: Advanced Search (2 days)

**Day 2: Rotated Arrays (3 hours)**
- ✅ #33 Search in Rotated Sorted Array (Medium)
- 🎯 #81 Search in Rotated Sorted Array II (Medium)
- 🎯 #153 Find Minimum in Rotated Array (Medium)
- 🎯 #154 Find Minimum in Rotated Array II (Hard)

**Day 3: Range Search (3 hours)**
- ✅ #34 Find First and Last Position (Medium)
- ✅ #162 Find Peak Element (Medium)
- 🎯 #852 Peak Index in Mountain Array (Medium)
- 🎯 #1095 Find in Mountain Array (Hard)

#### Part C: Binary Search on Answer (2 days) **🚨 Advanced Pattern**

**Day 4: Minimization (3 hours)**
- 🎯 #875 Koko Eating Bananas (Medium) - **Template**
- 🎯 #1011 Capacity To Ship Packages (Medium)
- 🎯 #774 Minimize Max Distance to Gas Station (Hard)

**Day 5: Allocation/Split (3-4 hours)**
- 🎯 #410 Split Array Largest Sum (Hard) - **Classic**
- 🎯 #1482 Minimum Days to Make Bouquets (Medium)
- 🎯 #1552 Magnetic Force Between Balls (Medium)

#### Part D: 2D Binary Search (1 day)

**Day 6: Matrix Search (2-3 hours)**
- ✅ #74 Search a 2D Matrix (Medium)
- 🎯 #240 Search a 2D Matrix II (Medium)
- ✅ #378 Kth Smallest in Sorted Matrix (Medium)

---

### 1️⃣1️⃣ Tries (4-5 days) **🚨 Major Gap!**

**Your Progress:** 1/15 Core Problems ⚠️ Critical weakness!

**Key Concepts:**
- Prefix trees
- Insert, search, startsWith
- Wildcard search
- Word games (Boggle)

**Day 1: Trie Basics (3 hours)**
- ✅ #208 Implement Trie (Medium) - **Template**
- 🎯 #211 Add and Search Word (Medium) - **Wildcard search**
- 🎯 #1804 Implement Trie II (Medium, Premium)

**Day 2: Trie Applications (3 hours)**
- 🎯 #648 Replace Words (Medium)
- 🎯 #677 Map Sum Pairs (Medium)
- 🎯 #720 Longest Word in Dictionary (Medium)

**Day 3: Trie with Backtracking (3-4 hours)**
- ✅ #79 Word Search (Medium) - You solved!
- 🎯 #212 Word Search II (Hard) - **Must know Trie + backtracking**
- 🎯 #425 Word Squares (Hard, Premium)

**Day 4: Advanced Trie (3-4 hours)**
- 🎯 #336 Palindrome Pairs (Hard)
- 🎯 #421 Maximum XOR of Two Numbers (Medium) - Binary trie
- 🎯 #1707 Maximum XOR with Element from Array (Hard)

**Day 5: Design Problems (3 hours)**
- 🎯 #642 Design Search Autocomplete System (Hard, Premium)
- 🎯 #1268 Search Suggestions System (Medium)

---

### 1️⃣2️⃣ Backtracking (5-6 days)

**Your Progress:** 12/20 Core Problems ✅ Good coverage!

**Key Concepts:**
- Decision tree exploration
- Choose → Explore → Unchoose
- Pruning
- Permutations vs combinations

**Day 1: Combinations (2-3 hours)**
- ✅ #77 Combinations (Medium)
- ✅ #39 Combination Sum (Medium)
- ✅ #40 Combination Sum II (Medium)
- 🎯 #216 Combination Sum III (Medium)

**Day 2: Permutations (2-3 hours)**
- ✅ #46 Permutations (Medium)
- ✅ #47 Permutations II (Medium)
- 🎯 #31 Next Permutation (Medium) - ✅ You solved!
- ✅ #60 Permutation Sequence (Hard)

**Day 3: Subsets (2-3 hours)**
- ✅ #78 Subsets (Medium)
- ✅ #90 Subsets II (Medium)
- 🎯 #491 Non-decreasing Subsequences (Medium)

**Day 4: String Backtracking (3 hours)**
- ✅ #17 Letter Combinations of Phone (Medium)
- 🎯 #93 Restore IP Addresses (Medium)
- 🎯 #131 Palindrome Partitioning (Medium)

**Day 5: Board Problems (3-4 hours)**
- ✅ #79 Word Search (Medium)
- ✅ #51 N-Queens (Hard)
- ✅ #52 N-Queens II (Hard)
- 🎯 #37 Sudoku Solver (Hard)

**Day 6: Advanced (3-4 hours)**
- ✅ #22 Generate Parentheses (Medium)
- 🎯 #301 Remove Invalid Parentheses (Hard)
- 🎯 #351 Android Unlock Patterns (Medium, Premium)

---

### 1️⃣3️⃣ Greedy Algorithms (4-5 days)

**Your Progress:** 5/20 Core Problems ⚠️ Need more!

**Key Concepts:**
- Local optimal → global optimal
- Proof techniques
- Interval scheduling
- Huffman coding

**Day 1: Greedy Basics (2-3 hours)**
- ✅ #55 Jump Game (Medium)
- ✅ #45 Jump Game II (Medium)
- 🎯 #134 Gas Station (Medium)
- 🎯 #135 Candy (Hard)

**Day 2: Interval Scheduling (3 hours)**
- ✅ #56 Merge Intervals (Medium)
- ✅ #57 Insert Interval (Medium)
- 🎯 #435 Non-overlapping Intervals (Medium)
- 🎯 #452 Minimum Arrows to Burst Balloons (Medium)

**Day 3: String Greedy (3 hours)**
- 🎯 #392 Is Subsequence (Easy)
- 🎯 #763 Partition Labels (Medium)
- 🎯 #767 Reorganize String (Medium)
- 🎯 #1053 Previous Permutation (Medium)

**Day 4: Advanced Greedy (3-4 hours)**
- 🎯 #621 Task Scheduler (Medium)
- 🎯 #630 Course Schedule III (Hard)
- 🎯 #871 Minimum Number of Refueling Stops (Hard)

---

### 1️⃣4️⃣ Design Problems (5-6 days) **🎯 Interview Critical**

**Your Progress:** 7/25 Core Problems ⚠️ Need variety!

**Key Concepts:**
- API design
- Data structure selection
- Trade-offs
- Scalability considerations

**Day 1: Cache Design (3 hours)**
- 🎯 #146 LRU Cache (Medium) - **#1 most important**
- 🎯 #460 LFU Cache (Hard)
- ✅ JavaScript #2762 Cache with Time Limit

**Day 2: Data Structure Design (3 hours)**
- 🎯 #380 Insert Delete GetRandom O(1) (Medium)
- 🎯 #381 Insert Delete GetRandom with Duplicates (Hard)
- 🎯 #432 All O(1) Data Structure (Hard)

**Day 3: Iterator Design (3 hours)**
- ✅ #341 Flatten Nested List Iterator (Medium)
- 🎯 #251 Flatten 2D Vector (Medium, Premium)
- 🎯 #284 Peeking Iterator (Medium)
- 🎯 #281 Zigzag Iterator (Medium, Premium)

**Day 4: Range Query (3 hours)**
- ✅ #303 Range Sum Query Immutable (Easy)
- ✅ #307 Range Sum Query Mutable (Medium)
- 🎯 #308 Range Sum Query 2D Mutable (Hard, Premium)

**Day 5: System Design (3-4 hours)**
- 🎯 #355 Design Twitter (Medium)
- 🎯 #362 Design Hit Counter (Medium, Premium)
- 🎯 #588 Design In-Memory File System (Hard, Premium)

**Day 6: Advanced Design (4 hours)**
- 🎯 #895 Maximum Frequency Stack (Hard)
- 🎯 #1348 Tweet Counts Per Frequency (Medium)
- 🎯 #1472 Design Browser History (Medium)

---

### 1️⃣5️⃣ Bit Manipulation (3-4 days)

**Your Progress:** 8/20 Core Problems ✅ Decent coverage!

**Key Concepts:**
- Bitwise operators (&, |, ^, ~, <<, >>)
- XOR properties
- Bit masks
- Binary representation tricks

**Day 1: Basics (2-3 hours)**
- ✅ #191 Number of 1 Bits (Easy)
- 🎯 #136 Single Number (Easy) - XOR trick
- 🎯 #268 Missing Number (Easy)
- ✅ #338 Counting Bits (Easy)

**Day 2: XOR Applications (3 hours)**
- 🎯 #137 Single Number II (Medium)
- 🎯 #260 Single Number III (Medium)
- ✅ #371 Sum of Two Integers (Medium)

**Day 3: Bit Manipulation (3 hours)**
- ✅ #342 Power of Four (Easy)
- 🎯 #190 Reverse Bits (Easy)
- 🎯 #201 Bitwise AND of Numbers Range (Medium)
- 🎯 #393 UTF-8 Validation (Medium)

**Day 4: Advanced (3-4 hours)**
- 🎯 #421 Maximum XOR of Two Numbers (Medium) - Trie
- 🎯 #1542 Find Longest Awesome Substring (Hard) - Bitmask DP
- 🎯 #1239 Maximum Length of Concatenated String (Medium)

---

## 🎯 Suggested Learning Order (Overall Priority)

### Phase 1: Foundation (Weeks 1-4)
1. **Arrays & Two Pointers** (3 days)
2. **Linked Lists** (5 days)
3. **Binary Trees Basics** (4 days)
4. **Hash Tables** (3 days)
5. **Stack & Queue Basics** (3 days)

### Phase 2: Core Patterns (Weeks 5-10)
1. **Sliding Window** (4 days) - **Critical gap**
2. **Dynamic Programming** (12 days) - **Major topic**
3. **Binary Search** (5 days)
4. **Backtracking** (5 days)

### Phase 3: Advanced Structures (Weeks 11-14)
1. **Graphs & Union-Find** (10 days) - **Critical gap**
2. **Heaps** (5 days)
3. **Tries** (5 days) - **Critical gap**
4. **Monotonic Stack/Queue** (3 days)

### Phase 4: Interview Prep (Weeks 15-16)
1. **Design Problems** (5 days) - **Interview critical**
2. **Greedy** (4 days)
3. **Review & Mock Interviews** (5 days)

---

## 📊 Progress Tracking Template

Copy this template to track your progress:

```markdown
## Week X Progress

### Monday - Topic: _______
- [ ] Problem 1
- [ ] Problem 2
- [ ] Problem 3
- Notes: 
- Time spent: 
- Difficulty rating (1-5):

### Tuesday - Topic: _______
...

### Weekly Reflection
- Concepts mastered:
- Concepts struggling with:
- Patterns recognized:
- Next week focus:
```

---

## Interview Problems for Candidates

When interviewing software engineering candidates, these problems effectively assess problem-solving ability, coding skills, and understanding of complexity trade-offs.

### Easy Level Problems (3 Problems)

#### Problem 1: Two Sum (#1)
**Problem Statement:**
Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`. You may assume that each input would have exactly one solution, and you may not use the same element twice.

**Example:**
```
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: nums[0] + nums[1] == 9, so we return [0, 1]
```

**Solution Approaches:**

**Approach 1: Brute Force**

```python
def twoSum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
```

- **Time Complexity:** O(n²) - nested loops through array
- **Space Complexity:** O(1) - only storing indices
- **Pros:** Simple, no extra space needed
- **Cons:** Inefficient for large arrays

**Approach 2: Hash Map (Optimal)**

```python
def twoSum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
```

- **Time Complexity:** O(n) - single pass through array
- **Space Complexity:** O(n) - hash map storage
- **Pros:** Much faster, optimal solution
- **Cons:** Uses extra memory
- **Trade-off Analysis:** Hash map approach trades space for time. For n > 1000, the time savings dramatically outweigh memory cost.

**What to Look For in Candidate:**
- Do they start with brute force and optimize?
- Can they identify the trade-off between time and space?
- Do they handle edge cases (empty array, no solution)?

---

#### Problem 2: Valid Parentheses (#20)
**Problem Statement:**
Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid. An input string is valid if: open brackets are closed by the same type, and open brackets are closed in the correct order.

**Example:**
```
Input: s = "()[]{}"
Output: true

Input: s = "([)]"
Output: false
```

**Solution Approaches:**

**Approach 1: Stack (Optimal)**

```python
def isValid(s):
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:
            top = stack.pop() if stack else '#'
            if mapping[char] != top:
                return False
        else:
            stack.append(char)
    
    return not stack
```

- **Time Complexity:** O(n) - single pass through string
- **Space Complexity:** O(n) - worst case all opening brackets
- **Pros:** Clean, efficient, intuitive
- **Cons:** Requires extra space for stack

**Approach 2: Counter Method (Incorrect but instructive)**

```python
def isValid(s):
    count = {')': 0, '}': 0, ']': 0}
    # This approach fails for "([)]"
```

- **Why It Fails:** Order matters, not just counts
- **Learning Point:** Demonstrates why stack is necessary

**Trade-off Analysis:**
- Stack is the only correct approach for this problem
- The space used by the stack is proportional to nesting depth
- Best case: O(1) space for strings like "()()()"
- Worst case: O(n) space for strings like "(((((("

**What to Look For in Candidate:**
- Recognition that this is a stack problem
- Proper handling of edge cases (empty string, odd length)
- Clean implementation with proper error handling

---

#### Problem 3: Merge Two Sorted Lists (#21)
**Problem Statement:**
Merge two sorted linked lists and return it as a sorted list. The list should be made by splicing together the nodes of the first two lists.

**Example:**
```
Input: list1 = [1,2,4], list2 = [1,3,4]
Output: [1,1,2,3,4,4]
```

**Solution Approaches:**

**Approach 1: Iterative with Dummy Node (Optimal)**

```python
def mergeTwoLists(l1, l2):
    dummy = ListNode(0)
    current = dummy
    
    while l1 and l2:
        if l1.val < l2.val:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next
    
    current.next = l1 if l1 else l2
    return dummy.next
```

- **Time Complexity:** O(n + m) - visit each node once
- **Space Complexity:** O(1) - only pointer manipulation
- **Pros:** Most efficient, in-place merging
- **Cons:** Modifies original lists

**Approach 2: Recursive**

```python
def mergeTwoLists(l1, l2):
    if not l1:
        return l2
    if not l2:
        return l1
    
    if l1.val < l2.val:
        l1.next = mergeTwoLists(l1.next, l2)
        return l1
    else:
        l2.next = mergeTwoLists(l1, l2.next)
        return l2
```

- **Time Complexity:** O(n + m) - visit each node once
- **Space Complexity:** O(n + m) - recursion call stack
- **Pros:** Elegant, easier to understand
- **Cons:** Stack overflow risk for very long lists

**Approach 3: Create New List**

```python
def mergeTwoLists(l1, l2):
    dummy = ListNode(0)
    current = dummy
    
    while l1 and l2:
        if l1.val < l2.val:
            current.next = ListNode(l1.val)
            l1 = l1.next
        else:
            current.next = ListNode(l2.val)
            l2 = l2.next
        current = current.next
    # ... copy remaining nodes
```

- **Time Complexity:** O(n + m)
- **Space Complexity:** O(n + m) - creating new nodes
- **Pros:** Preserves original lists
- **Cons:** Uses extra memory unnecessarily

**Trade-off Analysis:**
- **Iterative vs Recursive:** Iterative uses less space (O(1) vs O(n+m))
- **In-place vs New List:** In-place saves memory but mutates input
- For production: Use iterative in-place
- For interviews: Discuss all three approaches

**What to Look For in Candidate:**
- Understanding of linked list pointer manipulation
- Awareness of dummy node technique
- Discussion of trade-offs between approaches
- Handling edge cases:
  - **Empty lists:** One or both lists are null/None
  - **Different lengths:** list1 has 1 node, list2 has 100 nodes
  - **All elements smaller:** All of list1 < all of list2 (or vice versa)
  - **Duplicate values:** Both lists contain the same values
  - **Single element lists:** Both lists have only 1 node each

**Note on Cycles/Infinite Loops:**
- For this problem, cycles aren't a concern (sorted lists are linear by definition)
- **However**, in a general interview discussion, mention:
  - "I'm assuming no cycles in the input lists as per the problem constraints"
  - "If cycles were possible, I'd need to detect them first (Floyd's algorithm)"
  - Cycles ARE important for problems like: #141 (Linked List Cycle), #142 (Linked List Cycle II)

---

### Medium Level Problems (3 Problems)

#### Problem 1: LRU Cache (#146)
**Problem Statement:**
Design a data structure that follows the constraints of a Least Recently Used (LRU) cache. Implement `LRUCache` class with methods:
- `LRUCache(int capacity)` - Initialize with positive size capacity
- `int get(int key)` - Return value if exists, otherwise -1
- `void put(int key, int value)` - Update or insert value. If cache is full, evict the least recently used key

Both `get` and `put` must run in O(1) average time complexity.

**Example:**
```
LRUCache cache = new LRUCache(2);
cache.put(1, 1);
cache.put(2, 2);
cache.get(1);       // returns 1
cache.put(3, 3);    // evicts key 2
cache.get(2);       // returns -1
```

**Solution Approaches:**

**Approach 1: OrderedDict (Python-specific)**

**What is OrderedDict?**
- A dictionary that maintains insertion order
- Provides O(1) operations to move items to end and remove from beginning
- Internally uses: hash table + doubly linked list (same as our manual Approach 2!)

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        # OrderedDict maintains order: oldest → newest (left → right)
        self.cache = OrderedDict()
        self.capacity = capacity
    
    def get(self, key):
        # Step 1: Check if key exists
        if key not in self.cache:
            return -1
        
        # Step 2: Mark as recently used by moving to end (most recent position)
        # OrderedDict order: [old items...] → [this key] (moved to right/end)
        self.cache.move_to_end(key)  # O(1) operation
        
        # Step 3: Return the value
        return self.cache[key]
    
    def put(self, key, value):
        # Step 1: If key exists, mark as recently used (move to end)
        if key in self.cache:
            self.cache.move_to_end(key)  # O(1) - update access order
        
        # Step 2: Insert or update the key-value pair
        # If key is new, it's automatically added at the end (most recent)
        self.cache[key] = value
        
        # Step 3: If cache exceeds capacity, evict the LRU item
        if len(self.cache) > self.capacity:
            # popitem(last=False) removes from LEFT/FRONT (oldest item)
            # popitem(last=True) would remove from RIGHT/END (newest item)
            self.cache.popitem(last=False)  # O(1) - evict least recently used

# Example walkthrough:
# cache = LRUCache(2)
# 
# cache.put(1, 1)  → OrderedDict: [1]
# cache.put(2, 2)  → OrderedDict: [1, 2]
# cache.get(1)     → OrderedDict: [2, 1] (1 moved to end, most recent)
# cache.put(3, 3)  → OrderedDict: [1, 3] (2 evicted from front, capacity exceeded)
# cache.get(2)     → return -1 (2 was evicted)
```

- **Time Complexity:** O(1) for both operations
- **Space Complexity:** O(capacity)
- **Pros:** Simple, clean, Pythonic, leverages built-in data structure
- **Cons:** Language-specific, doesn't demonstrate data structure knowledge in interviews
- **When to use:** Production code in Python, rapid prototyping
- **Interview note:** Good to mention, but show you can implement manually (Approach 2)

**Approach 2: HashMap + Doubly Linked List (Optimal & Universal)**

```python
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}  # key -> node
        self.head = Node(0, 0)  # dummy head
        self.tail = Node(0, 0)  # dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _remove(self, node):
        prev, nxt = node.prev, node.next
        prev.next, nxt.prev = nxt, prev
    
    def _add_to_head(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
    
    def get(self, key):
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._add_to_head(node)
        return node.value
    
    def put(self, key, value):
        if key in self.cache:
            self._remove(self.cache[key])
        
        node = Node(key, value)
        self.cache[key] = node
        self._add_to_head(node)
        
        if len(self.cache) > self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]
```

- **Time Complexity:** O(1) for both operations
- **Space Complexity:** O(capacity)
- **Pros:** Demonstrates deep understanding, language-agnostic
- **Cons:** More complex implementation

**Approach 3: HashMap with Timestamp (Incorrect for O(1))**

```python
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.timestamps = {}
        self.time = 0
    
    def get(self, key):
        if key not in self.cache:
            return -1
        self.timestamps[key] = self.time
        self.time += 1
        return self.cache[key]
    
    def put(self, key, value):
        if len(self.cache) >= self.capacity and key not in self.cache:
            # Need to find minimum timestamp - O(n) operation!
            lru = min(self.timestamps, key=self.timestamps.get)
            del self.cache[lru]
            del self.timestamps[lru]
        
        self.cache[key] = value
        self.timestamps[key] = self.time
        self.time += 1
```

- **Time Complexity:** O(n) for put when eviction needed
- **Space Complexity:** O(capacity)
- **Why It Fails:** Finding LRU item requires scanning all timestamps

**Trade-off Analysis:**
- **HashMap + Doubly Linked List:**
  - Doubly linked list allows O(1) removal and insertion at both ends
  - HashMap provides O(1) access to any node
  - Together they achieve O(1) for all operations
  - Memory overhead: 2 extra pointers per entry

- **OrderedDict:** Uses hash table + doubly linked list internally (same approach)
- **Array-based approaches:** Would require O(n) shifts on updates
- **Single LinkedList:** Would require O(n) to find previous node

**What to Look For in Candidate:**
- Recognition that two data structures are needed
- Understanding why doubly linked list (not singly linked)
- Proper handling of edge cases (capacity 1, duplicate keys)
- Clean abstraction with helper methods
- Discussion of why simpler approaches don't achieve O(1)

---

#### Problem 2: Course Schedule (#207)
**Problem Statement:**
There are a total of `numCourses` courses labeled from `0` to `numCourses - 1`. You are given an array `prerequisites` where `prerequisites[i] = [ai, bi]` indicates that you must take course `bi` first if you want to take course `ai`. Return `true` if you can finish all courses.

**Example:**
```
Input: numCourses = 2, prerequisites = [[1,0]]
Output: true

Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
Output: false (cycle exists)
```

**Solution Approaches:**

**Approach 1: DFS with Cycle Detection (Optimal)**

```python
def canFinish(numCourses, prerequisites):
    graph = {i: [] for i in range(numCourses)}
    for course, prereq in prerequisites:
        graph[course].append(prereq)
    
    # 0 = unvisited, 1 = visiting, 2 = visited
    state = [0] * numCourses
    
    def has_cycle(course):
        if state[course] == 1:  # Currently visiting - cycle!
            return True
        if state[course] == 2:  # Already processed
            return False
        
        state[course] = 1  # Mark as visiting
        for prereq in graph[course]:
            if has_cycle(prereq):
                return True
        state[course] = 2  # Mark as visited
        return False
    
    for course in range(numCourses):
        if has_cycle(course):
            return False
    return True
```

- **Time Complexity:** O(V + E) - visit each vertex and edge once
- **Space Complexity:** O(V + E) - graph storage + O(V) recursion stack
- **Pros:** Intuitive, detects cycles early
- **Cons:** Recursion depth could be an issue for very deep graphs

**Approach 2: BFS with Topological Sort (Kahn's Algorithm)**

```python
def canFinish(numCourses, prerequisites):
    graph = {i: [] for i in range(numCourses)}
    indegree = [0] * numCourses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        indegree[course] += 1
    
    queue = [i for i in range(numCourses) if indegree[i] == 0]
    completed = 0
    
    while queue:
        course = queue.pop(0)
        completed += 1
        
        for next_course in graph[course]:
            indegree[next_course] -= 1
            if indegree[next_course] == 0:
                queue.append(next_course)
    
    return completed == numCourses
```

- **Time Complexity:** O(V + E)
- **Space Complexity:** O(V + E)
- **Pros:** No recursion, iterative, easier to understand for some
- **Cons:** Requires understanding of indegree concept

**Approach 3: Union-Find (Less Suitable)**

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False  # Already connected - creates cycle
        self.parent[px] = py
        return True

def canFinish(numCourses, prerequisites):
    uf = UnionFind(numCourses)
    for course, prereq in prerequisites:
        if not uf.union(course, prereq):
            return False
    return True
```

- **Time Complexity:** O(E × α(V)) where α is inverse Ackermann
- **Space Complexity:** O(V)
- **Why It Fails:** Union-Find can't properly detect cycles in directed graphs
- **Use Case:** Better for undirected graph connectivity

**Trade-off Analysis:**

| Approach | Time | Space | Pros | Cons |
|----------|------|-------|------|------|
| DFS | O(V+E) | O(V+E) | Early cycle detection, elegant | Recursion depth |
| BFS | O(V+E) | O(V+E) | Iterative, no stack overflow | More code |
| Union-Find | O(E×α(V)) | O(V) | Simple | Doesn't work for directed graphs |

**Key Insights:**
- This is fundamentally a cycle detection problem in a directed graph
- DFS with three states (unvisited, visiting, visited) is the cleanest approach
- BFS with indegree tracking (Kahn's algorithm) is equally valid
- Choice between DFS/BFS is often personal preference

**What to Look For in Candidate:**
- Recognition this is a graph problem
- Understanding of cycle detection in directed graphs
- Ability to implement either DFS or BFS approach
- Discussion of why Union-Find doesn't work here
- Handling edge cases (no courses, no prerequisites, self-loops)

---

#### Problem 3: Longest Consecutive Sequence (#128)
**Problem Statement:**
Given an unsorted array of integers `nums`, return the length of the longest consecutive elements sequence. Your algorithm should run in O(n) time.

**Example:**
```
Input: nums = [100,4,200,1,3,2]
Output: 4
Explanation: The longest consecutive sequence is [1,2,3,4]
```

**Solution Approaches:**

**Approach 1: Sorting (Suboptimal)**

```python
def longestConsecutive(nums):
    if not nums:
        return 0
    
    nums.sort()
    longest = 1
    current = 1
    
    for i in range(1, len(nums)):
        if nums[i] == nums[i-1]:
            continue
        elif nums[i] == nums[i-1] + 1:
            current += 1
        else:
            longest = max(longest, current)
            current = 1
    
    return max(longest, current)
```

- **Time Complexity:** O(n log n) - dominated by sorting
- **Space Complexity:** O(1) or O(n) depending on sort implementation
- **Pros:** Simple, intuitive
- **Cons:** Doesn't meet O(n) requirement

**Approach 2: Hash Set (Optimal)**

```python
def longestConsecutive(nums):
    if not nums:
        return 0
    
    num_set = set(nums)
    longest = 0
    
    for num in num_set:
        # Only start counting if this is the beginning of a sequence
        if num - 1 not in num_set:
            current_num = num
            current_length = 1
            
            while current_num + 1 in num_set:
                current_num += 1
                current_length += 1
            
            longest = max(longest, current_length)
    
    return longest
```

- **Time Complexity:** O(n) - each number visited at most twice
- **Space Complexity:** O(n) - hash set storage
- **Pros:** Achieves required O(n) time, elegant
- **Cons:** Uses extra space

**Key Insight:** The algorithm is O(n) even though there's a nested loop because:
- We only start counting from the beginning of sequences (num - 1 not in set)
- Each number is examined at most twice (once as potential start, once in a sequence)
- Total operations across all numbers is O(n)

**Approach 3: Union-Find (Overcomplicated)**

```python
class UnionFind:
    def __init__(self):
        self.parent = {}
        self.size = {}
    
    def add(self, x):
        if x not in self.parent:
            self.parent[x] = x
            self.size[x] = 1
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return
        if self.size[px] < self.size[py]:
            px, py = py, px
        self.parent[py] = px
        self.size[px] += self.size[py]

def longestConsecutive(nums):
    if not nums:
        return 0
    
    uf = UnionFind()
    for num in nums:
        if num in uf.parent:
            continue
        uf.add(num)
        if num - 1 in uf.parent:
            uf.union(num, num - 1)
        if num + 1 in uf.parent:
            uf.union(num, num + 1)
    
    return max(uf.size.values())
```

- **Time Complexity:** O(n × α(n)) ≈ O(n)
- **Space Complexity:** O(n)
- **Pros:** Works correctly, interesting approach
- **Cons:** Overcomplicated, harder to implement correctly

**Approach 4: HashMap with Range Tracking (Advanced)**

```python
def longestConsecutive(nums):
    if not nums:
        return 0
    
    ranges = {}  # num -> length of sequence containing num
    longest = 0
    
    for num in nums:
        if num in ranges:
            continue
        
        left = ranges.get(num - 1, 0)
        right = ranges.get(num + 1, 0)
        length = left + right + 1
        
        # Update boundaries
        ranges[num] = length
        ranges[num - left] = length
        ranges[num + right] = length
        
        longest = max(longest, length)
    
    return longest
```

- **Time Complexity:** O(n)
- **Space Complexity:** O(n)
- **Pros:** Single pass, very efficient
- **Cons:** More complex logic, harder to understand

**Trade-off Analysis:**

| Approach | Time | Space | Difficulty | Best For |
|----------|------|-------|------------|----------|
| Sorting | O(n log n) | O(1) | Easy | When O(n log n) is acceptable |
| Hash Set | O(n) | O(n) | Medium | **Interviews - best balance** |
| Union-Find | O(n×α(n)) | O(n) | Hard | Learning UF, not practical here |
| HashMap Range | O(n) | O(n) | Hard | Performance-critical applications |

**What to Look For in Candidate:**

1. **Initial Approach:** Do they start with sorting? (Shows honesty about thought process)
2. **Optimization:** Can they recognize the O(n) hash set approach?
3. **Key Insight:** Do they understand why checking `num - 1 not in set` makes it O(n)?
4. **Edge Cases:** Empty array, duplicates, negative numbers
5. **Communication:** Can they explain why the nested loop doesn't make it O(n²)?

**Follow-up Questions:**
- What if the array is already sorted? (Can use O(1) space)
- What if we need to return the actual sequence, not just length?
- How would this work with a stream of numbers?

---

## Complexity Analysis Summary

### Time Complexity Hierarchy (Best to Worst)
1. **O(1)** - Constant: Hash table lookup, array access
2. **O(log n)** - Logarithmic: Binary search, balanced tree operations
3. **O(n)** - Linear: Single pass through data
4. **O(n log n)** - Linearithmic: Efficient sorting (merge, heap, quick)
5. **O(n²)** - Quadratic: Nested loops, bubble sort
6. **O(2ⁿ)** - Exponential: Recursive fibonacci without memoization
7. **O(n!)** - Factorial: Generating all permutations

### Space Complexity Considerations
- **In-place algorithms:** O(1) extra space (sorting, two pointers)
- **Hash tables:** O(n) space for O(1) lookups
- **Recursion:** O(recursion depth) stack space
- **DP:** Often trade O(n) or O(n²) space for optimized time

### Common Trade-offs
- **Time vs Space:** Hash maps trade memory for speed
- **Preprocessing:** Sorting data upfront may enable faster queries
- **Caching:** Memoization trades space for avoiding recomputation
- **Data Structures:** Trie uses more space but enables faster string operations

---

## Interview Tips

### For Interviewers (Evaluating Candidates)
1. **Start Simple:** Let them solve with brute force first
2. **Ask for Optimization:** "Can you improve the time complexity?"
3. **Probe Understanding:** "Why does this approach work? What's the complexity?"
4. **Edge Cases:** "What happens if the input is empty/null/negative?"
5. **Trade-offs:** "Why did you choose this approach over alternatives?"

### Problem Difficulty Guidelines
- **Easy (5-15 min):** Basic data structures, simple algorithms
- **Medium (20-35 min):** Multiple approaches, optimization required
- **Hard (35-45 min):** Complex algorithms, multiple data structures combined

### Red Flags & Green Flags

**Red Flags:**
- ❌ Can't explain their own code
- ❌ Doesn't consider edge cases
- ❌ Can't analyze time/space complexity
- ❌ Gives up without trying simpler approaches first

**Green Flags:**
- ✅ Communicates thought process clearly
- ✅ Starts with brute force and optimizes
- ✅ Tests code with examples
- ✅ Discusses trade-offs between approaches
- ✅ Asks clarifying questions about requirements

---

## Backup Instructions

### Prerequisites

- Python 3.8+ installed (`python3 --version`)
- A LeetCode account
- Basic terminal / shell familiarity

All commands below assume **macOS / Linux**. On Windows PowerShell, replace activation commands with the noted variants.

---

### Setup & Installation

**1. Create Project Directory:**

```bash
mkdir -p ~/projects/leetcode-export
cd ~/projects/leetcode-export
```

**2. Create Virtual Environment:**

```bash
python3 -m venv .venv
```

**3. Activate Virtual Environment:**

- macOS / Linux:
  ```bash
  source .venv/bin/activate
  ```

- Windows (PowerShell):
  ```powershell
  .venv\Scripts\Activate.ps1
  ```

You should now see `(.venv)` at the start of your shell prompt.

**4. Install leetcode-export:**

```bash
pip install leetcode-export
```

**5. Verify Installation:**

```bash
leetcode-export -V
leetcode-export -h
```

---

### Export Your Solutions

**1. Get Your LeetCode Cookies:**

The tool needs your **LeetCode session cookies** to access your submissions.

1. Log into [https://leetcode.com](https://leetcode.com) in your browser
2. Open **Developer Tools → Network** (F12 or right-click → Inspect)
3. Refresh the page
4. In the Network tab, click any request to `https://leetcode.com/...`
5. In the **Headers** section, find the `Cookie` header
6. Copy the entire cookie string, which will look like:
   ```
   LEETCODE_SESSION=...; csrftoken=...; other_cookie=...
   ```
7. In your terminal (with venv active), set an environment variable:
   ```bash
   export LC_COOKIES='LEETCODE_SESSION=...; csrftoken=...; other_cookie=...'
   ```

Use **single quotes** `'...'` to avoid shell parsing issues.

**2. Create Output Folder:**

```bash
mkdir -p leetcode-backup
```

**3. Run Basic Export:**

```bash
leetcode-export \
  --cookies "$LC_COOKIES" \
  --folder ./leetcode-backup \
  --only-accepted \
  --only-last-submission
```

**Options Explained:**
- `--cookies "$LC_COOKIES"` - Uses your logged-in browser session
- `--folder ./leetcode-backup` - Output directory
- `--only-accepted` - Saves only Accepted submissions
- `--only-last-submission` - Saves only latest submission per language

Add `-v` for verbose logging:

```bash
leetcode-export \
  --cookies "$LC_COOKIES" \
  --folder ./leetcode-backup \
  --only-accepted \
  --only-last-submission \
  -v
```

---

### Advanced Options

**Filter by Language:**

```bash
leetcode-export \
  --cookies "$LC_COOKIES" \
  --folder ./leetcode-backup \
  --only-accepted \
  --only-last-submission \
  --language=typescript,python3 \
  -v
```

**Supported Languages:**
`python, python3, pythondata, c, cpp, csharp, java, kotlin, mysql, mssql, oraclesql, javascript, html, php, golang, scala, pythonml, rust, ruby, bash, swift, typescript, elixir, erlang, racket, dart`

**Skip Problem Statements:**

```bash
leetcode-export \
  --cookies "$LC_COOKIES" \
  --folder ./leetcode-backup \
  --only-accepted \
  --only-last-submission \
  --language=typescript,python3 \
  --no-problem-statement \
  -v
```

**Customize Folder Structure:**

```bash
leetcode-export \
  --cookies "$LC_COOKIES" \
  --folder ./leetcode-backup \
  --only-accepted \
  --only-last-submission \
  --language=typescript,python3 \
  --problem-folder-name="{frontend_id}-{title_slug}" \
  --submission-filename="{lang}.txt" \
  -v
```

**Typical Output Structure:**
```
leetcode-backup/
  0001-two-sum/
    typescript.txt
    python3.txt
  0002-add-two-numbers/
    typescript.txt
```

**Verify Exported Files:**

```bash
cd leetcode-backup
ls
ls 0001-two-sum
cat 0001-two-sum/typescript.txt
```

**Version Control (Optional):**

```bash
cd ~/projects/leetcode-export
git init
echo ".venv" >> .gitignore
echo "__pycache__/" >> .gitignore
git add leetcode-backup .gitignore
git commit -m "Initial LeetCode backup"
```

⚠️ Make sure the repo is **private** if you store problem statements.

**Re-running Export Later:**

```bash
cd ~/projects/leetcode-export
source .venv/bin/activate
export LC_COOKIES='LEETCODE_SESSION=...; csrftoken=...; other_cookie=...'

leetcode-export \
  --cookies "$LC_COOKIES" \
  --folder ./leetcode-backup \
  --only-accepted \
  --only-last-submission \
  --language=typescript,python3 \
  -v
```

---

### Troubleshooting

**401 / Unauthorized or Empty Output:**
- Your `LC_COOKIES` value may be stale
- Grab a fresh `Cookie` header from your browser and re-export it

**Quoting Issues:**
- Ensure `LC_COOKIES` is wrapped in **single quotes** `'...'`
- Pass as `"$LC_COOKIES"` to the command

**Virtualenv Not Active:**
- If `leetcode-export` is "not found", re-activate:
  ```bash
  cd ~/projects/leetcode-export
  source .venv/bin/activate
  ```

---

You now have a complete system for managing, analyzing, and backing up your LeetCode solutions!
