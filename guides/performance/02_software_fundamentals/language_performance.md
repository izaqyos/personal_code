# Language Performance Characteristics

Understanding performance differences between programming languages.

## Language Categories

### Compiled (Native)
```
C, C++, Rust, Go
- Direct machine code
- Manual or deterministic memory management
- Minimal runtime overhead
```

### JIT Compiled
```
Java, C#, JavaScript (V8), Julia
- Compiled at runtime
- Optimized based on actual usage
- Warm-up period for optimization
```

### Interpreted
```
Python, Ruby, PHP
- Executed line by line
- Dynamic types at runtime
- Significant overhead per operation
```

## Performance Comparison

### Relative Speed (vs C = 1.0)

| Task | C | C++ | Rust | Go | Java | JavaScript | Python |
|------|---|-----|------|-----|------|------------|--------|
| Numeric | 1.0 | 1.0 | 1.0 | 1.2 | 1.5 | 3.0 | 50-100 |
| String | 1.0 | 1.0 | 1.0 | 1.5 | 2.0 | 2.5 | 10-30 |
| I/O bound | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0-2.0 |

Note: These are rough estimates; actual performance varies by workload.

## Python Performance

### CPython Overhead
```python
# Simple loop - very slow
total = 0
for i in range(10_000_000):
    total += i
# ~500 ms (interpreter overhead each iteration)

# Use built-ins when possible
total = sum(range(10_000_000))
# ~150 ms (C implementation)
```

### NumPy Speedup
```python
import numpy as np

# Pure Python: 50-100x slower
def dot_python(a, b):
    return sum(x * y for x, y in zip(a, b))

# NumPy: Near C speed
def dot_numpy(a, b):
    return np.dot(a, b)

# 1M element dot product:
# Python: ~200 ms
# NumPy: ~2 ms
```

### Python Optimization Tips
```python
# 1. Use list comprehensions
result = [x * 2 for x in items]  # Faster than loop

# 2. Use local variables
def fast():
    local_len = len  # Local lookup faster
    return sum(local_len(s) for s in strings)

# 3. Use C extensions (NumPy, Pandas, etc.)
import pandas as pd
df.sum()  # C under the hood

# 4. Consider Cython, Numba, or PyPy
from numba import jit

@jit(nopython=True)
def fast_loop(arr):
    total = 0
    for x in arr:
        total += x
    return total
```

## JavaScript Performance

### V8 Optimizations
```javascript
// Monomorphic (fast): Same types every time
function add(a, b) {
    return a + b;
}
add(1, 2);  // int + int
add(3, 4);  // int + int - V8 optimizes this

// Polymorphic (slower): Different types
add(1, 2);       // int + int
add("a", "b");   // string + string - deoptimizes
```

### Hot Path Optimization
```javascript
// V8 optimizes frequently called code
function hotFunction(arr) {
    let sum = 0;
    for (let i = 0; i < arr.length; i++) {
        sum += arr[i];
    }
    return sum;
}

// After ~10K calls with same types: fully optimized
```

## Java Performance

### JIT Warmup
```java
// First 10K iterations: Interpreted (slow)
// After warmup: JIT compiled (fast)

public long measure() {
    long start = System.nanoTime();
    // ... work ...
    return System.nanoTime() - start;
}

// First call: 10 ms
// After warmup: 0.1 ms
```

### GC Considerations
```java
// Object allocation triggers GC
List<String> results = new ArrayList<>();
for (int i = 0; i < 1_000_000; i++) {
    results.add(new String("item" + i));  // 1M allocations
}
// GC pauses throughout

// Prefer primitives and pools for hot paths
int[] values = new int[1_000_000];  // Single allocation
```

## Rust Performance

### Zero-Cost Abstractions
```rust
// Iterator chains compile to optimal loops
let sum: i64 = values.iter()
    .filter(|x| **x > 0)
    .map(|x| x * 2)
    .sum();

// Compiles to same machine code as:
let mut sum = 0;
for x in values {
    if *x > 0 {
        sum += x * 2;
    }
}
```

### No GC Overhead
```rust
// Deterministic memory management
{
    let data = vec![1, 2, 3];
    // data freed here, no GC pause
}
```

## Go Performance

### Goroutines
```go
// Lightweight concurrency
for i := 0; i < 10000; i++ {
    go worker(tasks[i])  // 10K concurrent workers
}

// Goroutine overhead: ~2KB stack each
// Thread overhead: ~1MB stack each
```

### GC Considerations
```go
// Go's GC optimized for low latency
// Typical pause: <1 ms

// Avoid excessive allocations in hot paths
func processItems(items []Item) {
    // Pre-allocate if size known
    results := make([]Result, 0, len(items))
    for _, item := range items {
        results = append(results, process(item))
    }
}
```

## Memory Management Impact

### Manual (C/C++/Rust)
```
+ No GC pauses
+ Predictable performance
- Memory leaks possible (C/C++)
- More complex code
```

### Garbage Collected (Java/Go/JS/Python)
```
+ Automatic memory management
+ Simpler code
- GC pauses (varies by language)
- Memory overhead for GC metadata
```

### GC Pause Characteristics

| Language | Typical Pause | Max Pause |
|----------|---------------|-----------|
| Go | <1 ms | 1-2 ms |
| Java G1 | 10-50 ms | 100 ms |
| Java ZGC | <1 ms | 1-2 ms |
| Python | N/A (ref counting + GC) | Varies |
| JavaScript | <10 ms | 50 ms |

## Startup Time

| Language | Hello World | Web Server |
|----------|-------------|------------|
| C | 2 ms | 5 ms |
| Go | 10 ms | 20 ms |
| Rust | 5 ms | 10 ms |
| Java | 100 ms | 500 ms |
| Node.js | 50 ms | 200 ms |
| Python | 30 ms | 300 ms |

## When to Use What

| Use Case | Best Choice |
|----------|-------------|
| Systems programming | Rust, C++ |
| Web backend | Go, Java, Node.js |
| Data science | Python (with NumPy/Pandas) |
| Games | C++, Rust |
| Scripts/Automation | Python, Bash |
| Microservices | Go, Java, Node.js |
| Real-time systems | C, Rust |

## Quick Reference

### Performance Improvement Options

```
Python too slow?
  1. Use NumPy/Pandas for data
  2. Try Numba for numeric code
  3. Use Cython for hot spots
  4. Rewrite in Go/Rust

JavaScript too slow?
  1. Profile to find hot spots
  2. Avoid type polymorphism
  3. Use TypedArrays for numerics
  4. Consider WASM for compute

Java too slow?
  1. Profile GC behavior
  2. Reduce allocations
  3. Use primitives over objects
  4. Consider GraalVM
```

## Related Topics
- [Big-O Analysis](big_o_analysis.md)
- [Memory Allocation](memory_allocation.md)
