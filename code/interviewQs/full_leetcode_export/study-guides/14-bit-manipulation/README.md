# Bit Manipulation - Complete Guide

## 📋 Pattern Recognition

**When to use Bit Manipulation:**
- Problem mentions "XOR", "AND", "OR"
- Need O(1) space for set operations
- Checking even/odd, power of 2
- Counting set bits
- Finding single/duplicate numbers

**Keywords:** bit, binary, XOR, power of 2, even/odd, single number

---

## 🎯 Bit Manipulation Basics

### Binary Operators
```python
# AND (&) - both bits must be 1
5 & 3  # 0101 & 0011 = 0001 = 1

# OR (|) - at least one bit is 1
5 | 3  # 0101 | 0011 = 0111 = 7

# XOR (^) - bits are different
5 ^ 3  # 0101 ^ 0011 = 0110 = 6

# NOT (~) - flip all bits
~5  # ~0101 = 1010 (two's complement in Python)

# Left shift (<<) - multiply by 2^n
5 << 1  # 0101 << 1 = 1010 = 10
5 << 2  # 0101 << 2 = 10100 = 20

# Right shift (>>) - divide by 2^n
5 >> 1  # 0101 >> 1 = 0010 = 2
5 >> 2  # 0101 >> 2 = 0001 = 1
```

### Key Properties
```python
# XOR properties (CRITICAL!)
x ^ 0 = x          # Identity
x ^ x = 0          # Self-cancellation
x ^ y = y ^ x      # Commutative
(x ^ y) ^ z = x ^ (y ^ z)  # Associative

# Common bit tricks
x & 1 == 1         # Check if odd
x & (x-1) == 0     # Check if power of 2
x & (x-1)          # Remove rightmost 1 bit
x & -x             # Isolate rightmost 1 bit
x | (1 << i)       # Set i-th bit
x & ~(1 << i)      # Clear i-th bit
x ^ (1 << i)       # Toggle i-th bit
(x >> i) & 1       # Get i-th bit
```

---

## 🔧 Pattern 1: XOR Tricks

### Single Number
```python
def singleNumber(nums: list[int]) -> int:
    """
    LeetCode #136
    Every element appears twice except one
    
    Key insight: a ^ a = 0, so pairs cancel out
    Time: O(n), Space: O(1)
    """
    result = 0
    for num in nums:
        result ^= num
    return result

# Example: [4,1,2,1,2]
# 0 ^ 4 = 4
# 4 ^ 1 = 5
# 5 ^ 2 = 7
# 7 ^ 1 = 6
# 6 ^ 2 = 4 ✓
```

### Single Number II (Three times)
```python
def singleNumber2(nums: list[int]) -> int:
    """
    LeetCode #137
    Every element appears 3 times except one
    
    Track bits that appear 1 time and 2 times
    Time: O(n), Space: O(1)
    """
    ones = twos = 0
    
    for num in nums:
        # Add to twos if already in ones
        twos |= ones & num
        # Add to ones (XOR)
        ones ^= num
        # Remove if appears in both (seen 3 times)
        threes = ones & twos
        ones &= ~threes
        twos &= ~threes
    
    return ones
```

### Single Number III (Two singles)
```python
def singleNumber3(nums: list[int]) -> list[int]:
    """
    LeetCode #260
    Every element appears twice except TWO
    
    Strategy: Split into two groups using differing bit
    Time: O(n), Space: O(1)
    """
    # XOR of the two unique numbers
    xor = 0
    for num in nums:
        xor ^= num
    
    # Find rightmost set bit (where two numbers differ)
    rightmost_bit = xor & -xor
    
    # Divide into two groups and XOR separately
    a = b = 0
    for num in nums:
        if num & rightmost_bit:
            a ^= num
        else:
            b ^= num
    
    return [a, b]
```

---

## 🔧 Pattern 2: Counting Bits

### Number of 1 Bits
```python
def hammingWeight(n: int) -> int:
    """
    LeetCode #191
    Count number of 1 bits (Hamming Weight)
    
    Time: O(number of 1s), Space: O(1)
    """
    count = 0
    while n:
        n &= n - 1  # Remove rightmost 1 bit
        count += 1
    return count

# Example: n = 11 (1011)
# 1011 & 1010 = 1010 (removed rightmost 1)
# 1010 & 1001 = 1000
# 1000 & 0111 = 0000
# Count = 3
```

### Counting Bits for Range
```python
def countBits(n: int) -> list[int]:
    """
    LeetCode #338
    Count 1 bits for all numbers from 0 to n
    
    DP: ans[i] = ans[i >> 1] + (i & 1)
    Time: O(n), Space: O(1) excluding output
    """
    ans = [0] * (n + 1)
    
    for i in range(1, n + 1):
        # Number of 1s in i = (number in i//2) + (last bit of i)
        ans[i] = ans[i >> 1] + (i & 1)
    
    return ans

# Example: n = 5
# 0: 0000 → 0
# 1: 0001 → 1 (ans[0] + 1)
# 2: 0010 → 1 (ans[1] + 0)
# 3: 0011 → 2 (ans[1] + 1)
# 4: 0100 → 1 (ans[2] + 0)
# 5: 0101 → 2 (ans[2] + 1)
```

---

## 🔧 Pattern 3: Power of Two/Four

### Power of Two
```python
def isPowerOfTwo(n: int) -> bool:
    """
    LeetCode #231
    Check if n is power of 2
    
    Power of 2 has exactly one 1 bit
    Time: O(1), Space: O(1)
    """
    return n > 0 and (n & (n - 1)) == 0

# Examples:
# 8  = 1000 & 0111 = 0000 ✓
# 10 = 1010 & 1001 = 1000 ✗
```

### Power of Four
```python
def isPowerOfFour(n: int) -> bool:
    """
    LeetCode #342
    Check if n is power of 4
    
    Power of 4:
    1. Is power of 2
    2. 1 bit is at even position (0, 2, 4, ...)
    
    Time: O(1), Space: O(1)
    """
    # 0x55555555 = 01010101010101010101010101010101 (1s at even positions)
    return n > 0 and (n & (n - 1)) == 0 and (n & 0x55555555) != 0

# Powers of 4: 1, 4, 16, 64, 256, ...
# Binary:      1, 100, 10000, 1000000, 100000000, ...
# Position:    0, 2, 4, 6, 8, ... (all even)
```

---

## 🔧 Pattern 4: Bitmasking for Subsets

### Subsets using Bitmask
```python
def subsets(nums: list[int]) -> list[list[int]]:
    """
    LeetCode #78 (Alternative solution using bit manipulation)
    Generate all subsets using bitmask
    
    Time: O(n * 2^n), Space: O(1) excluding output
    """
    n = len(nums)
    result = []
    
    # 2^n possible subsets
    for mask in range(1 << n):  # 0 to 2^n - 1
        subset = []
        for i in range(n):
            # Check if i-th bit is set
            if mask & (1 << i):
                subset.append(nums[i])
        result.append(subset)
    
    return result

# Example: nums = [1,2,3]
# mask=0 (000): []
# mask=1 (001): [1]
# mask=2 (010): [2]
# mask=3 (011): [1,2]
# mask=4 (100): [3]
# mask=5 (101): [1,3]
# mask=6 (110): [2,3]
# mask=7 (111): [1,2,3]
```

### Maximum XOR of Two Numbers
```python
def findMaximumXOR(nums: list[int]) -> int:
    """
    LeetCode #421
    Find maximum XOR of two numbers
    
    Greedy + Trie approach
    Time: O(n), Space: O(n)
    """
    max_xor = 0
    mask = 0
    
    # Check from leftmost bit to rightmost
    for i in range(31, -1, -1):
        mask |= (1 << i)
        prefixes = {num & mask for num in nums}
        
        # Try to set current bit to 1
        temp = max_xor | (1 << i)
        
        # Check if any two prefixes XOR to temp
        for prefix in prefixes:
            if (temp ^ prefix) in prefixes:
                max_xor = temp
                break
    
    return max_xor
```

---

## 🔧 Pattern 5: Bit Manipulation + Math

### Sum of Two Integers (Without + or -)
```python
def getSum(a: int, b: int) -> int:
    """
    LeetCode #371
    Add two integers using bit manipulation
    
    Time: O(1), Space: O(1)
    """
    # Python specific: handle negative numbers
    mask = 0xFFFFFFFF
    
    while b != 0:
        # XOR gives sum without carry
        # AND gives carry bits
        a, b = (a ^ b) & mask, ((a & b) << 1) & mask
    
    # Handle negative result
    return a if a <= 0x7FFFFFFF else ~(a ^ mask)

# Example: 5 + 3
# a=0101, b=0011
# sum=0110, carry=0010
# a=0110, b=0100
# sum=0010, carry=1000
# a=0010, b=1000
# sum=1010, carry=0000
# a=1000, b=0000 → 8 ✗ Should be 8 ✓
```

### Missing Number
```python
def missingNumber(nums: list[int]) -> int:
    """
    LeetCode #268
    Find missing number in [0, n]
    
    XOR approach: all numbers XOR with their indices
    Time: O(n), Space: O(1)
    """
    result = len(nums)
    
    for i, num in enumerate(nums):
        result ^= i ^ num
    
    return result

# Example: [3,0,1]
# result = 3 ^ (0^3) ^ (1^0) ^ (2^1)
#        = 3 ^ 3 ^ 0 ^ 0 ^ 2 ^ 1 ^ 1
#        = 2 ✓
```

---

## 🔧 Pattern 6: Reverse/Swap Bits

### Reverse Bits
```python
def reverseBits(n: int) -> int:
    """
    LeetCode #190
    Reverse bits of 32-bit integer
    
    Time: O(1), Space: O(1)
    """
    result = 0
    
    for i in range(32):
        # Get i-th bit from right
        bit = (n >> i) & 1
        # Place it at (31-i)-th position from right
        result |= (bit << (31 - i))
    
    return result
```

---

## 🎓 Key Problems by Pattern

**XOR:**
- #136 Single Number 🚨
- #137 Single Number II
- #260 Single Number III
- #268 Missing Number

**Counting:**
- #191 Number of 1 Bits
- #338 Counting Bits
- #461 Hamming Distance

**Power:**
- #231 Power of Two
- #342 Power of Four
- #326 Power of Three

**Bitmasking:**
- #78 Subsets (alternative)
- #421 Maximum XOR

**Math:**
- #371 Sum of Two Integers
- #201 Bitwise AND of Numbers Range

---

## 🚨 Common Mistakes

1. **Forgetting XOR properties:**
   ```python
   # Remember: x ^ x = 0, x ^ 0 = x
   ```

2. **Not handling negative numbers:**
   ```python
   # Python: use mask for 32-bit operations
   mask = 0xFFFFFFFF
   ```

3. **Wrong bit check:**
   ```python
   # WRONG
   if n >> i:
   
   # CORRECT
   if (n >> i) & 1:
   ```

---

## 💡 Pro Tips

**Common bit tricks:**
```python
# Check even/odd
is_odd = n & 1

# Multiply/divide by 2
n << 1  # n * 2
n >> 1  # n // 2

# Swap without temp
a ^= b; b ^= a; a ^= b

# Remove rightmost 1
n & (n - 1)

# Isolate rightmost 1
n & -n

# Check power of 2
n > 0 and not (n & (n - 1))
```

**XOR applications:**
- Finding duplicates/missing numbers
- Swapping values
- Detecting differences

**When to use:**
- Space optimization (bitmask vs array)
- Constant time operations
- Mathematics-heavy problems

---

**Bit manipulation is powerful but can be tricky - practice the patterns!**

