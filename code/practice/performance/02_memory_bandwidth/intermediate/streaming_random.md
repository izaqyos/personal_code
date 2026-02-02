# Streaming vs Random Access - Intermediate

Deep dive into access pattern performance.

## Learning Objectives
- Quantify streaming vs random access performance
- Understand prefetching effects
- Calculate effective bandwidth for different patterns

## Background

### Access Patterns
```
Sequential: a[0], a[1], a[2], a[3], ...
  - CPU prefetcher predicts and preloads
  - Achieves near-peak bandwidth

Strided: a[0], a[64], a[128], a[192], ...
  - Prefetcher can often detect pattern
  - Efficiency depends on stride size

Random: a[5421], a[99812], a[3], a[45621], ...
  - No prefetching possible
  - Limited by memory latency
```

### Key Values
| Access Type | Effective Bandwidth |
|-------------|---------------------|
| Sequential | 40-60 GB/s |
| Stride-64 | 20-40 GB/s |
| Stride-4096 | 5-15 GB/s |
| Random (large array) | 0.5-2 GB/s |

---

## Exercise 1: Prefetching Effect

**Question:** Array traversal with different strides:
```cpp
// Array: 1 billion bytes (1 GB)
for (int i = 0; i < size; i += stride) {
    sum += array[i];
}
```

Calculate effective bandwidth and time for:
1. Stride = 1 (every byte)
2. Stride = 64 (every cache line)
3. Stride = 4096 (every page)

Elements accessed for each case, array size 1 GB.

**Your Answer:**
```
Stride 1:
  Elements = ?
  Data touched = ?
  Expected time = ?

Stride 64:
  Elements = ?
  Data touched = ?
  Expected time = ?

Stride 4096:
  Elements = ?
  Data touched = ?
  Expected time = ?
```

<details>
<summary>Solution</summary>

```
Stride 1 (Sequential):
  Elements: 1 billion
  Data: 1 GB (all bytes read)
  Bandwidth: ~50 GB/s (full prefetching)
  Time: 1 GB / 50 GB/s = 20 ms

Stride 64 (Cache line):
  Elements: 1B / 64 = 15.6 million
  Data: 1 GB (touching every cache line)
  Bandwidth: ~40 GB/s (prefetcher works)
  Time: 1 GB / 40 GB/s = 25 ms
  
Stride 4096 (Page):
  Elements: 1B / 4096 = 244K
  Data: 1 GB (touching every page)
  Bandwidth: ~10 GB/s (prefetcher struggles)
  Time: 1 GB / 10 GB/s = 100 ms

Key: Same data touched, 5x different time!
```
</details>

---

## Exercise 2: Random Access Calculation

**Question:** Random lookups in a hash table:
- Table size: 4 GB
- Lookups: 10 million
- Each lookup: 64-byte read
- Memory latency: 100 ns

Calculate:
1. Best case (all cached)
2. Worst case (all cache misses)
3. Realistic (80% cache miss rate)

**Your Answer:**
```
Best case (all cached) = ?
Worst case (all misses) = ?
Realistic (80% misses) = ?
```

<details>
<summary>Solution</summary>

```
Best Case (All Cached, L1):
  Latency: ~1 ns per access
  Time: 10M × 1 ns = 10 ms

Worst Case (All Misses):
  Latency: 100 ns per access
  Time: 10M × 100 ns = 1000 ms = 1 second

Realistic (80% Miss Rate):
  Hits (20%): 2M × 1 ns = 2 ms
  Misses (80%): 8M × 100 ns = 800 ms
  Total: 802 ms

Note: Random access to large data = latency bound
Bandwidth (10M × 64B = 640 MB) would only take 13 ms
if sequential!
```
</details>

---

## Exercise 3: Memory Level Parallelism

**Question:** Modern CPUs can have multiple outstanding memory requests:
- Memory Level Parallelism (MLP): 10 concurrent requests
- Memory latency: 100 ns

How does this affect random access throughput?

Calculate random access performance with MLP vs without.

**Your Answer:**
```
Without MLP:
  Throughput = ?
  Time for 1M accesses = ?

With MLP (10 concurrent):
  Throughput = ?
  Time for 1M accesses = ?
```

<details>
<summary>Solution</summary>

```
Without MLP:
  1 request at a time
  Throughput: 1 / 100 ns = 10 million accesses/sec
  1M accesses: 100 ms

With MLP (10 concurrent):
  10 requests overlapped
  Effective latency: 100 ns / 10 = 10 ns per access
  Throughput: 100 million accesses/sec
  1M accesses: 10 ms

Speedup: 10x with memory parallelism!

This is why code that enables multiple outstanding
requests (loop unrolling, software pipelining) performs
better for random access.
```
</details>

---

## Exercise 4: Matrix Traversal

**Question:** Process a 10,000 × 10,000 matrix of floats (400 MB):
```cpp
// Row-major storage (C/Python default)
for (int i = 0; i < 10000; i++) {
    for (int j = 0; j < 10000; j++) {
        sum += matrix[i][j];
    }
}
```

Compare row-major vs column-major traversal:
- Row-major: matrix[i][j] with inner loop on j
- Column-major: matrix[i][j] with inner loop on i

Memory bandwidth: 50 GB/s
Cache line: 64 bytes (16 floats)

**Your Answer:**
```
Row-major traversal time = ?
Column-major traversal time = ?
Slowdown from wrong order = ?
```

<details>
<summary>Solution</summary>

```
Row-Major Traversal (Cache-Friendly):
  Access pattern: Sequential in memory
  Data: 400 MB
  Bandwidth achieved: ~50 GB/s
  Time: 400 MB / 50 GB/s = 8 ms

Column-Major Traversal (Cache-Hostile):
  Access pattern: Stride of 40,000 bytes (10K floats)
  Each access loads cache line, uses 1 float
  Cache utilization: 4 / 64 = 6.25%
  Effective bandwidth: 50 GB/s × 0.0625 = 3.1 GB/s
  Time: 400 MB / 3.1 GB/s = 129 ms

Slowdown: 129 / 8 = 16x slower!

Rule: Always traverse arrays in storage order.
```
</details>

---

## Exercise 5: Pointer Chasing

**Question:** Linked list traversal:
```cpp
Node* current = head;
while (current != nullptr) {
    sum += current->value;
    current = current->next;  // Pointer chase
}
```

List: 1 million nodes, randomly placed in 1 GB heap
Node size: 16 bytes

Compare to array of same data.

**Your Answer:**
```
Linked list time = ?
Array time = ?
Speedup from array = ?
```

<details>
<summary>Solution</summary>

```
Linked List (Pointer Chasing):
  Each node access: cache miss (random location)
  Latency: 100 ns per node
  Time: 1M × 100 ns = 100 ms
  
  Note: MLP doesn't help - each next pointer
  depends on previous node's data!

Array (Sequential):
  Data: 1M × 16 bytes = 16 MB
  Bandwidth: 50 GB/s
  Time: 16 MB / 50 GB/s = 0.32 ms

Speedup: 100 ms / 0.32 ms = 312x faster!

Key insight: Pointer chasing defeats:
- Prefetching
- Memory level parallelism
- Cache utilization
```
</details>

---

## Exercise 6: Working Set Analysis

**Question:** An algorithm processes data in two phases:
- Phase 1: Sequential scan of 10 GB dataset
- Phase 2: Random lookups (5 million) in 1 MB index

Calculate total time and identify bottleneck.

System: 50 GB/s bandwidth, 100 ns latency, 32 MB L3 cache

**Your Answer:**
```
Phase 1 time = ?
Phase 2 time = ?
Total time = ?
Optimization suggestion = ?
```

<details>
<summary>Solution</summary>

```
Phase 1 (Sequential Scan):
  Data: 10 GB
  Bandwidth: 50 GB/s
  Time: 10 GB / 50 GB/s = 200 ms

Phase 2 (Random Lookups):
  Index size: 1 MB (fits in L3 cache!)
  First access: Some misses
  After warm-up: All in cache

  Cache hit latency: ~12 ns (L3)
  Time: 5M × 12 ns = 60 ms

Total: 200 + 60 = 260 ms

Bottleneck: Phase 1 (sequential I/O)

Optimization: 
  - If index used repeatedly, keep it hot in cache
  - For Phase 1, consider compression (trade CPU for I/O)
  - Parallelize Phase 1 reads with Phase 2 processing
```
</details>

---

## Key Takeaways

1. **Sequential is 10-100x faster** than random for large data
2. **Prefetching only works** for predictable access patterns
3. **MLP helps random access** but not pointer chasing
4. **Stride matters**: Even predictable strides lose efficiency
5. **Keep hot data in cache**: Working set size is critical

## Access Pattern Spectrum
```
Best → Worst:
Sequential > Small stride > Large stride > Random > Pointer chase
  50 GB/s     30 GB/s        10 GB/s       2 GB/s    0.5 GB/s
```

## Next Steps
- Try [Advanced: NUMA and Memory Placement](../advanced/numa_effects.md)
- Learn about [Cache Blocking](../../05_cache_effects/advanced/cache_blocking.md)
