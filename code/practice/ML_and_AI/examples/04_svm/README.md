# Support Vector Machines (SVM)

Maximum margin classifiers with kernel trick.

## Concepts Covered

- **Hyperplane**: Decision boundary
- **Margin**: Distance to nearest points
- **Support Vectors**: Points on the margin
- **Kernel Trick**: Non-linear boundaries (RBF, Polynomial)

## The Math

### Decision Function
```
f(x) = sign(w·x + b)
```

### Optimization (Soft Margin)
```
min (1/2)||w||² + C Σξᵢ
subject to: yᵢ(w·xᵢ + b) ≥ 1 - ξᵢ
```

### Kernels
- **Linear**: K(x,y) = x·y
- **RBF**: K(x,y) = exp(-γ||x-y||²)
- **Polynomial**: K(x,y) = (x·y + c)^d

## Usage

```bash
python train.py
python train.py --kernel rbf --C 1.0 --gamma scale
python inference.py
```

## Key Takeaways

1. **C Parameter**: Higher C = less regularization, tighter fit
2. **Gamma (RBF)**: Higher gamma = more complex boundaries
3. **Feature Scaling**: Absolutely essential for SVM
4. **Support Vectors**: Only these matter for the decision boundary
