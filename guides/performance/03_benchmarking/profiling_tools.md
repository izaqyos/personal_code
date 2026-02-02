# Profiling Tools

Finding performance bottlenecks with profiling.

## Types of Profiling

### CPU Profiling
Measures where time is spent in code.

### Memory Profiling
Tracks memory allocations and usage.

### I/O Profiling
Measures disk and network operations.

### Sampling vs Instrumentation

| Method | Overhead | Accuracy | Detail |
|--------|----------|----------|--------|
| Sampling | Low (1-5%) | Statistical | Function level |
| Instrumentation | High (10-100%) | Exact | Line level |

## Python Profiling

### cProfile (Built-in)
```python
import cProfile
import pstats

# Profile a function
cProfile.run('my_function()', 'output.prof')

# Analyze results
stats = pstats.Stats('output.prof')
stats.sort_stats('cumulative')
stats.print_stats(20)  # Top 20 functions
```

**Command line:**
```bash
python -m cProfile -s cumulative script.py
```

### line_profiler
```python
# Install: pip install line_profiler

@profile  # Decorator
def slow_function():
    # ... code ...
    pass

# Run: kernprof -l -v script.py
```

**Output:**
```
Line #   Hits    Time  Per Hit   % Time  Line Contents
     3     1      1.0      1.0      0.0  def slow_function():
     4  1000  50000.0     50.0     50.0      for i in range(1000):
     5  1000  50000.0     50.0     50.0          result = expensive_op(i)
```

### memory_profiler
```python
# Install: pip install memory_profiler

from memory_profiler import profile

@profile
def memory_heavy():
    a = [i for i in range(1000000)]
    return a

# Run: python -m memory_profiler script.py
```

### py-spy (Sampling)
```bash
# Install: pip install py-spy

# Profile running process
py-spy top --pid 12345

# Record to file
py-spy record -o profile.svg --pid 12345

# Profile command
py-spy record -o profile.svg -- python script.py
```

## JavaScript Profiling

### Chrome DevTools
```javascript
// Console timing
console.time('operation');
doSomething();
console.timeEnd('operation');

// Performance API
performance.mark('start');
doSomething();
performance.mark('end');
performance.measure('operation', 'start', 'end');
```

### Node.js Profiling
```bash
# V8 profiler
node --prof script.js
node --prof-process isolate-*.log > processed.txt

# Flamegraph
node --perf-basic-prof script.js
```

## Java Profiling

### JVM Tools
```bash
# JVisualVM (built-in)
jvisualvm

# Async-profiler (low overhead)
java -agentpath:libasyncProfiler.so=start,file=profile.html -jar app.jar
```

### JFR (Java Flight Recorder)
```bash
# Start recording
java -XX:StartFlightRecording=duration=60s,filename=recording.jfr -jar app.jar

# Analyze with JMC (Java Mission Control)
jmc recording.jfr
```

## C/C++ Profiling

### gprof
```bash
# Compile with profiling
gcc -pg -o program program.c

# Run program (generates gmon.out)
./program

# Analyze
gprof program gmon.out > analysis.txt
```

### perf (Linux)
```bash
# CPU profiling
perf record ./program
perf report

# Flamegraph
perf record -g ./program
perf script | stackcollapse-perf.pl | flamegraph.pl > flame.svg
```

### Valgrind
```bash
# Memory profiling
valgrind --tool=massif ./program
ms_print massif.out.*

# Cache profiling
valgrind --tool=cachegrind ./program
cg_annotate cachegrind.out.*
```

## Flame Graphs

Visual representation of profiled stack traces.

### Reading Flame Graphs
```
Width = Time spent in function
Y-axis = Call stack depth
Bottom = Entry point
Top = Leaf functions

Wide bars at top = Optimization targets
```

### Generating Flame Graphs
```bash
# Python
py-spy record -o flame.svg -- python script.py

# Node.js
node --perf-basic-prof script.js
perf record -g -- node script.js
perf script | stackcollapse-perf.pl | flamegraph.pl > flame.svg

# Java (async-profiler)
./profiler.sh -d 30 -f flame.svg <pid>
```

## Benchmarking Best Practices

### Warm-up
```python
# Let JIT optimize before measuring
for _ in range(1000):
    function_to_benchmark()

# Now measure
import time
start = time.perf_counter()
for _ in range(10000):
    function_to_benchmark()
elapsed = time.perf_counter() - start
print(f"Average: {elapsed / 10000 * 1000:.3f} ms")
```

### Statistical Rigor
```python
import statistics
import time

def benchmark(func, iterations=100):
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        func()
        times.append(time.perf_counter() - start)
    
    return {
        'mean': statistics.mean(times),
        'median': statistics.median(times),
        'stdev': statistics.stdev(times),
        'min': min(times),
        'max': max(times),
    }
```

### Isolate Variables
```bash
# Disable CPU frequency scaling
sudo cpupower frequency-set --governor performance

# Disable turbo boost
echo 1 | sudo tee /sys/devices/system/cpu/intel_pstate/no_turbo

# Pin to single CPU
taskset -c 0 ./benchmark
```

## Quick Profiling Checklist

### 1. High-Level First
```python
import time

start = time.perf_counter()
main_operation()
print(f"Total: {time.perf_counter() - start:.3f}s")
```

### 2. Function-Level
```bash
python -m cProfile -s cumulative script.py 2>&1 | head -30
```

### 3. Line-Level (if needed)
```bash
kernprof -l -v script.py
```

### 4. Memory (if suspected)
```bash
python -m memory_profiler script.py
```

## Common Bottleneck Patterns

### CPU-Bound
```
- High CPU usage
- Flame graph shows computation functions
- Fix: Algorithm optimization, vectorization, parallelism
```

### Memory-Bound
```
- High memory allocation
- GC pauses in profile
- Fix: Object pooling, reduce allocations
```

### I/O-Bound
```
- Low CPU usage
- Time in I/O functions
- Fix: Async I/O, caching, batching
```

### Lock Contention
```
- Low CPU usage with multiple threads
- Time in lock acquire
- Fix: Reduce lock scope, lock-free structures
```

## Quick Reference

### Python Profiling Commands
```bash
# CPU (function level)
python -m cProfile -s cumulative script.py

# CPU (line level)
kernprof -l -v script.py

# Memory
python -m memory_profiler script.py

# Flame graph
py-spy record -o flame.svg -- python script.py
```

### Profiler Selection

| Need | Tool |
|------|------|
| Quick overview | cProfile |
| Line-by-line | line_profiler |
| Memory leaks | memory_profiler |
| Production | py-spy |
| Visualization | Flame graphs |

## Related Topics
- [Microbenchmarks](microbenchmarks.md)
- [Load Testing](load_testing.md)
