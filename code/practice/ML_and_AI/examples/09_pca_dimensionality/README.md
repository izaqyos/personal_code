# Principal Component Analysis (PCA)

Dimensionality reduction through linear transformation.

## Concepts Covered

- **Principal Components**: Directions of maximum variance
- **Explained Variance**: How much info each component captures
- **Dimensionality Reduction**: Fewer features, retain information
- **Data Visualization**: Project to 2D/3D

## The Math

### Covariance Matrix
```
C = (1/n) XᵀX
```

### Eigendecomposition
```
Cv = λv
```
Where v = eigenvector (principal component), λ = eigenvalue (variance)

## Usage

```bash
python train.py
python train.py --n-components 2
python inference.py
```

## Key Takeaways

1. **Centering**: Data must be centered (mean subtracted)
2. **Scaling**: Often beneficial before PCA
3. **Explained Variance**: Cumulative sum shows info retained
4. **Components**: Ordered by variance explained
