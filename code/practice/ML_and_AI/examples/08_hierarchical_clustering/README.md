# Hierarchical Clustering

Build a hierarchy of clusters using agglomerative (bottom-up) approach.

## Concepts Covered

- **Dendrogram**: Tree visualization of cluster hierarchy
- **Linkage Methods**: Single, Complete, Average, Ward
- **Distance Matrix**: Pairwise distances between points
- **Cutting the Tree**: Choose number of clusters

## Linkage Methods

- **Single**: Min distance between clusters
- **Complete**: Max distance between clusters
- **Average**: Mean distance between clusters
- **Ward**: Minimizes within-cluster variance

## Usage

```bash
python train.py
python train.py --n-clusters 3 --linkage ward
python inference.py
```

## Key Takeaways

1. **No K Required Initially**: Explore dendrogram first
2. **Linkage Matters**: Ward works best for compact clusters
3. **Dendrogram**: Visual tool for choosing cluster count
4. **Not Scalable**: O(n²) or worse for large datasets
