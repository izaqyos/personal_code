# Performance Knowledge Base

Understanding hardware and software performance fundamentals for system design and optimization.

## Contents

### [01. Hardware Fundamentals](01_hardware_fundamentals/)
Core hardware concepts that affect performance.

- [CPU Architecture](01_hardware_fundamentals/cpu_architecture.md) - Cores, clock speed, pipelines, IPC
- [Cache Hierarchy](01_hardware_fundamentals/cache_hierarchy.md) - L1/L2/L3 caches, cache lines, locality
- [Memory](01_hardware_fundamentals/memory.md) - DDR4/DDR5, bandwidth, latency
- [Storage](01_hardware_fundamentals/storage.md) - SSD vs HDD, NVMe, IOPS, sequential vs random
- [Network](01_hardware_fundamentals/network.md) - Latency, bandwidth, RTT, TCP/UDP

### [02. Software Fundamentals](02_software_fundamentals/)
Software-level performance considerations.

- [Big-O to Wall Clock](02_software_fundamentals/bigO_to_wallclock.md) - Converting complexity to real time
- [Constant Factors](02_software_fundamentals/constant_factors.md) - Why O(n) != O(n)
- [Memory Management](02_software_fundamentals/memory_management.md) - Allocation, GC, memory pools
- [Concurrency](02_software_fundamentals/concurrency.md) - Threading overhead, locks, contention
- [I/O Patterns](02_software_fundamentals/io_patterns.md) - Blocking vs async, buffering

### [03. Benchmarking](03_benchmarking/)
Measuring and analyzing performance.

- [Profiling Tools](03_benchmarking/profiling_tools.md) - perf, flamegraphs, Instruments
- [Microbenchmarks](03_benchmarking/microbenchmarks.md) - Pitfalls, methodology
- [Load Testing](03_benchmarking/load_testing.md) - wrk, k6, JMeter
- [Latency Numbers](03_benchmarking/latency_numbers.md) - Numbers every programmer should know

## Key Numbers to Memorize

### Latency Reference (2024)
| Operation | Time |
|-----------|------|
| L1 cache reference | 1 ns |
| L2 cache reference | 4 ns |
| L3 cache reference | 12 ns |
| Main memory reference | 100 ns |
| SSD random read | 16 μs |
| SSD sequential read (1 MB) | 250 μs |
| HDD seek | 4 ms |
| Round trip same datacenter | 0.5 ms |
| Round trip cross-continent | 150 ms |

### Throughput Reference
| Resource | Throughput |
|----------|------------|
| DDR5 memory bandwidth | ~50 GB/s |
| NVMe SSD sequential | ~7 GB/s |
| 10 Gbps network | 1.25 GB/s |
| SATA SSD | ~550 MB/s |

### CPU Comparison (Approximate)
| Platform | Single-core Performance |
|----------|------------------------|
| Intel i9-13900K | ~3.0 GHz effective |
| Apple M4 Pro | ~3.5 GHz effective |
| AWS c7g (Graviton3) | ~2.6 GHz effective |

## Learning Path

| Week | Focus | Topics |
|------|-------|--------|
| 1 | Hardware I | CPU, Cache |
| 2 | Hardware II | Memory, Storage, Network |
| 3 | Software | Algorithms, Memory, I/O |
| 4 | Benchmarking | Tools, Methodology |

## Related Resources

- [Practice Exercises](../../code/practice/performance/) - Calculation problems
- [System Design KB](../system_design/) - Architecture patterns

## References

- Systems Performance (Brendan Gregg)
- Computer Architecture: A Quantitative Approach (Hennessy & Patterson)
- What Every Programmer Should Know About Memory (Drepper)
