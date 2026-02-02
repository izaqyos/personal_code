# SIMD Optimization - Advanced

Understanding Single Instruction Multiple Data parallelism.

## Learning Objectives
- Calculate SIMD speedup potential
- Understand vector width limitations
- Analyze real-world SIMD benefits

## Background

### SIMD Vector Widths
| Instruction Set | Width | Floats | Doubles | Ints |
|-----------------|-------|--------|---------|------|
| SSE | 128-bit | 4 | 2 | 4 |
| AVX2 | 256-bit | 8 | 4 | 8 |
| AVX-512 | 512-bit | 16 | 8 | 16 |
| ARM NEON | 128-bit | 4 | 2 | 4 |

### SIMD Operation
```
Scalar:
a[0] = b[0] + c[0]  (1 op)
a[1] = b[1] + c[1]  (1 op)
a[2] = b[2] + c[2]  (1 op)
a[3] = b[3] + c[3]  (1 op)
Total: 4 operations, 4 cycles

SIMD (4-wide):
a[0:4] = b[0:4] + c[0:4]  (1 vector op)
Total: 1 operation, 1 cycle (ideally)
```

---

## Exercise 1: Theoretical SIMD Speedup

**Question:** Add two arrays of 1 million floats:
```cpp
for (int i = 0; i < 1000000; i++) {
    c[i] = a[i] + b[i];
}
```

Calculate speedup with:
1. SSE (128-bit, 4 floats)
2. AVX2 (256-bit, 8 floats)
3. AVX-512 (512-bit, 16 floats)

Assume: Perfect vectorization, no memory bottleneck, 3 GHz CPU, 1 cycle per operation.

**Your Answer:**
```
Scalar time = ?
SSE time = ?
AVX2 time = ?
AVX-512 time = ?
```

<details>
<summary>Solution</summary>

```
Scalar:
  Operations: 1,000,000
  Cycles: 1,000,000
  Time: 1M / 3 × 10^9 = 333 μs

SSE (4-wide):
  Vector ops: 1,000,000 / 4 = 250,000
  Cycles: 250,000
  Time: 250K / 3 × 10^9 = 83 μs
  Speedup: 4x

AVX2 (8-wide):
  Vector ops: 1,000,000 / 8 = 125,000
  Cycles: 125,000
  Time: 125K / 3 × 10^9 = 42 μs
  Speedup: 8x

AVX-512 (16-wide):
  Vector ops: 1,000,000 / 16 = 62,500
  Cycles: 62,500
  Time: 62.5K / 3 × 10^9 = 21 μs
  Speedup: 16x

Reality check: Memory bandwidth often limits actual speedup to 2-4x
```
</details>

---

## Exercise 2: Memory Bandwidth Limit

**Question:** Same array addition, but consider memory:
- Array size: 1M floats = 4 MB per array
- Total data: 3 arrays × 4 MB = 12 MB
- Memory bandwidth: 50 GB/s
- CPU: 3 GHz with AVX2

What limits performance: Compute or memory?

**Your Answer:**
```
Compute time (AVX2) = ?
Memory time = ?
Actual limiting factor = ?
```

<details>
<summary>Solution</summary>

```
Compute Time (AVX2):
  As calculated: 42 μs

Memory Time:
  Data: 12 MB (read 2 arrays, write 1)
  Bandwidth: 50 GB/s = 50,000 MB/s
  Time: 12 / 50,000 = 0.00024 s = 240 μs

Limiting factor: MEMORY!
Memory time (240 μs) >> Compute time (42 μs)

Even with AVX-512 (21 μs compute), memory is still the bottleneck.
Effective speedup from SIMD: limited by memory, not compute width.
```
</details>

---

## Exercise 3: Non-Unit Stride

**Question:** Strided access pattern:
```cpp
// Process every 4th element
for (int i = 0; i < 1000000; i += 4) {
    result[i/4] = data[i] * 2;
}
```

Compare SIMD efficiency for:
- Contiguous access (unit stride)
- Stride-4 access

Hint: SIMD gather operations are slower than contiguous loads.
- Contiguous vector load: 1 cycle
- Gather (strided): 4-8 cycles

**Your Answer:**
```
Contiguous SIMD efficiency = ?
Strided SIMD efficiency = ?
Recommendation = ?
```

<details>
<summary>Solution</summary>

```
Contiguous Access (Unit Stride):
  Load 8 floats: 1 cycle (AVX2)
  Multiply: 1 cycle
  Store: 1 cycle
  Total: 3 cycles for 8 elements = 0.375 cycles/element

Strided Access (Stride-4):
  Load 8 floats (gather): 6 cycles (expensive!)
  Multiply: 1 cycle
  Store: 1 cycle
  Total: 8 cycles for 8 elements = 1 cycle/element

Efficiency Loss: 1 / 0.375 = 2.67x slower with stride

Recommendation:
  1. Reorganize data for contiguous access if possible
  2. Or use scalar code if gather overhead > scalar cost
  3. Consider data transposition as preprocessing step
```
</details>

---

## Exercise 4: Conditional Operations

**Question:** SIMD with conditions:
```cpp
for (int i = 0; i < 1000000; i++) {
    if (a[i] > threshold) {
        b[i] = a[i] * 2;
    } else {
        b[i] = a[i];
    }
}
```

50% of elements > threshold (random distribution).

Compare:
1. Scalar with branch
2. SIMD with masking (compute both, blend)

Assume: Branch misprediction = 15 cycles, blend = 1 cycle extra.

**Your Answer:**
```
Scalar time (with mispredictions) = ?
SIMD time (with blending) = ?
Which is faster = ?
```

<details>
<summary>Solution</summary>

```
Scalar with Branch:
  Per element: 3 cycles base + 50% × 15 misprediction
  Average: 3 + 7.5 = 10.5 cycles per element
  Total: 1M × 10.5 = 10.5M cycles

SIMD with Masking (AVX2, 8-wide):
  Load a: 1 cycle
  Compare: 1 cycle
  Multiply (all elements): 1 cycle
  Blend: 1 cycle
  Store: 1 cycle
  Total: 5 cycles for 8 elements = 0.625 cycles/element
  Total: 1M × 0.625 = 625K cycles

SIMD is 16.8x faster!

Key insight: Branchless SIMD with masking eliminates
all branch mispredictions, even though it does "extra" work.
```
</details>

---

## Exercise 5: Horizontal Operations

**Question:** Sum all elements in an array:
```cpp
float sum = 0;
for (int i = 0; i < 1000000; i++) {
    sum += data[i];
}
```

Problem: Dependency chain (each add depends on previous sum).

Compare:
1. Scalar (fully sequential)
2. SIMD with 8 accumulators, final horizontal add

Scalar add latency: 3 cycles
SIMD vector add latency: 3 cycles
Horizontal add (reduce): 8 cycles at the end

**Your Answer:**
```
Scalar time = ?
SIMD (8 accumulators) time = ?
Speedup = ?
```

<details>
<summary>Solution</summary>

```
Scalar (Sequential):
  Each add waits for previous: 3-cycle latency
  Total: 1M × 3 = 3M cycles

SIMD (8 Parallel Accumulators):
  sum0 += data[0], sum1 += data[1], ..., sum7 += data[7]
  All 8 can execute in parallel (different dependency chains)

  Vector loads: 1M / 8 = 125K loads × 1 cycle = 125K cycles
  Vector adds: 125K × 3 = 375K cycles (parallel accumulators)
  
  But loads can overlap with adds (pipelining):
  Throughput-limited: 125K iterations × 1 cycle = 125K cycles
  Plus startup/drain: ~50 cycles
  Final horizontal add: 8 cycles
  
  Total: ~125K cycles

Speedup: 3M / 125K = 24x faster!

Key insight: Multiple accumulators break the dependency chain,
allowing instruction-level parallelism.
```
</details>

---

## Exercise 6: Real-World SIMD Analysis

**Question:** NumPy matrix multiply (1000×1000):
- Uses AVX2 (8 floats per op)
- Algorithm: ~2 billion FLOPs (2n³)
- Memory: 3 matrices × 4 MB = 12 MB (fits in L3 cache)

Calculate theoretical vs realistic performance:
- CPU: 3 GHz, 8-wide SIMD, 2 FMA units
- Peak: 3 × 10^9 × 8 × 2 = 48 GFLOPS

**Your Answer:**
```
Theoretical time = ?
Realistic time (50% efficiency) = ?
What limits efficiency = ?
```

<details>
<summary>Solution</summary>

```
Theoretical (100% efficiency):
  FLOPs: 2 × 10^9
  Peak throughput: 48 GFLOPS
  Time: 2 × 10^9 / 48 × 10^9 = 42 ms

Realistic (50% efficiency):
  Effective throughput: 24 GFLOPS
  Time: 2 × 10^9 / 24 × 10^9 = 83 ms

Actual libraries (NumPy/BLAS): ~50-100 ms for 1000×1000

Efficiency limiters:
  1. Cache blocking overhead
  2. Non-perfect data alignment
  3. Loop setup/cleanup
  4. Memory latency between blocks
  5. Thread synchronization (if parallel)

50% efficiency is actually quite good for complex algorithms.
Highly optimized BLAS can reach 70-80% of peak.
```
</details>

---

## Key Takeaways

1. **SIMD gives 4-16x speedup in theory**, often 2-4x in practice
2. **Memory bandwidth often limits** actual SIMD benefit
3. **Data layout matters**: Contiguous access essential for SIMD
4. **Branchless with masking** beats branchy scalar code
5. **Multiple accumulators** break dependency chains
6. **50% of peak is good** for real-world code

## SIMD Checklist
```
□ Is data contiguous in memory?
□ Is data properly aligned (16/32/64 byte)?
□ Are there dependency chains to break?
□ Is memory bandwidth sufficient?
□ Can conditions be converted to masks?
□ Is auto-vectorization possible, or manual needed?
```

## Next Steps
- Try [Memory Bandwidth Exercises](../../02_memory_bandwidth/beginner/memory_basics.md)
- Learn about [Cache Optimization](../../05_cache_effects/advanced/cache_blocking.md)
