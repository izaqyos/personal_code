# Cache Hierarchy

Understanding CPU caches for performance optimization.

## Cache Levels

```
CPU Core
   │
   ▼
┌──────────┐
│ L1 Cache │  32-64 KB, 1 ns, per-core
└────┬─────┘
     ▼
┌──────────┐
│ L2 Cache │  256 KB - 1 MB, 4 ns, per-core
└────┬─────┘
     ▼
┌──────────┐
│ L3 Cache │  8-64 MB, 12 ns, shared
└────┬─────┘
     ▼
┌──────────┐
│   RAM    │  16-128 GB, 100 ns
└──────────┘
```

## Cache Characteristics

| Level | Size | Latency | Bandwidth | Scope |
|-------|------|---------|-----------|-------|
| L1D | 32-64 KB | 1 ns (4 cycles) | 1+ TB/s | Per core |
| L1I | 32-64 KB | 1 ns | 1+ TB/s | Per core |
| L2 | 256 KB-1 MB | 4 ns (12 cycles) | 500 GB/s | Per core |
| L3 | 8-64 MB | 12 ns (40 cycles) | 200 GB/s | Shared |
| RAM | 16-128 GB | 100 ns (300+ cycles) | 50-100 GB/s | System |

## Cache Lines

- Typical size: 64 bytes
- Data is fetched in cache line units
- Adjacent data often benefits (spatial locality)

```
Cache Line (64 bytes):
[int][int][int][int][int][int][int][int]  = 32 bytes for 8 ints
[float][float][float][float]...           = 32 bytes for 8 floats
```

## Locality Principles

### Temporal Locality
Recently accessed data likely accessed again.
```python
# Good: reuse data while it's cached
for i in range(1000):
    total += array[i % 10]  # Same 10 elements, stay in cache
```

### Spatial Locality
Adjacent data likely accessed together.
```python
# Good: sequential access
for i in range(n):
    sum += array[i]  # Cache line brings adjacent elements

# Bad: strided access
for i in range(0, n, 64):
    sum += array[i]  # Wastes most of each cache line
```

## Cache Effects in Code

### Row-Major vs Column-Major

```python
# Row-major (good for C/Python)
for i in range(rows):
    for j in range(cols):
        process(matrix[i][j])  # Sequential in memory

# Column-major (bad for C/Python)
for j in range(cols):
    for i in range(rows):
        process(matrix[i][j])  # Jumps around in memory
```

**Impact:** 10-100x slower for large matrices

### Structure of Arrays vs Array of Structures

```python
# Array of Structures (AoS)
class Point:
    x: float
    y: float
    z: float
    color: int
    
points = [Point() for _ in range(1000)]

# If you only need x:
for p in points:
    use(p.x)  # Loads x, y, z, color; wastes 75%

# Structure of Arrays (SoA)
class Points:
    x: list[float]
    y: list[float]
    z: list[float]
    color: list[int]

# Now:
for x in points.x:
    use(x)  # Perfect cache utilization
```

## Cache Miss Types

1. **Compulsory (Cold):** First access to data
2. **Capacity:** Cache too small for working set
3. **Conflict:** Multiple items map to same cache location
4. **Coherence:** Multi-core invalidation (shared data)

## Cache Performance Metrics

### Hit Rate
```
Hit Rate = Cache Hits / Total Accesses
Miss Rate = 1 - Hit Rate
```

### Average Access Time
```
AMAT = Hit_Time + (Miss_Rate × Miss_Penalty)

Example:
L1: 1 ns, 95% hit rate
L2 miss penalty: 100 ns

AMAT = 1 + (0.05 × 100) = 6 ns
```

## Optimization Tips

### Fit Working Set in Cache
```python
# L1: 32 KB = 8000 floats or 4000 doubles
# L2: 256 KB = 64000 floats
# L3: 8 MB = 2M floats
```

### Prefetching
```c
// Manual prefetch (C)
__builtin_prefetch(&array[i + 64], 0, 3);

// Often automatic for sequential access
```

### Cache-Oblivious Algorithms
Algorithms that perform well regardless of cache size:
- Recursive divide-and-conquer
- Block matrix operations

## Quick Reference

### Data Sizes in Cache Lines (64 bytes)
- 16 ints (32-bit)
- 8 longs/doubles (64-bit)
- 4 SIMD vectors (128-bit)

### Typical Cache Sizes by Platform

| Platform | L1 | L2 | L3 |
|----------|----|----|-----|
| Intel Desktop | 48 KB | 1.25 MB | 24 MB |
| AMD Desktop | 32 KB | 512 KB | 32 MB |
| Apple M4 | 128 KB | 16 MB | - |
| Server | 32 KB | 1 MB | 64 MB |

## Related Topics
- [CPU Architecture](cpu_architecture.md)
- [Memory](memory.md)
