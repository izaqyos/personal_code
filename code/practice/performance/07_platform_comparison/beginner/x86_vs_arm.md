# x86 vs ARM Comparison - Beginner

Comparing Intel/AMD (x86) and Apple/ARM architectures.

## Learning Objectives
- Understand architectural differences
- Compare performance characteristics
- Estimate cross-platform performance

## Background

### Architecture Overview
| Aspect | x86 (Intel/AMD) | ARM (Apple M-series) |
|--------|-----------------|----------------------|
| Type | CISC | RISC |
| Clock Speed | 3-5.5 GHz | 2.5-4.5 GHz |
| Cores (typical) | 8-24 | 8-14 (P+E) |
| Power (laptop) | 45-65W | 20-40W |
| Memory | DDR4/DDR5 | Unified (on-chip) |

### Performance Cores Comparison (2024)
| CPU | Cores | Single-Thread | Multi-Thread | TDP |
|-----|-------|---------------|--------------|-----|
| Intel i9-14900K | 24 (8P+16E) | 2200 | 40000 | 125W |
| AMD Ryzen 9 7950X | 16 | 2100 | 38000 | 170W |
| Apple M4 Pro | 14 (10P+4E) | 3500 | 22000 | 30W |

---

## Exercise 1: Clock Speed vs IPC

**Question:** Compare execution of same workload:
- Intel i9: 5.5 GHz, IPC = 4.0
- Apple M4: 4.5 GHz, IPC = 5.0

Calculate theoretical throughput (instructions/second).

**Your Answer:**
```
Intel throughput = ?
Apple throughput = ?
Which is faster = ?
Per-watt efficiency = ?
```

<details>
<summary>Solution</summary>

```
Intel i9:
  Throughput = 5.5 GHz × 4.0 IPC = 22 billion IPS
  Power: 125W
  Efficiency: 22B / 125W = 176 MIPS/W

Apple M4:
  Throughput = 4.5 GHz × 5.0 IPC = 22.5 billion IPS
  Power: 30W
  Efficiency: 22.5B / 30W = 750 MIPS/W

Comparison:
  Raw throughput: Nearly identical!
  Power efficiency: M4 is 4.3x more efficient

This is why:
- M4 matches Intel on single-thread despite lower clock
- M4 has amazing battery life
- Different design philosophies work for different use cases
```
</details>

---

## Exercise 2: Memory Architecture Impact

**Question:** Apple uses unified memory architecture.
- Intel: Separate CPU/GPU memory, transfer via PCIe
- Apple M4: Shared memory, no transfer needed

ML inference loading 10 GB model:
- Intel: DDR5 to RAM, then PCIe to GPU (10 GB/s)
- Apple: Direct access from unified pool

**Your Answer:**
```
Intel load time = ?
Apple load time = ?
Practical impact = ?
```

<details>
<summary>Solution</summary>

```
Intel:
  Load to RAM: 10 GB / 50 GB/s = 200 ms
  Transfer to GPU: 10 GB / 10 GB/s = 1000 ms
  Total: 1.2 seconds

Apple M4 Pro:
  Load to unified memory: 10 GB / 120 GB/s = 83 ms
  GPU access: 0 ms (same memory!)
  Total: 83 ms

Speedup: 14x faster for ML model loading

Practical Impact:
- Faster model switching
- Can run larger models (memory not duplicated)
- Better for interactive ML applications
- Intel needs double memory for same effective capacity
```
</details>

---

## Exercise 3: Multi-Core Scaling

**Question:** Parallel task on each platform:
- Intel i9-14900K: 8 P-cores + 16 E-cores
- Apple M4 Pro: 10 P-cores + 4 E-cores

Workload is perfectly parallelizable but only benefits from P-cores.
E-cores are ~60% of P-core performance.

**Your Answer:**
```
Intel effective cores = ?
Apple effective cores = ?
Multi-threaded comparison = ?
```

<details>
<summary>Solution</summary>

```
Intel i9-14900K:
  P-cores: 8 × 1.0 = 8.0 effective
  E-cores: 16 × 0.6 = 9.6 effective
  Total: 17.6 effective cores
  
  Note: E-cores share resources, actual ~15 effective

Apple M4 Pro:
  P-cores: 10 × 1.0 = 10.0 effective
  E-cores: 4 × 0.6 = 2.4 effective
  Total: 12.4 effective cores

Multi-Threaded:
  Intel has ~25% more parallel capacity
  But at 4x power consumption

Use Cases:
  Intel: Desktop workstation, render farms
  Apple: Laptop productivity, efficiency-critical
  
  For a single heavy task: Intel wins on raw multi-core
  For battery-constrained: Apple wins dramatically
```
</details>

---

## Exercise 4: Real-World Compilation

**Question:** Compile a large C++ project (100K lines):
- Build system: Ninja with max parallelism
- Intel workstation: i9-14900K, 128 GB RAM
- Apple laptop: M4 Pro, 48 GB RAM

Intel measured: 5 minutes (peak 200W).
Estimate Apple performance.

**Your Answer:**
```
Apple build time estimate = ?
Energy used Intel = ?
Energy used Apple = ?
```

<details>
<summary>Solution</summary>

```
Compilation Analysis:
  Single-file compile: I/O + parse + optimize + codegen
  Highly parallelizable across files
  
Intel Build:
  Time: 5 minutes = 300 seconds
  Effective cores: ~15
  Work: 300 × 15 = 4500 core-seconds

Apple Estimate:
  Effective cores: ~12
  Per-core similar performance (compile is balanced)
  Time: 4500 / 12 = 375 seconds ≈ 6.25 minutes

Energy Comparison:
  Intel: 300s × 200W = 60,000 Wh = 60 kJ
  Apple: 375s × 35W = 13,125 Wh = 13 kJ

Results:
  Intel: 25% faster
  Apple: 78% less energy

For mobile development, Apple provides:
  - Reasonable build times
  - Long battery life
  - Silent operation (no throttling)
```
</details>

---

## Exercise 5: Virtualization Performance

**Question:** Running x86 code on ARM (Apple M-series):
- Rosetta 2 translation overhead: ~20-30%
- Native ARM: 100% performance

Common scenarios:
1. Run x86 Docker containers
2. Run x86 Windows VM
3. Run native macOS apps

**Your Answer:**
```
Docker (x86 emulation) = ?
Windows VM = ?
Native apps = ?
Recommendation = ?
```

<details>
<summary>Solution</summary>

```
1. Docker (x86 emulation):
   Performance: 50-70% of native
   Issues: 
     - qemu/Rosetta translation overhead
     - Some x86 instructions not supported
   Solution: Use ARM-native containers when possible
   
2. Windows VM (x86):
   Performance: 30-50% of native
   Why:
     - Full system emulation
     - Nested translations
     - No hardware virtualization for x86
   Solution: Use Windows on ARM (limited support)

3. Native macOS Apps:
   Universal Binary: 100% native performance
   Rosetta translated: 70-90% performance
   
   Most popular apps are now universal.

Recommendation:
  - Prefer ARM-native software
  - Docker: Use ARM images (linux/arm64)
  - Development: Most tools work natively
  - Legacy x86: Expect 30-50% performance hit
```
</details>

---

## Exercise 6: Sorting Benchmark

**Question:** Sort 100 million integers:
- Intel i9-14900K: 3.5 seconds (single-thread)
- Apple M4 Pro: 3.2 seconds (single-thread)

Now with parallel sort:
- Intel: 8 P-cores available
- Apple: 10 P-cores available

Estimate parallel times (assume 60% scaling efficiency).

**Your Answer:**
```
Intel parallel time = ?
Apple parallel time = ?
Analysis = ?
```

<details>
<summary>Solution</summary>

```
Single-Thread:
  Intel: 3.5 seconds
  Apple: 3.2 seconds (9% faster)

Parallel Sort (60% efficiency):
  Speedup = cores × efficiency

Intel Parallel:
  Effective speedup: 8 × 0.6 = 4.8x
  Time: 3.5 / 4.8 = 0.73 seconds

Apple Parallel:
  Effective speedup: 10 × 0.6 = 6.0x
  Time: 3.2 / 6.0 = 0.53 seconds

Results:
  Apple is 27% faster in this parallel task
  
Why:
  - More P-cores (10 vs 8)
  - Slightly better single-thread
  - Better memory bandwidth for parallel access

This matches real-world observations:
  Apple M4 Pro often beats Intel on well-parallelized tasks
  despite lower power consumption.
```
</details>

---

## Key Takeaways

1. **Clock speed ≠ performance**: IPC matters equally
2. **Apple wins on efficiency**: 3-5x better perf/watt
3. **Intel wins on raw multi-core**: More cores for desktop
4. **Unified memory is powerful**: Especially for ML/GPU
5. **Emulation costs ~30-50%**: Use native when possible

## Quick Reference
```
Single-thread: M4 Pro ≈ Intel i9 (M4 often slightly faster)
Multi-thread: Intel has more raw power, Apple more efficient
Power: M4 Pro ~30W, Intel i9 ~125W

Development: Both excellent, Apple has battery life
Heavy compute: Intel/AMD for desktop, Apple for laptop
```

## Next Steps
- Try [Intermediate: Server vs Desktop](../intermediate/server_desktop.md)
- Learn about [Real-World Scenarios](../../08_real_world_scenarios/beginner/web_server_estimation.md)
