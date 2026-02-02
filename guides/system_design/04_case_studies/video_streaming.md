# Video Streaming Design

Design a video streaming platform like Netflix or YouTube.

## Requirements

### Functional Requirements
- Upload videos
- Stream videos
- Search videos
- Recommendations
- Comments, likes, subscriptions
- Video analytics (views, watch time)

### Non-Functional Requirements
- Low latency video start (< 2s)
- Adaptive bitrate (handle network changes)
- High availability (99.9%)
- Global distribution
- Scale: 1B daily views, 500 hours uploaded/minute

## Capacity Estimation

### Traffic
```
Daily views: 1B
Average view duration: 5 minutes
Peak concurrent viewers: 10M

Uploads: 500 hours/minute = 30,000 hours/day
```

### Storage
```
Video storage (after encoding):
  - 1 hour video ≈ 3 GB (multiple qualities)
  - Daily: 30,000 hours × 3 GB = 90 PB/day
  - Yearly: 90 PB × 365 = 33 EB

With replication (3x): 100 EB/year
```

### Bandwidth
```
Streaming:
  - 10M concurrent × 5 Mbps average = 50 Tbps
  
Upload processing:
  - 500 hours/min × 1 GB/hour = 8.3 GB/min = 1.1 Gbps
```

## High-Level Design

```
                    ┌─────────────────────────────────────┐
                    │            CDN Network              │
                    │  (Edge locations worldwide)         │
                    └─────────────────┬───────────────────┘
                                      │
                    ┌─────────────────┴───────────────────┐
                    │           Origin Servers            │
                    └─────────────────┬───────────────────┘
                                      │
┌─────────────────┐     ┌─────────────┴─────────────┐
│  Upload Path    │     │      Streaming Path       │
│                 │     │                           │
│  ┌───────────┐  │     │  ┌──────────────────┐   │
│  │ Ingestion │  │     │  │  Video Metadata  │   │
│  │  Service  │  │     │  │     Service      │   │
│  └─────┬─────┘  │     │  └──────────────────┘   │
│        │        │     │                           │
│  ┌─────▼─────┐  │     │  ┌──────────────────┐   │
│  │Transcoding│  │     │  │  Recommendation  │   │
│  │  Pipeline │  │     │  │     Service      │   │
│  └─────┬─────┘  │     │  └──────────────────┘   │
│        │        │     │                           │
│  ┌─────▼─────┐  │     └───────────────────────────┘
│  │  Storage  │  │
│  │  (S3/GCS) │  │
│  └───────────┘  │
└─────────────────┘
```

## Video Upload Pipeline

### Upload Flow

```
1. Client → API: Request upload URL
2. API → Storage: Generate signed URL
3. Client → Storage: Upload video directly
4. Storage → Queue: Trigger processing
5. Transcoding → Multiple qualities
6. Storage: Store transcoded videos
7. Metadata: Update video status
```

### Chunked Upload

```python
class UploadService:
    CHUNK_SIZE = 5 * 1024 * 1024  # 5 MB
    
    def initiate_upload(self, user_id, video_metadata):
        upload_id = generate_upload_id()
        
        # Store upload session
        redis.set(f"upload:{upload_id}", {
            "user_id": user_id,
            "metadata": video_metadata,
            "chunks": [],
            "status": "in_progress"
        })
        
        return upload_id
    
    def upload_chunk(self, upload_id, chunk_number, chunk_data):
        # Upload chunk to object storage
        key = f"uploads/{upload_id}/chunk_{chunk_number}"
        storage.upload(key, chunk_data)
        
        # Track chunk
        session = redis.get(f"upload:{upload_id}")
        session["chunks"].append(chunk_number)
        redis.set(f"upload:{upload_id}", session)
    
    def complete_upload(self, upload_id):
        session = redis.get(f"upload:{upload_id}")
        
        # Combine chunks
        chunks = sorted(session["chunks"])
        combined_key = f"videos/raw/{upload_id}"
        storage.combine_chunks(upload_id, chunks, combined_key)
        
        # Trigger processing
        queue.publish("video_processing", {
            "video_id": upload_id,
            "source_key": combined_key
        })
```

## Video Transcoding

### Transcoding Pipeline

```
Raw Video ─────────────────────────────────────────────────────
     │
     ▼
┌──────────────────────────────────────────────────────────────┐
│                     Transcoding Pipeline                      │
│                                                              │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐ │
│  │ Extract  │ → │ Encode   │ → │ Package  │ → │  Upload  │ │
│  │ Metadata │   │ Multiple │   │ HLS/DASH │   │  to CDN  │ │
│  │          │   │ Qualities│   │          │   │          │ │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘ │
│                       │                                      │
│          ┌────────────┼────────────┐                        │
│          ▼            ▼            ▼                        │
│       240p         720p         1080p                       │
│       360p         1080p        4K                          │
│       480p                                                  │
└──────────────────────────────────────────────────────────────┘
```

### Encoding Profiles

```yaml
profiles:
  - name: 240p
    width: 426
    height: 240
    bitrate: 300k
    
  - name: 480p
    width: 854
    height: 480
    bitrate: 1000k
    
  - name: 720p
    width: 1280
    height: 720
    bitrate: 2500k
    
  - name: 1080p
    width: 1920
    height: 1080
    bitrate: 5000k
    
  - name: 4k
    width: 3840
    height: 2160
    bitrate: 15000k
```

### DAG (Directed Acyclic Graph) Processing

```
                    ┌─────────────┐
                    │   Raw Video │
                    └──────┬──────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │Audio Only│    │  Video   │    │Thumbnails│
    └────┬─────┘    │Extraction│    └────┬─────┘
         │          └────┬─────┘         │
         │               │               │
         │    ┌──────────┼──────────┐    │
         │    ▼          ▼          ▼    │
         │ ┌─────┐   ┌─────┐   ┌─────┐  │
         │ │ 480p│   │ 720p│   │1080p│  │
         │ └──┬──┘   └──┬──┘   └──┬──┘  │
         │    │         │         │     │
         └────┼─────────┼─────────┼─────┘
              │         │         │
              ▼         ▼         ▼
         ┌────────────────────────────┐
         │       HLS Packaging        │
         └────────────────────────────┘
```

## Adaptive Bitrate Streaming

### HLS (HTTP Live Streaming)

```
Master Playlist (master.m3u8):
┌─────────────────────────────────────────┐
│ #EXTM3U                                 │
│ #EXT-X-STREAM-INF:BANDWIDTH=300000      │
│ 240p/playlist.m3u8                      │
│ #EXT-X-STREAM-INF:BANDWIDTH=1000000     │
│ 480p/playlist.m3u8                      │
│ #EXT-X-STREAM-INF:BANDWIDTH=2500000     │
│ 720p/playlist.m3u8                      │
│ #EXT-X-STREAM-INF:BANDWIDTH=5000000     │
│ 1080p/playlist.m3u8                     │
└─────────────────────────────────────────┘

Quality Playlist (720p/playlist.m3u8):
┌─────────────────────────────────────────┐
│ #EXTM3U                                 │
│ #EXT-X-TARGETDURATION:10               │
│ #EXTINF:10.0,                          │
│ segment_0.ts                           │
│ #EXTINF:10.0,                          │
│ segment_1.ts                           │
│ #EXTINF:10.0,                          │
│ segment_2.ts                           │
│ ...                                    │
└─────────────────────────────────────────┘
```

### Player Adaptation Logic

```javascript
class AdaptivePlayer {
    selectQuality() {
        const bandwidth = this.measureBandwidth();
        const bufferHealth = this.getBufferHealth();
        
        // Find highest quality that fits bandwidth
        const targetBitrate = bandwidth * 0.8; // 80% margin
        
        const qualities = this.qualities.filter(
            q => q.bitrate < targetBitrate
        );
        
        if (bufferHealth < 0.5) {
            // Low buffer - be conservative
            return qualities[0];
        }
        
        return qualities[qualities.length - 1];
    }
}
```

## CDN Strategy

### Multi-Tier CDN

```
User ──> Edge (PoP) ──> Regional ──> Origin
             │
        Cache Hit?
           Yes → Return
           No  → Fetch from Regional
```

### Cache Strategy

```yaml
caching:
  manifest:
    ttl: 5  # seconds (for live content)
    
  segments:
    ttl: 31536000  # 1 year (immutable)
    
  thumbnails:
    ttl: 86400  # 1 day
```

### Pre-warming Popular Content

```python
def prewarm_trending_videos():
    trending = get_trending_videos()
    
    for video in trending:
        for edge_location in cdn.get_all_edges():
            cdn.prewarm(edge_location, video.url)
```

## Database Design

### Videos Table

```sql
CREATE TABLE videos (
    video_id UUID PRIMARY KEY,
    user_id UUID,
    title VARCHAR(200),
    description TEXT,
    duration_seconds INT,
    status VARCHAR(20),  -- 'processing', 'ready', 'failed'
    upload_date TIMESTAMP,
    view_count BIGINT DEFAULT 0,
    like_count BIGINT DEFAULT 0
);
```

### Video Metadata (for playback)

```json
{
  "video_id": "abc123",
  "master_playlist": "https://cdn.example.com/videos/abc123/master.m3u8",
  "thumbnails": {
    "default": "https://cdn.example.com/videos/abc123/thumb.jpg",
    "sprite": "https://cdn.example.com/videos/abc123/sprite.jpg"
  },
  "qualities": [
    {"quality": "240p", "bitrate": 300000},
    {"quality": "720p", "bitrate": 2500000},
    {"quality": "1080p", "bitrate": 5000000}
  ],
  "subtitles": [
    {"language": "en", "url": "..."},
    {"language": "es", "url": "..."}
  ]
}
```

## Recommendations

### Recommendation Pipeline

```
User Activity ──> Feature Store ──> ML Model ──> Recommendations
     │                                   │
     ▼                                   ▼
Event Stream                      Personalized
(Kafka)                           Video List
```

### Features Used

- Watch history
- Search history
- Demographics
- Video metadata (category, tags)
- Social signals (friends watching)
- Time of day

## Analytics

### View Counting

```python
# Approximate count using probabilistic data structure
class ViewCounter:
    def __init__(self):
        self.redis = Redis()
    
    def record_view(self, video_id, user_id):
        # HyperLogLog for unique viewers
        self.redis.pfadd(f"views:unique:{video_id}", user_id)
        
        # Simple counter for total views
        self.redis.incr(f"views:total:{video_id}")
    
    def get_view_count(self, video_id):
        return self.redis.get(f"views:total:{video_id}")
    
    def get_unique_viewers(self, video_id):
        return self.redis.pfcount(f"views:unique:{video_id}")
```

### Watch Time Tracking

```python
def track_watch_session(video_id, user_id, events):
    """
    events: [(timestamp, position), ...]
    """
    total_watch_time = 0
    last_pos = 0
    
    for timestamp, position in events:
        if position > last_pos:
            total_watch_time += position - last_pos
        last_pos = position
    
    analytics.record({
        "video_id": video_id,
        "user_id": user_id,
        "watch_time": total_watch_time
    })
```

## Trade-offs

| Decision | Trade-off |
|----------|-----------|
| HLS vs DASH | Compatibility vs features |
| Segment duration | Startup time vs adaptability |
| Encoding profiles | Storage cost vs quality range |
| CDN tiers | Cost vs latency |

## Interview Tips

1. Start with capacity estimation
2. Separate upload and streaming paths
3. Explain transcoding pipeline and qualities
4. Detail adaptive bitrate streaming
5. Discuss CDN strategy for global distribution
6. Address video analytics challenges

## Related Topics

- [CDN](../02_building_blocks/cdn.md)
- [Message Queues](../02_building_blocks/message_queues.md)
- [Databases](../02_building_blocks/databases.md)
