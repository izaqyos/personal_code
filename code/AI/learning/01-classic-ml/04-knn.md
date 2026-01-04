# K-Nearest Neighbors (KNN)

> Instance-based learning - classify by voting among neighbors.

---

## Overview

KNN is a non-parametric algorithm that makes predictions based on the K closest training examples.

**Key idea**: Similar inputs have similar outputs.

```
Query point: ?
K = 3

    │ ∘         ∘
    │   ∘   ?─┐
    │     ∘←──┤ 3 nearest neighbors
    │   ∘←────┘
    │ ×    ×
    │   ×
    └─────────────

Classification: Majority vote → Class ∘
Regression: Average of neighbors' values
```

---

## Algorithm

```
Training Phase:
1. Store all training data (that's it!)

Prediction Phase:
1. Calculate distance from query point to all training points
2. Select K nearest neighbors
3. Classification: Return majority class
   Regression: Return mean of neighbors' values
```

---

## Distance Metrics

### Euclidean Distance (L2)

```
d(p, q) = √(Σᵢ(pᵢ - qᵢ)²)

Most common, works well for continuous features
```

### Manhattan Distance (L1)

```
d(p, q) = Σᵢ|pᵢ - qᵢ|

Better for high-dimensional or grid-like data
```

### Minkowski Distance (Generalized)

```
d(p, q) = (Σᵢ|pᵢ - qᵢ|^p)^(1/p)

p=1: Manhattan
p=2: Euclidean
p→∞: Chebyshev (max difference)
```

### Cosine Similarity

```
similarity = (p · q) / (||p|| × ||q||)

For text/high-dimensional sparse data
```

---

## Choosing K

```
K too small (e.g., K=1):    K too large (e.g., K=n):
- High variance              - High bias
- Sensitive to noise         - Underfits
- Overfits                   - Ignores local structure

    K=1              K=5              K=50
  ┌─┬─┬─┐          ┌─────┐          ┌─────────┐
  │∘│×│∘│          │∘ ∘ ×│          │mostly ∘ │
  ├─┼─┼─┤          │∘ × ∘│          │entire   │
  │×│∘│×│          │× ∘ ×│          │region   │
  └─┴─┴─┘          └─────┘          └─────────┘
  Jagged           Smooth           Too smooth
```

**Heuristics:**
- Start with K = √n (where n = number of samples)
- Use odd K for binary classification (avoid ties)
- Cross-validate to find optimal K

---

## Weighted KNN

Give closer neighbors more influence:

```
Standard KNN: All K neighbors vote equally
Weighted KNN: Weight by 1/distance or 1/distance²

Example (K=3):
Distances: [0.1, 0.5, 1.0]
Weights:   [10,  2,   1]   (using 1/d)

Closer neighbor has 10× more influence
```

---

## Implementation

### From Scratch

```python
import numpy as np
from collections import Counter

class KNN:
    def __init__(self, k=3, metric='euclidean'):
        self.k = k
        self.metric = metric

    def fit(self, X, y):
        self.X_train = X
        self.y_train = y

    def _distance(self, x1, x2):
        if self.metric == 'euclidean':
            return np.sqrt(np.sum((x1 - x2) ** 2))
        elif self.metric == 'manhattan':
            return np.sum(np.abs(x1 - x2))

    def predict(self, X):
        return np.array([self._predict_one(x) for x in X])

    def _predict_one(self, x):
        # Calculate distances to all training points
        distances = [self._distance(x, x_train) for x_train in self.X_train]

        # Get K nearest neighbors
        k_indices = np.argsort(distances)[:self.k]
        k_labels = self.y_train[k_indices]

        # Majority vote
        most_common = Counter(k_labels).most_common(1)
        return most_common[0][0]
```

### Using scikit-learn

```python
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.preprocessing import StandardScaler

# IMPORTANT: Scale features first!
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Classification
knn = KNeighborsClassifier(n_neighbors=5, weights='distance', metric='euclidean')
knn.fit(X_train_scaled, y_train)
y_pred = knn.predict(X_test_scaled)

# Regression
knn_reg = KNeighborsRegressor(n_neighbors=5, weights='distance')
knn_reg.fit(X_train_scaled, y_train)
```

---

## The Curse of Dimensionality

KNN degrades in high dimensions:

```
In high dimensions:
1. All points become roughly equidistant
2. "Nearest" neighbor may not be meaningful
3. Need exponentially more data to maintain density

Volume of unit hypersphere:
d=2:  π ≈ 3.14
d=10: ≈ 2.55
d=100: ≈ 0.00000...

Most volume concentrates near the surface!
```

**Solutions:**
- Dimensionality reduction (PCA, t-SNE)
- Feature selection
- Use tree-based methods instead

---

## Efficient KNN: KD-Trees and Ball Trees

Naive KNN is O(n×d) per prediction. Trees speed this up:

```python
# scikit-learn automatically chooses algorithm
knn = KNeighborsClassifier(algorithm='auto')  # auto, ball_tree, kd_tree, brute

# For high dimensions, brute force may be faster
knn = KNeighborsClassifier(algorithm='brute')
```

| Algorithm | Best For | Complexity |
|-----------|----------|------------|
| Brute Force | Small n or high d | O(n×d) |
| KD-Tree | Low d (<20) | O(log n) average |
| Ball Tree | Higher d | O(log n) average |

---

## Pros and Cons

| Pros | Cons |
|------|------|
| Simple, intuitive | Slow prediction (no training) |
| No training phase | Memory-intensive (stores all data) |
| Non-linear boundaries | Sensitive to irrelevant features |
| Works for multi-class | Curse of dimensionality |
| No assumptions about data | Requires feature scaling |

---

## Exercises

1. **Implement**: Add weighted voting to the from-scratch KNN
2. **Tune**: Use cross-validation to find optimal K on a dataset
3. **Compare**: Plot decision boundaries for K=1, 5, 20
4. **Scale**: Show the effect of not scaling features
5. **Dimensionality**: Train KNN on data with 2, 10, 50, 100 features. What happens?

---

## Key Takeaways

- KNN classifies by majority vote of K nearest neighbors
- Distance metric matters (Euclidean, Manhattan, etc.)
- Feature scaling is critical
- K controls bias-variance tradeoff
- Struggles with high dimensionality
- Lazy learning: no training, expensive prediction

---

## Next Steps

→ Continue to [05-svm.md](./05-svm.md)
