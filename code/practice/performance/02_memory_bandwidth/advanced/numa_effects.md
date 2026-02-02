# NUMA Effects - Advanced

Understanding Non-Uniform Memory Access in multi-socket systems.

## Learning Objectives
- Understand NUMA architecture impact
- Calculate NUMA penalty for remote access
- Design NUMA-aware data placement

## Background

### NUMA Architecture
```
┌─────────────────┐         ┌─────────────────┐
│     CPU 0       │◄───────►│     CPU 1       │
│  (8 cores)      │  QPI/UPI│  (8 cores)      │
└────────┬────────┘         └────────┬────────┘
         │                           │
    ┌────▼────┐                 ┌────▼────┐
    │Memory 0 │                 │Memory 1 │
    │ (64 GB) │                 │ (64 GB) │
    └─────────┘                 └─────────┘
```

### Key Values
| Access Type | Latency | Bandwidth |
|-------------|---------|-----------|
| Local Memory | 80-100 ns | 50 GB/s |
| Remote Memory | 130-180 ns | 25-35 GB/s |
| Cross-socket Ratio | 1.5-2x slower | 0.5-0.7x bandwidth |

---

## Exercise 1: NUMA Latency Impact

**Question:** A thread on Socket 0 accesses data:
- 70% of accesses: Local memory (Socket 0)
- 30% of accesses: Remote memory (Socket 1)

Local latency: 100 ns
Remote latency: 160 ns

Calculate average memory latency and compare to all-local.

**Your Answer:**
```
Average latency = ?
All-local latency = ?
NUMA penalty = ?
```

<details>
<summary>Solution</summary>

```
Average Latency:
  Local: 70% × 100 ns = 70 ns
  Remote: 30% × 160 ns = 48 ns
  Total: 70 + 48 = 118 ns

All-Local Latency: 100 ns

NUMA Penalty: 118 / 100 = 18% slower

For 1 billion memory accesses:
  With NUMA: 1B × 118 ns = 118 seconds
  All local: 1B × 100 ns = 100 seconds
  
Time lost: 18 seconds due to poor placement
```
</details>

---

## Exercise 2: Bandwidth Analysis

**Question:** Multi-threaded application on 2-socket server:
- Each socket: 4 threads processing data
- Total data: 20 GB (10 GB per socket, ideally)
- Current: All data on Socket 0

Calculate throughput difference:
- NUMA-aware: Each socket accesses local data
- NUMA-unaware: Socket 1 threads access Socket 0 memory

Local bandwidth: 50 GB/s per socket
Remote bandwidth: 30 GB/s (cross-socket)

**Your Answer:**
```
NUMA-aware aggregate bandwidth = ?
NUMA-unaware aggregate bandwidth = ?
Performance difference = ?
```

<details>
<summary>Solution</summary>

```
NUMA-Aware (Optimal):
  Socket 0: 10 GB at 50 GB/s = 200 ms
  Socket 1: 10 GB at 50 GB/s = 200 ms
  (Parallel) Total time: 200 ms
  Aggregate bandwidth: 20 GB / 0.2 s = 100 GB/s

NUMA-Unaware (All on Socket 0):
  Socket 0 threads: 50 GB/s
  Socket 1 threads: 30 GB/s (remote)
  Combined: ~80 GB/s (but contention!)
  
  Actually worse due to:
  - Remote access contention
  - Memory controller saturation
  Realistic: ~50-60 GB/s
  
  Time: 20 GB / 50 GB/s = 400 ms

Performance Difference: 
  NUMA-aware: 200 ms
  NUMA-unaware: 400 ms
  Slowdown: 2x slower without NUMA awareness!
```
</details>

---

## Exercise 3: First-Touch Policy

**Question:** Memory is allocated on the NUMA node where it's first accessed (first-touch policy).

```cpp
// Thread on Socket 0 initializes
float* data = malloc(8 GB);
for (int i = 0; i < N; i++) {
    data[i] = 0;  // First touch → Socket 0
}

// Later: Thread on Socket 1 processes
// All accesses are now remote!
for (int i = 0; i < N; i++) {
    process(data[i]);  // Remote access
}
```

How to fix this pattern?

**Your Answer:**
```
Problem = ?
Solution = ?
Time improvement = ?
```

<details>
<summary>Solution</summary>

```
Problem:
  - Initialization on Socket 0
  - All data pages allocated on Socket 0
  - Socket 1 processing pays remote penalty for ALL accesses

Solution - Parallel First Touch:
```cpp
// Parallel initialization
#pragma omp parallel for
for (int i = 0; i < N; i++) {
    data[i] = 0;  // Each thread touches its portion
}

// Each thread's data allocated on its local NUMA node
// Later processing is local
```

Alternative - Interleaved Allocation:
```cpp
// Distribute pages round-robin across nodes
numa_set_interleave_mask(numa_all_nodes_ptr);
float* data = malloc(8 GB);
```

Time Improvement:
  Remote: 160 ns × 1B = 160 seconds
  Local: 100 ns × 1B = 100 seconds
  Savings: 60 seconds (37% faster)
```
</details>

---

## Exercise 4: NUMA-Aware Thread Placement

**Question:** 16-core server with 2 sockets (8 cores each).
Application has 4 independent tasks, each needs 10 GB data.

Compare scheduling strategies:
1. All 4 tasks on Socket 0
2. 2 tasks per socket, data co-located

Memory per socket: 64 GB
Bandwidth per socket: 50 GB/s local

**Your Answer:**
```
Strategy 1 (all on Socket 0):
  Data placement = ?
  Bandwidth available = ?
  Time for all tasks = ?

Strategy 2 (distributed):
  Data placement = ?
  Bandwidth available = ?
  Time for all tasks = ?
```

<details>
<summary>Solution</summary>

```
Strategy 1 (All on Socket 0):
  Data: 40 GB on Socket 0
  Bandwidth: 50 GB/s (saturated)
  All 4 tasks share bandwidth
  Per-task bandwidth: 50 / 4 = 12.5 GB/s
  Time: 10 GB / 12.5 GB/s = 800 ms per task
  
  All tasks compete → Slowest task: 800 ms

Strategy 2 (2 per Socket):
  Socket 0: 2 tasks, 20 GB local data
  Socket 1: 2 tasks, 20 GB local data
  
  Each socket bandwidth: 50 GB/s
  Per-task bandwidth: 50 / 2 = 25 GB/s
  Time: 10 GB / 25 GB/s = 400 ms per task

Improvement: 2x faster with proper NUMA placement

Additional benefit: 
  - No cross-socket traffic
  - Better cache utilization (fewer cores sharing)
```
</details>

---

## Exercise 5: Database NUMA Optimization

**Question:** Database with:
- Table data: 100 GB (read-mostly)
- Index: 10 GB (very hot)
- Write buffer: 1 GB (write-intensive)

2-socket server, 64 GB per socket.

Design NUMA placement strategy:

**Your Answer:**
```
Socket 0 allocation = ?
Socket 1 allocation = ?
Query thread placement = ?
Write thread placement = ?
```

<details>
<summary>Solution</summary>

```
Optimal Placement:

Socket 0:
  - Write buffer: 1 GB (write-intensive, keep local)
  - Index copy 1: 10 GB
  - Table data pages: 50 GB

Socket 1:
  - Index copy 2: 10 GB (replicated for local access)
  - Table data pages: 50 GB

Thread Placement:
  - Write threads: Pinned to Socket 0 (near write buffer)
  - Query threads: Distributed based on data access
  - Index scans: Either socket (index replicated)

Benefits:
  - Writes always local (1 GB × many writes = significant)
  - Index reads local (hot path optimized)
  - Table scans parallel across sockets

Cost:
  - 10 GB memory for index replication
  - Synchronization for index updates

Trade-off: Worth it if index is accessed frequently.
20 GB index vs 100% local access for hot data.
```
</details>

---

## Exercise 6: NUMA Detection and Profiling

**Question:** An application runs 40% slower than expected on a 2-socket server. How to diagnose NUMA issues?

**Your Answer:**
```
Diagnostic steps = ?
Key metrics to check = ?
Expected findings = ?
```

<details>
<summary>Solution</summary>

```
Diagnostic Steps:

1. Check NUMA topology:
   $ numactl --hardware
   $ lscpu | grep NUMA

2. Profile memory access patterns:
   $ perf stat -e \
       numa_hit,numa_miss,numa_foreign \
       ./application

3. Check memory placement:
   $ numastat -p <pid>
   
4. Monitor cross-socket traffic:
   $ perf stat -e \
       offcore_response.demand_data_rd.l3_miss.any_snoop \
       ./application

Key Metrics:
  - numa_miss / numa_hit ratio > 0.1 = problem
  - Remote memory % > 20% = investigate
  - UPI/QPI utilization > 50% = cross-socket bottleneck

Expected Findings for 40% Slowdown:
  - High numa_miss rate (>30%)
  - First-touch on wrong socket
  - Threads migrating between sockets
  - Large remote memory allocation

Fixes:
  - numactl --membind=<node> ./application
  - Parallel first-touch initialization
  - Thread pinning: taskset or pthread_setaffinity
  - Interleaved allocation for shared data
```
</details>

---

## Key Takeaways

1. **Remote memory is 1.5-2x slower** in latency and bandwidth
2. **First-touch policy** determines placement - initialize carefully
3. **Thread-data affinity** is critical for performance
4. **Replicate read-only hot data** if memory allows
5. **Profile with numastat and perf** to detect issues

## NUMA Optimization Checklist
```
□ Check system topology (numactl --hardware)
□ Initialize data in parallel (first-touch)
□ Pin threads to NUMA nodes (taskset/numactl)
□ Co-locate threads with their data
□ Consider replicating hot read-only data
□ Monitor with numastat during runtime
```

## Next Steps
- Try [Disk I/O Performance](../../03_disk_io/beginner/disk_basics.md)
- Learn about [Platform Comparison](../../07_platform_comparison/beginner/x86_vs_arm.md)
