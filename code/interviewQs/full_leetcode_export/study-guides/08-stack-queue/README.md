# Stack & Queue - Complete Guide

## 📋 Pattern Recognition

**When to use Stack/Queue:**
- **Stack (LIFO):** Matching pairs, expression evaluation, undo operations
- **Queue (FIFO):** Level-order traversal, BFS, task scheduling
- **Monotonic Stack:** Next greater/smaller element

**Keywords:** parentheses, expression, calculator, next greater, temperatures

---

## 🎯 Basics

### Stack Operations
```python
stack = []
stack.append(x)  # push - O(1)
x = stack.pop()  # pop - O(1)
x = stack[-1]    # peek - O(1)
```

### Queue Operations
```python
from collections import deque

queue = deque()
queue.append(x)      # enqueue - O(1)
x = queue.popleft()  # dequeue - O(1)
```

---

## 🔧 Pattern 1: Valid Parentheses

```python
def isValid(s: str) -> bool:
    """
    LeetCode #20
    Time: O(n), Space: O(n)
    """
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:
            if not stack or stack[-1] != mapping[char]:
                return False
            stack.pop()
        else:
            stack.append(char)
    
    return len(stack) == 0
```

---

## 🔧 Pattern 2: Monotonic Stack 🚨 CRITICAL

### Next Greater Element
```python
def nextGreaterElements(nums: list[int]) -> list[int]:
    """
    LeetCode #503
    Monotonic decreasing stack
    
    Time: O(n), Space: O(n)
    """
    n = len(nums)
    result = [-1] * n
    stack = []  # indices
    
    # Process array twice for circular
    for i in range(2 * n):
        while stack and nums[stack[-1]] < nums[i % n]:
            result[stack.pop()] = nums[i % n]
        
        if i < n:
            stack.append(i)
    
    return result
```

### Daily Temperatures
```python
def dailyTemperatures(temperatures: list[int]) -> list[int]:
    """
    LeetCode #739
    Time: O(n), Space: O(n)
    """
    n = len(temperatures)
    result = [0] * n
    stack = []  # indices
    
    for i, temp in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < temp:
            prev_idx = stack.pop()
            result[prev_idx] = i - prev_idx
        stack.append(i)
    
    return result
```

---

## 🔧 Pattern 3: Expression Evaluation

### Basic Calculator II
```python
def calculate(s: str) -> int:
    """
    LeetCode #227 - Handle +, -, *, /
    Time: O(n), Space: O(n)
    """
    stack = []
    num = 0
    operator = '+'
    
    for i, char in enumerate(s):
        if char.isdigit():
            num = num * 10 + int(char)
        
        if char in '+-*/' or i == len(s) - 1:
            if operator == '+':
                stack.append(num)
            elif operator == '-':
                stack.append(-num)
            elif operator == '*':
                stack.append(stack.pop() * num)
            elif operator == '/':
                stack.append(int(stack.pop() / num))
            
            operator = char
            num = 0
    
    return sum(stack)
```

---

## 🔧 Pattern 4: Sliding Window Maximum

### Using Deque (Monotonic Queue)
```python
from collections import deque

def maxSlidingWindow(nums: list[int], k: int) -> list[int]:
    """
    LeetCode #239 🚨 MUST DO
    Monotonic decreasing deque
    
    Time: O(n), Space: O(k)
    """
    dq = deque()  # indices of useful elements
    result = []
    
    for i, num in enumerate(nums):
        # Remove elements outside window
        if dq and dq[0] < i - k + 1:
            dq.popleft()
        
        # Remove smaller elements (not useful)
        while dq and nums[dq[-1]] < num:
            dq.pop()
        
        dq.append(i)
        
        # Add to result when window is full
        if i >= k - 1:
            result.append(nums[dq[0]])
    
    return result
```

---

## 🎓 Key Problems

### Must Do:
1. #20 Valid Parentheses (Stack basics)
2. #739 Daily Temperatures (Monotonic stack)
3. #84 Largest Rectangle in Histogram (Monotonic stack)
4. #239 Sliding Window Maximum (Monotonic deque)
5. #227 Basic Calculator II (Expression evaluation)

---

## 💡 Pro Tip

**Monotonic Stack Pattern:**
```python
# Template for "next greater" problems
stack = []
for i, num in enumerate(nums):
    while stack and condition:
        # Process elements
        stack.pop()
    stack.append(i)
```

---

**Remember:** Stack for matching/evaluation, Monotonic Stack for next greater/smaller!

