# Support Vector Machines (SVM)

> Find the optimal hyperplane that maximizes margin between classes.

---

## Overview

SVM finds the decision boundary that maximizes the distance (margin) to the nearest training points (support vectors).

```
         │       Class +
         │    ⊕    ⊕
         │  ⊕        ⊕
    ─────┼─────────────── Decision boundary
  margin │ ↕
    ─────┼───────────────
         │  ⊖   ⊖
         │    ⊖     ⊖
         │       Class -

⊕ ⊖ = Support vectors (closest points)
```

---

## Mathematical Formulation

### Linear SVM

```
Decision function:  f(x) = w·x + b

Prediction:
  f(x) > 0  → Class +1
  f(x) < 0  → Class -1
  f(x) = 0  → On decision boundary

Margin = 2 / ||w||

Goal: Maximize margin = Minimize ||w||²
```

### Optimization Problem

```
minimize:    (1/2) ||w||²

subject to:  yᵢ(w·xᵢ + b) ≥ 1  for all i

Where yᵢ ∈ {-1, +1}
```

---

## Hard vs Soft Margin

### Hard Margin
- Requires linearly separable data
- No misclassifications allowed
- Sensitive to outliers

### Soft Margin (C-SVM)

Allow some misclassifications via slack variables:

```
minimize:    (1/2)||w||² + C × Σξᵢ

subject to:  yᵢ(w·xᵢ + b) ≥ 1 - ξᵢ
             ξᵢ ≥ 0

C = regularization parameter
- Large C: Low tolerance for errors (may overfit)
- Small C: High tolerance for errors (may underfit)
```

```
High C:                    Low C:
Tight margin               Wide margin
Few violations             More violations
      │  ⊕ ⊕                    │  ⊕ ⊕
      │⊕─────                   │ ⊕ ────
      │──────                   │   ─────
      │⊖─────                   │  ⊖ ────
      │  ⊖ ⊖                    │  ⊖ ⊖
```

---

## The Kernel Trick

Transform data into higher dimensions where it's linearly separable:

```
Original space (not separable):     Feature space (separable):
       ⊖ ⊖                              ⊖ ⊖
    ⊕      ⊕       φ(x)              ⊕      ⊕
    ⊕  ⊖⊖  ⊕      ──────→               ⊖⊖
       ⊖ ⊖                           ──────────
                                      (separating hyperplane)
```

**Key insight**: We don't need to compute φ(x) explicitly. We only need dot products, which can be computed via kernel functions:

```
K(xᵢ, xⱼ) = φ(xᵢ) · φ(xⱼ)
```

### Common Kernels

| Kernel | Formula | Use Case |
|--------|---------|----------|
| **Linear** | K(x,y) = x·y | Linearly separable |
| **Polynomial** | K(x,y) = (γx·y + r)^d | Polynomial boundaries |
| **RBF (Gaussian)** | K(x,y) = exp(-γ\|\|x-y\|\|²) | Most common, general |
| **Sigmoid** | K(x,y) = tanh(γx·y + r) | Similar to neural net |

### RBF Kernel Intuition

```
γ controls influence radius:

Small γ:                    Large γ:
Smooth boundary             Jagged boundary
Each point influences       Each point influences
wide region                 small region

    ~~~~~~~~~~~                 ∿∿∿∿∿∿∿
     /       \                 /\/\/\/\
```

---

## Implementation

### Using scikit-learn

```python
from sklearn.svm import SVC, SVR
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Always scale for SVM!
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('svm', SVC(kernel='rbf', C=1.0, gamma='scale'))
])

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)

# Access support vectors
svm_model = pipeline.named_steps['svm']
print(f"Support vectors: {svm_model.n_support_}")
```

### Grid Search for Hyperparameters

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'svm__C': [0.1, 1, 10, 100],
    'svm__gamma': ['scale', 'auto', 0.1, 0.01],
    'svm__kernel': ['rbf', 'poly']
}

grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

print(f"Best params: {grid_search.best_params_}")
```

---

## Multiclass Classification

SVM is inherently binary. For multiclass:

### One-vs-One (OvO)
- Train K(K-1)/2 classifiers (one per class pair)
- Prediction: Voting among all classifiers
- Default in scikit-learn

### One-vs-Rest (OvR)
- Train K classifiers (one per class vs rest)
- Prediction: Class with highest confidence

```python
# OvO (default)
SVC(decision_function_shape='ovr')  # Actually uses OvO internally

# OvR explicitly
from sklearn.multiclass import OneVsRestClassifier
ovr = OneVsRestClassifier(SVC())
```

---

## Support Vector Regression (SVR)

Instead of maximizing margin, fit within ε-tube:

```
           │     ⊕
    ε-tube │   ⊕   ⊕
  ═════════│══════════════ f(x)
    ε-tube │  ⊕    ⊕
           │    ⊕
```

Points outside tube contribute to loss:

```python
from sklearn.svm import SVR

svr = SVR(kernel='rbf', C=1.0, epsilon=0.1)
svr.fit(X_train, y_train)
```

---

## Pros and Cons

| Pros | Cons |
|------|------|
| Effective in high dimensions | Slow on large datasets O(n²-n³) |
| Memory efficient (only stores SVs) | Sensitive to feature scaling |
| Versatile kernels | Doesn't provide probabilities directly |
| Works well with clear margins | Choosing kernel/params is tricky |
| Robust to overfitting (high dim) | Hard to interpret |

---

## When to Use SVM

**Good for:**
- Text classification (high dimensions)
- Image classification
- When n_features > n_samples
- Binary classification with clear margins

**Avoid when:**
- Very large datasets (>100k samples)
- Lots of noise/overlapping classes
- Need probability estimates
- Need interpretability

---

## Exercises

1. **Visualize**: Plot decision boundaries for linear, polynomial (d=3), and RBF kernels
2. **Tune**: Grid search C and γ. Plot validation accuracy heatmap
3. **Support Vectors**: Count SVs for different C values. What's the relationship?
4. **Scale**: Show effect of not scaling features
5. **Compare**: SVM vs Logistic Regression on same dataset

---

## Key Takeaways

- SVM maximizes margin between classes
- Support vectors are the critical training points
- C controls error tolerance (regularization)
- Kernel trick enables non-linear boundaries
- RBF kernel is most versatile, γ controls smoothness
- Always scale features!

---

## Next Steps

→ Continue to [06-decision-trees.md](./06-decision-trees.md)
