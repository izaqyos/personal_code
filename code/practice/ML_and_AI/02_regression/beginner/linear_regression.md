# Linear Regression Practice - Beginner

Predict continuous values using linear regression.

## Learning Objectives
- Understand regression vs classification
- Train and evaluate linear regression models
- Interpret coefficients and metrics

## Setup

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
```

---

## Exercise 1: Simple Linear Regression

Predict house price from size.

```python
# Generate sample data
np.random.seed(42)
size = np.random.uniform(1000, 3000, 100)  # Square feet
price = 50000 + 100 * size + np.random.normal(0, 20000, 100)  # Price

# TODO: Reshape size for sklearn (needs 2D array)
X = # Your code here

# TODO: Split into train/test
X_train, X_test, y_train, y_test = # Your code here

# TODO: Create and train LinearRegression model

# TODO: Print coefficient (slope) and intercept

# TODO: Make predictions on test set

# TODO: Plot: actual vs predicted
```

<details>
<summary>Solution</summary>

```python
np.random.seed(42)
size = np.random.uniform(1000, 3000, 100)
price = 50000 + 100 * size + np.random.normal(0, 20000, 100)

X = size.reshape(-1, 1)
y = price

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

print(f"Coefficient (price per sqft): ${model.coef_[0]:.2f}")
print(f"Intercept: ${model.intercept_:.2f}")
print(f"Formula: Price = {model.coef_[0]:.2f} × Size + {model.intercept_:.2f}")

predictions = model.predict(X_test)

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.scatter(X_test, y_test, alpha=0.7, label='Actual')
plt.plot(X_test, predictions, color='red', label='Predicted')
plt.xlabel('Size (sqft)')
plt.ylabel('Price ($)')
plt.legend()

plt.subplot(1, 2, 2)
plt.scatter(y_test, predictions, alpha=0.7)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.xlabel('Actual Price')
plt.ylabel('Predicted Price')
plt.title('Actual vs Predicted')
plt.tight_layout()
plt.show()
```
</details>

---

## Exercise 2: Evaluate Regression Model

Calculate and interpret regression metrics.

```python
# Using model from Exercise 1

# TODO: Calculate Mean Squared Error (MSE)

# TODO: Calculate Root Mean Squared Error (RMSE)

# TODO: Calculate Mean Absolute Error (MAE)

# TODO: Calculate R² score

# TODO: Interpret: What does R² = 0.8 mean?
```

<details>
<summary>Solution</summary>

```python
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

mse = mean_squared_error(y_test, predictions)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("Regression Metrics:")
print(f"MSE:  ${mse:,.0f}")
print(f"RMSE: ${rmse:,.0f}")
print(f"MAE:  ${mae:,.0f}")
print(f"R²:   {r2:.4f}")

print(f"\nInterpretation:")
print(f"- RMSE of ${rmse:,.0f} means average error is about ${rmse:,.0f}")
print(f"- R² of {r2:.2%} means model explains {r2:.0%} of price variance")
```
</details>

---

## Exercise 3: Multiple Linear Regression

Predict price using multiple features.

```python
# Generate multi-feature data
np.random.seed(42)
n = 200

data = {
    'size': np.random.uniform(1000, 3000, n),
    'bedrooms': np.random.randint(2, 6, n),
    'age': np.random.uniform(0, 50, n),
    'distance_to_city': np.random.uniform(1, 30, n)
}
df = pd.DataFrame(data)

# True relationship
df['price'] = (
    50000 + 
    100 * df['size'] + 
    10000 * df['bedrooms'] - 
    500 * df['age'] - 
    2000 * df['distance_to_city'] + 
    np.random.normal(0, 20000, n)
)

# TODO: Prepare features and target
X = # Select all columns except 'price'
y = # Select 'price' column

# TODO: Split data

# TODO: Train model

# TODO: Print coefficients for each feature

# TODO: Which feature has the most impact?
```

<details>
<summary>Solution</summary>

```python
X = df[['size', 'bedrooms', 'age', 'distance_to_city']]
y = df['price']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

print("Feature Coefficients:")
for feature, coef in zip(X.columns, model.coef_):
    sign = '+' if coef >= 0 else ''
    print(f"  {feature:20}: {sign}{coef:,.2f}")
print(f"  {'Intercept':20}: {model.intercept_:,.2f}")

# Feature importance by absolute coefficient
importance = pd.DataFrame({
    'Feature': X.columns,
    'Coefficient': model.coef_,
    'Abs_Coefficient': np.abs(model.coef_)
}).sort_values('Abs_Coefficient', ascending=False)

print("\nFeature Importance (by absolute coefficient):")
print(importance)

# Evaluate
predictions = model.predict(X_test)
print(f"\nR² Score: {r2_score(y_test, predictions):.4f}")
print(f"RMSE: ${np.sqrt(mean_squared_error(y_test, predictions)):,.0f}")
```
</details>

---

## Exercise 4: Feature Scaling Impact

Compare model with and without feature scaling.

```python
from sklearn.preprocessing import StandardScaler

# TODO: Train model WITHOUT scaling (already done above)

# TODO: Scale features using StandardScaler

# TODO: Train model WITH scaled features

# TODO: Compare coefficients - what changed?

# TODO: Compare R² scores - are they the same?
```

<details>
<summary>Solution</summary>

```python
from sklearn.preprocessing import StandardScaler

# Without scaling
model_unscaled = LinearRegression()
model_unscaled.fit(X_train, y_train)
r2_unscaled = model_unscaled.score(X_test, y_test)

print("Without Scaling:")
print(f"Coefficients: {model_unscaled.coef_}")
print(f"R²: {r2_unscaled:.4f}")

# With scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model_scaled = LinearRegression()
model_scaled.fit(X_train_scaled, y_train)
r2_scaled = model_scaled.score(X_test_scaled, y_test)

print("\nWith Scaling:")
print(f"Coefficients: {model_scaled.coef_}")
print(f"R²: {r2_scaled:.4f}")

print("\nKey Observations:")
print("1. R² scores are identical (scaling doesn't change predictions)")
print("2. Scaled coefficients are now comparable in magnitude")
print("3. Larger scaled coefficient = more important feature")

# Compare feature importance
print("\nScaled Feature Importance:")
for feature, coef in sorted(zip(X.columns, np.abs(model_scaled.coef_)), 
                             key=lambda x: -x[1]):
    print(f"  {feature}: {coef:.2f}")
```
</details>

---

## Exercise 5: Polynomial Regression

Handle non-linear relationships.

```python
from sklearn.preprocessing import PolynomialFeatures

# Generate non-linear data
np.random.seed(42)
X = np.linspace(0, 10, 100).reshape(-1, 1)
y = 3 * X.flatten()**2 - 2 * X.flatten() + 5 + np.random.normal(0, 10, 100)

# TODO: Split data

# TODO: Fit linear regression and calculate R²

# TODO: Create polynomial features (degree=2)

# TODO: Fit polynomial regression and calculate R²

# TODO: Plot both fits
```

<details>
<summary>Solution</summary>

```python
from sklearn.preprocessing import PolynomialFeatures

np.random.seed(42)
X = np.linspace(0, 10, 100).reshape(-1, 1)
y = 3 * X.flatten()**2 - 2 * X.flatten() + 5 + np.random.normal(0, 10, 100)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Linear
linear = LinearRegression()
linear.fit(X_train, y_train)
linear_r2 = linear.score(X_test, y_test)

# Polynomial (degree 2)
poly = PolynomialFeatures(degree=2, include_bias=False)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)

poly_model = LinearRegression()
poly_model.fit(X_train_poly, y_train)
poly_r2 = poly_model.score(X_test_poly, y_test)

print(f"Linear R²: {linear_r2:.4f}")
print(f"Polynomial R²: {poly_r2:.4f}")

# Plot
plt.figure(figsize=(10, 5))
X_plot = np.linspace(0, 10, 100).reshape(-1, 1)

plt.scatter(X, y, alpha=0.5, label='Data')
plt.plot(X_plot, linear.predict(X_plot), 'r-', label=f'Linear (R²={linear_r2:.3f})')
plt.plot(X_plot, poly_model.predict(poly.transform(X_plot)), 'g-', 
         label=f'Polynomial (R²={poly_r2:.3f})')
plt.xlabel('X')
plt.ylabel('y')
plt.legend()
plt.title('Linear vs Polynomial Regression')
plt.show()
```
</details>

---

## Exercise 6: Regularization

Prevent overfitting with Ridge and Lasso.

```python
from sklearn.linear_model import Ridge, Lasso

# Use the multi-feature housing data from Exercise 3

# TODO: Train Ridge regression with alpha=1.0

# TODO: Train Lasso regression with alpha=1.0

# TODO: Compare coefficients between Linear, Ridge, and Lasso

# TODO: What happens to coefficients as alpha increases?
```

<details>
<summary>Solution</summary>

```python
from sklearn.linear_model import Ridge, Lasso

# Prepare data
X = df[['size', 'bedrooms', 'age', 'distance_to_city']]
y = df['price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features for regularization
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train models
linear = LinearRegression().fit(X_train_scaled, y_train)
ridge = Ridge(alpha=1.0).fit(X_train_scaled, y_train)
lasso = Lasso(alpha=1000).fit(X_train_scaled, y_train)

# Compare coefficients
print("Coefficient Comparison (scaled features):")
print(f"{'Feature':20} {'Linear':>12} {'Ridge':>12} {'Lasso':>12}")
print("-" * 58)
for i, feature in enumerate(X.columns):
    print(f"{feature:20} {linear.coef_[i]:12.2f} {ridge.coef_[i]:12.2f} {lasso.coef_[i]:12.2f}")

# Effect of alpha
print("\nLasso Coefficients vs Alpha:")
for alpha in [100, 1000, 5000, 10000]:
    lasso_temp = Lasso(alpha=alpha).fit(X_train_scaled, y_train)
    print(f"Alpha={alpha:5}: {lasso_temp.coef_}")
```
</details>

---

## Key Takeaways

1. **Linear regression** predicts continuous values using weighted features
2. **R² score** tells you how much variance your model explains
3. **RMSE** gives error in the same units as your target
4. **Feature scaling** doesn't change predictions but helps interpret coefficients
5. **Polynomial features** can capture non-linear relationships
6. **Regularization** prevents overfitting by shrinking coefficients

## Quick Reference

```python
# Linear Regression
model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)

# Metrics
from sklearn.metrics import mean_squared_error, r2_score
rmse = np.sqrt(mean_squared_error(y_test, predictions))
r2 = r2_score(y_test, predictions)

# Regularization
from sklearn.linear_model import Ridge, Lasso
ridge = Ridge(alpha=1.0)  # L2 penalty
lasso = Lasso(alpha=1.0)  # L1 penalty (can zero coefficients)
```

## Next Steps
- Try [Intermediate: Regularization Deep Dive](../intermediate/regularization.md)
- Learn about [Classification](../../03_classification/beginner/logistic_regression.md)
