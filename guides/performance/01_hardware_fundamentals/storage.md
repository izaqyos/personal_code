# Storage Performance

Understanding disk I/O for performance estimation.

## Storage Types Comparison

| Storage | Random Read | Sequential Read | Random Write | Sequential Write |
|---------|-------------|-----------------|--------------|------------------|
| HDD | 0.1-1 MB/s | 100-200 MB/s | 0.1-1 MB/s | 100-200 MB/s |
| SATA SSD | 50-100 MB/s | 500-550 MB/s | 50-100 MB/s | 500-550 MB/s |
| NVMe SSD | 100-500 MB/s | 3-7 GB/s | 100-400 MB/s | 3-7 GB/s |
| Optane | 300+ MB/s | 2.5 GB/s | 300+ MB/s | 2.5 GB/s |

## Key Metrics

### IOPS (I/O Operations Per Second)
```
HDD: 100-200 IOPS
SATA SSD: 50,000-100,000 IOPS
NVMe SSD: 100,000-1,000,000 IOPS
```

### Latency
```
HDD seek: 4-10 ms
SATA SSD: 100-200 μs
NVMe SSD: 10-50 μs
```

### Throughput
```
HDD: 100-200 MB/s
SATA SSD: 550 MB/s (SATA limit)
NVMe Gen4: 7 GB/s
NVMe Gen5: 14 GB/s
```

## HDD Mechanics

### Components Affecting Performance
```
Seek time: Moving head to track (~5-10 ms)
Rotational latency: Waiting for sector (~4 ms @ 7200 RPM)
Transfer time: Reading data (fast once positioned)

Total random access: ~10-15 ms
```

### Sequential vs Random
```
Sequential: 150 MB/s (head stays in place)
Random: 100 IOPS × 4 KB = 0.4 MB/s

Difference: 375x faster sequential!
```

## SSD Internals

### NAND Flash Characteristics
- Read unit: Page (4-16 KB)
- Write unit: Page
- Erase unit: Block (256-1024 pages)

### Write Amplification
```
Write 4 KB → May require erasing 1 MB block
Write amplification = 256x worst case

Mitigated by:
- Wear leveling
- Over-provisioning (extra hidden capacity)
- TRIM command
```

### SSD Durability
```
TBW (Terabytes Written):
  Consumer: 100-600 TBW
  Enterprise: 1-10 PBW

Example: 300 TBW SSD
  50 GB/day writes → 16 years
  500 GB/day writes → 1.6 years
```

## Access Patterns

### Sequential Read
Best case for all storage types.
```python
# Good: sequential file read
with open('large_file.bin', 'rb') as f:
    data = f.read()  # One sequential operation
```

### Sequential Write
```python
# Good: batch writes
with open('output.bin', 'wb') as f:
    f.write(large_buffer)  # Single write
```

### Random Read
```python
# Expensive for HDD, OK for SSD
for offset in random_offsets:
    f.seek(offset)
    data = f.read(4096)  # Random seeks
```

### Small Random Writes
```python
# Worst case: many small random writes
for i in range(100000):
    f.seek(random_offset())
    f.write(small_data)  # SSD write amplification
```

## Database Storage Considerations

### B-Tree Performance
```
Depth 4 B-tree, 1B rows:
  HDD: 4 seeks × 10 ms = 40 ms per lookup
  SSD: 4 reads × 50 μs = 200 μs per lookup
```

### Log-Structured Merge (LSM)
```
Writes: Always sequential (fast)
Reads: May check multiple levels (slower)
Good for: Write-heavy workloads
```

## Calculation Examples

### Example 1: Read Large File
```
Read 10 GB file:
  HDD: 10 GB / 150 MB/s = 67 seconds
  SATA SSD: 10 GB / 500 MB/s = 20 seconds
  NVMe: 10 GB / 5 GB/s = 2 seconds
```

### Example 2: Random Key Lookups
```
1 million random 4 KB reads:
  HDD: 1M / 100 IOPS = 10,000 seconds (2.8 hours!)
  SSD: 1M / 100K IOPS = 10 seconds
  NVMe: 1M / 500K IOPS = 2 seconds
```

### Example 3: Write Database
```
Insert 1 million rows (1 KB each):
  Random writes:
    HDD: 1M / 100 IOPS = 10,000 seconds
    SSD: 1M / 50K IOPS = 20 seconds
  
  Batched sequential:
    HDD: 1 GB / 150 MB/s = 7 seconds
    SSD: 1 GB / 500 MB/s = 2 seconds
```

## Storage Optimization

### Buffering
```python
# Bad: many small writes
for item in items:
    f.write(item)

# Good: buffer and batch
buffer = b''.join(items)
f.write(buffer)
```

### Read-Ahead
OS prefetches sequential data automatically.

### Compression
Trade CPU for I/O (often worth it):
```
1 GB compressed to 200 MB:
  Read time: 5x faster
  Decompress: ~1 second
  Net: 4x faster for HDD
```

## Quick Reference

### Time to Read/Write

| Size | HDD | SATA SSD | NVMe |
|------|-----|----------|------|
| 1 MB | 7 ms | 2 ms | 0.2 ms |
| 100 MB | 0.7 s | 0.2 s | 20 ms |
| 1 GB | 7 s | 2 s | 200 ms |
| 10 GB | 70 s | 20 s | 2 s |

### Random IOPS Comparison
```
HDD:     100 IOPS (10 ms/op)
SSD:     100,000 IOPS (10 μs/op)
NVMe:    500,000 IOPS (2 μs/op)
```

## Related Topics
- [Memory](memory.md)
- [Network](network.md)
