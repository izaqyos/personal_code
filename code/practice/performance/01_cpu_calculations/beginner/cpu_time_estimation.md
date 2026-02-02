# CPU Time Estimation - Beginner

Estimate execution time based on CPU characteristics.

## Learning Objectives
- Understand clock speed and its relation to execution time
- Calculate theoretical execution time for simple operations
- Compare different CPU architectures

## Background

### Key Formulas
```
Time = Cycles / Clock_Frequency
Cycles = Instructions × CPI (Cycles Per Instruction)
Clock_Frequency = GHz × 10^9
```

### Reference Values
| CPU | Clock Speed | Notes |
|-----|-------------|-------|
| Intel i9-14900K | 3.2-6.0 GHz | Desktop, high-end |
| AMD Ryzen 9 7950X | 4.5-5.7 GHz | Desktop, high-end |
| Apple M4 | 4.4 GHz | Laptop, efficiency |
| Apple M4 Pro | 4.5 GHz | Laptop, pro |

---

## Exercise 1: Basic Time Calculation

**Question:** A function executes 10 million (10^7) instructions on a 3 GHz CPU with CPI = 1.5. How long does it take?

**Your Answer:**
```
Time = ?

Show your work:
```

<details>
<summary>Solution</summary>

```
Cycles = 10^7 instructions × 1.5 CPI = 1.5 × 10^7 cycles
Clock = 3 GHz = 3 × 10^9 Hz
Time = 1.5 × 10^7 / 3 × 10^9 = 0.005 seconds = 5 ms
```
</details>

---

## Exercise 2: Sorting Estimation

**Question:** Quicksort on 1 million integers.
- Comparisons: ~20 million (n log n where n = 10^6)
- Assume 10 instructions per comparison
- CPU: 4 GHz, CPI = 2

How long should the sort take (theoretical minimum)?

**Your Answer:**
```
Time = ?

Show your work:
```

<details>
<summary>Solution</summary>

```
Instructions = 20 × 10^6 comparisons × 10 instructions = 2 × 10^8
Cycles = 2 × 10^8 × 2 = 4 × 10^8
Clock = 4 × 10^9 Hz
Time = 4 × 10^8 / 4 × 10^9 = 0.1 seconds = 100 ms

Note: Real-world will be 2-5x slower due to cache misses, branch mispredictions
```
</details>

---

## Exercise 3: Platform Comparison

**Question:** The same algorithm runs on two platforms:
- Platform A: 3 GHz, CPI = 1.2
- Platform B: 2 GHz, CPI = 0.8

Which is faster, and by how much?

**Your Answer:**
```
Platform A throughput (instructions/second) = ?
Platform B throughput (instructions/second) = ?
Which is faster = ?
```

<details>
<summary>Solution</summary>

```
Throughput = Clock / CPI (instructions per second)

Platform A: 3 × 10^9 / 1.2 = 2.5 × 10^9 IPS
Platform B: 2 × 10^9 / 0.8 = 2.5 × 10^9 IPS

They are equal! Higher clock doesn't always mean faster.
This is why CPI (instruction efficiency) matters.
```
</details>

---

## Exercise 4: Simple Loop Analysis

**Question:** Analyze this loop:
```python
total = 0
for i in range(1_000_000):
    total += array[i]
```

Estimate instructions per iteration and total time on a 3 GHz CPU (CPI = 1).

Hint: Each iteration has:
- Loop counter increment: 1 instruction
- Comparison: 1 instruction
- Array access: 1-2 instructions
- Addition: 1 instruction
- Branch: 1 instruction

**Your Answer:**
```
Instructions per iteration = ?
Total instructions = ?
Time = ?
```

<details>
<summary>Solution</summary>

```
Instructions per iteration ≈ 6
Total instructions = 6 × 10^6 = 6 × 10^6

At 3 GHz, CPI = 1:
Cycles = 6 × 10^6
Time = 6 × 10^6 / 3 × 10^9 = 2 ms

Reality check: Python is interpreted, so actual time is 50-100x slower (~100-200 ms)
C/compiled code would be close to 2 ms
```
</details>

---

## Exercise 5: x86 vs ARM Comparison

**Question:** Compare execution of 100 million arithmetic operations:

| CPU | Clock | Typical IPC |
|-----|-------|-------------|
| Intel i9-14900K | 5.5 GHz (turbo) | 4.0 |
| Apple M4 Pro | 4.5 GHz | 5.0 |

Which completes faster?

**Your Answer:**
```
Intel time = ?
Apple time = ?
Winner = ?
```

<details>
<summary>Solution</summary>

```
Intel i9-14900K:
  Throughput = 5.5 × 10^9 × 4.0 = 22 × 10^9 ops/sec
  Time = 10^8 / 22 × 10^9 = 4.5 ms

Apple M4 Pro:
  Throughput = 4.5 × 10^9 × 5.0 = 22.5 × 10^9 ops/sec
  Time = 10^8 / 22.5 × 10^9 = 4.4 ms

Result: Very close! M4 Pro slightly faster despite lower clock.
ARM's better IPC compensates for lower frequency.
```
</details>

---

## Key Takeaways

1. **Clock speed alone doesn't determine performance** - IPC matters equally
2. **Theoretical vs actual**: Real performance is 2-10x slower due to:
   - Cache misses
   - Branch mispredictions
   - Memory latency
   - Pipeline stalls
3. **Modern CPUs execute 2-4 billion instructions per second** under ideal conditions
4. **ARM vs x86**: Different approaches, often similar real-world performance

## Next Steps
- Try [Intermediate: Pipeline Effects](../intermediate/pipeline_effects.md)
- Learn about [Cache Effects](../../05_cache_effects/beginner/cache_basics.md)
