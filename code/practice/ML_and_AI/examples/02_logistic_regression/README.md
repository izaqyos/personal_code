# Logistic Regression

Binary and multiclass classification using logistic regression.

## Concepts Covered

- **Sigmoid Function**: Maps values to [0, 1]
- **Binary Classification**: Two classes (0/1)
- **Multiclass**: One-vs-Rest (OvR), Softmax
- **Decision Boundary**: Threshold selection
- **Metrics**: Accuracy, Precision, Recall, F1, ROC-AUC

## The Math

### Sigmoid Function
```
σ(z) = 1 / (1 + e^(-z))
```

### Model
```
P(y=1|x) = σ(β₀ + β₁x₁ + ... + βₙxₙ)
```

### Binary Cross-Entropy Loss
```
L = -[y·log(ŷ) + (1-y)·log(1-ŷ)]
```

## Files

```
02_logistic_regression/
├── README.md          # This file
├── train.py           # Train logistic regression
├── inference.py       # Load model and predict
└── model/
    └── model.joblib   # Saved model
```

## Usage

### Training
```bash
python train.py
python train.py --threshold 0.3  # Custom decision threshold
```

### Inference
```bash
python inference.py
```

## Dataset

Customer churn prediction:
- tenure: Months as customer
- monthly_charges: Monthly bill amount
- total_charges: Total billed
- contract: Month-to-month, one_year, two_year
- internet_service: DSL, fiber, none
- **Target**: churn (0=stayed, 1=churned)

## Key Takeaways

1. **Threshold Matters**: 0.5 is not always optimal
2. **Class Imbalance**: Use class_weight='balanced'
3. **Feature Encoding**: Categorical -> One-hot or Label encoding
4. **ROC-AUC**: Best single metric for binary classification
