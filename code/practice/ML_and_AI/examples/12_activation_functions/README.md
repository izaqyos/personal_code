# Activation Functions

Non-linear functions that enable neural networks to learn complex patterns.

## Covered Activations

- **Sigmoid**: σ(x) = 1/(1+e^(-x))
- **Tanh**: tanh(x) = (e^x - e^(-x))/(e^x + e^(-x))
- **ReLU**: max(0, x)
- **Leaky ReLU**: max(αx, x)
- **GELU**: x·Φ(x) (Gaussian Error Linear Unit)
- **Softmax**: e^xᵢ / Σe^xⱼ

## Properties

| Function | Range | Gradient Issue | Use Case |
|----------|-------|----------------|----------|
| Sigmoid | (0,1) | Vanishing | Output (binary) |
| Tanh | (-1,1) | Vanishing | Hidden layers |
| ReLU | [0,∞) | Dying ReLU | Hidden (default) |
| Leaky ReLU | (-∞,∞) | None | Hidden layers |
| GELU | (-0.17,∞) | None | Transformers |
| Softmax | (0,1) | - | Output (multiclass) |

## Usage

```bash
python train.py
python inference.py
```

## Key Takeaways

1. **Non-linearity**: Without it, stacked layers = single linear layer
2. **Vanishing Gradients**: Sigmoid/Tanh problematic for deep networks
3. **ReLU**: Fast, simple, most common
4. **GELU**: Smoother than ReLU, used in Transformers
