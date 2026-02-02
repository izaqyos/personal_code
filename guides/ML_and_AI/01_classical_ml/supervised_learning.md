# Supervised Learning

Learning from labeled examples to make predictions.

## Overview

Supervised learning uses labeled training data to learn a mapping from inputs to outputs.

```
Training: (X, y) pairs → Learn function f
Prediction: f(X_new) → y_predicted
```

## Problem Types

### Classification
Predict discrete categories.
```
Input: Email features
Output: Spam / Not Spam

Input: Image pixels
Output: Cat / Dog / Bird
```

### Regression
Predict continuous values.
```
Input: House features
Output: Price ($)

Input: Historical data
Output: Stock price
```

## The Learning Process

```
1. Collect labeled data (X, y)
2. Split into train/validation/test
3. Choose model and hyperparameters
4. Train on training set
5. Tune on validation set
6. Evaluate on test set
7. Deploy if satisfactory
```

## Key Concepts

### Bias-Variance Tradeoff
```
High Bias (Underfitting):
  - Model too simple
  - High error on training data
  - High error on test data
  
High Variance (Overfitting):
  - Model too complex
  - Low error on training data
  - High error on test data

Goal: Find the sweet spot
```

### Training/Validation/Test Split
```python
from sklearn.model_selection import train_test_split

# First split: train+val and test
X_trainval, X_test, y_trainval, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Second split: train and val
X_train, X_val, y_train, y_val = train_test_split(
    X_trainval, y_trainval, test_size=0.2, random_state=42
)

# Proportions: 64% train, 16% val, 20% test
```

### Cross-Validation
```python
from sklearn.model_selection import cross_val_score

# 5-fold cross-validation
scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
print(f"Accuracy: {scores.mean():.3f} (+/- {scores.std()*2:.3f})")
```

## Common Algorithms

### Linear Models
```python
from sklearn.linear_model import LinearRegression, LogisticRegression

# Regression
reg = LinearRegression()
reg.fit(X_train, y_train)
predictions = reg.predict(X_test)

# Classification
clf = LogisticRegression()
clf.fit(X_train, y_train)
predictions = clf.predict(X_test)
probabilities = clf.predict_proba(X_test)
```

### Decision Trees
```python
from sklearn.tree import DecisionTreeClassifier

clf = DecisionTreeClassifier(max_depth=5)
clf.fit(X_train, y_train)
predictions = clf.predict(X_test)
```

### Ensemble Methods
```python
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

# Random Forest
rf = RandomForestClassifier(n_estimators=100)
rf.fit(X_train, y_train)

# Gradient Boosting
gb = GradientBoostingClassifier(n_estimators=100)
gb.fit(X_train, y_train)
```

### Support Vector Machines
```python
from sklearn.svm import SVC, SVR

# Classification
svm_clf = SVC(kernel='rbf', C=1.0)
svm_clf.fit(X_train, y_train)

# Regression
svm_reg = SVR(kernel='rbf')
svm_reg.fit(X_train, y_train)
```

## Evaluation Metrics

### Classification Metrics
```python
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions)
recall = recall_score(y_test, predictions)
f1 = f1_score(y_test, predictions)
```

**Confusion Matrix:**
```
              Predicted
              Neg    Pos
Actual  Neg   TN     FP
        Pos   FN     TP

Accuracy = (TP + TN) / Total
Precision = TP / (TP + FP)  # Of predicted positive, how many correct?
Recall = TP / (TP + FN)     # Of actual positive, how many found?
F1 = 2 * (Precision * Recall) / (Precision + Recall)
```

### Regression Metrics
```python
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

mse = mean_squared_error(y_test, predictions)
rmse = mean_squared_error(y_test, predictions, squared=False)
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)
```

## Feature Engineering

### Scaling
```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Standardization (mean=0, std=1)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)

# Normalization (0-1 range)
normalizer = MinMaxScaler()
X_normalized = normalizer.fit_transform(X_train)
```

### Encoding Categories
```python
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

# One-hot encoding
encoder = OneHotEncoder(sparse=False)
X_encoded = encoder.fit_transform(X_categorical)

# Label encoding
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)
```

### Handling Missing Values
```python
from sklearn.impute import SimpleImputer

# Mean imputation
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)
```

## Hyperparameter Tuning

### Grid Search
```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'max_depth': [3, 5, 7, 10],
    'min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(
    DecisionTreeClassifier(),
    param_grid,
    cv=5,
    scoring='accuracy'
)
grid_search.fit(X_train, y_train)
print(f"Best params: {grid_search.best_params_}")
```

### Random Search
```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint

param_distributions = {
    'max_depth': randint(1, 20),
    'min_samples_split': randint(2, 20)
}

random_search = RandomizedSearchCV(
    DecisionTreeClassifier(),
    param_distributions,
    n_iter=20,
    cv=5
)
random_search.fit(X_train, y_train)
```

## Pipeline Pattern

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', SVC())
])

pipeline.fit(X_train, y_train)
predictions = pipeline.predict(X_test)
```

## Quick Reference

### Algorithm Selection Guide
```
Small dataset, interpretability: Decision Tree
Medium dataset, good default: Random Forest
Large dataset, tabular: Gradient Boosting (XGBoost/LightGBM)
Need probability: Logistic Regression
High dimensions, few samples: SVM
```

### Evaluation Metric Selection
```
Balanced classes: Accuracy
Imbalanced classes: F1, Precision, Recall, AUC-ROC
Regression: RMSE, MAE, R²
Ranking: AUC-ROC, NDCG
```

## Related Topics
- [Unsupervised Learning](unsupervised_learning.md)
- [Linear Regression](linear_regression.md)
- [Model Evaluation](model_evaluation.md)
