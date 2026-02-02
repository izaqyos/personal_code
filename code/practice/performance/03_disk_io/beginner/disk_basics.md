# Disk I/O Basics - Beginner

Understanding storage performance fundamentals.

## Learning Objectives
- Compare HDD vs SSD performance characteristics
- Calculate file read/write times
- Understand IOPS vs throughput

## Background

### Storage Comparison
| Metric | HDD | SATA SSD | NVMe SSD |
|--------|-----|----------|----------|
| Sequential Read | 150 MB/s | 550 MB/s | 3-7 GB/s |
| Sequential Write | 150 MB/s | 500 MB/s | 2-5 GB/s |
| Random IOPS | 100-200 | 50-100K | 200-500K |
| Latency | 5-10 ms | 100 μs | 20 μs |

### Key Formulas
```
Sequential Time = File Size / Throughput
Random Time = Number of Operations / IOPS
```

---

## Exercise 1: Simple File Read

**Question:** Read a 10 GB log file on different storage:
1. HDD (150 MB/s)
2. SATA SSD (500 MB/s)
3. NVMe SSD (5 GB/s)

**Your Answer:**
```
HDD time = ?
SATA SSD time = ?
NVMe SSD time = ?
```

<details>
<summary>Solution</summary>

```
HDD:
  10 GB / 150 MB/s = 10,000 MB / 150 MB/s = 67 seconds

SATA SSD:
  10 GB / 500 MB/s = 10,000 MB / 500 MB/s = 20 seconds

NVMe SSD:
  10 GB / 5,000 MB/s = 10,000 MB / 5,000 MB/s = 2 seconds

NVMe is 33x faster than HDD for large sequential reads!
```
</details>

---

## Exercise 2: Database Random Access

**Question:** Database performs 10,000 random 4 KB reads:
- HDD: 150 IOPS
- SATA SSD: 80,000 IOPS
- NVMe SSD: 400,000 IOPS

Calculate time for each storage type.

**Your Answer:**
```
HDD time = ?
SATA SSD time = ?
NVMe SSD time = ?
```

<details>
<summary>Solution</summary>

```
HDD:
  10,000 ops / 150 IOPS = 67 seconds

SATA SSD:
  10,000 ops / 80,000 IOPS = 0.125 seconds = 125 ms

NVMe SSD:
  10,000 ops / 400,000 IOPS = 0.025 seconds = 25 ms

For random access:
  HDD is 536x slower than SATA SSD
  HDD is 2,680x slower than NVMe SSD

This is why databases NEED SSDs!
```
</details>

---

## Exercise 3: Throughput vs IOPS

**Question:** Which is better for these workloads?

1. Video editing: Large file read/write
2. Database: Many small random reads
3. Log processing: Sequential large file read
4. Web server: Many small file serves

Classify each as throughput-bound or IOPS-bound.

**Your Answer:**
```
Video editing = ?
Database = ?
Log processing = ?
Web server = ?
```

<details>
<summary>Solution</summary>

```
Video Editing:
  Workload: Large sequential reads/writes
  Bound by: THROUGHPUT
  Best metric: MB/s or GB/s
  Storage: NVMe for speed, HDD OK for archives

Database:
  Workload: Random small reads/writes
  Bound by: IOPS
  Best metric: Random IOPS and latency
  Storage: Must have SSD (NVMe preferred)

Log Processing:
  Workload: Sequential reads of large files
  Bound by: THROUGHPUT
  Best metric: Sequential read MB/s
  Storage: Any SSD fine, even HDD acceptable

Web Server:
  Workload: Many small file reads (static assets)
  Bound by: IOPS (unless serving large files)
  Best metric: Random read IOPS
  Storage: SSD recommended, cache helps a lot
```
</details>

---

## Exercise 4: Practical File Operations

**Question:** Common developer operations:

1. Clone a 5 GB git repository
2. `npm install` downloading 500 MB, writing 100,000 files
3. Build project: read 1000 source files, write 500 binaries
4. Run tests: random read of test data (10,000 reads)

Calculate time difference between HDD and NVMe.

**Your Answer:**
```
Git clone: HDD = ?, NVMe = ?
npm install: HDD = ?, NVMe = ?
Build: HDD = ?, NVMe = ?
Tests: HDD = ?, NVMe = ?
```

<details>
<summary>Solution</summary>

```
Git Clone (5 GB + file creation):
  HDD: 5 GB / 150 MB/s + overhead = 35-40 seconds
  NVMe: 5 GB / 5 GB/s + overhead = 2-3 seconds

npm install (500 MB, 100K files):
  HDD: 
    Download: Network bound (not disk)
    Write 100K files: 100K / 150 IOPS = 667 seconds!
  NVMe:
    Write 100K files: 100K / 400K IOPS = 0.25 seconds
  
  Difference: HDD takes ~10 minutes, NVMe takes seconds!

Build (1000 reads, 500 writes):
  HDD: 1500 ops / 150 IOPS = 10 seconds I/O overhead
  NVMe: 1500 ops / 400K IOPS = 4 ms
  
  Difference: Significant, but compile time dominates

Tests (10K random reads):
  HDD: 10K / 150 = 67 seconds
  NVMe: 10K / 400K = 25 ms

Development Productivity:
  SSD is ESSENTIAL for development.
  npm install alone saves 10+ minutes!
```
</details>

---

## Exercise 5: File System Overhead

**Question:** Write 1 million 1 KB files vs one 1 GB file.

Storage: NVMe SSD
- Sequential write: 3 GB/s
- Random IOPS: 300,000

**Your Answer:**
```
One 1 GB file time = ?
1M x 1 KB files time = ?
Overhead factor = ?
```

<details>
<summary>Solution</summary>

```
One 1 GB File (Sequential):
  Time: 1 GB / 3 GB/s = 333 ms

1 Million 1 KB Files:
  Each file = 1 I/O operation
  Time: 1M ops / 300K IOPS = 3.3 seconds
  
  Plus file system overhead:
    - Create directory entries
    - Update metadata
    - Allocate blocks
  
  Realistic: 5-10 seconds

Overhead Factor: 10-30x slower for many small files!

Lesson: Batch small files or use archives.
tar/zip of 1M files then extract = faster than
copying 1M individual files.
```
</details>

---

## Exercise 6: Backup Time Estimation

**Question:** Backup a developer machine:
- Source: 500 GB on NVMe SSD
- Destination 1: External HDD (USB 3.0, 150 MB/s effective)
- Destination 2: Network drive (1 Gbps = 125 MB/s)
- Destination 3: Cloud storage (50 Mbps upload = 6.25 MB/s)

Calculate backup times.

**Your Answer:**
```
External HDD = ?
Network drive = ?
Cloud storage = ?
```

<details>
<summary>Solution</summary>

```
External HDD (150 MB/s):
  Time: 500 GB / 150 MB/s = 3,333 seconds = 56 minutes
  
  Note: USB 3.0 = 5 Gbps = 625 MB/s theoretical
  Real world with HDD: 100-150 MB/s

Network Drive (125 MB/s):
  Time: 500 GB / 125 MB/s = 4,000 seconds = 67 minutes
  
  Note: Gigabit ethernet is the bottleneck,
  not the NAS drive

Cloud Storage (6.25 MB/s):
  Time: 500 GB / 6.25 MB/s = 80,000 seconds = 22 hours!
  
  Note: This is why cloud backup:
  - Uses incremental backups
  - Compresses data
  - Runs continuously in background

Summary:
  Local external: ~1 hour
  Network: ~1 hour
  Cloud (full): ~1 day (but done incrementally)
```
</details>

---

## Key Takeaways

1. **HDD random access is 1000x slower** than SSD
2. **Sequential vs random** determines if IOPS or throughput matters
3. **Many small files** are much slower than one large file
4. **SSDs essential for development** - npm install, builds, tests
5. **Backup bottleneck** is usually the destination, not source

## Quick Reference
```
Read 1 GB:
  HDD: 7 seconds
  SATA SSD: 2 seconds
  NVMe: 0.2 seconds

10,000 random reads:
  HDD: 67 seconds
  SSD: 0.1 seconds
```

## Next Steps
- Try [Intermediate: I/O Patterns](../intermediate/io_patterns.md)
- Learn about [Network Performance](../../04_network_latency/beginner/network_basics.md)
