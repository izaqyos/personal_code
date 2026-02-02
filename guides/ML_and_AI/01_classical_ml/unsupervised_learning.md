# Unsupervised Learning

Discovering patterns in unlabeled data.

## Overview

Unsupervised learning finds structure in data without explicit labels.

```
Input: Unlabeled data X
Output: Discovered structure (clusters, dimensions, patterns)
```

## Problem Types

### Clustering
Group similar items together.
```
Input: Customer purchase data
Output: Customer segments

Input: News articles
Output: Topic clusters
```

### Dimensionality Reduction
Reduce features while preserving information.
```
Input: 1000 features
Output: 50 principal components

Input: High-dim embeddings
Output: 2D visualization
```

### Anomaly Detection
Identify unusual instances.
```
Input: Transaction data
Output: Fraudulent transactions
```

## Clustering Algorithms

### K-Means
```python
from sklearn.cluster import KMeans

# Basic K-Means
kmeans = KMeans(n_clusters=3, random_state=42)
labels = kmeans.fit_predict(X)
centroids = kmeans.cluster_centers_

# Elbow method for choosing k
inertias = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X)
    inertias.append(kmeans.inertia_)

# Plot inertias to find "elbow"
```

**When to use:**
- Known number of clusters
- Spherical cluster shapes
- Large datasets (fast)

### Hierarchical Clustering
```python
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage

# Agglomerative clustering
agg = AgglomerativeClustering(n_clusters=3, linkage='ward')
labels = agg.fit_predict(X)

# Dendrogram visualization
Z = linkage(X, method='ward')
dendrogram(Z)
```

**When to use:**
- Unknown number of clusters
- Need hierarchical structure
- Small to medium datasets

### DBSCAN
```python
from sklearn.cluster import DBSCAN

# Density-based clustering
dbscan = DBSCAN(eps=0.5, min_samples=5)
labels = dbscan.fit_predict(X)

# -1 label indicates noise/outliers
n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
n_noise = list(labels).count(-1)
```

**When to use:**
- Unknown number of clusters
- Non-spherical cluster shapes
- Need to identify outliers

### Gaussian Mixture Models
```python
from sklearn.mixture import GaussianMixture

# Probabilistic clustering
gmm = GaussianMixture(n_components=3, random_state=42)
gmm.fit(X)
labels = gmm.predict(X)
probabilities = gmm.predict_proba(X)

# Model selection using BIC
bics = []
for n in range(1, 11):
    gmm = GaussianMixture(n_components=n, random_state=42)
    gmm.fit(X)
    bics.append(gmm.bic(X))
```

**When to use:**
- Need soft assignments (probabilities)
- Clusters have different sizes/shapes
- Probabilistic model desired

## Dimensionality Reduction

### Principal Component Analysis (PCA)
```python
from sklearn.decomposition import PCA

# Reduce to 2 dimensions
pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X)

# Explained variance
print(f"Explained variance ratio: {pca.explained_variance_ratio_}")
print(f"Total variance explained: {sum(pca.explained_variance_ratio_):.2%}")

# Choose components by variance threshold
pca_auto = PCA(n_components=0.95)  # Keep 95% of variance
X_reduced = pca_auto.fit_transform(X)
print(f"Components needed: {pca_auto.n_components_}")
```

**When to use:**
- Reduce noise
- Visualization
- Speed up other algorithms
- Linear relationships

### t-SNE
```python
from sklearn.manifold import TSNE

# For visualization (2D or 3D only)
tsne = TSNE(n_components=2, perplexity=30, random_state=42)
X_embedded = tsne.fit_transform(X)

# Note: Cannot transform new data, must refit
```

**When to use:**
- Visualization only
- Local structure important
- Non-linear relationships

### UMAP
```python
import umap

# Better than t-SNE for many cases
reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, n_components=2)
X_embedded = reducer.fit_transform(X)

# Can transform new data
X_new_embedded = reducer.transform(X_new)
```

**When to use:**
- Visualization
- Faster than t-SNE
- Preserves global structure better
- Can transform new data

## Anomaly Detection

### Isolation Forest
```python
from sklearn.ensemble import IsolationForest

# Detect anomalies
iso_forest = IsolationForest(contamination=0.1, random_state=42)
predictions = iso_forest.fit_predict(X)
# -1 for anomalies, 1 for normal

# Anomaly scores
scores = iso_forest.decision_function(X)
```

### One-Class SVM
```python
from sklearn.svm import OneClassSVM

# Fit on normal data only
oc_svm = OneClassSVM(nu=0.1, kernel='rbf')
oc_svm.fit(X_normal)
predictions = oc_svm.predict(X_test)
```

### Local Outlier Factor
```python
from sklearn.neighbors import LocalOutlierFactor

lof = LocalOutlierFactor(n_neighbors=20, contamination=0.1)
predictions = lof.fit_predict(X)
```

## Evaluation Metrics

### Clustering (with labels available)
```python
from sklearn.metrics import (
    adjusted_rand_score,
    normalized_mutual_info_score,
    homogeneity_score
)

ari = adjusted_rand_score(true_labels, predicted_labels)
nmi = normalized_mutual_info_score(true_labels, predicted_labels)
homogeneity = homogeneity_score(true_labels, predicted_labels)
```

### Clustering (no labels)
```python
from sklearn.metrics import silhouette_score, calinski_harabasz_score

# Higher is better
silhouette = silhouette_score(X, labels)
calinski = calinski_harabasz_score(X, labels)
```

### Dimensionality Reduction
```python
# Reconstruction error for PCA
X_reconstructed = pca.inverse_transform(X_reduced)
reconstruction_error = np.mean((X - X_reconstructed) ** 2)

# Trustworthiness for visualization
from sklearn.manifold import trustworthiness
trust = trustworthiness(X, X_embedded, n_neighbors=5)
```

## Feature Extraction

### Text: TF-IDF
```python
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(max_features=1000)
X_tfidf = tfidf.fit_transform(documents)
```

### Images: Pre-trained Features
```python
# Using pre-trained model as feature extractor
from torchvision import models, transforms

model = models.resnet50(pretrained=True)
model = torch.nn.Sequential(*list(model.children())[:-1])

# Extract features
with torch.no_grad():
    features = model(images)
```

## Common Workflows

### Customer Segmentation
```python
# 1. Prepare data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(customer_data)

# 2. Find optimal k
silhouette_scores = []
for k in range(2, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(X_scaled)
    silhouette_scores.append(silhouette_score(X_scaled, labels))

# 3. Fit with best k
best_k = silhouette_scores.index(max(silhouette_scores)) + 2
kmeans = KMeans(n_clusters=best_k, random_state=42)
segments = kmeans.fit_predict(X_scaled)

# 4. Analyze segments
for i in range(best_k):
    segment_data = customer_data[segments == i]
    print(f"Segment {i}: {len(segment_data)} customers")
    print(segment_data.mean())
```

### Visualization Pipeline
```python
# 1. Reduce dimensions first with PCA (speed)
pca = PCA(n_components=50)
X_pca = pca.fit_transform(X)

# 2. Then use t-SNE/UMAP for visualization
tsne = TSNE(n_components=2, random_state=42)
X_viz = tsne.fit_transform(X_pca)

# 3. Color by cluster
plt.scatter(X_viz[:, 0], X_viz[:, 1], c=labels, cmap='viridis')
```

## Quick Reference

### Algorithm Selection
```
Clustering:
  Known k, spherical: K-Means
  Unknown k, hierarchical: Agglomerative
  Arbitrary shapes: DBSCAN
  Soft assignments: GMM

Dimensionality Reduction:
  Linear, fast: PCA
  Visualization: UMAP > t-SNE
  Sparse data: TruncatedSVD

Anomaly Detection:
  General purpose: Isolation Forest
  Very high dimensions: One-Class SVM
  Local outliers: LOF
```

## Related Topics
- [Supervised Learning](supervised_learning.md)
- [K-Nearest Neighbors](knn.md)
- [Neural Networks](../02_deep_learning/neural_networks.md)
