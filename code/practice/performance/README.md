# Performance Practice

Exercises for understanding hardware and software performance through calculation problems.

## Structure

Each topic directory contains:
- `beginner/` - Basic calculations, single concept
- `intermediate/` - Multi-factor problems, comparisons
- `advanced/` - Real-world scenarios, optimization decisions

## Topics

| # | Topic | Focus |
|---|-------|-------|
| 01 | [CPU Calculations](01_cpu_calculations/) | Cycles, instructions, clock speed |
| 02 | [Memory Bandwidth](02_memory_bandwidth/) | DDR throughput, copy times |
| 03 | [Disk I/O](03_disk_io/) | SSD/HDD, sequential vs random |
| 04 | [Network Latency](04_network_latency/) | RTT, bandwidth-delay product |
| 05 | [Cache Effects](05_cache_effects/) | Hit rates, cache line effects |
| 06 | [Algorithm Comparison](06_algorithm_comparison/) | Theory vs practice, constant factors |
| 07 | [Platform Comparison](07_platform_comparison/) | x86 vs ARM, cloud instances |
| 08 | [Real World Scenarios](08_real_world_scenarios/) | End-to-end system estimation |

## Sample Questions

### CPU
- "How long to sort 1M 64-bit integers on a 3GHz single-core CPU?"
- "Compare sorting time on Intel i9 vs Apple M4 Pro"

### Memory
- "Time to copy 1GB buffer in DDR4 vs DDR5 memory?"
- "Impact of NUMA on large array operations?"

### Disk
- "Time to read 10GB file sequentially on NVMe vs SATA SSD?"
- "Random vs sequential read: how many IOPS?"

### Network
- "RTT from NYC to London over fiber?"
- "Bandwidth-delay product for transcontinental link?"

### Cache
- "How much faster is cache-friendly array traversal?"
- "Calculate L1/L2/L3 hit rate impact on loop performance?"

### Real World
- "Time to process 10M log entries in Python vs C++?"
- "Can we handle 100K requests/second on this hardware?"

## How to Solve

1. **Identify the bottleneck** - CPU, memory, disk, or network?
2. **Gather the numbers** - Clock speed, bandwidth, latency
3. **Calculate step by step** - Show your work
4. **Sanity check** - Does the answer make sense?
5. **Consider real-world factors** - OS overhead, inefficiencies

## Reference Numbers

See [Latency Numbers](../../guides/performance/03_benchmarking/latency_numbers.md) for key figures.

## Progress Tracking

Use the [LEARNING_ROADMAP.md](LEARNING_ROADMAP.md) for a structured weekly schedule.

## Related Resources

- [Performance KB](../../../guides/performance/) - Theory and reference
- [System Design Practice](../system_design/) - Capacity estimation context
