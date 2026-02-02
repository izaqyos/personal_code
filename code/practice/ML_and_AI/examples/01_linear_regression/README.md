# Linear Regression

Predict continuous values using linear relationships.

## Concepts Covered

- **Simple Linear Regression**: Single feature prediction
- **Multiple Linear Regression**: Multiple features
- **Regularization**: Ridge (L2), Lasso (L1), ElasticNet
- **Metrics**: MSE, RMSE, MAE, R²

## The Math

### Model
```
y = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ + ε
```

### Cost Function (MSE)
```
J(β) = (1/n) Σ(yᵢ - ŷᵢ)²
```

### Regularization
- **Ridge**: J(β) + λ Σβᵢ²
- **Lasso**: J(β) + λ Σ|βᵢ|

## Files

```
01_linear_regression/
├── README.md          # This file
├── train.py           # Train Linear, Ridge, Lasso models
├── inference.py       # Load model and predict
├── data/
│   ├── train.csv      # Training data (copy from shared)
│   └── test.csv       # Test data
└── model/
    └── model.joblib   # Saved model
```

## Usage

### Training
```bash
python train.py
# Or with options
python train.py --model ridge --alpha 1.0
```

### Inference
```bash
python inference.py
# Or with custom input
python inference.py --sqft 2000 --bedrooms 3 --bathrooms 2 --age 10 --garage 2
```

## Dataset

Housing prices with features:
- sqft: Square footage (800-4000)
- bedrooms: Number of bedrooms (1-5)
- bathrooms: Number of bathrooms (1-3)
- age: House age in years (0-50)
- garage: Garage capacity (0-2)
- **Target**: price

## Key Takeaways

1. **Feature Scaling**: Important for regularized models
2. **R² Interpretation**: 1.0 is perfect, 0.0 is baseline
3. **Ridge vs Lasso**: Ridge shrinks, Lasso can zero out features
4. **Overfitting**: Use regularization when R² differs train vs test
