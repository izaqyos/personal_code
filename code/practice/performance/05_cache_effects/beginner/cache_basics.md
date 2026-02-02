# Cache Effects Basics - Beginner

Understanding how CPU caches affect performance.

## Learning Objectives
- Understand cache hierarchy and sizes
- Calculate cache miss penalties
- Identify cache-friendly access patterns

## Background

### Cache Hierarchy
| Level | Size | Latency | Bandwidth |
|-------|------|---------|-----------|
| L1 | 32-64 KB | 1 ns (4 cycles) | 1+ TB/s |
| L2 | 256 KB - 1 MB | 4 ns (12 cycles) | 500 GB/s |
| L3 | 8-64 MB | 12 ns (40 cycles) | 200 GB/s |
| RAM | 16-128 GB | 100 ns (300 cycles) | 50 GB/s |

### Cache Line
- Size: 64 bytes
- When you access 1 byte, 64 bytes are loaded
- Spatial locality: Adjacent data often comes for "free"

---

## Exercise 1: Working Set Size

**Question:** Which cache level fits this data?
1. Array of 1,000 integers (4 bytes each)
2. Array of 100,000 integers
3. Array of 10,000,000 integers

Typical cache sizes: L1 = 32 KB, L2 = 256 KB, L3 = 8 MB

**Your Answer:**
```
1,000 integers: Size = ?, Fits in = ?
100,000 integers: Size = ?, Fits in = ?
10,000,000 integers: Size = ?, Fits in = ?
```

<details>
<summary>Solution</summary>

```
1,000 integers:
  Size: 1,000 × 4 = 4 KB
  Fits in: L1 cache (32 KB)
  Performance: Best possible

100,000 integers:
  Size: 100,000 × 4 = 400 KB
  Fits in: L2 cache (256 KB) - NO, spills to L3
  Actually fits in: L3 cache (8 MB)
  Performance: Good, but L3 latency (12 ns vs 4 ns)

10,000,000 integers:
  Size: 10,000,000 × 4 = 40 MB
  Fits in: RAM only (larger than L3)
  Performance: Will experience RAM latency (100 ns)
```
</details>

---

## Exercise 2: Cache Miss Penalty

**Question:** Sum an array that doesn't fit in cache.
- Array size: 100 MB (25 million integers)
- Access pattern: Sequential

Calculate effective memory access time with:
- L3 hit rate: 0% (array too large)
- Memory latency: 100 ns
- Memory bandwidth: 50 GB/s

**Your Answer:**
```
If latency-bound (random): Time = ?
If bandwidth-bound (sequential): Time = ?
Which applies here = ?
```

<details>
<summary>Solution</summary>

```
Latency-Bound (Random Access):
  25M accesses × 100 ns = 2.5 seconds
  
Bandwidth-Bound (Sequential Access):
  100 MB / 50 GB/s = 2 ms
  
Which Applies?
  Sequential access → Bandwidth-bound
  Time: ~2 ms
  
  Why so different?
  - Sequential: Prefetcher loads ahead
  - Random: Each access waits for memory
  
  Difference: 1000x faster with sequential access!
```
</details>

---

## Exercise 3: Cache Line Utilization

**Question:** Compare array access patterns:
```python
# Pattern A: Sequential (every element)
for i in range(n):
    sum += array[i]

# Pattern B: Strided (every 16th element)
for i in range(0, n, 16):
    sum += array[i]
```

Array: 16 million integers (64 MB)
Cache line: 64 bytes (16 integers)

**Your Answer:**
```
Pattern A:
  Elements accessed = ?
  Cache lines loaded = ?
  Utilization = ?

Pattern B:
  Elements accessed = ?
  Cache lines loaded = ?
  Utilization = ?
```

<details>
<summary>Solution</summary>

```
Pattern A (Sequential):
  Elements: 16M
  Cache lines: 16M / 16 = 1M lines
  Data loaded: 1M × 64 = 64 MB
  Utilization: 100% (every byte used)
  
Pattern B (Stride 16):
  Elements: 1M
  Cache lines: 1M (each element from different line!)
  Data loaded: 1M × 64 = 64 MB
  Utilization: 4 bytes / 64 bytes = 6.25%

Same memory loaded, but:
  Pattern A: 16x more useful work!
  
Time comparison (at 50 GB/s):
  Both load 64 MB: 1.3 ms
  Pattern A: 16M operations
  Pattern B: 1M operations
  
  Pattern A is 16x more efficient.
```
</details>

---

## Exercise 4: Matrix Traversal

**Question:** 1000×1000 matrix of floats (4 MB total):
```python
# Row-major (cache-friendly for C/Python)
for i in range(1000):
    for j in range(1000):
        sum += matrix[i][j]

# Column-major (cache-unfriendly)
for j in range(1000):
    for i in range(1000):
        sum += matrix[i][j]
```

Assuming matrix fits in L3, estimate time difference.
- L3 latency: 12 ns
- Cache line: 64 bytes (16 floats)

**Your Answer:**
```
Row-major: Cache misses = ?, Time factor = ?
Column-major: Cache misses = ?, Time factor = ?
Slowdown = ?
```

<details>
<summary>Solution</summary>

```
Row-Major (Cache-Friendly):
  Access pattern: Sequential in memory
  Cache misses: 1M elements / 16 per line = 62,500 misses
  Each miss loads 16 useful elements
  
Column-Major (Cache-Unfriendly):
  Access pattern: Stride of 4000 bytes (1000 floats)
  Each access likely misses (stride > cache line)
  Cache misses: ~1,000,000 (every access!)
  Each miss loads 1 useful element

Slowdown: 1M / 62.5K = 16x slower

Time estimate:
  Row-major: 62.5K × 12 ns = 0.75 ms
  Column-major: 1M × 12 ns = 12 ms
  
  Actual difference might be 10-50x due to
  prefetching benefits for row-major.
```
</details>

---

## Exercise 5: Hot/Cold Data

**Question:** A data structure has:
- Hot path: 100 bytes (accessed every call)
- Cold path: 10,000 bytes (accessed 1% of time)

Compare two layouts:
```python
# Layout A: Mixed
class Object:
    hot_field1: int     # 8 bytes
    cold_data: bytes    # 10,000 bytes
    hot_field2: int     # 8 bytes
    # ... more mixed

# Layout B: Separated
class Object:
    hot_fields: HotData  # 100 bytes
    cold_ref: ColdData   # pointer to 10,000 bytes
```

**Your Answer:**
```
Layout A cache lines for hot path = ?
Layout B cache lines for hot path = ?
Memory loaded difference = ?
```

<details>
<summary>Solution</summary>

```
Layout A (Mixed):
  Hot data scattered across structure
  To access 100 bytes of hot data:
    May load 20-50 cache lines (depends on layout)
    Data loaded: 1,280 - 3,200 bytes
    Most is cold data (wasted)

Layout B (Separated):
  Hot data: 100 bytes contiguous
  Cache lines: 100 / 64 = 2 cache lines
  Data loaded: 128 bytes
  
Memory Efficiency:
  Layout A: Loads 10-25x more data for hot path
  Layout B: Minimal, just what's needed

Performance Impact:
  If L3 hit: 2x cache line loads vs 20x
  If RAM: 128 bytes vs 3200 bytes = 25x more latency

Lesson: Keep hot data together, separate cold data.
This is why struct/class field ordering matters!
```
</details>

---

## Exercise 6: Practical Example

**Question:** Game entity update loop:
```python
for entity in entities:  # 10,000 entities
    entity.x += entity.velocity_x
    entity.y += entity.velocity_y
```

Entity size: 256 bytes each
Only x, y, velocity_x, velocity_y used (32 bytes)
Total data: 10,000 × 256 = 2.5 MB

Compare Array of Structures (AoS) vs Structure of Arrays (SoA).

**Your Answer:**
```
AoS data loaded = ?
SoA data loaded = ?
Cache efficiency improvement = ?
```

<details>
<summary>Solution</summary>

```
Array of Structures (AoS):
  Each entity: 256 bytes
  Cache lines per entity: 4 (256/64)
  Total cache lines: 40,000
  Data loaded: 2.5 MB
  Useful data: 10,000 × 32 = 320 KB
  Efficiency: 320 KB / 2.5 MB = 12.5%

Structure of Arrays (SoA):
  Separate arrays: x[], y[], velocity_x[], velocity_y[]
  Each array: 10,000 × 8 bytes = 80 KB
  Total: 320 KB
  Cache lines: 320 KB / 64 = 5,000
  Efficiency: 100%

Improvement:
  Cache lines: 40,000 → 5,000 (8x fewer)
  Data loaded: 2.5 MB → 320 KB (8x less)
  
Performance Impact:
  If memory-bound: ~8x faster
  If compute-bound: Still faster due to prefetching
  
Typical game engines use SoA for hot data!
```
</details>

---

## Key Takeaways

1. **L1 is 100x faster than RAM** - keep hot data small
2. **Sequential access is 10-100x faster** than random
3. **Cache line is 64 bytes** - access patterns should consider this
4. **Stride access wastes cache** - reorganize data if needed
5. **Separate hot and cold data** - don't load what you don't need

## Quick Reference
```
Cache line: 64 bytes
L1: 32 KB, 1 ns
L2: 256 KB, 4 ns
L3: 8 MB, 12 ns
RAM: 100 ns

Sequential vs Random: 100-1000x difference
```

## Next Steps
- Try [Intermediate: Cache Blocking](../intermediate/cache_blocking.md)
- Learn about [Algorithm Comparison](../../06_algorithm_comparison/beginner/sorting_comparison.md)
