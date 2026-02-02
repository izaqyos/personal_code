# Microbenchmarks

Measuring small code snippets accurately.

## Python Microbenchmarking

### timeit Module
```python
import timeit

# Simple usage
timeit.timeit('sum(range(1000))', number=10000)

# With setup
timeit.timeit(
    'sorted(data)',
    setup='import random; data = [random.random() for _ in range(1000)]',
    number=1000
)

# Function benchmarking
def my_function():
    return sum(range(1000))

timeit.timeit(my_function, number=10000)
```

### Command Line
```bash
python -m timeit "sum(range(1000))"
python -m timeit -s "import random; data = [random.random() for _ in range(1000)]" "sorted(data)"
```

### perf_counter for Custom Timing
```python
import time

def benchmark(func, iterations=1000):
    # Warm-up
    for _ in range(100):
        func()
    
    # Measure
    start = time.perf_counter()
    for _ in range(iterations):
        func()
    elapsed = time.perf_counter() - start
    
    return elapsed / iterations
```

## Benchmarking Pitfalls

### 1. Dead Code Elimination
```python
# Bad: Compiler might optimize away
def benchmark_bad():
    result = expensive_calculation()
    # result not used!

# Good: Use the result
def benchmark_good():
    result = expensive_calculation()
    return result  # Forces computation
```

### 2. Constant Folding
```python
# Bad: Computed at compile time
timeit.timeit('2 + 3')  # Near zero

# Good: Use variables
timeit.timeit('a + b', setup='a = 2; b = 3')
```

### 3. Caching Effects
```python
# First run: Cold cache, slow
# Subsequent runs: Warm cache, fast

# Measure both scenarios:
def benchmark_with_cache_flush():
    # Cold cache scenario
    for _ in range(10):
        flush_cache()  # Access unrelated large data
        result = function_to_test()
    
    # Warm cache scenario
    for _ in range(10):
        result = function_to_test()
```

### 4. CPU Frequency Scaling
```bash
# Check current governor
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor

# Set to performance (Linux)
sudo cpupower frequency-set --governor performance
```

### 5. Outliers
```python
import statistics

times = [measure() for _ in range(100)]

# Report multiple statistics
print(f"Mean: {statistics.mean(times):.6f}")
print(f"Median: {statistics.median(times):.6f}")
print(f"Stdev: {statistics.stdev(times):.6f}")
print(f"Min: {min(times):.6f}")
print(f"Max: {max(times):.6f}")

# Trim outliers
sorted_times = sorted(times)
trimmed = sorted_times[5:-5]  # Remove top/bottom 5%
print(f"Trimmed mean: {statistics.mean(trimmed):.6f}")
```

## Comparison Benchmarks

### A/B Testing Code
```python
import timeit

def solution_a(data):
    return [x * 2 for x in data]

def solution_b(data):
    result = []
    for x in data:
        result.append(x * 2)
    return result

# Setup
setup = "data = list(range(10000))"

# Benchmark both
time_a = timeit.timeit(
    "solution_a(data)",
    setup=setup + "\nfrom __main__ import solution_a",
    number=1000
)

time_b = timeit.timeit(
    "solution_b(data)",
    setup=setup + "\nfrom __main__ import solution_b",
    number=1000
)

print(f"Solution A: {time_a:.4f}s")
print(f"Solution B: {time_b:.4f}s")
print(f"A is {time_b/time_a:.2f}x faster")
```

### Scaling Analysis
```python
def benchmark_scaling(func, sizes):
    """Benchmark function with different input sizes."""
    results = {}
    for n in sizes:
        data = list(range(n))
        time_taken = timeit.timeit(
            lambda: func(data),
            number=100
        ) / 100
        results[n] = time_taken
        print(f"n={n:>8}: {time_taken:.6f}s")
    
    # Check scaling
    for i in range(1, len(sizes)):
        ratio = results[sizes[i]] / results[sizes[i-1]]
        size_ratio = sizes[i] / sizes[i-1]
        print(f"Time ratio: {ratio:.2f}x for {size_ratio}x size")
    
    return results

# Example: Check if O(n) or O(n²)
sizes = [1000, 2000, 4000, 8000]
benchmark_scaling(sorted, sizes)
# O(n log n): expect ~2.2x per doubling
# O(n²): expect ~4x per doubling
```

## Memory Benchmarking

### tracemalloc
```python
import tracemalloc

tracemalloc.start()

# Code to measure
data = [i ** 2 for i in range(100000)]

current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

print(f"Current: {current / 1024:.2f} KB")
print(f"Peak: {peak / 1024:.2f} KB")
```

### sys.getsizeof
```python
import sys

# Object size (shallow)
data = [1, 2, 3, 4, 5]
print(f"List: {sys.getsizeof(data)} bytes")

# Deep size calculation
def deep_sizeof(obj, seen=None):
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum(deep_sizeof(k, seen) + deep_sizeof(v, seen)
                    for k, v in obj.items())
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes)):
        size += sum(deep_sizeof(i, seen) for i in obj)
    return size
```

## JavaScript Microbenchmarks

### Console Timing
```javascript
console.time('operation');
for (let i = 0; i < 100000; i++) {
    // operation
}
console.timeEnd('operation');
```

### Performance API
```javascript
function benchmark(func, iterations = 1000) {
    // Warm-up
    for (let i = 0; i < 100; i++) func();
    
    const start = performance.now();
    for (let i = 0; i < iterations; i++) {
        func();
    }
    return (performance.now() - start) / iterations;
}

const avgTime = benchmark(() => myFunction());
console.log(`Average: ${avgTime.toFixed(4)} ms`);
```

## Benchmark Frameworks

### Python: pytest-benchmark
```python
# pip install pytest-benchmark

def test_my_function(benchmark):
    data = list(range(10000))
    result = benchmark(sorted, data)
    assert result == sorted(data)
```

```bash
pytest --benchmark-only test_perf.py
```

### JavaScript: Benchmark.js
```javascript
const Benchmark = require('benchmark');

const suite = new Benchmark.Suite;

suite
    .add('method1', function() { method1(); })
    .add('method2', function() { method2(); })
    .on('cycle', function(event) {
        console.log(String(event.target));
    })
    .on('complete', function() {
        console.log('Fastest is ' + this.filter('fastest').map('name'));
    })
    .run();
```

## Reporting Results

### Standard Format
```
Benchmark: String Concatenation
Environment: Python 3.11, macOS, Apple M2

| Method      | Mean     | Std Dev  | Iterations |
|-------------|----------|----------|------------|
| + operator  | 1.234 ms | 0.012 ms | 1000       |
| join()      | 0.089 ms | 0.003 ms | 1000       |
| f-strings   | 0.092 ms | 0.002 ms | 1000       |

Winner: join() is 13.9x faster than + operator
```

### Essential Information
```
1. What was benchmarked
2. Environment (language version, OS, hardware)
3. Methodology (iterations, warm-up)
4. Statistics (mean, stdev, min, max)
5. Raw data or reproducible code
```

## Quick Reference

### Python Timing Cheatsheet
```python
# Quick timing
%timeit expression  # IPython

# Module
import timeit
timeit.timeit('code', number=1000)

# Manual
import time
start = time.perf_counter()
# code
elapsed = time.perf_counter() - start

# Memory
import tracemalloc
tracemalloc.start()
# code
tracemalloc.get_traced_memory()
```

### Benchmark Checklist
```
□ Warm-up runs before measurement
□ Multiple iterations for statistics
□ Disable CPU frequency scaling
□ Use result to prevent dead code elimination
□ Report environment details
□ Show statistical measures (mean, stdev)
□ Check for outliers
```

## Related Topics
- [Profiling Tools](profiling_tools.md)
- [Load Testing](load_testing.md)
