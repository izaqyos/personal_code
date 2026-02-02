# Memory Allocation

Understanding memory allocation and its performance impact.

## Allocation Basics

### Stack vs Heap

| Aspect | Stack | Heap |
|--------|-------|------|
| Speed | Very fast (~1 ns) | Slower (~50-200 ns) |
| Size | Limited (1-8 MB) | Limited by RAM |
| Lifetime | Automatic (scope) | Manual/GC |
| Fragmentation | None | Possible |

```c
// Stack allocation (fast)
int array[1000];  // Fixed size, automatic cleanup

// Heap allocation (slower)
int* array = malloc(1000 * sizeof(int));  // Dynamic
free(array);  // Manual cleanup required
```

## Allocation Overhead

### Per-Allocation Cost
```
malloc() small object: 50-200 ns
malloc() large object: 200+ ns (may need system call)
new Object() in Java: 20-100 ns
Python object creation: 100-500 ns
```

### Hidden Allocations
```python
# Each creates new object
s = "hello" + "world"   # New string
l = [1, 2, 3]           # New list
d = {"a": 1}            # New dict

# List growth reallocates
for i in range(1000):
    lst.append(i)  # ~10 reallocations
```

## Memory Pools

Pre-allocate to avoid allocation in hot paths.

### Object Pool Pattern
```python
class ObjectPool:
    def __init__(self, factory, size=100):
        self.pool = [factory() for _ in range(size)]
        self.available = list(range(size))
    
    def acquire(self):
        if self.available:
            idx = self.available.pop()
            return self.pool[idx]
        return None  # Pool exhausted
    
    def release(self, idx):
        self.available.append(idx)
```

### Arena Allocation
```c
// Allocate large chunk once
char* arena = malloc(1_000_000);
size_t offset = 0;

// Fast allocation from arena
void* arena_alloc(size_t size) {
    void* ptr = arena + offset;
    offset += size;
    return ptr;
}

// Free everything at once
void arena_reset() {
    offset = 0;
}
```

## String Allocation

### String Interning
```python
# Small strings often interned
a = "hello"
b = "hello"
print(a is b)  # True (same object)

# Large/dynamic strings not interned
a = "hello" + str(123)
b = "hello" + str(123)
print(a is b)  # False (different objects)
```

### String Building
```python
# Bad: O(n²) due to reallocations
s = ""
for i in range(10000):
    s += str(i)  # New string each time

# Good: O(n)
parts = []
for i in range(10000):
    parts.append(str(i))
s = "".join(parts)  # Single allocation

# Even better for simple cases
s = "".join(str(i) for i in range(10000))
```

## Array/List Allocation

### Pre-sizing
```python
# Bad: Multiple reallocations
lst = []
for i in range(100000):
    lst.append(i)

# Good: Single allocation
lst = [None] * 100000
for i in range(100000):
    lst[i] = i

# Best: Use range directly
lst = list(range(100000))
```

### NumPy Pre-allocation
```python
import numpy as np

# Bad: Creates many intermediate arrays
result = np.zeros(1000000)
for i in range(1000000):
    result[i] = compute(i)

# Good: Vectorized single operation
result = compute(np.arange(1000000))

# Pre-allocate for multiple operations
buffer = np.empty((1000, 1000))
np.multiply(a, b, out=buffer)  # No allocation
```

## Garbage Collection

### GC Overhead
```
Young generation GC: 1-10 ms
Full GC: 100 ms - 1 s+
```

### Reducing GC Pressure
```java
// Bad: Many allocations
for (int i = 0; i < 1000000; i++) {
    String s = "item" + i;  // New String each time
    process(s);
}

// Good: StringBuilder reuse
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 1000000; i++) {
    sb.setLength(0);
    sb.append("item").append(i);
    process(sb.toString());
}
```

### Python Memory
```python
# Reference counting + GC
import gc

# Disable GC for performance-critical section
gc.disable()
# ... performance-critical code ...
gc.enable()
gc.collect()
```

## Memory Layout

### Contiguous vs Fragmented
```python
# Contiguous (cache-friendly)
import array
arr = array.array('i', range(10000))

# Fragmented (cache-unfriendly)
lst = [i for i in range(10000)]  # Each int is separate object
```

### Struct of Arrays vs Array of Structs
```python
# Array of Structs (AoS) - common but slower
class Point:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

points = [Point(i, i, i) for i in range(10000)]

# Struct of Arrays (SoA) - cache-friendly
class Points:
    def __init__(self, n):
        self.x = [0.0] * n
        self.y = [0.0] * n
        self.z = [0.0] * n

# NumPy SoA
import numpy as np
x = np.zeros(10000)
y = np.zeros(10000)
z = np.zeros(10000)
```

## Memory Alignment

### Alignment Impact
```
Aligned access: 1 cycle
Unaligned access: 2+ cycles (may cross cache line)
```

### Structure Padding
```c
// Unpadded (inefficient)
struct Bad {
    char a;    // 1 byte
    int b;     // 4 bytes (needs 4-byte alignment)
    char c;    // 1 byte
};
// Size: 12 bytes (with padding)

// Better ordering
struct Good {
    int b;     // 4 bytes
    char a;    // 1 byte
    char c;    // 1 byte
};
// Size: 8 bytes
```

## Estimation Examples

### Example 1: String Concatenation
```python
# Concatenating 10K strings of 100 chars each

# Bad way (O(n²)):
#   Copy 100 + 200 + 300 + ... + 1M = ~500M chars copied
#   Time: ~500 ms

# Good way (join):
#   Single allocation + copy: 1M chars
#   Time: ~1 ms

# Speedup: 500x
```

### Example 2: Object Creation
```python
# Create 1M objects

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Time: ~500 ms (Python overhead)

# With __slots__:
class Point:
    __slots__ = ['x', 'y']
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Time: ~400 ms (slightly faster, less memory)

# With NumPy:
points = np.zeros((1000000, 2))
# Time: ~10 ms
```

## Quick Reference

### Allocation Speed
```
Stack: ~1 ns
Small heap: ~50 ns
Large heap: ~200 ns
Python object: ~100-500 ns
Java object: ~20-100 ns
```

### Memory Overhead
```
Python int: 28 bytes (vs 8 bytes raw)
Python list: 56 bytes + 8 bytes/element
Python dict: 64 bytes + ~40 bytes/entry
Java Object: 16 bytes header
```

### Optimization Strategies
```
1. Pre-allocate when size known
2. Use object pools for hot paths
3. Prefer stack over heap
4. Batch allocations
5. Reuse buffers
6. Use language-native data structures
```

## Related Topics
- [Language Performance](language_performance.md)
- [Big-O Analysis](big_o_analysis.md)
