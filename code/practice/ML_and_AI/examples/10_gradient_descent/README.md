# Gradient Descent

The fundamental optimization algorithm for machine learning.

## Concepts Covered

- **Batch Gradient Descent**: Use all data per update
- **Stochastic GD (SGD)**: Use one sample per update
- **Mini-batch GD**: Use small batches
- **Momentum**: Accelerate convergence
- **Learning Rate**: Step size control

## The Math

### Update Rule
```
θ = θ - α ∇J(θ)
```

### With Momentum
```
v = βv + α∇J(θ)
θ = θ - v
```

## Usage

```bash
python train.py
python train.py --variant sgd --lr 0.01
python inference.py
```

## Key Takeaways

1. **Learning Rate**: Too high = diverge, too low = slow
2. **Mini-batch**: Balance of speed and stability
3. **Momentum**: Helps escape local minima
4. **Convergence**: Monitor loss decrease
