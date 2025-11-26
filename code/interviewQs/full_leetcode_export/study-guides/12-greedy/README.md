# Greedy Algorithms - Complete Guide

## 📋 Pattern Recognition

**When to use Greedy:**
- "Maximize/minimize" something
- Making locally optimal choices
- Interval scheduling problems
- Array/string manipulation with simple rule
- Problem has "greedy choice property"

**Keywords:** maximum, minimum, optimal, schedule, earliest, latest

---

## 🎯 Greedy vs DP

**Use Greedy when:**
- Local optimum leads to global optimum
- No need to reconsider previous choices
- Simple decision rule exists

**Use DP when:**
- Need to try all possibilities
- Overlapping subproblems
- Previous choices affect future

---

## 🔧 Pattern 1: Interval Scheduling

### Non-overlapping Intervals
```python
def eraseOverlapIntervals(intervals: list[list[int]]) -> int:
    """
    LeetCode #435
    Remove minimum intervals to make rest non-overlapping
    
    Greedy: Always keep interval that ends earliest
    Time: O(n log n), Space: O(1)
    """
    if not intervals:
        return 0
    
    # Sort by end time
    intervals.sort(key=lambda x: x[1])
    
    count = 0
    prev_end = intervals[0][1]
    
    for i in range(1, len(intervals)):
        if intervals[i][0] < prev_end:
            # Overlapping - remove current
            count += 1
        else:
            # Non-overlapping - update end time
            prev_end = intervals[i][1]
    
    return count

# Why greedy works:
# Keeping the interval that ends earliest leaves
# maximum room for future intervals
```

### Meeting Rooms II
```python
def minMeetingRooms(intervals: list[list[int]]) -> int:
    """
    LeetCode #253 (Premium)
    Find minimum meeting rooms needed
    
    Time: O(n log n), Space: O(n)
    """
    if not intervals:
        return 0
    
    # Separate start and end times
    starts = sorted([i[0] for i in intervals])
    ends = sorted([i[1] for i in intervals])
    
    rooms = 0
    max_rooms = 0
    s = e = 0
    
    while s < len(starts):
        if starts[s] < ends[e]:
            # Meeting starting, need room
            rooms += 1
            max_rooms = max(max_rooms, rooms)
            s += 1
        else:
            # Meeting ending, free room
            rooms -= 1
            e += 1
    
    return max_rooms
```

---

## 🔧 Pattern 2: Jump Game

### Jump Game I
```python
def canJump(nums: list[int]) -> bool:
    """
    LeetCode #55
    Can reach last index?
    [2,3,1,1,4] → True, [3,2,1,0,4] → False
    
    Greedy: Track furthest reachable position
    Time: O(n), Space: O(1)
    """
    max_reach = 0
    
    for i in range(len(nums)):
        # Can't reach position i
        if i > max_reach:
            return False
        
        # Update furthest reachable
        max_reach = max(max_reach, i + nums[i])
        
        # Can reach end
        if max_reach >= len(nums) - 1:
            return True
    
    return True
```

### Jump Game II - Minimum Jumps
```python
def jump(nums: list[int]) -> int:
    """
    LeetCode #45
    Minimum jumps to reach end
    
    Greedy: Jump to position that gives furthest reach
    Time: O(n), Space: O(1)
    """
    if len(nums) <= 1:
        return 0
    
    jumps = 0
    current_end = 0
    farthest = 0
    
    for i in range(len(nums) - 1):
        # Update farthest reachable from current position
        farthest = max(farthest, i + nums[i])
        
        # Reached end of current jump range
        if i == current_end:
            jumps += 1
            current_end = farthest
            
            # Can reach end
            if current_end >= len(nums) - 1:
                break
    
    return jumps

# Example: [2,3,1,1,4]
# i=0: farthest=2, jumps=1, current_end=2
# i=1: farthest=4, jumps=1
# i=2: farthest=4, jumps=2, current_end=4 (reached end)
```

---

## 🔧 Pattern 3: Greedy with Sorting

### Maximum Units on Truck
```python
def maximumUnits(boxTypes: list[list[int]], truckSize: int) -> int:
    """
    LeetCode #1710
    boxTypes[i] = [numberOfBoxes, unitsPerBox]
    
    Greedy: Take boxes with most units first
    Time: O(n log n), Space: O(1)
    """
    # Sort by units per box (descending)
    boxTypes.sort(key=lambda x: x[1], reverse=True)
    
    total_units = 0
    remaining = truckSize
    
    for boxes, units in boxTypes:
        # Take as many boxes as possible
        take = min(boxes, remaining)
        total_units += take * units
        remaining -= take
        
        if remaining == 0:
            break
    
    return total_units
```

### Boats to Save People
```python
def numRescueBoats(people: list[int], limit: int) -> int:
    """
    LeetCode #881
    Each boat carries at most 2 people
    
    Greedy: Pair heaviest with lightest
    Time: O(n log n), Space: O(1)
    """
    people.sort()
    
    left, right = 0, len(people) - 1
    boats = 0
    
    while left <= right:
        # Try to pair heaviest with lightest
        if people[left] + people[right] <= limit:
            left += 1  # Lightest person fits
        
        # Always take heaviest person
        right -= 1
        boats += 1
    
    return boats
```

---

## 🔧 Pattern 4: Gas Station (Circular Array)

```python
def canCompleteCircuit(gas: list[int], cost: list[int]) -> int:
    """
    LeetCode #134
    Find starting gas station to complete circuit
    
    Key insight: If total gas >= total cost, solution exists
    Start from first station where we don't run out of gas
    
    Time: O(n), Space: O(1)
    """
    total_tank = 0
    current_tank = 0
    start = 0
    
    for i in range(len(gas)):
        total_tank += gas[i] - cost[i]
        current_tank += gas[i] - cost[i]
        
        # Can't reach next station from current start
        if current_tank < 0:
            # Try starting from next station
            start = i + 1
            current_tank = 0
    
    # If total gas >= total cost, solution exists
    return start if total_tank >= 0 else -1

# Why greedy works:
# If we can't reach station j from station i,
# we also can't reach j from any station between i and j
```

---

## 🔧 Pattern 5: String Manipulation

### Remove K Digits
```python
def removeKdigits(num: str, k: int) -> str:
    """
    LeetCode #402
    Remove k digits to make smallest number
    "1432219" k=3 → "1219"
    
    Greedy: Remove larger digits from left
    Time: O(n), Space: O(n)
    """
    stack = []
    
    for digit in num:
        # Remove larger digits from stack
        while k > 0 and stack and stack[-1] > digit:
            stack.pop()
            k -= 1
        
        stack.append(digit)
    
    # Remove remaining k digits from end
    stack = stack[:-k] if k > 0 else stack
    
    # Remove leading zeros
    result = ''.join(stack).lstrip('0')
    
    return result or '0'
```

### Partition Labels
```python
def partitionLabels(s: str) -> list[int]:
    """
    LeetCode #763
    Partition string into max number of parts
    Each letter appears in at most one part
    
    "ababcbacadefegdehijhklij" → [9,7,8]
    
    Time: O(n), Space: O(1) - only 26 letters
    """
    # Record last occurrence of each character
    last = {char: i for i, char in enumerate(s)}
    
    partitions = []
    start = 0
    end = 0
    
    for i, char in enumerate(s):
        # Extend partition to include last occurrence
        end = max(end, last[char])
        
        # Reached end of current partition
        if i == end:
            partitions.append(end - start + 1)
            start = i + 1
    
    return partitions
```

---

## 🔧 Pattern 6: Maximize/Minimize with Constraints

### Maximum Subarray (Kadane's Algorithm)
```python
def maxSubArray(nums: list[int]) -> int:
    """
    LeetCode #53
    Find subarray with maximum sum
    
    Greedy: If current sum becomes negative, start fresh
    Time: O(n), Space: O(1)
    """
    max_sum = nums[0]
    current_sum = nums[0]
    
    for i in range(1, len(nums)):
        # Either extend current subarray or start new
        current_sum = max(nums[i], current_sum + nums[i])
        max_sum = max(max_sum, current_sum)
    
    return max_sum
```

### Best Time to Buy and Sell Stock II
```python
def maxProfit(prices: list[int]) -> int:
    """
    LeetCode #122
    Buy and sell multiple times (unlimited transactions)
    
    Greedy: Capture all upward movements
    Time: O(n), Space: O(1)
    """
    profit = 0
    
    for i in range(1, len(prices)):
        # If price increased, capture the profit
        if prices[i] > prices[i-1]:
            profit += prices[i] - prices[i-1]
    
    return profit
```

---

## 🎓 Key Problems by Pattern

**Intervals:**
- #435 Non-overlapping Intervals
- #452 Minimum Arrows to Burst Balloons
- #253 Meeting Rooms II (Premium)

**Jump:**
- #55 Jump Game
- #45 Jump Game II

**Sorting + Greedy:**
- #881 Boats to Save People
- #1710 Maximum Units on Truck
- #621 Task Scheduler

**Circular:**
- #134 Gas Station

**String:**
- #402 Remove K Digits
- #763 Partition Labels
- #316 Remove Duplicate Letters

**Array:**
- #53 Maximum Subarray (Kadane)
- #122 Best Time to Buy and Sell Stock II

---

## 🚨 Common Mistakes

1. **Not proving greedy works:**
   - Verify local optimal leads to global optimal
   - Consider counterexamples

2. **Wrong sorting key:**
   ```python
   # For intervals, often sort by END time, not start
   intervals.sort(key=lambda x: x[1])  # End time
   ```

3. **Forgetting edge cases:**
   - Empty input
   - Single element
   - All same values

---

## 💡 Pro Tips

**How to identify greedy:**
1. Problem asks for max/min
2. Simple decision rule exists
3. Can't construct counterexample where greedy fails

**Common greedy strategies:**
- Sort + process in order
- Track min/max so far
- Make decision based on current state only
- Use stack for monotonic properties

**Proving correctness:**
- Exchange argument (swapping doesn't improve)
- Induction (optimal for n-1 → optimal for n)
- Contradiction (greedy not optimal → contradiction)

**Greedy vs DP:**
| Greedy | DP |
|--------|-----|
| O(n) or O(n log n) | O(n²) or higher |
| No reconsideration | Tries all options |
| Local → Global | Bottom-up/Top-down |

---

**When greedy works, it's the most elegant solution!**

