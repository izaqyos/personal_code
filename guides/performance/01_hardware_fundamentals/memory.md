# Memory Performance

Understanding RAM and memory bandwidth for performance estimation.

## Memory Hierarchy Latency

```
Register      ~0.3 ns   (1 cycle)
L1 Cache      ~1 ns     (4 cycles)
L2 Cache      ~4 ns     (12 cycles)
L3 Cache      ~12 ns    (40 cycles)
Main Memory   ~100 ns   (300+ cycles)
```

## Memory Bandwidth

### DDR Generations

| Type | Speed | Bandwidth | Latency |
|------|-------|-----------|---------|
| DDR4-3200 | 3200 MT/s | ~25 GB/s/channel | ~15 ns |
| DDR4-3600 | 3600 MT/s | ~28 GB/s/channel | ~14 ns |
| DDR5-4800 | 4800 MT/s | ~38 GB/s/channel | ~13 ns |
| DDR5-6000 | 6000 MT/s | ~48 GB/s/channel | ~12 ns |

### Total System Bandwidth
```
Typical desktop: 2 channels × 25 GB/s = 50 GB/s
Server: 8 channels × 25 GB/s = 200 GB/s
Apple M4 Pro: ~120 GB/s (unified memory)
```

## Memory Access Patterns

### Sequential Access
```python
# Best case: utilizes full bandwidth
for i in range(n):
    sum += array[i]
```
Achieves near-theoretical bandwidth.

### Random Access
```python
# Worst case: limited by latency
for i in random_indices:
    sum += array[i]
```
Limited by 100 ns latency × cache miss rate.

### Bandwidth vs Latency Bound

**Bandwidth-bound (streaming):**
```
Time = Data_Size / Bandwidth
10 GB at 50 GB/s = 200 ms
```

**Latency-bound (random access):**
```
Time = Accesses × Latency
10M random accesses × 100 ns = 1 second
```

## Memory Calculations

### Time to Copy Data

```
Copy 1 GB:
  Sequential at 50 GB/s: 20 ms
  (Read + Write = 2 GB transferred)
  Actual: 1 GB / (50/2) = 40 ms
```

### Memory Bandwidth Utilization

```python
# Simple copy
for i in range(n):
    dest[i] = src[i]

# Bytes moved: 2 × n × element_size (read + write)
# Time = Total_Bytes / Bandwidth
```

## NUMA (Non-Uniform Memory Access)

### Multi-Socket Servers
```
┌─────────┐         ┌─────────┐
│  CPU 0  │◄───────►│  CPU 1  │
└────┬────┘         └────┬────┘
     │                   │
┌────▼────┐         ┌────▼────┐
│ Memory 0│         │ Memory 1│
└─────────┘         └─────────┘
```

**Access latencies:**
- Local memory: 100 ns
- Remote memory: 150-200 ns

### NUMA-Aware Programming
```python
# Allocate memory on local NUMA node
# Process data on same CPU that allocated it
```

## Virtual Memory

### Page Sizes
- Standard: 4 KB
- Large pages: 2 MB
- Huge pages: 1 GB

### TLB (Translation Lookaside Buffer)
Caches virtual→physical address translations.

```
TLB Miss penalty: 10-100 cycles
```

**Large pages reduce TLB misses:**
- 4 KB pages: 1 GB needs 256K entries
- 2 MB pages: 1 GB needs 512 entries

## Memory Allocation

### Allocation Overhead
```
malloc() small:  ~50-200 ns
malloc() large:  ~1-10 μs (may trigger system call)
```

### Memory Pools
Pre-allocate to avoid allocation in hot path:
```python
pool = [Object() for _ in range(1000)]  # Pre-allocate

def get_object():
    return pool.pop()  # Fast, no allocation
```

## Estimation Examples

### Example 1: Array Sum
```
Sum 1M doubles (8 MB):
  Data: 8 MB
  Bandwidth: 50 GB/s
  Time: 8 MB / 50 GB/s = 0.16 ms

  Plus: 1M additions at 3 GHz
  Time: 1M / 3B = 0.33 ms
  
  Total: ~0.5 ms (bandwidth limited)
```

### Example 2: Random Lookups
```
1M random lookups in 1GB array:
  Cache miss rate: ~99% (array >> cache)
  Latency: 100 ns per miss
  Time: 1M × 0.99 × 100 ns = 99 ms
```

### Example 3: Matrix Multiply
```
1000×1000 matrices (8 MB each):
  Naive: O(n³) = 1B operations
  Memory: 3 matrices = 24 MB (fits in L3)
  
  Compute: 1B ops / 3B Hz = 333 ms
  With SIMD: ~40 ms
  With blocking: ~30 ms
```

## Quick Reference

### Data Size Guidelines
```
L1 cache: Work with < 32 KB for best performance
L2 cache: Work with < 256 KB for good performance
L3 cache: Work with < 8 MB for reasonable performance
RAM: Anything larger pays full memory latency
```

### Bandwidth Rules of Thumb
```
1 GB copy: ~40 ms
10 GB copy: ~400 ms
100 GB copy: ~4 seconds
```

## Related Topics
- [Cache Hierarchy](cache_hierarchy.md)
- [CPU Architecture](cpu_architecture.md)
