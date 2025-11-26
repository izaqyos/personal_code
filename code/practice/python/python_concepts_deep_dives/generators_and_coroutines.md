# Deep Dive: Generators and Coroutines in Python

**Last Updated**: 2025-11-12  
**Python Version**: 3.11+  
**Level**: Advanced

---

## Table of Contents

1. [Generator Fundamentals](#generator-fundamentals)
2. [The Generator Protocol](#the-generator-protocol)
3. [Generator Methods: send(), throw(), close()](#generator-methods)
4. [Generator Expressions vs Generator Functions](#generator-expressions-vs-functions)
5. [yield from and Delegation](#yield-from-and-delegation)
6. [Coroutines: Generators as Consumers](#coroutines-generators-as-consumers)
7. [Advanced Patterns](#advanced-patterns)
8. [Performance Analysis](#performance-analysis)
9. [Real-World Use Cases](#real-world-use-cases)
10. [Common Pitfalls](#common-pitfalls)
11. [From Generators to async/await](#from-generators-to-asyncawait)

---

## Generator Fundamentals

### What Is a Generator Really?

A generator is a special type of iterator that:
1. **Lazily produces values** - values are computed on-demand
2. **Maintains state** - remembers where it left off between calls
3. **Is single-use** - exhausts after iteration completes
4. **Is memory efficient** - only one value exists at a time

```python
# Regular function - returns all values at once
def get_squares_list(n):
    result = []
    for i in range(n):
        result.append(i ** 2)
    return result  # All values in memory

# Generator function - yields values one at a time
def get_squares_generator(n):
    for i in range(n):
        yield i ** 2  # Value produced on-demand
```

### The Magic of `yield`

The `yield` keyword transforms a regular function into a generator factory:

```python
def countdown(n):
    print(f"Starting countdown from {n}")
    while n > 0:
        yield n  # Execution pauses here
        n -= 1
    print("Liftoff!")

# Calling the function doesn't execute it
gen = countdown(3)
print(type(gen))  # <class 'generator'>

# Execution happens when we iterate
for value in gen:
    print(f"T-minus {value}")
    
# Output:
# Starting countdown from 3
# T-minus 3
# T-minus 2
# T-minus 1
# Liftoff!
```

**Key Insight**: The function's local state (variables, execution position) is preserved between `yield` statements.

### Memory Efficiency Demonstration

```python
import sys

# List: All values in memory
large_list = [i ** 2 for i in range(1_000_000)]
print(f"List size: {sys.getsizeof(large_list):,} bytes")
# Output: ~8,448,728 bytes (8+ MB)

# Generator: Constant memory
large_gen = (i ** 2 for i in range(1_000_000))
print(f"Generator size: {sys.getsizeof(large_gen):,} bytes")
# Output: ~192 bytes (tiny!)
```

**Space Complexity**:
- List comprehension: O(n)
- Generator expression: O(1)

---

## The Generator Protocol

Generators implement the **iterator protocol** plus additional methods:

```python
class GeneratorProtocol:
    """Conceptual representation of generator protocol"""
    
    def __iter__(self):
        """Returns the iterator object (self)"""
        return self
    
    def __next__(self):
        """Returns next value or raises StopIteration"""
        pass
    
    # Additional generator-specific methods
    def send(self, value):
        """Send a value INTO the generator"""
        pass
    
    def throw(self, exc_type, exc_value=None, exc_tb=None):
        """Raise an exception inside the generator"""
        pass
    
    def close(self):
        """Raise GeneratorExit inside the generator"""
        pass
```

### Under the Hood: Generator State

A generator has several states:

```python
import inspect

def simple_gen():
    yield 1
    yield 2
    yield 3

gen = simple_gen()

# GEN_CREATED - just created, not started
print(inspect.getgeneratorstate(gen))  # GEN_CREATED

# GEN_SUSPENDED - paused at a yield
next(gen)
print(inspect.getgeneratorstate(gen))  # GEN_SUSPENDED

# Consume all values
list(gen)
# GEN_CLOSED - finished execution
print(inspect.getgeneratorstate(gen))  # GEN_CLOSED
```

**States**:
1. `GEN_CREATED` - Created but not started
2. `GEN_RUNNING` - Currently executing (only visible from inside)
3. `GEN_SUSPENDED` - Paused at a yield
4. `GEN_CLOSED` - Finished or closed

---

## Generator Methods

### `send()` - Two-Way Communication

Generators can not only produce values but also **consume** them:

```python
def echo_generator():
    print("Generator started")
    while True:
        received = yield  # Receives value sent via send()
        print(f"Received: {received}")

gen = echo_generator()

# MUST prime the generator first!
next(gen)  # Or gen.send(None)
# Output: Generator started

# Now we can send values
gen.send("Hello")    # Output: Received: Hello
gen.send("World")    # Output: Received: World
gen.send(42)         # Output: Received: 42
```

**Advanced: Both yield and receive**

```python
def accumulator():
    total = 0
    while True:
        value = yield total  # Yield current total, receive next value
        if value is not None:
            total += value

acc = accumulator()
next(acc)  # Prime it, returns 0

print(acc.send(10))  # Add 10, returns 10
print(acc.send(20))  # Add 20, returns 30
print(acc.send(5))   # Add 5, returns 35
```

**Critical Pattern**: You must "prime" a generator before sending non-None values. See the detailed explanation below.

#### Understanding Priming - A Deep Dive

**What Is Priming?**

Priming means advancing a generator to its first `yield` statement so it's ready to receive values via `send()`.

**Why Is Priming Needed?**

When you create a generator, it hasn't started executing yet - it's in a `GEN_CREATED` state, paused before the first line:

```python
def my_coroutine():
    print("Starting!")
    while True:
        value = yield  # Waiting to receive data
        print(f"Received: {value}")

gen = my_coroutine()  # Created but NOT started
# The "Starting!" hasn't printed yet
# The generator hasn't reached the yield statement
```

**The Problem**: You can't send a value to a generator that hasn't reached a `yield`:

```python
gen.send(10)  # ❌ TypeError: can't send non-None value to a just-started generator
```

**The Solution**: Prime it first:

```python
gen = my_coroutine()
next(gen)  # ✅ Prime - advances to first yield
# Output: "Starting!"

# Now it's waiting at the yield, ready to receive
gen.send(10)  # ✅ Works!
# Output: "Received: 10"
```

**Visual Execution Flow**:

```python
def echo():
    print("1. Generator started")
    while True:
        value = yield  # <-- Execution pauses HERE after priming
        print(f"2. Got value: {value}")
        print("3. Processing...")

# Step 1: Create (not started)
gen = echo()

# Step 2: Prime (run until first yield)
next(gen)  # Output: "1. Generator started"
           # Now paused at yield, waiting

# Step 3: Send data
gen.send("Hello")  
# Output:
# "2. Got value: Hello"
# "3. Processing..."
# Loops back, pauses at yield again
```

**The Priming Decorator Pattern**:

```python
def coroutine(func):
    """Decorator to auto-prime coroutines"""
    def wrapper(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)  # Prime it automatically
        return gen
    return wrapper

@coroutine
def echo():
    while True:
        received = yield
        print(f"Got: {received}")

gen = echo()  # Already primed!
gen.send("Hello")  # Works immediately ✅
```

**When You DON'T Need Priming**:

Only coroutines (using `send()`) need priming. Regular generators don't:

```python
# Regular generator (producer) - NO priming needed
def producer():
    yield 1
    yield 2

for value in producer():  # Just iterate
    print(value)
```

**Two Ways to Prime**:

```python
gen = my_coroutine()

# Method 1: Use next()
next(gen)

# Method 2: Send None
gen.send(None)

# Both do the same thing
```

**Think of it like turning on a machine**:
- **Create**: `gen = my_coroutine()` - Machine built but OFF
- **Prime**: `next(gen)` - Turn machine ON, ready to receive
- **Use**: `gen.send(data)` - Feed data into running machine

### `throw()` - Exception Injection

Inject exceptions into a generator:

```python
def robust_generator():
    try:
        while True:
            value = yield
            print(f"Processing: {value}")
    except ValueError as e:
        print(f"Caught ValueError: {e}")
        yield "error_handled"
    except GeneratorExit:
        print("Generator is closing")
    finally:
        print("Cleanup code here")

gen = robust_generator()
next(gen)

gen.send(10)                    # Processing: 10
gen.throw(ValueError, "Bad!")   # Caught ValueError: Bad!
next(gen)                       # Gets "error_handled"
gen.close()                     # Generator is closing
                                # Cleanup code here
```

**Use Case**: Error recovery in pipelines

```python
def resilient_pipeline(items):
    """Continue processing even if some items fail"""
    for item in items:
        try:
            result = yield item
            print(f"Success: {result}")
        except Exception as e:
            print(f"Error processing {item}: {e}")
            continue
```

### `close()` - Graceful Shutdown

Close a generator and run cleanup code:

```python
def resource_generator():
    print("Acquiring resource")
    resource = open("data.txt", "w")
    
    try:
        while True:
            data = yield
            resource.write(data)
    except GeneratorExit:
        print("Closing resource")
        resource.close()
        raise  # Must re-raise GeneratorExit

gen = resource_generator()
next(gen)
gen.send("some data\n")
gen.close()  # Triggers cleanup
```

**Best Practice**: Use context managers with generators for resource management.

---

## Generator Expressions vs Functions

### When to Use Each

**Generator Expression** (like list comprehension but with `()`):
```python
# Simple transformations
squares = (x**2 for x in range(10))
filtered = (x for x in data if x > 0)
combined = (x.strip().upper() for x in lines)
```

**Use When**:
- Single expression transformation
- Simple filtering
- Pipeline component
- One-liner is clearer

**Generator Function** (with `yield`):
```python
def complex_processing(data):
    buffer = []
    for item in data:
        # Complex logic
        if len(buffer) > 10:
            yield process_batch(buffer)
            buffer = []
        buffer.append(item)
    
    if buffer:
        yield process_batch(buffer)
```

**Use When**:
- Complex logic
- Multiple yields
- State management
- Need early termination
- Error handling required

### Performance Comparison

```python
import timeit

# Generator expression - slightly faster for simple cases
gen_expr = lambda n: (x**2 for x in range(n))

# Generator function - more overhead but more flexible
def gen_func(n):
    for x in range(n):
        yield x**2

# For simple transformations, expression is ~5-10% faster
# For complex logic, function overhead is negligible
```

**Space Complexity**: Both are O(1) - no difference

**Time Complexity**: 
- Generator creation: O(1) for both
- Full consumption: O(n) for both
- Per-item overhead: Expression slightly faster

---

## yield from and Delegation

`yield from` (Python 3.3+) delegates to a sub-generator:

### Basic Delegation

```python
def inner_gen():
    yield 1
    yield 2
    yield 3

def outer_gen():
    # Long way
    for value in inner_gen():
        yield value
    
    # Short way with yield from
    yield from inner_gen()

# Both produce: 1, 2, 3, 1, 2, 3
```

### Why `yield from` Matters

It's not just syntactic sugar - it properly delegates the full generator protocol:

```python
def reader():
    """Sub-generator that receives data"""
    while True:
        data = yield
        if data is None:
            break
        print(f"Read: {data}")

def reader_wrapper():
    """Delegating generator"""
    # This properly forwards send(), throw(), close()
    yield from reader()

gen = reader_wrapper()
next(gen)  # Prime it
gen.send("Hello")  # Properly forwarded to inner reader
gen.send("World")
gen.send(None)     # Breaks inner loop
```

**Without** `yield from`, you'd need:
```python
def reader_wrapper_manual():
    inner = reader()
    try:
        value = next(inner)
        while True:
            try:
                sent = yield value
                value = inner.send(sent)
            except Exception as e:
                value = inner.throw(type(e), e)
    except StopIteration:
        pass
```

### Recursive Generators with yield from

```python
def traverse_tree(node):
    """Traverse nested tree structure"""
    yield node.value
    
    for child in node.children:
        yield from traverse_tree(child)  # Recursive delegation

# Flatten nested lists
def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)  # Recurse
        else:
            yield item

nested = [1, [2, [3, 4], 5], 6, [7, 8]]
print(list(flatten(nested)))  # [1, 2, 3, 4, 5, 6, 7, 8]
```

### Return Values from Sub-generators

`yield from` captures the return value of the sub-generator:

```python
def accumulate(items):
    total = 0
    for item in items:
        total += item
        yield total
    return total  # Final total

def process_batches(data, batch_size):
    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]
        # Get the final total from accumulate
        final = yield from accumulate(batch)
        print(f"Batch sum: {final}")

data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
list(process_batches(data, 3))
# Outputs: Batch sum: 6, Batch sum: 15, Batch sum: 24
```

---

## Coroutines: Generators as Consumers

Before `async/await`, generators were used to implement coroutines (cooperative multitasking).

### Generator-Based Coroutines

A coroutine is a generator that primarily **consumes** data rather than produces it:

```python
def coroutine(func):
    """Decorator to auto-prime coroutines"""
    def wrapper(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)  # Prime it
        return gen
    return wrapper

@coroutine
def grep(pattern):
    """Coroutine that filters lines matching pattern"""
    print(f"Looking for {pattern}")
    while True:
        line = yield  # Receive data
        if pattern in line:
            print(line)

# Usage
matcher = grep("python")
matcher.send("I love python")  # Prints: I love python
matcher.send("Java is cool")   # No output
matcher.send("Python rocks")   # Prints: Python rocks
```

### Pipeline Pattern with Coroutines

Build data processing pipelines:

```python
@coroutine
def consumer():
    """Final stage - consume data"""
    while True:
        item = yield
        print(f"Consuming: {item}")

@coroutine
def filter_stage(predicate, target):
    """Middle stage - filter and forward"""
    while True:
        item = yield
        if predicate(item):
            target.send(item)

@coroutine
def transform_stage(transform_func, target):
    """Middle stage - transform and forward"""
    while True:
        item = yield
        target.send(transform_func(item))

# Build pipeline
pipe = transform_stage(
    lambda x: x**2,
    filter_stage(
        lambda x: x % 2 == 0,
        consumer()
    )
)

# Send data through pipeline
for i in range(10):
    pipe.send(i)

# Output: 0, 4, 16, 36, 64 (evens squared)
```

### Broadcasting to Multiple Targets

```python
@coroutine
def broadcast(*targets):
    """Send received items to multiple coroutines"""
    while True:
        item = yield
        for target in targets:
            target.send(item)

# Send to multiple destinations
@coroutine
def printer(name):
    while True:
        item = yield
        print(f"{name}: {item}")

pipe = broadcast(
    printer("A"),
    printer("B"),
    printer("C")
)

pipe.send("Hello")
# Output:
# A: Hello
# B: Hello
# C: Hello
```

### Real-World Example: Log Processing

```python
import re

@coroutine
def log_parser(targets):
    """Parse log lines and route to targets"""
    pattern = re.compile(
        r'(?P<level>\w+):(?P<code>\d+) - (?P<message>.*)'
    )
    
    while True:
        line = yield
        match = pattern.match(line)
        if match:
            entry = match.groupdict()
            for target in targets:
                target.send(entry)

@coroutine
def error_filter(target):
    """Filter only ERROR level logs"""
    while True:
        entry = yield
        if entry['level'] == 'ERROR':
            target.send(entry)

@coroutine
def code_counter():
    """Count error codes"""
    counts = {}
    while True:
        entry = yield
        code = entry['code']
        counts[code] = counts.get(code, 0) + 1
        print(f"Error {code} count: {counts[code]}")

@coroutine
def alert_system():
    """Alert on critical errors"""
    while True:
        entry = yield
        if int(entry['code']) >= 500:
            print(f"🚨 CRITICAL: {entry['message']}")

# Build pipeline
pipeline = log_parser([
    error_filter(code_counter()),
    error_filter(alert_system())
])

# Send log lines
logs = [
    "INFO:200 - Request completed",
    "ERROR:404 - Page not found",
    "ERROR:500 - Internal server error",
    "ERROR:404 - Another 404",
    "ERROR:503 - Service unavailable"
]

for log in logs:
    pipeline.send(log)
```

### Coroutine State Management

Coroutines can maintain complex state:

```python
@coroutine
def moving_average(window_size):
    """Calculate moving average over window"""
    values = []
    
    while True:
        value = yield
        values.append(value)
        
        if len(values) > window_size:
            values.pop(0)
        
        avg = sum(values) / len(values)
        print(f"Value: {value}, Moving Avg: {avg:.2f}")

ma = moving_average(3)
for i in [10, 20, 30, 40, 50]:
    ma.send(i)

# Output:
# Value: 10, Moving Avg: 10.00
# Value: 20, Moving Avg: 15.00
# Value: 30, Moving Avg: 20.00
# Value: 40, Moving Avg: 30.00
# Value: 50, Moving Avg: 40.00
```

---

## Advanced Patterns

### 1. Generator Context Manager

Combine generators with context management:

```python
from contextlib import contextmanager

@contextmanager
def managed_resource(name):
    """Generator-based context manager"""
    print(f"Acquiring {name}")
    resource = {"name": name, "data": []}
    
    try:
        yield resource  # Provide resource
    except Exception as e:
        print(f"Error with {name}: {e}")
        raise
    finally:
        print(f"Releasing {name}")
        resource["data"].clear()

with managed_resource("database") as db:
    db["data"].append("some data")
    print(db)
```

### 2. Generator Chains for Lazy Evaluation

```python
def read_lines(filename):
    """Generator: read file line by line"""
    with open(filename) as f:
        for line in f:
            yield line

def strip_lines(lines):
    """Generator: strip whitespace"""
    for line in lines:
        yield line.strip()

def filter_comments(lines):
    """Generator: remove comments"""
    for line in lines:
        if not line.startswith('#'):
            yield line

def parse_json(lines):
    """Generator: parse JSON objects"""
    import json
    for line in lines:
        try:
            yield json.loads(line)
        except json.JSONDecodeError:
            continue

# Build lazy pipeline - nothing executes yet!
pipeline = parse_json(
    filter_comments(
        strip_lines(
            read_lines("data.jsonl")
        )
    )
)

# Only read/process when we iterate
for obj in pipeline:
    print(obj)  # Process one at a time, memory efficient
```

**Performance**:
- Time Complexity: O(n) - same as eager evaluation
- Space Complexity: O(1) - vs O(n) for eager
- Bonus: Can stop early without processing everything

### 3. Infinite Generators

Generators can represent infinite sequences:

```python
def fibonacci():
    """Infinite Fibonacci sequence"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

def primes():
    """Infinite prime numbers"""
    yield 2
    primes_found = [2]
    candidate = 3
    
    while True:
        is_prime = True
        for p in primes_found:
            if p * p > candidate:
                break
            if candidate % p == 0:
                is_prime = False
                break
        
        if is_prime:
            primes_found.append(candidate)
            yield candidate
        
        candidate += 2

# Use with itertools
import itertools

# First 10 Fibonacci numbers
print(list(itertools.islice(fibonacci(), 10)))

# Primes less than 100
print([p for p in itertools.takewhile(lambda x: x < 100, primes())])
```

### 4. Bidirectional Communication Pattern

```python
def task_processor():
    """Process tasks with status reporting"""
    while True:
        task = yield "ready"  # Yield status, receive task
        
        try:
            result = perform_task(task)
            response = yield f"success:{result}"
        except Exception as e:
            response = yield f"error:{e}"

processor = task_processor()
print(next(processor))  # 'ready'

result1 = processor.send({"id": 1, "action": "process"})
print(result1)  # 'success:...'

result2 = processor.send({"id": 2, "action": "process"})
print(result2)  # Next status
```

### 5. Stateful Generators for FSM (Finite State Machines)

```python
def traffic_light():
    """Traffic light state machine"""
    while True:
        # Green state
        print("🟢 GREEN")
        for _ in range(30):
            yield "green"
        
        # Yellow state
        print("🟡 YELLOW")
        for _ in range(5):
            yield "yellow"
        
        # Red state
        print("🔴 RED")
        for _ in range(35):
            yield "red"

light = traffic_light()
for _ in range(75):  # Run for 75 ticks
    state = next(light)
    # Do something based on state
```

---

## Performance Analysis

### Time Complexity

| Operation | List | Generator |
|-----------|------|-----------|
| Creation | O(n) | O(1) |
| Get first item | O(n) | O(1) |
| Get all items | O(n) | O(n) |
| Memory footprint | O(n) | O(1) |

### Real Benchmarks

```python
import time
import tracemalloc

def benchmark_memory(func, *args):
    tracemalloc.start()
    result = func(*args)
    # Force evaluation for generators
    if hasattr(result, '__iter__') and not isinstance(result, list):
        result = list(result)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak / 1024 / 1024  # MB

def benchmark_time(func, *args):
    start = time.perf_counter()
    result = func(*args)
    # Force evaluation
    if hasattr(result, '__iter__') and not isinstance(result, list):
        list(result)
    return time.perf_counter() - start

# Test functions
def list_processing(n):
    return [x**2 for x in range(n)]

def gen_processing(n):
    return (x**2 for x in range(n))

n = 10_000_000

print(f"List memory: {benchmark_memory(list_processing, n):.2f} MB")
print(f"Generator memory: {benchmark_memory(gen_processing, n):.2f} MB")

print(f"List time: {benchmark_time(list_processing, n):.4f}s")
print(f"Generator time: {benchmark_time(gen_processing, n):.4f}s")
```

### When Generators Are Slower

```python
# Scenario 1: Multiple iterations
data_list = list(range(1000))
data_gen = (x for x in range(1000))

# Fast - direct access
sum1 = sum(data_list)
sum2 = sum(data_list)  # Reuses list

# Slow - generator exhausted
sum1 = sum(data_gen)
# sum2 = sum(data_gen)  # Won't work! Generator exhausted

# Scenario 2: Random access
data_list[500]  # O(1)
# Can't do: data_gen[500]  # Not supported

# Scenario 3: Small datasets
# For n < 1000, list overhead is negligible
# Generator overhead might actually be slower
```

**Rule of Thumb**:
- **Use generators** when:
  - Data is large (> 10,000 items)
  - Single-pass iteration
  - Memory constrained
  - Infinite sequences
  
- **Use lists** when:
  - Data is small (< 1,000 items)
  - Need random access
  - Multiple iterations needed
  - Need list methods (sort, reverse, etc.)

---

## Real-World Use Cases

### 1. Processing Large Files

```python
def process_large_csv(filename):
    """Memory-efficient CSV processing"""
    import csv
    
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Process one row at a time
            if row['status'] == 'active':
                yield transform_row(row)

# Process 1GB file with constant memory
for transformed in process_large_csv('huge_data.csv'):
    save_to_database(transformed)
```

### 2. Streaming API Responses

```python
def fetch_paginated_api(url, page_size=100):
    """Generator for paginated API"""
    page = 1
    while True:
        response = requests.get(
            url,
            params={'page': page, 'size': page_size}
        )
        data = response.json()
        
        if not data:
            break
        
        for item in data:
            yield item
        
        page += 1

# Process millions of records without loading all
for record in fetch_paginated_api('https://api.example.com/data'):
    process_record(record)
```

### 3. Real-Time Data Processing

```python
import time

def sensor_readings(sensor_id, interval=1.0):
    """Simulate real-time sensor data"""
    while True:
        reading = read_sensor(sensor_id)
        yield {
            'timestamp': time.time(),
            'sensor_id': sensor_id,
            'value': reading
        }
        time.sleep(interval)

def anomaly_detector(readings, threshold=100):
    """Detect anomalies in stream"""
    window = []
    
    for reading in readings:
        window.append(reading['value'])
        if len(window) > 10:
            window.pop(0)
        
        avg = sum(window) / len(window)
        if abs(reading['value'] - avg) > threshold:
            yield reading  # Anomaly detected

# Real-time monitoring
sensor_stream = sensor_readings('SENSOR_001')
anomalies = anomaly_detector(sensor_stream)

for anomaly in anomalies:
    alert_system(anomaly)
```

### 4. Database Query Streaming

```python
def stream_database_results(query, batch_size=1000):
    """Stream large result sets"""
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(query)
    
    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        
        for row in batch:
            yield row
    
    cursor.close()
    connection.close()

# Process millions of rows efficiently
for row in stream_database_results("SELECT * FROM huge_table"):
    process_row(row)
```

### 5. ETL Pipeline

```python
def extract(source_file):
    """Extract data from source"""
    with open(source_file) as f:
        for line in f:
            yield json.loads(line)

def transform(records):
    """Transform records"""
    for record in records:
        # Complex transformations
        transformed = {
            'id': record['id'],
            'name': record['name'].upper(),
            'value': float(record['value']) * 1.1
        }
        yield transformed

def load(records, target_file):
    """Load to target"""
    with open(target_file, 'w') as f:
        for record in records:
            f.write(json.dumps(record) + '\n')
            yield record  # Allow further processing

# Lazy ETL pipeline
pipeline = load(
    transform(
        extract('source.jsonl')
    ),
    'target.jsonl'
)

# Execute pipeline
for processed in pipeline:
    print(f"Processed: {processed['id']}")
```

---

## Common Pitfalls

### 1. Forgetting Generators Are Single-Use

```python
gen = (x**2 for x in range(5))

list1 = list(gen)  # [0, 1, 4, 9, 16]
list2 = list(gen)  # [] - generator exhausted!

# Solution: Use itertools.tee for multiple iterators
import itertools
gen = (x**2 for x in range(5))
gen1, gen2 = itertools.tee(gen, 2)
```

### 2. Not Priming Coroutines

```python
def coroutine():
    while True:
        value = yield
        print(value)

gen = coroutine()
# gen.send(10)  # ❌ ERROR! Must prime first
next(gen)  # ✅ Prime it
gen.send(10)  # ✅ OK now
```

**Quick Reference**:

| Operation | Need Priming? | Correct Usage |
|-----------|---------------|---------------|
| `for x in gen` | ❌ No | Just iterate |
| `next(gen)` | ❌ No | Call directly |
| `gen.send(value)` | ✅ YES | `next(gen)` first, then `send()` |
| `list(gen)` | ❌ No | Works directly |

**Remember**: Priming = advancing to first `yield` so the generator is "waiting" for data.

### 3. Generator Object vs Generator Expression

```python
# Generator object - one instance
def my_gen():
    yield 1
    yield 2

gen = my_gen()  # Creates ONE generator

# Generator expression - creates new generator each time
gen_expr = (x for x in [1, 2])
```

### 4. Modifying Iterable During Generation

```python
data = [1, 2, 3, 4, 5]

def process(lst):
    for item in lst:
        yield item * 2
        # DON'T DO THIS:
        # lst.append(item)  # Modifying during iteration!

# Safe approach: work with copy or snapshot
def process_safe(lst):
    for item in lst[:]:  # Iterate over copy
        yield item * 2
```

### 5. Exception Handling in Generator Chains

```python
def stage1():
    try:
        for i in range(5):
            yield i
    except GeneratorExit:
        print("Stage 1 closing")

def stage2(source):
    try:
        for item in source:
            yield item * 2
    except GeneratorExit:
        print("Stage 2 closing")

pipeline = stage2(stage1())
print(next(pipeline))
print(next(pipeline))
pipeline.close()  # Both stages clean up
```

### 6. Memory Leaks with Circular References

```python
def leaky_generator():
    # Holding reference to large object
    large_data = [0] * 10_000_000
    
    def inner():
        yield from large_data
    
    return inner()  # large_data stays in memory!

# Better: Don't capture unnecessary references
def efficient_generator():
    def inner(data):
        yield from data
    
    large_data = [0] * 10_000_000
    return inner(large_data)
```

---

## From Generators to async/await

Generator-based coroutines were the foundation for `async/await`:

### The Evolution

```python
# Old style: Generator-based coroutines (Python 3.4)
@asyncio.coroutine
def old_style():
    result = yield from some_async_operation()
    return result

# New style: Native coroutines (Python 3.5+)
async def new_style():
    result = await some_async_operation()
    return result
```

### Key Differences

| Feature | Generator Coroutines | async/await |
|---------|---------------------|-------------|
| Syntax | `yield from` | `await` |
| Declaration | `@coroutine` + `def` | `async def` |
| Protocol | Generator protocol | Coroutine protocol |
| Type checking | Harder | Better support |
| Mixing | Can mix with generators | Separated |

### When to Use Each

**Generator-based coroutines** (legacy):
- Maintaining old codebases
- Understanding historical context
- Learning foundations

**async/await** (modern):
- All new async code
- Better readability
- Type checking support
- Future-proof

### The Connection

```python
# Under the hood, async/await uses similar state machine
async def async_func():
    await something()

# Roughly equivalent to:
def async_func_desugar():
    yield from something()
```

**Key Insight**: Generators taught Python how to pause and resume function execution, which enabled async/await.

---

## Advanced Topics for Further Study

### 1. Generator-Based Parser Combinators

Building parsers using generator composition.

### 2. Asynchronous Generators (async def + yield)

```python
async def async_generator():
    for i in range(10):
        await asyncio.sleep(0.1)
        yield i
```

### 3. Generator Send/Receive Patterns

Complex state machines with bidirectional communication.

### 4. Generator Performance Optimization

- Using Cython for generator hotspots
- Profiling generator overhead
- When to use `yield` vs `return`

### 5. Generator Testing Strategies

- Mocking generators
- Testing state transitions
- Ensuring cleanup in failure scenarios

---

## Summary

### Key Takeaways

1. **Generators are lazy iterators** - O(1) space complexity
2. **`yield` pauses execution** - maintains function state
3. **Generators can receive data** via `send()` - bidirectional communication
4. **`yield from` delegates** - proper protocol forwarding
5. **Generator coroutines** - foundation for async/await
6. **Use for large data** - streaming, pipelines, infinite sequences

### Decision Matrix

**Choose Generators When**:
- ✅ Large datasets (memory constraint)
- ✅ Single-pass iteration
- ✅ Stream processing
- ✅ Pipeline composition
- ✅ Infinite sequences
- ✅ Stateful iteration

**Choose Lists When**:
- ✅ Small datasets (< 1000 items)
- ✅ Multiple iterations
- ✅ Random access needed
- ✅ Need list methods
- ✅ Serialization required
- ✅ Debugging (easier to inspect)

### Performance Rules

- **Space**: Generator = O(1), List = O(n)
- **Time**: Usually similar, but generators have per-call overhead
- **Creation**: Generator = O(1), List = O(n)
- **Break-even**: Around 10,000 items for memory-constrained environments

---

## References and Further Reading

- **PEP 255** - Simple Generators
- **PEP 342** - Coroutines via Enhanced Generators (send/throw)
- **PEP 380** - Syntax for Delegating to a Subgenerator (yield from)
- **PEP 525** - Asynchronous Generators
- **Book**: "Fluent Python" by Luciano Ramalho - Chapter 14, 16
- **Book**: "Python Cookbook" by David Beazley - Chapter 4
- **Talk**: "A Curious Course on Coroutines and Concurrency" by David Beazley

---

**Last Updated**: 2025-11-12  
**Next Deep Dive**: Decorators and Metaprogramming

