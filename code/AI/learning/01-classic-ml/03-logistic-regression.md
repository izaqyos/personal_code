# Logistic Regression

> Classification using probability - despite the name, it's for classification, not regression.

---

## Overview

Logistic regression predicts the probability that an input belongs to a class.

```
Linear Regression:    y = wx + b           (unbounded output)
Logistic Regression:  p = σ(wx + b)        (output in [0, 1])

Where σ is the sigmoid function:
σ(z) = 1 / (1 + e⁻ᶻ)
```

---

## The Sigmoid Function

```
         1.0 ──────────────────∘∘∘∘∘
             │               ∘∘
         0.5 │- - - - - - -∘- - - - -
             │            ∘∘
         0.0 ∘∘∘∘∘∘∘∘∘∘∘∘──────────────
            -6   -3    0    3    6
                       z
```

**Properties:**
- Output always between 0 and 1
- σ(0) = 0.5
- Smooth, differentiable (important for gradient descent)

---

## Decision Boundary

```
Class prediction:
ŷ = 1  if p ≥ 0.5  (σ(z) ≥ 0.5 → z ≥ 0)
ŷ = 0  if p < 0.5

Linear decision boundary where wx + b = 0:

  x₂│     Class 1
    │   ∘ ∘   ∘
    │  ∘  ∘ ∘
────┼────────────  ← Decision boundary (wx + b = 0)
    │  × × ×
    │ × ×  ×   Class 0
    └───────────── x₁
```

---

## Cost Function

Why not use MSE? Non-convex for logistic regression, leading to local minima.

### Binary Cross-Entropy (Log Loss)

```
J(w, b) = -(1/m) × Σ[yᵢ log(p̂ᵢ) + (1-yᵢ) log(1-p̂ᵢ)]

Intuition:
- If y=1: We want p̂ close to 1, so -log(p̂) is small
- If y=0: We want p̂ close to 0, so -log(1-p̂) is small
```

```
Cost when y=1:        Cost when y=0:
    │                     │
    │\                    │          /
cost│ \                cost│        /
    │  \__                │    ___/
    └───────── p̂         └───────── p̂
    0       1             0       1
```

---

## Gradient Descent Update

```
Gradient:
∂J/∂wⱼ = (1/m) × Σ(p̂ᵢ - yᵢ)xᵢⱼ

Update rule:
wⱼ := wⱼ - α × ∂J/∂wⱼ

Note: Same form as linear regression gradient!
```

---

## Implementation

### From Scratch

```python
import numpy as np

class LogisticRegression:
    def __init__(self, learning_rate=0.01, n_iterations=1000):
        self.lr = learning_rate
        self.n_iter = n_iterations
        self.weights = None
        self.bias = None

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-np.clip(z, -500, 500)))

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0

        for _ in range(self.n_iter):
            z = np.dot(X, self.weights) + self.bias
            p = self.sigmoid(z)

            # Gradients
            dw = (1/n_samples) * np.dot(X.T, (p - y))
            db = (1/n_samples) * np.sum(p - y)

            # Update
            self.weights -= self.lr * dw
            self.bias -= self.lr * db

    def predict_proba(self, X):
        z = np.dot(X, self.weights) + self.bias
        return self.sigmoid(z)

    def predict(self, X, threshold=0.5):
        return (self.predict_proba(X) >= threshold).astype(int)
```

### Using scikit-learn

```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

model = LogisticRegression(C=1.0, max_iter=1000)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]  # Probability of class 1

print(classification_report(y_test, y_pred))
```

---

## Multiclass Classification

### One-vs-Rest (OvR)

Train K binary classifiers, one per class:
```
Classifier 1: Class A vs (B, C)
Classifier 2: Class B vs (A, C)
Classifier 3: Class C vs (A, B)

Prediction: Class with highest probability
```

### Softmax (Multinomial)

Generalize sigmoid to multiple classes:

```
softmax(zᵢ) = e^zᵢ / Σⱼe^zⱼ

Output: Probability distribution over all classes
Sum of all probabilities = 1
```

```python
# scikit-learn handles this automatically
model = LogisticRegression(multi_class='multinomial', solver='lbfgs')
```

---

## Regularization

Same as linear regression:

```python
# L2 (default)
LogisticRegression(penalty='l2', C=1.0)  # C = 1/λ

# L1 (requires solver='liblinear' or 'saga')
LogisticRegression(penalty='l1', solver='saga', C=1.0)

# Elastic Net
LogisticRegression(penalty='elasticnet', solver='saga', l1_ratio=0.5)
```

---

## Threshold Tuning

Default threshold (0.5) may not be optimal:

```python
from sklearn.metrics import precision_recall_curve, roc_curve

# Find threshold that maximizes F1
precision, recall, thresholds = precision_recall_curve(y_test, y_prob)
f1_scores = 2 * (precision * recall) / (precision + recall + 1e-8)
best_threshold = thresholds[np.argmax(f1_scores)]

# Or based on business requirements
# High recall (catch all positives): lower threshold
# High precision (minimize false positives): higher threshold
```

---

## Exercises

1. **Derive**: Show that the gradient of binary cross-entropy is (p̂ - y)x
2. **Implement**: Add L2 regularization to the from-scratch implementation
3. **Tune**: Train on imbalanced data. Plot precision-recall curve and find optimal threshold
4. **Multiclass**: Implement softmax from scratch
5. **Interpret**: Train on interpretable data. What do the coefficients mean?

---

## Key Takeaways

- Logistic regression uses sigmoid to output probabilities
- Binary cross-entropy loss is convex (global minimum)
- Decision boundary is linear (wx + b = 0)
- Threshold can be tuned for precision/recall tradeoff
- Extends to multiclass via OvR or softmax

---

## Next Steps

→ Continue to [04-knn.md](./04-knn.md)
