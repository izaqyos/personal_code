# Linear Regression

> The foundation of predictive modeling - fitting a line to data.

---

## Overview

Linear regression models the relationship between features (X) and a continuous target (y) as a linear combination.

```
Simple:   y = wx + b
Multiple: y = w₁x₁ + w₂x₂ + ... + wₙxₙ + b

Where:
- y: predicted value
- w: weights (coefficients)
- x: features
- b: bias (intercept)
```

---

## Visual Intuition

```
y │
  │         ∘
  │       ∘    ∘    ← Data points
  │     ∘   ─────── ← Best fit line
  │   ∘  ───
  │ ∘ ──
  │────────────── x
```

**Goal**: Find the line that minimizes the distance between predictions and actual values.

---

## Mathematical Formulation

### Cost Function (Mean Squared Error)

```
J(w, b) = (1/2m) × Σᵢ (ŷᵢ - yᵢ)²

Where:
- m = number of samples
- ŷᵢ = predicted value
- yᵢ = actual value
```

### Matrix Form

```
y = Xw + b

Solution (Normal Equation):
w = (XᵀX)⁻¹Xᵀy
```

---

## Assumptions

Linear regression assumes:

1. **Linearity**: Relationship between X and y is linear
2. **Independence**: Observations are independent
3. **Homoscedasticity**: Constant variance of residuals
4. **Normality**: Residuals are normally distributed
5. **No multicollinearity**: Features are not highly correlated

```
Good residuals:          Bad residuals (heteroscedastic):
    │  ∘ ∘                    │     ∘
    │∘  ∘  ∘                  │   ∘ ∘ ∘
────┼─────────              ──┼────∘───∘──∘
    │ ∘ ∘  ∘                  │ ∘
    │  ∘                      │∘
```

---

## Regularization

Prevent overfitting by penalizing large weights:

### Ridge Regression (L2)

```
J(w) = MSE + λ × Σwᵢ²

- Shrinks weights toward zero
- Keeps all features
- Good when many features contribute
```

### Lasso Regression (L1)

```
J(w) = MSE + λ × Σ|wᵢ|

- Can zero out weights completely
- Performs feature selection
- Good for sparse solutions
```

### Elastic Net

```
J(w) = MSE + λ₁×Σ|wᵢ| + λ₂×Σwᵢ²

- Combines L1 and L2
- Best of both worlds
```

---

## Implementation

### From Scratch (NumPy)

```python
import numpy as np

class LinearRegression:
    def __init__(self, learning_rate=0.01, n_iterations=1000):
        self.lr = learning_rate
        self.n_iter = n_iterations
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0

        for _ in range(self.n_iter):
            y_pred = np.dot(X, self.weights) + self.bias

            # Gradients
            dw = (1/n_samples) * np.dot(X.T, (y_pred - y))
            db = (1/n_samples) * np.sum(y_pred - y)

            # Update
            self.weights -= self.lr * dw
            self.bias -= self.lr * db

    def predict(self, X):
        return np.dot(X, self.weights) + self.bias
```

### Using scikit-learn

```python
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train
model = LinearRegression()
model.fit(X_train, y_train)

# Predict & Evaluate
y_pred = model.predict(X_test)
print(f"MSE: {mean_squared_error(y_test, y_pred):.4f}")
print(f"R²: {r2_score(y_test, y_pred):.4f}")

# Coefficients
print(f"Weights: {model.coef_}")
print(f"Bias: {model.intercept_}")
```

---

## Polynomial Regression

Extend linear regression to capture non-linear relationships:

```python
from sklearn.preprocessing import PolynomialFeatures

# Original: [x]
# Degree 2: [1, x, x²]
# Degree 3: [1, x, x², x³]

poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)

model = LinearRegression()
model.fit(X_poly, y)
```

```
Linear:              Polynomial (degree 2):
  │                    │    ∘
  │    ∘  ∘            │  ∘   ∘
  │  ∘─────            │ ∘─────∘
  │∘──                 │∘       ∘
  └─────────           └──────────
```

---

## Feature Scaling

Important for gradient descent convergence:

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Standardization (zero mean, unit variance)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Min-Max (scale to [0, 1])
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)
```

---

## Exercises

1. **Implement**: Write the normal equation solution in NumPy
2. **Compare**: Train models with and without feature scaling. What happens?
3. **Regularization**: Train Ridge with different λ values. Plot weights vs λ
4. **Polynomial**: Fit degree 1, 3, and 10 polynomials. Which overfits?
5. **Diagnostics**: Plot residuals. Are assumptions violated?

---

## Key Takeaways

- Linear regression minimizes squared error
- Regularization prevents overfitting (Ridge=L2, Lasso=L1)
- Feature scaling helps gradient descent converge
- Polynomial features capture non-linear patterns
- Always check assumptions via residual analysis

---

## Next Steps

→ Continue to [03-logistic-regression.md](./03-logistic-regression.md)
