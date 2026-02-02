# K-Means Clustering

Partition data into K clusters by minimizing within-cluster variance.

## Concepts Covered

- **Centroid**: Cluster center point
- **Inertia**: Within-cluster sum of squares
- **Elbow Method**: Finding optimal K
- **Silhouette Score**: Cluster quality metric

## Algorithm

1. Initialize K random centroids
2. Assign each point to nearest centroid
3. Update centroids as mean of assigned points
4. Repeat until convergence

## The Math

### Objective
```
argmin_C Σ Σ ||xᵢ - μⱼ||²
```

### Silhouette Score
```
s(i) = (b(i) - a(i)) / max(a(i), b(i))
```
Where a(i) = intra-cluster distance, b(i) = nearest-cluster distance

## Usage

```bash
python train.py
python train.py --k 3
python inference.py
```

## Key Takeaways

1. **K Selection**: Use elbow method or silhouette score
2. **Initialization**: K-means++ is more robust
3. **Scaling**: Essential before clustering
4. **Limitations**: Assumes spherical clusters of similar size
