# Pipeline Effects - Intermediate

Understanding how CPU pipeline affects performance.

## Learning Objectives
- Understand pipeline stalls and their impact
- Calculate performance impact of branch misprediction
- Analyze data dependency effects

## Background

### CPU Pipeline
```
Fetch → Decode → Execute → Memory → Writeback
```

Modern CPUs overlap these stages for different instructions (pipelining).

### Pipeline Hazards
1. **Data Hazard**: Instruction depends on result of previous instruction
2. **Control Hazard**: Branch changes program flow
3. **Structural Hazard**: Multiple instructions need same resource

### Key Values
- Branch misprediction penalty: 15-20 cycles
- Data dependency stall: 1-3 cycles
- Pipeline depth: 14-20 stages (modern CPUs)

---

## Exercise 1: Branch Misprediction Cost

**Question:** A loop runs 10,000 iterations with a condition that's 50% predictable:
```python
for i in range(10000):
    if random_condition():  # 50% true
        do_something()      # 5 cycles
    else:
        do_other()          # 5 cycles
```

Compare performance with:
- Perfect prediction (100% accurate)
- Random prediction (50% accurate)

Assume: 20-cycle misprediction penalty, 3 GHz CPU

**Your Answer:**
```
Perfect prediction time = ?
Random prediction (50% misses) time = ?
Slowdown = ?
```

<details>
<summary>Solution</summary>

```
Perfect Prediction:
  Work per iteration: 5 cycles
  Total: 10,000 × 5 = 50,000 cycles
  Time: 50,000 / 3 × 10^9 = 16.7 μs

50% Misprediction:
  Work per iteration: 5 cycles
  Mispredictions: 5,000 × 20 = 100,000 cycles
  Total: 50,000 + 100,000 = 150,000 cycles
  Time: 150,000 / 3 × 10^9 = 50 μs

Slowdown: 50 / 16.7 = 3x slower with random branches!
```
</details>

---

## Exercise 2: Sorted vs Unsorted

**Question:** This code processes an array:
```cpp
for (int i = 0; i < size; i++) {
    if (data[i] >= 128) {
        sum += data[i];
    }
}
```

Data contains random values 0-255 (50% >= 128).

Compare execution time:
- Array size: 100,000
- Sorted array: Perfect branch prediction
- Unsorted array: 50% misprediction
- Work when true: 5 cycles
- Loop overhead: 3 cycles per iteration
- Misprediction penalty: 15 cycles

**Your Answer:**
```
Sorted array time = ?
Unsorted array time = ?
Speedup from sorting = ?
```

<details>
<summary>Solution</summary>

```
Sorted Array:
  Loop overhead: 100,000 × 3 = 300,000 cycles
  Work (50% true): 50,000 × 5 = 250,000 cycles
  Mispredictions: ~1 (at transition point) = 15 cycles
  Total: 550,015 cycles

Unsorted Array:
  Loop overhead: 100,000 × 3 = 300,000 cycles
  Work (50% true): 50,000 × 5 = 250,000 cycles
  Mispredictions: 50,000 × 15 = 750,000 cycles
  Total: 1,300,000 cycles

Sorted: 550,000 / 3 × 10^9 = 183 μs
Unsorted: 1,300,000 / 3 × 10^9 = 433 μs

Speedup: 2.4x faster when sorted!

This is the famous "sorted array is faster" effect.
```
</details>

---

## Exercise 3: Data Dependency Chain

**Question:** Compare these two code patterns:
```cpp
// Pattern A: Dependency chain
a = input1;
b = a + 1;      // depends on a
c = b + 1;      // depends on b
d = c + 1;      // depends on c
result = d + 1; // depends on d

// Pattern B: Independent operations
a = input1 + 1;
b = input2 + 1;  // independent
c = input3 + 1;  // independent
d = input4 + 1;  // independent
result = a + b + c + d;
```

Assume:
- Addition: 1 cycle latency
- 4-wide superscalar (4 ops per cycle possible)
- No other stalls

Calculate cycles for each pattern.

**Your Answer:**
```
Pattern A cycles = ?
Pattern B cycles = ?
Speedup = ?
```

<details>
<summary>Solution</summary>

```
Pattern A (Dependency Chain):
  Each operation must wait for previous:
  a = input1       : cycle 1
  b = a + 1        : cycle 2 (waits for a)
  c = b + 1        : cycle 3 (waits for b)
  d = c + 1        : cycle 4 (waits for c)
  result = d + 1   : cycle 5 (waits for d)
  Total: 5 cycles

Pattern B (Independent):
  a, b, c, d computed in parallel: cycle 1 (all 4 at once)
  result = a + b   : cycle 2
  result = result + c: cycle 3
  result = result + d: cycle 4
  Total: 4 cycles (could be 3 with tree reduction)

  Or with better reduction:
  temp1 = a + b, temp2 = c + d: cycle 2 (parallel)
  result = temp1 + temp2: cycle 3
  Total: 3 cycles

Speedup: 5/3 = 1.67x for independent operations
```
</details>

---

## Exercise 4: Loop Unrolling Benefit

**Question:** Unrolling reduces branch frequency:
```cpp
// Original: 1M iterations, 1 branch per iteration
for (int i = 0; i < 1000000; i++) {
    sum += array[i];
}

// Unrolled 4x: 250K iterations
for (int i = 0; i < 1000000; i += 4) {
    sum += array[i];
    sum += array[i+1];
    sum += array[i+2];
    sum += array[i+3];
}
```

Calculate cycle savings:
- Original: 3 cycle loop overhead per iteration
- Unrolled: 4 cycle loop overhead per iteration (larger loop)
- Addition: 1 cycle each
- Branch misprediction: 1 per loop (at the end)

**Your Answer:**
```
Original total cycles = ?
Unrolled total cycles = ?
Savings = ?
```

<details>
<summary>Solution</summary>

```
Original Loop (1M iterations):
  Work: 1M × 1 = 1M cycles
  Overhead: 1M × 3 = 3M cycles
  Final misprediction: 20 cycles
  Total: 4M cycles

Unrolled Loop (250K iterations):
  Work: 1M × 1 = 1M cycles (same work)
  Overhead: 250K × 4 = 1M cycles
  Final misprediction: 20 cycles
  Total: 2M cycles

Savings: 4M - 2M = 2M cycles
Speedup: 2x faster!

Key insight: Reduced branch frequency, even with slightly
higher per-iteration overhead.
```
</details>

---

## Exercise 5: Speculative Execution

**Question:** CPU speculatively executes both branches:
```cpp
if (likely_true_99_percent) {
    quick_operation();    // 10 cycles
} else {
    slow_operation();     // 100 cycles
}
```

Calculate expected cycles with and without speculation:
- Branch takes 5 cycles to resolve
- Correct speculation: Continue, no penalty
- Wrong speculation: 20 cycle rollback + actual path

1,000 iterations, 99% branch taken.

**Your Answer:**
```
Without speculation = ?
With speculation = ?
Benefit = ?
```

<details>
<summary>Solution</summary>

```
Without Speculation:
  Every iteration waits 5 cycles for branch resolution
  Then: 990 × 10 + 10 × 100 = 9,900 + 1,000 = 10,900 cycles work
  Plus: 1,000 × 5 = 5,000 cycles waiting
  Total: 15,900 cycles

With Speculation (99% correct):
  990 correct: 990 × 10 = 9,900 cycles (no wait)
  10 wrong: 10 × (20 + 100) = 1,200 cycles
  Total: 11,100 cycles

Benefit: 15,900 - 11,100 = 4,800 cycles saved
Speedup: 1.43x faster with speculation

This is why branch prediction is so valuable!
```
</details>

---

## Key Takeaways

1. **Branch misprediction is expensive**: 15-20 cycles per miss
2. **Data dependencies limit ILP**: Can't parallelize dependent operations
3. **Predictable branches are fast**: Sorted data often faster
4. **Loop unrolling reduces overhead**: Fewer branches, more work per iteration
5. **Speculation helps**: Correct guesses avoid stalls

## Next Steps
- Try [Advanced: SIMD and Vectorization](../advanced/simd_optimization.md)
- Learn about [Memory Effects](../../02_memory_bandwidth/beginner/memory_basics.md)
