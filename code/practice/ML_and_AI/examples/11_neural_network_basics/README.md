# Neural Network Basics

Multi-layer perceptron with forward and backward pass.

## Concepts Covered

- **Forward Pass**: Input -> Hidden -> Output
- **Backpropagation**: Gradient computation via chain rule
- **Weight Initialization**: Random, Xavier, He
- **Training Loop**: Forward, loss, backward, update

## Architecture

```
Input Layer -> Hidden Layer (ReLU) -> Output Layer (Softmax)
    [n]           [hidden]                [classes]
```

## The Math

### Forward Pass
```
z₁ = W₁x + b₁
a₁ = ReLU(z₁)
z₂ = W₂a₁ + b₂
ŷ = softmax(z₂)
```

### Backward Pass (Chain Rule)
```
∂L/∂W₂ = ∂L/∂ŷ · ∂ŷ/∂z₂ · ∂z₂/∂W₂
```

## Usage

```bash
python train.py
python train.py --hidden-size 64 --epochs 100
python inference.py
```

## Key Takeaways

1. **Depth**: More layers = more complex functions
2. **Width**: More neurons = more capacity
3. **Activation**: Non-linearity is essential
4. **Backprop**: Gradients flow backward through the network
