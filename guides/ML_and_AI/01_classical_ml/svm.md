# Support Vector Machines (SVM)

Maximum margin classifier with kernel trick.

## Overview

SVM finds the hyperplane that maximizes the margin between classes.

```
Goal: Find hyperplane w·x + b = 0 that maximizes margin

Support vectors: Points closest to the hyperplane
Margin: Distance from hyperplane to nearest points
```

## Linear SVM

For linearly separable data.

```python
from sklearn.svm import SVC

# Linear kernel
svm = SVC(kernel='linear', C=1.0)
svm.fit(X_train, y_train)
predictions = svm.predict(X_test)

# Access support vectors
print(f"Number of support vectors: {len(svm.support_vectors_)}")
```

### The Margin

```
         w·x + b = 1   (positive class boundary)
  +  +      │
   +        │ ← margin = 2/||w||
━━━━━━━━━━━━│━━━━━━━━━━━  w·x + b = 0 (decision boundary)
            │
   -  -     │
         w·x + b = -1  (negative class boundary)

Larger margin → Better generalization
```

## Regularization (C Parameter)

Controls trade-off between margin and misclassification.

```python
# High C: Smaller margin, fewer misclassifications
svm_hard = SVC(kernel='linear', C=100)

# Low C: Larger margin, more misclassifications allowed
svm_soft = SVC(kernel='linear', C=0.1)
```

```
High C:
  - Strictly minimize misclassifications
  - May overfit
  
Low C:
  - Allow some misclassifications for wider margin
  - Better generalization
```

## Kernel Trick

Transform data to higher dimension where it's linearly separable.

```python
# Linear (no transformation)
svm_linear = SVC(kernel='linear')

# RBF (Gaussian) - most common
svm_rbf = SVC(kernel='rbf', gamma='scale')

# Polynomial
svm_poly = SVC(kernel='poly', degree=3)

# Sigmoid
svm_sigmoid = SVC(kernel='sigmoid')
```

### RBF Kernel (Radial Basis Function)

```python
# K(x, x') = exp(-gamma * ||x - x'||²)

# gamma controls influence of each training sample
# High gamma: Points must be very close to influence each other
# Low gamma: Points influence each other from further away

svm = SVC(kernel='rbf', gamma='scale')  # gamma = 1 / (n_features * X.var())
svm = SVC(kernel='rbf', gamma='auto')   # gamma = 1 / n_features
svm = SVC(kernel='rbf', gamma=0.1)      # custom value
```

### Polynomial Kernel

```python
# K(x, x') = (gamma * x·x' + coef0)^degree

svm = SVC(
    kernel='poly',
    degree=3,      # Polynomial degree
    gamma='scale',
    coef0=0        # Independent term
)
```

## Hyperparameter Tuning

```python
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Pipeline with scaling
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('svm', SVC())
])

# Parameter grid
param_grid = {
    'svm__kernel': ['rbf', 'linear'],
    'svm__C': [0.1, 1, 10, 100],
    'svm__gamma': ['scale', 'auto', 0.01, 0.1, 1]
}

grid_search = GridSearchCV(
    pipeline,
    param_grid,
    cv=5,
    scoring='accuracy',
    n_jobs=-1
)

grid_search.fit(X_train, y_train)
print(f"Best params: {grid_search.best_params_}")
```

## Probability Estimates

```python
# Enable probability predictions (slower)
svm = SVC(kernel='rbf', probability=True)
svm.fit(X_train, y_train)

# Get class probabilities
probabilities = svm.predict_proba(X_test)

# Note: Uses Platt scaling, adds computational cost
```

## SVM for Regression (SVR)

```python
from sklearn.svm import SVR

# Epsilon-tube: No penalty for errors within epsilon
svr = SVR(kernel='rbf', C=1.0, epsilon=0.1)
svr.fit(X_train, y_train)
predictions = svr.predict(X_test)
```

## Multi-class Classification

SVM is inherently binary. Sklearn uses one-vs-one by default.

```python
# One-vs-One: n*(n-1)/2 classifiers
svm = SVC(decision_function_shape='ovo')

# One-vs-Rest: n classifiers
svm = SVC(decision_function_shape='ovr')
```

## Feature Scaling (Essential!)

SVM is sensitive to feature scales.

```python
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Always scale for SVM
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('svm', SVC(kernel='rbf'))
])
```

## Handling Imbalanced Classes

```python
# Automatic class weights
svm = SVC(kernel='rbf', class_weight='balanced')

# Custom weights
svm = SVC(kernel='rbf', class_weight={0: 1, 1: 10})
```

## Large-Scale SVMs

For large datasets, use LinearSVC or SGDClassifier.

```python
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier

# LinearSVC: Fast linear SVM (uses liblinear)
linear_svm = LinearSVC(C=1.0, max_iter=1000)

# SGDClassifier with hinge loss: Online learning
sgd_svm = SGDClassifier(loss='hinge', alpha=0.0001, max_iter=1000)
```

### Comparison

```
SVC (libsvm):
  - O(n² to n³) complexity
  - Best for small-medium datasets
  - Supports all kernels

LinearSVC (liblinear):
  - O(n) complexity
  - Linear kernel only
  - Good for large datasets

SGDClassifier:
  - O(n) complexity
  - Online learning
  - Good for very large/streaming data
```

## Advantages and Disadvantages

### Advantages
```
✓ Effective in high dimensions
✓ Memory efficient (uses support vectors only)
✓ Versatile (different kernels)
✓ Robust to overfitting in high-dim spaces
```

### Disadvantages
```
✗ Slow for large datasets O(n² to n³)
✗ Sensitive to feature scaling
✗ Not good for noisy data
✗ Hard to interpret (black box)
✗ Probability estimates require extra step
```

## Complete Example

```python
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix

# Load and split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Create pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('svm', SVC(random_state=42))
])

# Hyperparameter grid
param_grid = {
    'svm__kernel': ['rbf', 'linear'],
    'svm__C': [0.1, 1, 10],
    'svm__gamma': ['scale', 0.1, 1]
}

# Grid search
grid_search = GridSearchCV(
    pipeline, param_grid, 
    cv=5, scoring='f1_macro', n_jobs=-1
)
grid_search.fit(X_train, y_train)

# Results
print(f"Best parameters: {grid_search.best_params_}")
print(f"Best CV score: {grid_search.best_score_:.3f}")

# Evaluate on test set
predictions = grid_search.predict(X_test)
print("\nClassification Report:")
print(classification_report(y_test, predictions))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))
```

## Quick Reference

```python
# Classification
SVC(
    kernel='rbf',        # 'linear', 'poly', 'sigmoid'
    C=1.0,               # Regularization (lower = more reg)
    gamma='scale',       # Kernel coefficient
    probability=False,   # Enable predict_proba (slower)
    class_weight=None    # 'balanced' for imbalanced data
)

# Regression
SVR(
    kernel='rbf',
    C=1.0,
    epsilon=0.1          # Width of epsilon-tube
)

# Fast linear SVM (large data)
LinearSVC(C=1.0, max_iter=1000)

# Essential: Always scale features!
```

## Related Topics
- [Supervised Learning](supervised_learning.md)
- [KNN](knn.md)
- [Model Evaluation](model_evaluation.md)
