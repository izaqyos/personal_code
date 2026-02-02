# Exercise: Search Indexing Pipeline

## Objective
Design a document indexing pipeline.

## Requirements
- 10M documents
- Real-time indexing (< 1 minute)
- Full-text search
- Faceted search

## Tasks

### Task 1: Pipeline Design
Design the indexing flow:
```
Document → ___ → ___ → ___ → Searchable
```

### Task 2: Schema Design
Design Elasticsearch mapping for e-commerce products:
```json
{
  "mappings": {
    "properties": {
      // TODO
    }
  }
}
```

### Task 3: Near Real-Time
How to achieve < 1 minute indexing latency?
- Refresh interval: ___
- Bulk indexing: ___
- Trade-offs: ___

---

<details>
<summary>Solution</summary>

**Pipeline:** Document → Queue → Enrichment (NLP) → Tokenization → Index.

**Mapping:** text fields for search, keyword for filters, nested for variants.

**NRT:** 30-second refresh, bulk API for batch, trade search freshness vs performance.

</details>
