# Exercise: Video Transcoding Pipeline

## Objective
Design a video transcoding pipeline.

## Requirements
- 1000 hours uploaded/day
- Multiple output qualities (240p to 4K)
- < 2 hour processing time
- Cost-efficient

## Tasks

### Task 1: Pipeline Design
Design the transcoding workflow:
```
Upload → ___ → ___ → ___ → Ready
```

### Task 2: Parallelization
How to speed up transcoding?
- Chunking strategy: ___
- Worker scaling: ___

### Task 3: Quality Profiles
Define encoding profiles:
| Quality | Resolution | Bitrate | Use Case |
|---------|------------|---------|----------|
| 240p | | | |
| 480p | | | |
| 720p | | | |
| 1080p | | | |

---

<details>
<summary>Solution</summary>

**Pipeline:** Upload → Chunk (10s segments) → Parallel encode per quality → Merge → Package HLS.

**Parallelization:** Split into 10-second chunks, encode each independently, merge at end.

</details>
