# Linked Lists - Complete Guide

## 📋 Pattern Recognition

**When to use Linked Lists:**
- Problems mention "list" or "chain" of nodes
- Need to insert/delete in middle frequently (O(1) after finding position)
- Don't need random access
- Memory is fragmented

**Common Keywords:**
- "Merge", "Reverse", "Cycle", "Remove", "Partition", "Rotate"
- "nth node from end", "middle of list"

---

## 🎯 Key Concepts

### 1. Node Structure
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

### 2. Core Operations Complexity
- **Access:** O(n) - must traverse from head
- **Search:** O(n) - linear search
- **Insert at beginning:** O(1)
- **Insert at end:** O(n) without tail pointer, O(1) with tail
- **Delete:** O(n) to find, O(1) to delete

---

## 🔧 Essential Techniques

### Technique 1: Dummy Node
**When:** Simplifies edge cases when head might change

```python
def example(head: ListNode) -> ListNode:
    dummy = ListNode(0)  # Create dummy node
    dummy.next = head
    current = dummy
    
    # Do operations...
    
    return dummy.next  # Return new head
```

**Use Cases:**
- Merging lists
- Removing nodes (including head)
- Building new lists

---

### Technique 2: Two Pointers (Fast & Slow)
**When:** Find middle, detect cycles, find nth from end

#### Pattern A: Find Middle
```python
def findMiddle(head: ListNode) -> ListNode:
    """
    Fast moves 2x speed, slow moves 1x
    When fast reaches end, slow is at middle
    """
    slow = fast = head
    
    while fast and fast.next:
        slow = slow.next        # Move 1 step
        fast = fast.next.next   # Move 2 steps
    
    return slow  # Middle node
```

#### Pattern B: Detect Cycle (Floyd's Algorithm)
```python
def hasCycle(head: ListNode) -> bool:
    """
    If there's a cycle, fast will eventually catch slow
    Like runners on a circular track
    """
    if not head:
        return False
    
    slow = fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
        if slow == fast:  # They met!
            return True
    
    return False
```

#### Pattern C: Find Nth from End
```python
def findNthFromEnd(head: ListNode, n: int) -> ListNode:
    """
    Two pointers n nodes apart
    When first reaches end, second is at target
    """
    first = second = head
    
    # Move first n steps ahead
    for _ in range(n):
        if not first:
            return None
        first = first.next
    
    # Move both until first reaches end
    while first:
        first = first.next
        second = second.next
    
    return second
```

---

### Technique 3: Reversing
**When:** Reverse entire list, reverse in groups, palindrome check

#### Pattern A: Reverse Entire List (Iterative)
```python
def reverseList(head: ListNode) -> ListNode:
    """
    Reverse pointers iteratively
    
    Before: 1 → 2 → 3 → None
    After:  None ← 1 ← 2 ← 3
    """
    prev = None
    current = head
    
    while current:
        # Save next node
        next_node = current.next
        
        # Reverse the pointer
        current.next = prev
        
        # Move forward
        prev = current
        current = next_node
    
    return prev  # New head
```

#### Pattern B: Reverse Entire List (Recursive)
```python
def reverseListRecursive(head: ListNode) -> ListNode:
    """
    Recursive reversal - elegant but uses O(n) stack space
    """
    # Base case
    if not head or not head.next:
        return head
    
    # Reverse rest of list
    new_head = reverseListRecursive(head.next)
    
    # Reverse pointer
    head.next.next = head
    head.next = None
    
    return new_head
```

#### Pattern C: Reverse Between Positions
```python
def reverseBetween(head: ListNode, left: int, right: int) -> ListNode:
    """
    Reverse nodes from position left to right
    LeetCode #92
    """
    if not head or left == right:
        return head
    
    dummy = ListNode(0)
    dummy.next = head
    prev = dummy
    
    # Move to node before 'left'
    for _ in range(left - 1):
        prev = prev.next
    
    # Reverse the sublist
    current = prev.next
    for _ in range(right - left):
        next_node = current.next
        current.next = next_node.next
        next_node.next = prev.next
        prev.next = next_node
    
    return dummy.next
```

---

### Technique 4: Merging Lists
**When:** Combine multiple sorted lists

```python
def mergeTwoLists(l1: ListNode, l2: ListNode) -> ListNode:
    """
    Merge two sorted lists
    LeetCode #21
    """
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
    
    # Append remaining nodes
    current.next = l1 if l1 else l2
    
    return dummy.next
```

---

## 💡 Common Patterns & Solutions

### Pattern 1: Remove Nodes
```python
def removeElements(head: ListNode, val: int) -> ListNode:
    """
    Remove all nodes with value = val
    LeetCode #203
    """
    dummy = ListNode(0)
    dummy.next = head
    current = dummy
    
    while current.next:
        if current.next.val == val:
            current.next = current.next.next  # Skip node
        else:
            current = current.next
    
    return dummy.next


def removeNthFromEnd(head: ListNode, n: int) -> ListNode:
    """
    Remove nth node from end
    LeetCode #19
    """
    dummy = ListNode(0)
    dummy.next = head
    first = second = dummy
    
    # Move first n+1 steps ahead
    for _ in range(n + 1):
        first = first.next
    
    # Move both until first reaches end
    while first:
        first = first.next
        second = second.next
    
    # Remove node
    second.next = second.next.next
    
    return dummy.next
```

### Pattern 2: Palindrome Check
```python
def isPalindrome(head: ListNode) -> bool:
    """
    Check if linked list is palindrome
    LeetCode #234
    
    Strategy:
    1. Find middle (fast/slow pointers)
    2. Reverse second half
    3. Compare both halves
    """
    if not head or not head.next:
        return True
    
    # Find middle
    slow = fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    
    # Reverse second half
    second_half = reverseList(slow.next)
    slow.next = None
    
    # Compare
    p1, p2 = head, second_half
    result = True
    while p2:
        if p1.val != p2.val:
            result = False
            break
        p1 = p1.next
        p2 = p2.next
    
    return result
```

### Pattern 3: Cycle Detection & Finding Entry
```python
def detectCycle(head: ListNode) -> ListNode:
    """
    Find where cycle begins
    LeetCode #142
    
    Floyd's Algorithm:
    1. Detect cycle with fast/slow
    2. Move one pointer to head
    3. Move both at same speed - they meet at cycle start
    """
    if not head:
        return None
    
    # Detect cycle
    slow = fast = head
    has_cycle = False
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
        if slow == fast:
            has_cycle = True
            break
    
    if not has_cycle:
        return None
    
    # Find cycle start
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next
    
    return slow
```

### Pattern 4: Reorder List
```python
def reorderList(head: ListNode) -> None:
    """
    Reorder L0→L1→L2→...→Ln to L0→Ln→L1→Ln-1→L2→Ln-2→...
    LeetCode #143
    
    Strategy:
    1. Find middle
    2. Reverse second half
    3. Merge alternately
    """
    if not head or not head.next:
        return
    
    # Find middle
    slow = fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    
    # Reverse second half
    second = slow.next
    slow.next = None
    second = reverseList(second)
    
    # Merge alternately
    first = head
    while second:
        tmp1, tmp2 = first.next, second.next
        first.next = second
        second.next = tmp1
        first, second = tmp1, tmp2
```

---

## 🎓 Practice Problems by Difficulty

### Easy
1. **#206 Reverse Linked List** - Master this first!
2. **#21 Merge Two Sorted Lists** - Dummy node pattern
3. **#141 Linked List Cycle** - Floyd's algorithm basics
4. **#234 Palindrome Linked List** - Combine multiple techniques
5. **#83 Remove Duplicates from Sorted List**

### Medium
1. **#19 Remove Nth Node From End** - Two pointers
2. **#142 Linked List Cycle II** - Find cycle entry
3. **#143 Reorder List** - Multiple techniques combined
4. **#2 Add Two Numbers** - List traversal with carry
5. **#138 Copy List with Random Pointer** - Hash map + cloning
6. **#148 Sort List** - Merge sort on linked list
7. **#92 Reverse Linked List II** - Partial reversal

### Hard
1. **#25 Reverse Nodes in k-Group** - Advanced reversal
2. **#23 Merge k Sorted Lists** - Heap or divide & conquer

---

## 🐛 Common Mistakes & How to Avoid

### Mistake 1: Losing Reference to Head
```python
# ❌ WRONG
def example(head):
    while head:
        head = head.next  # Lost original head!
    return head

# ✅ CORRECT
def example(head):
    current = head  # Use separate pointer
    while current:
        current = current.next
    return head
```

### Mistake 2: Not Checking for None
```python
# ❌ WRONG - Will crash if node is None
next_node = current.next.next

# ✅ CORRECT
if current and current.next:
    next_node = current.next.next
```

### Mistake 3: Forgetting to Update Pointers
```python
# ❌ WRONG - Infinite loop!
while current:
    # Forgot to move current forward
    pass

# ✅ CORRECT
while current:
    current = current.next
```

### Mistake 4: Off-by-One in Two Pointers
```python
# When finding nth from end:
# Move first pointer n steps, not n+1 (unless you want prev node)

# To remove nth from end, need prev node:
for _ in range(n + 1):  # One extra step
    first = first.next
```

---

## 💡 Pro Tips

### Tip 1: Draw It Out
Always draw the linked list on paper/whiteboard before coding:
```
Before: 1 → 2 → 3 → 4 → None
         ↑       ↑
       prev   current

After:  1 ← 2   3 → 4 → None
```

### Tip 2: Use Dummy Node Liberally
When in doubt, use a dummy node! It simplifies:
- Edge cases when head changes
- Building new lists
- Merging/splitting operations

### Tip 3: Check These Edge Cases
```python
# Always test:
1. Empty list (head = None)
2. Single node
3. Two nodes
4. Odd vs even length
5. Target at head
6. Target at tail
```

### Tip 4: Space-Time Tradeoffs
```python
# Hash Map: O(n) space, O(n) time
visited = set()
while current:
    if current in visited:
        return True
    visited.add(current)
    current = current.next

# Two Pointers: O(1) space, O(n) time
# Use two pointers when possible to save space
```

---

## 🎯 Interview Strategy

### Step 1: Clarify (30 seconds)
- "Is this a singly or doubly linked list?"
- "Can the list have cycles?"
- "What should I return if the list is empty?"

### Step 2: Examples (1 minute)
Draw 2-3 examples:
- Normal case
- Edge case (empty, single node)
- Tricky case

### Step 3: Approach (1-2 minutes)
- Explain technique (two pointers, reversal, etc.)
- Mention time/space complexity
- Get approval before coding

### Step 4: Code (5-10 minutes)
- Use clear variable names
- Add comments for tricky parts
- Handle edge cases first

### Step 5: Test (2-3 minutes)
Walk through your code with:
- Your example inputs
- Edge cases
- Verify pointers are updated correctly

---

## 📚 Additional Resources

**Helper Functions to Know:**
```python
def printList(head: ListNode) -> None:
    """Print list for debugging"""
    values = []
    while head:
        values.append(str(head.val))
        head = head.next
    print(" → ".join(values))


def createList(values: list) -> ListNode:
    """Create list from array for testing"""
    if not values:
        return None
    head = ListNode(values[0])
    current = head
    for val in values[1:]:
        current.next = ListNode(val)
        current = current.next
    return head


def listToArray(head: ListNode) -> list:
    """Convert list to array for testing"""
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result
```

**Remember:** Linked lists are all about pointer manipulation. Master the basics (reversal, two pointers) and everything else builds on top!

