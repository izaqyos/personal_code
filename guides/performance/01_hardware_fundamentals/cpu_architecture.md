# CPU Architecture

Understanding CPU fundamentals for performance estimation.

## Key Concepts

### Clock Speed
- Measured in GHz (billions of cycles per second)
- 3 GHz = 3 billion cycles/second
- One cycle ≈ 0.33 nanoseconds at 3 GHz

### Instructions Per Cycle (IPC)
Modern CPUs execute multiple instructions per cycle:
- Simple instructions: 3-4 IPC possible
- Complex workloads: Often < 1 IPC due to dependencies
- Typical real-world: 1-2 IPC

### CPU Pipeline
```
Fetch → Decode → Execute → Memory → Writeback
```
Pipeline allows overlapping instruction execution.

**Pipeline stalls occur from:**
- Branch mispredictions (~15-20 cycles penalty)
- Cache misses (wait for memory)
- Data dependencies

## Modern CPU Features

### Superscalar Execution
Multiple execution units allow parallel instruction execution:
- Integer ALU (arithmetic)
- Floating-point unit
- Load/Store units
- SIMD units

### Out-of-Order Execution
CPU reorders instructions for efficiency:
```python
# Original order
a = load(x)     # Slow if cache miss
b = 5 + 3       # Fast
c = a + 1       # Depends on a

# CPU might execute b while waiting for a
```

### Branch Prediction
CPU guesses branch outcomes to avoid pipeline stalls:
- ~95-99% accuracy for well-predicted branches
- Misprediction: 15-20 cycle penalty

### SIMD (Single Instruction, Multiple Data)
Process multiple data elements in parallel:
- SSE: 128-bit (4 floats)
- AVX2: 256-bit (8 floats)
- AVX-512: 512-bit (16 floats)

```
Traditional:     SIMD (4-wide):
a[0] = b[0] + c[0]    a[0:4] = b[0:4] + c[0:4]
a[1] = b[1] + c[1]    (single instruction)
a[2] = b[2] + c[2]
a[3] = b[3] + c[3]
```

## CPU Comparison

### x86 (Intel/AMD)
- Higher clock speeds (up to 5+ GHz)
- Complex instruction set
- Strong single-thread performance
- Higher power consumption

### ARM (Apple M-series, Graviton)
- Efficiency-focused design
- RISC (simpler instructions)
- Better performance per watt
- Growing multi-thread performance

### Quick Reference (2024)

| CPU | Cores | Base Clock | Single-Thread | Multi-Thread |
|-----|-------|------------|---------------|--------------|
| Intel i9-14900K | 24 | 3.2 GHz | ~2200 (CB) | ~40000 |
| AMD Ryzen 9 7950X | 16 | 4.5 GHz | ~2100 | ~38000 |
| Apple M4 Pro | 14 | 4.5 GHz | ~3500 | ~22000 |
| AWS Graviton3 | 64 | 2.6 GHz | ~1200 | ~35000 |

## Estimation Tips

### Cycles for Operations

| Operation | Cycles |
|-----------|--------|
| Integer add/sub | 1 |
| Integer multiply | 3-4 |
| Integer divide | 20-100 |
| Float add/sub | 3-5 |
| Float multiply | 3-5 |
| Float divide | 10-20 |
| Branch (predicted) | 0-1 |
| Branch (mispredicted) | 15-20 |

### Time Estimation Formula
```
Time = (Instructions × CPI) / Clock_Frequency

Where:
  CPI = Cycles Per Instruction (often 1-3)
  Clock = Hz
```

### Example
Sort 1M integers on 3 GHz CPU:
```
Quicksort: O(n log n) comparisons
= 1M × 20 = 20M comparisons
≈ 100M instructions (with overhead)

At 1 IPC: 100M cycles
At 3 GHz: 100M / 3B = 33ms

Reality: 50-100ms (cache effects, memory)
```

## Related Topics
- [Cache Hierarchy](cache_hierarchy.md)
- [Memory](memory.md)
