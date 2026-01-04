# Decision Trees

> Make predictions by learning simple decision rules from features.

---

## Overview

Decision trees recursively split data based on feature thresholds to create a tree of decisions.

```
                    Is age > 30?
                   /            \
                 Yes             No
                 /                 \
        Income > 50k?          Student?
         /        \             /      \
       Yes        No          Yes       No
        ↓          ↓            ↓        ↓
      Buy        Wait         Buy      Wait
```

---

## Key Concepts

### Splitting Criteria

How do we choose the best feature and threshold to split on?

#### For Classification

**Gini Impurity:**
```
Gini(D) = 1 - Σᵢ pᵢ²

Where pᵢ = proportion of class i in dataset D

Example:
50% class A, 50% class B → Gini = 1 - (0.5² + 0.5²) = 0.5 (impure)
100% class A           → Gini = 1 - (1²) = 0 (pure)
```

**Entropy / Information Gain:**
```
Entropy(D) = -Σᵢ pᵢ log₂(pᵢ)

Information Gain = Entropy(parent) - Weighted Entropy(children)

Higher gain = Better split
```

```
Entropy vs Gini:
Entropy  │      ___
         │   _/     \_
         │ /           \
    0    └───────────────
         0     0.5      1
              proportion

Both are maximized at 0.5 (maximum uncertainty)
Both are 0 at 0 or 1 (pure class)
```

#### For Regression

**Mean Squared Error (MSE):**
```
MSE = (1/n) Σ(yᵢ - ȳ)²

Split to minimize weighted MSE of children
```

---

## Building the Tree

### Recursive Algorithm (CART)

```
function BuildTree(D, depth):
    # Stopping conditions
    if depth == max_depth or |D| < min_samples or D is pure:
        return LeafNode(majority_class or mean_value)

    # Find best split
    best_gain = 0
    for each feature f:
        for each threshold t:
            gain = information_gain(D, f, t)
            if gain > best_gain:
                best_gain, best_f, best_t = gain, f, t

    # Split data
    D_left = {x ∈ D : x[best_f] ≤ best_t}
    D_right = {x ∈ D : x[best_f] > best_t}

    # Recurse
    left_child = BuildTree(D_left, depth + 1)
    right_child = BuildTree(D_right, depth + 1)

    return DecisionNode(best_f, best_t, left_child, right_child)
```

---

## Controlling Complexity (Regularization)

Prevent overfitting with hyperparameters:

| Parameter | Effect | Typical Values |
|-----------|--------|----------------|
| `max_depth` | Maximum tree depth | 3-20 |
| `min_samples_split` | Min samples to split node | 2-20 |
| `min_samples_leaf` | Min samples in leaf | 1-10 |
| `max_features` | Features to consider per split | sqrt(n), log2(n) |
| `max_leaf_nodes` | Maximum leaf nodes | None, 10-100 |

```
max_depth=2:            max_depth=10:
   ┌───┐                  ┌───┐
   │   │                  │   │
  ┌┴┐ ┌┴┐               ┌─┴─┐ ┌─┴─┐
  │ │ │ │              ┌┴┐ ┌┴┐┌┴┐ ┌┴┐
                       ... (many levels)
  Underfits            Overfits
```

---

## Pruning

### Pre-pruning (Early Stopping)
Stop growing before overfitting:
- Set `max_depth`, `min_samples_split`, etc.

### Post-pruning
Grow full tree, then remove branches:
- Cost-complexity pruning (α parameter)
- Reduced error pruning

```python
# Cost-complexity pruning in scikit-learn
clf = DecisionTreeClassifier(ccp_alpha=0.01)

# Find optimal alpha via cross-validation
path = clf.cost_complexity_pruning_path(X_train, y_train)
alphas = path.ccp_alphas
```

---

## Implementation

### Using scikit-learn

```python
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.tree import plot_tree, export_text
import matplotlib.pyplot as plt

# Classification
clf = DecisionTreeClassifier(
    criterion='gini',      # or 'entropy'
    max_depth=5,
    min_samples_split=10,
    min_samples_leaf=5,
    random_state=42
)
clf.fit(X_train, y_train)

# Visualize
plt.figure(figsize=(20, 10))
plot_tree(clf, feature_names=feature_names, class_names=class_names, filled=True)
plt.show()

# Text representation
print(export_text(clf, feature_names=feature_names))

# Feature importance
importances = clf.feature_importances_
```

---

## Feature Importance

How much each feature contributes to reducing impurity:

```python
import pandas as pd

importance_df = pd.DataFrame({
    'feature': feature_names,
    'importance': clf.feature_importances_
}).sort_values('importance', ascending=False)

print(importance_df)
```

```
Feature importance (example):
age            0.35  ████████████
income         0.28  ██████████
education      0.22  ████████
occupation     0.15  █████
```

---

## Ensemble Methods Preview

Decision trees are the building block for powerful ensembles:

| Method | Idea | Reduces |
|--------|------|---------|
| **Random Forest** | Average many trees | Variance |
| **Gradient Boosting** | Sequentially fix errors | Bias |
| **AdaBoost** | Focus on hard examples | Both |

---

## Pros and Cons

| Pros | Cons |
|------|------|
| Easy to interpret/visualize | Prone to overfitting |
| No scaling required | Unstable (small data changes) |
| Handles non-linear relationships | Biased toward features with many levels |
| Works with mixed feature types | Can't extrapolate |
| Fast training and prediction | Axis-aligned splits only |
| Handles missing values (some impls) | Not competitive alone |

---

## Exercises

1. **Build**: Train tree with max_depth=3. Visualize and interpret each split
2. **Compare**: Gini vs Entropy - any performance difference?
3. **Tune**: Grid search depth and min_samples_leaf. Plot accuracy vs complexity
4. **Prune**: Apply cost-complexity pruning. Find optimal α
5. **Importance**: Which features are most important? Does it match intuition?

---

## Key Takeaways

- Trees split data recursively using feature thresholds
- Gini/Entropy measure impurity, used to find best splits
- Regularization (depth, min_samples) prevents overfitting
- Trees are interpretable but unstable
- Foundation for powerful ensemble methods

---

## Next Steps

→ Continue to [07-gradient-descent.md](./07-gradient-descent.md)
