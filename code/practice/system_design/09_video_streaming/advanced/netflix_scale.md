# Exercise: Netflix-Scale Streaming

## Objective
Design a video streaming platform for 200M subscribers.

## Requirements
- 200M subscribers
- 100M concurrent streams (peak)
- Global presence (190 countries)
- Adaptive bitrate
- Personalized recommendations
- 99.99% availability

## Tasks

### Task 1: CDN Strategy
Design content distribution:
- Number of edge locations: ___
- Cache strategy: ___
- Origin architecture: ___

### Task 2: Adaptive Streaming
Design client-side quality selection:
- How to measure bandwidth?
- When to switch quality?
- Buffer management?

### Task 3: Recommendations
High-level recommendation system design:
- Features used: ___
- Real-time vs batch: ___

### Task 4: Cost Estimation
Estimate monthly CDN cost for streaming.

---

<details>
<summary>Solution</summary>

**CDN:** 1000+ edge locations, cache popular content (20% of catalog = 80% traffic), Open Connect appliances.

**Adaptive:** Measure throughput per segment, switch with hysteresis, maintain 30-60s buffer.

**Cost:** ~$0.02/GB, 100M streams × 2GB/hour average × 2 hours = 400 PB = $8M/month.

</details>
