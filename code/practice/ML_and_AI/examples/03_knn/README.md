# K-Nearest Neighbors (KNN)

Instance-based learning for classification and regression.

## Concepts Covered

- **Distance Metrics**: Euclidean, Manhattan, Cosine
- **K Selection**: Choosing optimal number of neighbors
- **Weighted KNN**: Distance-weighted voting
- **Curse of Dimensionality**: High-dim challenges

## The Math

### Euclidean Distance
```
d(x, y) = √(Σ(xᵢ - yᵢ)²)
```

### Manhattan Distance
```
d(x, y) = Σ|xᵢ - yᵢ|
```

### Prediction (Classification)
```
ŷ = mode(y of k nearest neighbors)
```

## Usage

```bash
python train.py
python train.py --k 5 --metric euclidean
python inference.py
```

## Key Takeaways

1. **Feature Scaling**: Essential for distance-based methods
2. **K Value**: Odd numbers avoid ties, larger K = smoother boundaries
3. **Curse of Dimensionality**: Performance degrades in high dimensions
4. **No Training**: All computation at prediction time (lazy learner)
