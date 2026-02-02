# Loss Functions

Objective functions that neural networks minimize during training.

## Covered Loss Functions

### Regression
- **MSE**: Mean Squared Error
- **MAE**: Mean Absolute Error
- **Huber**: Smooth L1 (robust to outliers)

### Classification
- **BCE**: Binary Cross-Entropy
- **CE**: Cross-Entropy (multiclass)
- **Focal**: Focus on hard examples

## The Math

### MSE (L2 Loss)
```
L = (1/n) Σ(yᵢ - ŷᵢ)²
```

### Cross-Entropy
```
L = -Σ yᵢ log(ŷᵢ)
```

### Focal Loss
```
L = -αₜ(1 - pₜ)^γ log(pₜ)
```

## Usage

```bash
python train.py
python inference.py
```

## Key Takeaways

1. **Regression**: MSE penalizes large errors more than MAE
2. **Classification**: Cross-entropy is standard
3. **Imbalanced Data**: Use weighted loss or focal loss
4. **Outliers**: Use Huber or MAE instead of MSE
