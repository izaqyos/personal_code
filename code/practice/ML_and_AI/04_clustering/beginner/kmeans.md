# K-Means Clustering - Beginner

Group similar data points together without labels.

## Learning Objectives
- Understand unsupervised learning concepts
- Apply K-Means clustering
- Choose optimal number of clusters

## Setup

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
```

---

## Exercise 1: Basic K-Means

Cluster simple 2D data.

```python
from sklearn.datasets import make_blobs

# Generate clustered data
X, true_labels = make_blobs(
    n_samples=300, centers=4, cluster_std=0.60, random_state=42
)

# TODO: Visualize the data (scatter plot)

# TODO: Create KMeans with n_clusters=4

# TODO: Fit and predict cluster labels

# TODO: Visualize clusters with colors

# TODO: Plot cluster centers
```

<details>
<summary>Solution</summary>

```python
from sklearn.datasets import make_blobs

X, true_labels = make_blobs(
    n_samples=300, centers=4, cluster_std=0.60, random_state=42
)

# Visualize raw data
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.scatter(X[:, 0], X[:, 1], alpha=0.7)
plt.title('Raw Data')

# K-Means
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
labels = kmeans.fit_predict(X)

# Visualize clusters
plt.subplot(1, 2, 2)
plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis', alpha=0.7)
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], 
            s=200, c='red', marker='X', edgecolors='black', linewidth=2,
            label='Centroids')
plt.title('K-Means Clusters')
plt.legend()
plt.tight_layout()
plt.show()

print(f"Cluster sizes: {np.bincount(labels)}")
```
</details>

---

## Exercise 2: Elbow Method

Find optimal number of clusters.

```python
# TODO: Run K-Means for k=1 to k=10

# TODO: Record inertia (within-cluster sum of squares) for each k

# TODO: Plot the elbow curve

# TODO: Identify the "elbow" - where does adding clusters stop helping much?
```

<details>
<summary>Solution</summary>

```python
inertias = []
K_range = range(1, 11)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X)
    inertias.append(kmeans.inertia_)

# Plot elbow curve
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(K_range, inertias, 'bo-')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Inertia')
plt.title('Elbow Method')

# Calculate rate of change
plt.subplot(1, 2, 2)
diffs = np.diff(inertias)
plt.plot(range(2, 11), -diffs, 'ro-')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Inertia Reduction')
plt.title('Rate of Inertia Decrease')
plt.tight_layout()
plt.show()

print("The elbow is around k=4 (matching our generated data)")
```
</details>

---

## Exercise 3: Silhouette Score

Quantitatively evaluate clustering quality.

```python
from sklearn.metrics import silhouette_score, silhouette_samples

# TODO: Calculate silhouette score for k=2 to k=10

# TODO: Plot silhouette scores

# TODO: Which k has the best silhouette score?
```

<details>
<summary>Solution</summary>

```python
from sklearn.metrics import silhouette_score, silhouette_samples

silhouette_scores = []
K_range = range(2, 11)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)
    score = silhouette_score(X, labels)
    silhouette_scores.append(score)
    print(f"k={k}: Silhouette Score = {score:.3f}")

plt.figure(figsize=(8, 5))
plt.plot(K_range, silhouette_scores, 'go-')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Silhouette Score')
plt.title('Silhouette Score vs Number of Clusters')
plt.show()

best_k = K_range[np.argmax(silhouette_scores)]
print(f"\nBest k by silhouette score: {best_k}")
```
</details>

---

## Exercise 4: Customer Segmentation

Apply clustering to a business problem.

```python
# Simulate customer data
np.random.seed(42)
n_customers = 500

# Create customer features
customers = pd.DataFrame({
    'annual_income': np.random.normal(50000, 20000, n_customers).clip(20000, 150000),
    'spending_score': np.random.normal(50, 25, n_customers).clip(1, 100),
    'age': np.random.normal(40, 15, n_customers).clip(18, 80),
    'visits_per_month': np.random.exponential(3, n_customers).clip(0, 20)
})

# TODO: Scale the features (important for K-Means!)

# TODO: Apply K-Means with k=5

# TODO: Add cluster labels to dataframe

# TODO: Analyze cluster characteristics (mean values per cluster)
```

<details>
<summary>Solution</summary>

```python
np.random.seed(42)
n_customers = 500

customers = pd.DataFrame({
    'annual_income': np.random.normal(50000, 20000, n_customers).clip(20000, 150000),
    'spending_score': np.random.normal(50, 25, n_customers).clip(1, 100),
    'age': np.random.normal(40, 15, n_customers).clip(18, 80),
    'visits_per_month': np.random.exponential(3, n_customers).clip(0, 20)
})

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(customers)

# Cluster
kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
customers['cluster'] = kmeans.fit_predict(X_scaled)

# Analyze clusters
print("Cluster Analysis:")
print("=" * 60)
cluster_summary = customers.groupby('cluster').agg({
    'annual_income': 'mean',
    'spending_score': 'mean',
    'age': 'mean',
    'visits_per_month': 'mean',
    'cluster': 'count'
}).rename(columns={'cluster': 'count'})

print(cluster_summary.round(2))

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].scatter(customers['annual_income'], customers['spending_score'], 
                c=customers['cluster'], cmap='viridis', alpha=0.7)
axes[0].set_xlabel('Annual Income')
axes[0].set_ylabel('Spending Score')
axes[0].set_title('Clusters: Income vs Spending')

axes[1].scatter(customers['age'], customers['visits_per_month'], 
                c=customers['cluster'], cmap='viridis', alpha=0.7)
axes[1].set_xlabel('Age')
axes[1].set_ylabel('Visits per Month')
axes[1].set_title('Clusters: Age vs Visits')

plt.tight_layout()
plt.show()
```
</details>

---

## Exercise 5: Initialization Matters

See how initialization affects results.

```python
# Create data that's harder to cluster
X_hard, _ = make_blobs(n_samples=300, centers=3, cluster_std=1.5, random_state=42)

# TODO: Run K-Means 10 times with different random_state

# TODO: Record inertia for each run

# TODO: Plot the distribution of inertias

# TODO: Compare with n_init=10 vs n_init=1
```

<details>
<summary>Solution</summary>

```python
X_hard, _ = make_blobs(n_samples=300, centers=3, cluster_std=1.5, random_state=42)

# Single initialization (n_init=1)
inertias_single = []
for seed in range(20):
    kmeans = KMeans(n_clusters=3, random_state=seed, n_init=1)
    kmeans.fit(X_hard)
    inertias_single.append(kmeans.inertia_)

# Multiple initializations (n_init=10)
inertias_multi = []
for seed in range(20):
    kmeans = KMeans(n_clusters=3, random_state=seed, n_init=10)
    kmeans.fit(X_hard)
    inertias_multi.append(kmeans.inertia_)

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.hist(inertias_single, bins=10, alpha=0.7, label='n_init=1')
plt.xlabel('Inertia')
plt.title('Single Initialization')

plt.subplot(1, 2, 2)
plt.hist(inertias_multi, bins=10, alpha=0.7, color='orange', label='n_init=10')
plt.xlabel('Inertia')
plt.title('Multiple Initializations')

plt.tight_layout()
plt.show()

print(f"n_init=1:  Mean={np.mean(inertias_single):.1f}, Std={np.std(inertias_single):.1f}")
print(f"n_init=10: Mean={np.mean(inertias_multi):.1f}, Std={np.std(inertias_multi):.1f}")
print("\nMultiple initializations give more consistent results!")
```
</details>

---

## Exercise 6: K-Means Limitations

Understand when K-Means fails.

```python
from sklearn.datasets import make_moons, make_circles

# Create non-spherical data
X_moons, _ = make_moons(n_samples=200, noise=0.05, random_state=42)
X_circles, _ = make_circles(n_samples=200, noise=0.05, factor=0.5, random_state=42)

# TODO: Apply K-Means with k=2 to both datasets

# TODO: Visualize results

# TODO: Why does K-Means fail on these shapes?
```

<details>
<summary>Solution</summary>

```python
from sklearn.datasets import make_moons, make_circles

X_moons, _ = make_moons(n_samples=200, noise=0.05, random_state=42)
X_circles, _ = make_circles(n_samples=200, noise=0.05, factor=0.5, random_state=42)

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Moons
kmeans_moons = KMeans(n_clusters=2, random_state=42, n_init=10)
labels_moons = kmeans_moons.fit_predict(X_moons)

axes[0, 0].scatter(X_moons[:, 0], X_moons[:, 1])
axes[0, 0].set_title('Moons: Raw Data')

axes[0, 1].scatter(X_moons[:, 0], X_moons[:, 1], c=labels_moons, cmap='viridis')
axes[0, 1].scatter(kmeans_moons.cluster_centers_[:, 0], kmeans_moons.cluster_centers_[:, 1], 
                   s=200, c='red', marker='X')
axes[0, 1].set_title('Moons: K-Means (k=2) - FAILS')

# Circles
kmeans_circles = KMeans(n_clusters=2, random_state=42, n_init=10)
labels_circles = kmeans_circles.fit_predict(X_circles)

axes[1, 0].scatter(X_circles[:, 0], X_circles[:, 1])
axes[1, 0].set_title('Circles: Raw Data')

axes[1, 1].scatter(X_circles[:, 0], X_circles[:, 1], c=labels_circles, cmap='viridis')
axes[1, 1].scatter(kmeans_circles.cluster_centers_[:, 0], kmeans_circles.cluster_centers_[:, 1], 
                   s=200, c='red', marker='X')
axes[1, 1].set_title('Circles: K-Means (k=2) - FAILS')

plt.tight_layout()
plt.show()

print("K-Means Limitations:")
print("1. Assumes spherical clusters")
print("2. Assumes clusters are similar size")
print("3. Cannot handle non-convex shapes")
print("\nFor these shapes, use DBSCAN or Spectral Clustering")
```
</details>

---

## Key Takeaways

1. **K-Means** partitions data into k spherical clusters
2. **Feature scaling** is essential before clustering
3. **Elbow method** and **silhouette score** help choose k
4. **n_init > 1** gives more robust results
5. **K-Means fails** on non-spherical cluster shapes
6. **Interpret clusters** by examining feature means

## Quick Reference

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Cluster
kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
labels = kmeans.fit_predict(X_scaled)

# Evaluate
inertia = kmeans.inertia_  # Lower is better
silhouette = silhouette_score(X_scaled, labels)  # Higher is better (-1 to 1)

# Access centroids
centroids = kmeans.cluster_centers_
```

## Next Steps
- Try [Intermediate: Hierarchical Clustering](../intermediate/hierarchical.md)
- Learn about [Model Evaluation](../../07_model_evaluation/beginner/cross_validation.md)
