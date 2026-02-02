# Linear Regression

Predicting continuous values with linear models.

## Overview

Linear regression models the relationship between features and target as a linear combination.

```
y = w₁x₁ + w₂x₂ + ... + wₙxₙ + b

Where:
  y = predicted value
  x = features
  w = weights (coefficients)
  b = bias (intercept)
```

## Simple Linear Regression

One feature predicting one target.

```python
import numpy as np
from sklearn.linear_model import LinearRegression

# Example: House size → Price
X = np.array([[1400], [1600], [1700], [1875], [1100], [1550]])
y = np.array([245000, 312000, 279000, 308000, 199000, 219000])

model = LinearRegression()
model.fit(X, y)

print(f"Coefficient (slope): {model.coef_[0]:.2f}")
print(f"Intercept: {model.intercept_:.2f}")
print(f"Equation: Price = {model.coef_[0]:.2f} × Size + {model.intercept_:.2f}")

# Predict
new_house = [[1650]]
predicted_price = model.predict(new_house)
print(f"Predicted price for 1650 sqft: ${predicted_price[0]:,.0f}")
```

## Multiple Linear Regression

Multiple features predicting target.

```python
# Multiple features: size, bedrooms, age
X = np.array([
    [1400, 3, 20],
    [1600, 3, 15],
    [1700, 4, 10],
    [1875, 4, 5],
    [1100, 2, 25],
])
y = np.array([245000, 312000, 279000, 308000, 199000])

model = LinearRegression()
model.fit(X, y)

print("Coefficients:")
for feature, coef in zip(['Size', 'Bedrooms', 'Age'], model.coef_):
    print(f"  {feature}: {coef:.2f}")
print(f"Intercept: {model.intercept_:.2f}")
```

## The Math Behind It

### Ordinary Least Squares (OLS)
Minimizes the sum of squared residuals:

```
Loss = Σ(yᵢ - ŷᵢ)² = Σ(yᵢ - (Xw + b))²

Solution (closed form):
w = (XᵀX)⁻¹Xᵀy
```

### Gradient Descent Alternative
For large datasets, iterative optimization:

```python
def gradient_descent(X, y, learning_rate=0.01, iterations=1000):
    m, n = X.shape
    w = np.zeros(n)
    b = 0
    
    for _ in range(iterations):
        y_pred = X @ w + b
        error = y_pred - y
        
        # Gradients
        dw = (2/m) * X.T @ error
        db = (2/m) * np.sum(error)
        
        # Update
        w -= learning_rate * dw
        b -= learning_rate * db
    
    return w, b
```

## Assumptions

Linear regression assumes:

1. **Linearity**: Relationship is linear
2. **Independence**: Observations are independent
3. **Homoscedasticity**: Constant variance of errors
4. **Normality**: Errors are normally distributed
5. **No multicollinearity**: Features aren't highly correlated

### Checking Assumptions

```python
import matplotlib.pyplot as plt
from scipy import stats

# Fit model
model = LinearRegression()
model.fit(X, y)
predictions = model.predict(X)
residuals = y - predictions

# 1. Residuals vs Fitted (linearity, homoscedasticity)
plt.scatter(predictions, residuals)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('Fitted values')
plt.ylabel('Residuals')
plt.title('Residuals vs Fitted')

# 2. Q-Q plot (normality)
stats.probplot(residuals, plot=plt)

# 3. Check for multicollinearity (VIF)
from statsmodels.stats.outliers_influence import variance_inflation_factor

vif_data = []
for i in range(X.shape[1]):
    vif = variance_inflation_factor(X, i)
    vif_data.append(vif)
print(f"VIF scores: {vif_data}")  # VIF > 5 indicates multicollinearity
```

## Regularization

Prevent overfitting by penalizing large weights.

### Ridge Regression (L2)
```python
from sklearn.linear_model import Ridge

# L2 penalty: adds λ × Σw²
ridge = Ridge(alpha=1.0)
ridge.fit(X, y)
```

### Lasso Regression (L1)
```python
from sklearn.linear_model import Lasso

# L1 penalty: adds λ × Σ|w|
# Drives some coefficients to exactly 0 (feature selection)
lasso = Lasso(alpha=0.1)
lasso.fit(X, y)

# Check which features were selected
for feature, coef in zip(feature_names, lasso.coef_):
    if coef != 0:
        print(f"{feature}: {coef:.4f}")
```

### Elastic Net
```python
from sklearn.linear_model import ElasticNet

# Combination of L1 and L2
elastic = ElasticNet(alpha=0.1, l1_ratio=0.5)
elastic.fit(X, y)
```

## Polynomial Regression

Capture non-linear relationships.

```python
from sklearn.preprocessing import PolynomialFeatures

# Create polynomial features
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)

# Fit linear model on polynomial features
model = LinearRegression()
model.fit(X_poly, y)
```

## Evaluation Metrics

```python
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

predictions = model.predict(X_test)

# Mean Squared Error
mse = mean_squared_error(y_test, predictions)
print(f"MSE: {mse:.2f}")

# Root Mean Squared Error (same units as target)
rmse = np.sqrt(mse)
print(f"RMSE: {rmse:.2f}")

# Mean Absolute Error
mae = mean_absolute_error(y_test, predictions)
print(f"MAE: {mae:.2f}")

# R² Score (coefficient of determination)
r2 = r2_score(y_test, predictions)
print(f"R²: {r2:.4f}")
```

### Interpreting R²
```
R² = 1 - (SS_res / SS_tot)

Where:
  SS_res = Σ(y - ŷ)² (residual sum of squares)
  SS_tot = Σ(y - ȳ)² (total sum of squares)

R² = 0: Model explains nothing (predicting mean)
R² = 1: Perfect predictions
R² < 0: Model worse than predicting mean
```

## Feature Importance

```python
# Standardize features first for fair comparison
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = LinearRegression()
model.fit(X_scaled, y)

# Now coefficients are comparable
importance = pd.DataFrame({
    'Feature': feature_names,
    'Coefficient': model.coef_,
    'Abs_Coefficient': np.abs(model.coef_)
}).sort_values('Abs_Coefficient', ascending=False)

print(importance)
```

## Complete Example

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score

# Load data
df = pd.read_csv('housing.csv')
X = df.drop('price', axis=1)
y = df['price']

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('regressor', Ridge(alpha=1.0))
])

# Cross-validation
cv_scores = cross_val_score(pipeline, X_train, y_train, 
                           cv=5, scoring='neg_mean_squared_error')
print(f"CV RMSE: {np.sqrt(-cv_scores.mean()):.2f}")

# Final training
pipeline.fit(X_train, y_train)

# Evaluate
predictions = pipeline.predict(X_test)
print(f"Test RMSE: {np.sqrt(mean_squared_error(y_test, predictions)):.2f}")
print(f"Test R²: {r2_score(y_test, predictions):.4f}")
```

## When to Use

**Use Linear Regression when:**
- Relationship appears linear
- Interpretability is important
- Baseline model needed
- Few features relative to samples

**Consider alternatives when:**
- Non-linear relationships (→ Polynomial, Trees)
- Many irrelevant features (→ Lasso)
- Multicollinearity (→ Ridge, PCA)
- Outliers present (→ Robust regression)

## Quick Reference

```python
# Basic
LinearRegression()

# With L2 regularization
Ridge(alpha=1.0)

# With L1 regularization (feature selection)
Lasso(alpha=0.1)

# Combined
ElasticNet(alpha=0.1, l1_ratio=0.5)

# Key metrics
r2_score(y_true, y_pred)  # -∞ to 1, higher better
mean_squared_error(y_true, y_pred)  # 0 to ∞, lower better
```

## Related Topics
- [Gradient Descent](gradient_descent.md)
- [Supervised Learning](supervised_learning.md)
- [Model Evaluation](model_evaluation.md)
