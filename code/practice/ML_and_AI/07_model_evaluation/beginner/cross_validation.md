# Cross-Validation - Beginner

Robust model evaluation techniques.

## Learning Objectives
- Understand why cross-validation is important
- Apply different CV strategies
- Compare models reliably

## Setup

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import (
    cross_val_score, KFold, StratifiedKFold, LeaveOneOut
)
from sklearn.datasets import load_iris, load_wine
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
```

---

## Exercise 1: Simple Cross-Validation

Use cross_val_score for quick evaluation.

```python
from sklearn.datasets import load_wine
from sklearn.linear_model import LogisticRegression

# Load data
wine = load_wine()
X, y = wine.data, wine.target

# TODO: Create a LogisticRegression model

# TODO: Perform 5-fold cross-validation

# TODO: Print individual fold scores

# TODO: Print mean and standard deviation
```

<details>
<summary>Solution</summary>

```python
from sklearn.datasets import load_wine
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

wine = load_wine()
X, y = wine.data, wine.target

model = LogisticRegression(max_iter=5000)

# 5-fold cross-validation
cv_scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')

print("Cross-Validation Results:")
print(f"Individual fold scores: {cv_scores}")
print(f"Mean accuracy: {cv_scores.mean():.4f}")
print(f"Std deviation: {cv_scores.std():.4f}")
print(f"95% CI: {cv_scores.mean():.4f} +/- {cv_scores.std()*2:.4f}")
```
</details>

---

## Exercise 2: Compare Multiple Models

Use CV to fairly compare different algorithms.

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

# TODO: Create a list of models to compare
models = [
    ("Logistic Regression", LogisticRegression(max_iter=5000)),
    # Add more models...
]

# TODO: Run 5-fold CV for each model

# TODO: Create a comparison table with mean and std

# TODO: Which model is best? Is the difference significant?
```

<details>
<summary>Solution</summary>

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

models = [
    ("Logistic Regression", LogisticRegression(max_iter=5000)),
    ("Decision Tree", DecisionTreeClassifier(max_depth=5)),
    ("KNN (k=5)", KNeighborsClassifier(n_neighbors=5)),
    ("SVM (RBF)", SVC(kernel='rbf')),
    ("Random Forest", RandomForestClassifier(n_estimators=100)),
]

results = []
for name, model in models:
    scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
    results.append({
        'Model': name,
        'Mean': scores.mean(),
        'Std': scores.std(),
        'Min': scores.min(),
        'Max': scores.max()
    })

results_df = pd.DataFrame(results).sort_values('Mean', ascending=False)
print("Model Comparison (5-fold CV):")
print(results_df.to_string(index=False))

print("\nNote: Models within 1-2 std of each other may not be significantly different")
```
</details>

---

## Exercise 3: Stratified K-Fold

Maintain class proportions in each fold.

```python
from sklearn.model_selection import KFold, StratifiedKFold

# Create imbalanced dataset
from sklearn.datasets import make_classification
X_imb, y_imb = make_classification(
    n_samples=100, n_features=10, weights=[0.9, 0.1], random_state=42
)

# TODO: Check class distribution

# TODO: Compare regular KFold vs StratifiedKFold
# Examine class distribution in each fold

# TODO: Why does stratification matter for imbalanced data?
```

<details>
<summary>Solution</summary>

```python
from sklearn.model_selection import KFold, StratifiedKFold

X_imb, y_imb = make_classification(
    n_samples=100, n_features=10, weights=[0.9, 0.1], random_state=42
)

print(f"Overall class distribution: {np.bincount(y_imb)}")
print(f"Minority class: {y_imb.mean():.1%}\n")

# Regular KFold
print("Regular KFold:")
kfold = KFold(n_splits=5, shuffle=True, random_state=42)
for fold, (train_idx, val_idx) in enumerate(kfold.split(X_imb)):
    train_dist = np.bincount(y_imb[train_idx], minlength=2)
    val_dist = np.bincount(y_imb[val_idx], minlength=2)
    print(f"  Fold {fold+1}: Train {train_dist}, Val {val_dist}")

# Stratified KFold
print("\nStratified KFold:")
stratified = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
for fold, (train_idx, val_idx) in enumerate(stratified.split(X_imb, y_imb)):
    train_dist = np.bincount(y_imb[train_idx], minlength=2)
    val_dist = np.bincount(y_imb[val_idx], minlength=2)
    print(f"  Fold {fold+1}: Train {train_dist}, Val {val_dist}")

print("\nStratified maintains class proportions in each fold!")
print("Critical for imbalanced datasets to avoid folds with no minority class")
```
</details>

---

## Exercise 4: Multiple Scoring Metrics

Evaluate with multiple metrics simultaneously.

```python
from sklearn.model_selection import cross_validate

# TODO: Use cross_validate with multiple metrics
# 'accuracy', 'precision_macro', 'recall_macro', 'f1_macro'

# TODO: Print mean and std for each metric
```

<details>
<summary>Solution</summary>

```python
from sklearn.model_selection import cross_validate

wine = load_wine()
X, y = wine.data, wine.target

model = LogisticRegression(max_iter=5000)

# Multiple metrics
scoring = ['accuracy', 'precision_macro', 'recall_macro', 'f1_macro']

cv_results = cross_validate(
    model, X, y, 
    cv=5, 
    scoring=scoring,
    return_train_score=True
)

print("Cross-Validation Results (Multiple Metrics):")
print("-" * 60)
for metric in scoring:
    train_key = f'train_{metric}'
    test_key = f'test_{metric}'
    print(f"{metric}:")
    print(f"  Train: {cv_results[train_key].mean():.4f} (+/- {cv_results[train_key].std():.4f})")
    print(f"  Test:  {cv_results[test_key].mean():.4f} (+/- {cv_results[test_key].std():.4f})")
```
</details>

---

## Exercise 5: Nested Cross-Validation

Avoid data leakage during hyperparameter tuning.

```python
from sklearn.model_selection import GridSearchCV

# Outer CV: Model evaluation
# Inner CV: Hyperparameter selection

# TODO: Define parameter grid for KNN (k from 1 to 20)

# TODO: Create GridSearchCV for inner loop

# TODO: Use cross_val_score for outer loop

# TODO: Compare with non-nested CV (just GridSearchCV)
```

<details>
<summary>Solution</summary>

```python
from sklearn.model_selection import GridSearchCV, cross_val_score

# Inner CV: Hyperparameter tuning
param_grid = {'n_neighbors': range(1, 21)}
inner_cv = KFold(n_splits=3, shuffle=True, random_state=42)

grid_search = GridSearchCV(
    KNeighborsClassifier(),
    param_grid,
    cv=inner_cv,
    scoring='accuracy'
)

# Outer CV: Model evaluation
outer_cv = KFold(n_splits=5, shuffle=True, random_state=42)
nested_scores = cross_val_score(grid_search, X, y, cv=outer_cv)

print("Nested Cross-Validation:")
print(f"Scores: {nested_scores}")
print(f"Mean: {nested_scores.mean():.4f} (+/- {nested_scores.std():.4f})")

# Non-nested (biased) estimate
grid_search.fit(X, y)
print(f"\nNon-nested best score (biased): {grid_search.best_score_:.4f}")
print(f"Best k: {grid_search.best_params_}")

print("\nNote: Non-nested score is typically optimistic (biased)")
print("Nested CV gives unbiased estimate of generalization performance")
```
</details>

---

## Exercise 6: Leave-One-Out CV

Maximum use of data for small datasets.

```python
from sklearn.model_selection import LeaveOneOut

# Small dataset
from sklearn.datasets import load_iris
iris = load_iris()
X_small = iris.data[:30]  # Use only 30 samples
y_small = iris.target[:30]

# TODO: Apply Leave-One-Out CV

# TODO: Compare with 5-fold CV

# TODO: When is LOOCV appropriate?
```

<details>
<summary>Solution</summary>

```python
from sklearn.model_selection import LeaveOneOut, cross_val_score

iris = load_iris()
X_small = iris.data[:30]
y_small = iris.target[:30]

model = LogisticRegression(max_iter=5000)

# Leave-One-Out
loo = LeaveOneOut()
loo_scores = cross_val_score(model, X_small, y_small, cv=loo)
print(f"Leave-One-Out CV ({len(loo_scores)} folds):")
print(f"  Accuracy: {loo_scores.mean():.4f} (+/- {loo_scores.std():.4f})")

# 5-Fold for comparison
kfold_scores = cross_val_score(model, X_small, y_small, cv=5)
print(f"\n5-Fold CV:")
print(f"  Accuracy: {kfold_scores.mean():.4f} (+/- {kfold_scores.std():.4f})")

print("\nWhen to use LOOCV:")
print("+ Very small datasets (< 50 samples)")
print("+ Maximum use of training data")
print("- Computationally expensive (n iterations)")
print("- High variance (each fold is very similar)")
```
</details>

---

## Key Takeaways

1. **Cross-validation** gives reliable performance estimates
2. **5-10 folds** is typically a good balance
3. **Stratified** CV essential for imbalanced data
4. **Nested CV** needed when tuning hyperparameters
5. **LOOCV** for very small datasets
6. **Report mean ± std** to show variability

## Quick Reference

```python
from sklearn.model_selection import (
    cross_val_score, cross_validate,
    KFold, StratifiedKFold, LeaveOneOut
)

# Simple CV
scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
print(f"Accuracy: {scores.mean():.4f} (+/- {scores.std():.4f})")

# Multiple metrics
results = cross_validate(model, X, y, cv=5, 
                         scoring=['accuracy', 'f1_macro'])

# Stratified for classification
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=cv)

# Nested CV for hyperparameter tuning
grid_search = GridSearchCV(model, param_grid, cv=3)
nested_scores = cross_val_score(grid_search, X, y, cv=5)
```

## Next Steps
- Try [Intermediate: Hyperparameter Tuning](../intermediate/hyperparameter_tuning.md)
- Learn about [PyTorch Basics](../../08_pytorch_basics/beginner/tensors.md)
