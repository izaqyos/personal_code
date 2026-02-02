# K-Nearest Neighbors (KNN)

Simple, instance-based learning algorithm.

## Overview

KNN makes predictions based on the k closest training examples.

```
Classification: Majority vote of k neighbors
Regression: Average of k neighbors' values
```

No training phase - all computation happens at prediction time.

## How It Works

```
1. Store all training data
2. For new point:
   a. Calculate distance to all training points
   b. Find k nearest neighbors
   c. Vote (classification) or average (regression)
```

## Basic Implementation

```python
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Classification
knn_clf = KNeighborsClassifier(n_neighbors=5)
knn_clf.fit(X_train, y_train)
predictions = knn_clf.predict(X_test)
probabilities = knn_clf.predict_proba(X_test)

# Regression
knn_reg = KNeighborsRegressor(n_neighbors=5)
knn_reg.fit(X_train, y_train)
predictions = knn_reg.predict(X_test)
```

## Distance Metrics

### Euclidean Distance (L2)
Most common, works well for continuous features.

```python
# Default in sklearn
knn = KNeighborsClassifier(n_neighbors=5, metric='euclidean')

# Formula: sqrt(sum((a - b)²))
import numpy as np
def euclidean(a, b):
    return np.sqrt(np.sum((a - b) ** 2))
```

### Manhattan Distance (L1)
Better for high dimensions, less sensitive to outliers.

```python
knn = KNeighborsClassifier(n_neighbors=5, metric='manhattan')

# Formula: sum(|a - b|)
def manhattan(a, b):
    return np.sum(np.abs(a - b))
```

### Minkowski Distance
Generalization of L1 and L2.

```python
# p=1: Manhattan, p=2: Euclidean
knn = KNeighborsClassifier(n_neighbors=5, metric='minkowski', p=2)
```

### Cosine Similarity
For text and high-dimensional sparse data.

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics.pairwise import cosine_distances

knn = KNeighborsClassifier(n_neighbors=5, metric='cosine')
```

## Choosing K

```python
from sklearn.model_selection import cross_val_score

# Test different k values
k_values = range(1, 21)
cv_scores = []

for k in k_values:
    knn = KNeighborsClassifier(n_neighbors=k)
    scores = cross_val_score(knn, X_train, y_train, cv=5, scoring='accuracy')
    cv_scores.append(scores.mean())

# Find optimal k
optimal_k = k_values[np.argmax(cv_scores)]
print(f"Optimal k: {optimal_k}")

# Plot
import matplotlib.pyplot as plt
plt.plot(k_values, cv_scores)
plt.xlabel('K')
plt.ylabel('Cross-validation accuracy')
plt.title('KNN Performance vs K')
plt.show()
```

### K Guidelines
```
Small k (e.g., 1-3):
  - More sensitive to noise
  - Complex decision boundary
  - May overfit

Large k (e.g., 10-20):
  - Smoother decision boundary
  - Less sensitive to noise
  - May underfit

Common practice:
  - Start with k = sqrt(n) where n = training samples
  - Use odd k for binary classification (avoid ties)
  - Cross-validate to find optimal
```

## Feature Scaling (Essential!)

KNN is distance-based, so features must be scaled.

```python
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Always scale for KNN
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('knn', KNeighborsClassifier(n_neighbors=5))
])

pipeline.fit(X_train, y_train)
predictions = pipeline.predict(X_test)
```

### Why Scaling Matters

```
Feature 1: Age (0-100)
Feature 2: Income ($0-$1,000,000)

Without scaling:
  Distance dominated by income
  Age differences ignored

With scaling:
  Both features contribute equally
```

## Weighted KNN

Give closer neighbors more influence.

```python
# Uniform: all neighbors equal weight
knn_uniform = KNeighborsClassifier(n_neighbors=5, weights='uniform')

# Distance: closer neighbors weighted more (1/distance)
knn_weighted = KNeighborsClassifier(n_neighbors=5, weights='distance')

# Custom weight function
def custom_weights(distances):
    return np.exp(-distances)  # Gaussian weighting

knn_custom = KNeighborsClassifier(n_neighbors=5, weights=custom_weights)
```

## Performance Optimization

### KD-Tree (Default for low dimensions)
```python
# Efficient for d < 20
knn = KNeighborsClassifier(
    n_neighbors=5,
    algorithm='kd_tree',
    leaf_size=30
)
```

### Ball Tree
```python
# Better for higher dimensions
knn = KNeighborsClassifier(
    n_neighbors=5,
    algorithm='ball_tree'
)
```

### Brute Force
```python
# Use for small datasets or high dimensions
knn = KNeighborsClassifier(
    n_neighbors=5,
    algorithm='brute'
)
```

### Approximate Nearest Neighbors
For very large datasets, use approximate methods:

```python
# Using Annoy (Spotify)
from annoy import AnnoyIndex

# Build index
f = X.shape[1]  # Number of features
index = AnnoyIndex(f, 'euclidean')
for i, vector in enumerate(X):
    index.add_item(i, vector)
index.build(10)  # 10 trees

# Query
neighbors = index.get_nns_by_vector(query_vector, k=5)
```

## Curse of Dimensionality

KNN struggles in high dimensions.

```
Problem:
  - In high dimensions, all points become equidistant
  - Distances become less meaningful
  - Need exponentially more data

Solutions:
  - Dimensionality reduction (PCA, UMAP)
  - Feature selection
  - Use cosine distance for sparse data
```

```python
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline

# Reduce dimensions before KNN
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('pca', PCA(n_components=50)),
    ('knn', KNeighborsClassifier(n_neighbors=5))
])
```

## Advantages and Disadvantages

### Advantages
```
✓ Simple to understand and implement
✓ No training phase
✓ Naturally handles multi-class
✓ Can capture complex boundaries
✓ Non-parametric (no assumptions about data)
```

### Disadvantages
```
✗ Slow prediction (O(n) per query)
✗ Memory-intensive (stores all data)
✗ Sensitive to irrelevant features
✗ Curse of dimensionality
✗ Requires feature scaling
```

## Common Applications

```
1. Recommendation systems
   - Similar users/items

2. Image classification
   - Compare feature vectors

3. Anomaly detection
   - Points with few neighbors

4. Imputation
   - Fill missing values from neighbors
```

## Complete Example

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import classification_report

# Prepare data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('knn', KNeighborsClassifier())
])

# Hyperparameter search
param_grid = {
    'knn__n_neighbors': [3, 5, 7, 9, 11],
    'knn__weights': ['uniform', 'distance'],
    'knn__metric': ['euclidean', 'manhattan']
}

grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

print(f"Best parameters: {grid_search.best_params_}")
print(f"Best CV accuracy: {grid_search.best_score_:.3f}")

# Evaluate
predictions = grid_search.predict(X_test)
print(classification_report(y_test, predictions))
```

## Quick Reference

```python
# Classification
KNeighborsClassifier(
    n_neighbors=5,
    weights='distance',  # or 'uniform'
    metric='euclidean',  # or 'manhattan', 'cosine'
    algorithm='auto'     # 'kd_tree', 'ball_tree', 'brute'
)

# Regression
KNeighborsRegressor(n_neighbors=5, weights='distance')

# Essential: Always scale features!
Pipeline([
    ('scaler', StandardScaler()),
    ('knn', KNeighborsClassifier())
])
```

## Related Topics
- [Supervised Learning](supervised_learning.md)
- [Clustering](unsupervised_learning.md)
- [SVM](svm.md)
