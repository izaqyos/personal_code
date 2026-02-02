# Memory Bandwidth Basics - Beginner

Understanding memory performance fundamentals.

## Learning Objectives
- Calculate memory transfer times
- Understand bandwidth vs latency
- Estimate data copy performance

## Background

### Key Values
| Metric | Typical Value |
|--------|---------------|
| DDR4 Bandwidth | 25-50 GB/s |
| DDR5 Bandwidth | 40-80 GB/s |
| L3 Cache | 200+ GB/s |
| Memory Latency | ~100 ns |

### Important Formula
```
Time = Data Size / Bandwidth
```

---

## Exercise 1: Simple Copy Time

**Question:** Copy 1 GB of data in memory.
- System bandwidth: 50 GB/s
- Operation: Read source + Write destination

Calculate total time.

**Your Answer:**
```
Data transferred = ?
Time = ?
```

<details>
<summary>Solution</summary>

```
Data transferred = 1 GB read + 1 GB write = 2 GB
Bandwidth = 50 GB/s
Time = 2 GB / 50 GB/s = 40 ms

Note: memcpy of 1 GB typically takes 30-50 ms on modern systems.
```
</details>

---

## Exercise 2: Array Operations

**Question:** Process a 10 million element float array:
```python
for i in range(10_000_000):
    output[i] = input[i] * 2
```

- Float size: 4 bytes
- Memory bandwidth: 50 GB/s

Is this memory-bound or compute-bound?

**Your Answer:**
```
Data size = ?
Memory time = ?
Compute time (at 3 GHz) = ?
Bottleneck = ?
```

<details>
<summary>Solution</summary>

```
Data Size:
  Input array: 10M × 4 bytes = 40 MB
  Output array: 10M × 4 bytes = 40 MB
  Total transfer: 80 MB

Memory Time:
  80 MB / 50 GB/s = 80 / 50,000 = 1.6 ms

Compute Time (at 3 GHz):
  10M multiplications
  With SIMD (8-wide): 1.25M vector ops
  At 1 op/cycle: 1.25M / 3 × 10^9 = 0.4 ms

Bottleneck: MEMORY (1.6 ms >> 0.4 ms)
```
</details>

---

## Exercise 3: Cache Comparison

**Question:** Same array operation, but data fits in:
1. L3 cache (200 GB/s internal bandwidth)
2. Main memory (50 GB/s)

Calculate the time difference for processing 1 MB of data.

**Your Answer:**
```
L3 cache time = ?
Memory time = ?
Speedup = ?
```

<details>
<summary>Solution</summary>

```
Data transfer: 2 MB (read + write)

L3 Cache:
  Time = 2 MB / 200 GB/s = 2 / 200,000 = 10 μs

Main Memory:
  Time = 2 MB / 50 GB/s = 2 / 50,000 = 40 μs

Speedup: 4x faster from cache

This is why keeping working set in cache matters!
```
</details>

---

## Exercise 4: Bandwidth vs Latency

**Question:** Random access pattern vs sequential:

Sequential:
```python
for i in range(1_000_000):
    sum += array[i]
```

Random:
```python
for i in random_indices:  # 1M random indices
    sum += array[i]
```

Array size: 1 GB (larger than cache)
Memory latency: 100 ns
Memory bandwidth: 50 GB/s

**Your Answer:**
```
Sequential time = ?
Random time = ?
Random slowdown = ?
```

<details>
<summary>Solution</summary>

```
Sequential Access:
  Data: 1M × 8 bytes = 8 MB
  Bandwidth-limited: 8 MB / 50 GB/s = 0.16 ms
  
Random Access:
  Each access: cache miss → 100 ns latency
  1M accesses × 100 ns = 100 ms
  
Random Slowdown: 100 ms / 0.16 ms = 625x slower!

Key insight: Sequential access utilizes bandwidth,
random access is limited by latency.
```
</details>

---

## Exercise 5: Practical Estimation

**Question:** Load a 500 MB dataset into memory for processing.
- Disk: NVMe SSD (5 GB/s)
- Memory: DDR5 (50 GB/s)

Calculate:
1. Time to load from disk to memory
2. Time to copy within memory (for backup)
3. Time to process (assume compute: 100 ms)

**Your Answer:**
```
Disk load time = ?
Memory copy time = ?
Processing time = ?
Total time = ?
```

<details>
<summary>Solution</summary>

```
Disk Load:
  500 MB / 5 GB/s = 100 ms

Memory Copy:
  500 MB × 2 (read + write) = 1 GB
  1 GB / 50 GB/s = 20 ms

Processing:
  100 ms (given)

Total: 100 + 20 + 100 = 220 ms

Note: Disk I/O (100 ms) is significant!
Consider memory-mapping for repeated access.
```
</details>

---

## Exercise 6: Data Structure Size

**Question:** A program uses these data structures:
- 1 million User objects (each 256 bytes)
- 10 million Transaction records (each 64 bytes)
- Index structure: 5 million entries (each 16 bytes)

Calculate:
1. Total memory footprint
2. Time to load all data if currently on SSD
3. Does this fit in typical L3 cache (32 MB)?

**Your Answer:**
```
Users = ?
Transactions = ?
Index = ?
Total = ?
Load time = ?
Fits in L3? = ?
```

<details>
<summary>Solution</summary>

```
Users: 1M × 256 bytes = 256 MB
Transactions: 10M × 64 bytes = 640 MB
Index: 5M × 16 bytes = 80 MB
Total: 256 + 640 + 80 = 976 MB ≈ 1 GB

Load from SSD (5 GB/s):
  1 GB / 5 GB/s = 200 ms

Fits in L3 (32 MB)?
  NO! 1 GB >> 32 MB
  
Working set analysis:
  - Can we process in chunks?
  - Index alone (80 MB) might fit with hot data
  - Consider caching strategy
```
</details>

---

## Key Takeaways

1. **Memory bandwidth is 50-80 GB/s** for typical systems
2. **Sequential is 100-1000x faster** than random access
3. **Cache bandwidth is 4-10x higher** than memory
4. **Latency matters for random access** (~100 ns per miss)
5. **Estimate data size first** to understand bottleneck

## Quick Reference
```
1 KB = 0.02 μs at 50 GB/s
1 MB = 20 μs at 50 GB/s
1 GB = 20 ms at 50 GB/s
```

## Next Steps
- Try [Intermediate: Streaming vs Random](../intermediate/streaming_random.md)
- Learn about [Cache Effects](../../05_cache_effects/beginner/cache_basics.md)
