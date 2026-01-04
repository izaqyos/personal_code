# Perceptrons and Neural Network Basics

> From biological neurons to artificial intelligence.

---

## Biological Inspiration

```
Biological Neuron:                Artificial Neuron:

    Dendrites                        Inputs
       │ │ │                          x₁ ──w₁──┐
       ▼ ▼ ▼                          x₂ ──w₂──┼──→ Σ ──→ f(z) ──→ output
   ┌─────────┐                        x₃ ──w₃──┘      │
   │  Soma   │─── Axon ───→                          bias
   │ (cell)  │
   └─────────┘

Biological:                          Artificial:
- Dendrites receive signals         - Inputs × weights
- Soma processes/sums               - Weighted sum
- Fires if threshold reached        - Activation function
- Axon transmits to next neuron     - Output to next layer
```

---

## The Perceptron (Single Neuron)

Simplest neural network - binary linear classifier:

```
       x₁ ─────w₁─────┐
                       │
       x₂ ─────w₂─────┼───→ Σ + b ───→ step(z) ───→ ŷ
                       │
       x₃ ─────w₃─────┘

z = w₁x₁ + w₂x₂ + w₃x₃ + b = wᵀx + b

step(z) = { 1  if z ≥ 0
          { 0  if z < 0
```

### Learning Rule

```
For each training example (x, y):
    ŷ = step(wᵀx + b)
    error = y - ŷ
    w = w + α × error × x
    b = b + α × error
```

---

## Multi-Layer Perceptron (MLP)

Stack neurons in layers to learn non-linear patterns:

```
Input Layer    Hidden Layer(s)    Output Layer

   x₁ ─────────┐   ┌─────────┐   ┌───────→ ŷ₁
               ├──→│ neuron  │──→│
   x₂ ─────────┤   ├─────────┤   ├───────→ ŷ₂
               ├──→│ neuron  │──→│
   x₃ ─────────┤   ├─────────┤   └───────→ ŷ₃
               └──→│ neuron  │
                   └─────────┘

Each connection has a weight
Each neuron applies: activation(Σ(wᵢxᵢ) + b)
```

### Forward Pass

```
Layer 1:  z⁽¹⁾ = W⁽¹⁾x + b⁽¹⁾
          a⁽¹⁾ = f(z⁽¹⁾)

Layer 2:  z⁽²⁾ = W⁽²⁾a⁽¹⁾ + b⁽²⁾
          a⁽²⁾ = f(z⁽²⁾)

...continue for all layers...

Output:   ŷ = a⁽L⁾
```

---

## Why Hidden Layers?

Single perceptron can only learn linear boundaries:

```
Perceptron (linear):         MLP (non-linear):

   │  ∘ ∘ ∘                     │  ∘ ∘ ∘
   │ ∘────────                  │ ∘ ╭───╮
   │────────×                   │───╯   ╰──×
   │ × × ×                      │ × × ×
   └─────────                   └─────────

Can't solve XOR!              Can learn any shape
```

**Universal Approximation Theorem**: A single hidden layer with enough neurons can approximate any continuous function.

---

## Implementation

### From Scratch (NumPy)

```python
import numpy as np

class MLP:
    def __init__(self, layer_sizes):
        """
        layer_sizes: [input_size, hidden1, hidden2, ..., output_size]
        """
        self.weights = []
        self.biases = []

        for i in range(len(layer_sizes) - 1):
            # Xavier initialization
            w = np.random.randn(layer_sizes[i], layer_sizes[i+1]) * np.sqrt(2.0 / layer_sizes[i])
            b = np.zeros((1, layer_sizes[i+1]))
            self.weights.append(w)
            self.biases.append(b)

    def relu(self, z):
        return np.maximum(0, z)

    def relu_derivative(self, z):
        return (z > 0).astype(float)

    def softmax(self, z):
        exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))
        return exp_z / np.sum(exp_z, axis=1, keepdims=True)

    def forward(self, X):
        self.activations = [X]
        self.z_values = []

        for i, (w, b) in enumerate(zip(self.weights, self.biases)):
            z = self.activations[-1] @ w + b
            self.z_values.append(z)

            if i == len(self.weights) - 1:  # Output layer
                a = self.softmax(z)
            else:  # Hidden layers
                a = self.relu(z)

            self.activations.append(a)

        return self.activations[-1]

    def backward(self, y_true):
        m = y_true.shape[0]
        self.gradients_w = []
        self.gradients_b = []

        # Output layer gradient (cross-entropy + softmax)
        delta = self.activations[-1] - y_true

        for i in reversed(range(len(self.weights))):
            grad_w = self.activations[i].T @ delta / m
            grad_b = np.mean(delta, axis=0, keepdims=True)

            self.gradients_w.insert(0, grad_w)
            self.gradients_b.insert(0, grad_b)

            if i > 0:
                delta = (delta @ self.weights[i].T) * self.relu_derivative(self.z_values[i-1])

    def update(self, learning_rate):
        for i in range(len(self.weights)):
            self.weights[i] -= learning_rate * self.gradients_w[i]
            self.biases[i] -= learning_rate * self.gradients_b[i]

    def train(self, X, y, epochs=100, lr=0.01):
        for epoch in range(epochs):
            # Forward
            predictions = self.forward(X)

            # Backward
            self.backward(y)

            # Update
            self.update(lr)

            if epoch % 10 == 0:
                loss = -np.mean(np.sum(y * np.log(predictions + 1e-8), axis=1))
                print(f"Epoch {epoch}, Loss: {loss:.4f}")
```

### Using PyTorch

```python
import torch
import torch.nn as nn

class MLP(nn.Module):
    def __init__(self, input_size, hidden_sizes, output_size):
        super().__init__()

        layers = []
        prev_size = input_size

        for hidden_size in hidden_sizes:
            layers.append(nn.Linear(prev_size, hidden_size))
            layers.append(nn.ReLU())
            prev_size = hidden_size

        layers.append(nn.Linear(prev_size, output_size))

        self.network = nn.Sequential(*layers)

    def forward(self, x):
        return self.network(x)

# Usage
model = MLP(input_size=784, hidden_sizes=[256, 128], output_size=10)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Training loop
for epoch in range(epochs):
    for batch_x, batch_y in dataloader:
        optimizer.zero_grad()
        outputs = model(batch_x)
        loss = criterion(outputs, batch_y)
        loss.backward()
        optimizer.step()
```

---

## Key Hyperparameters

| Parameter | Description | Typical Values |
|-----------|-------------|----------------|
| Hidden layers | Depth of network | 1-5 for MLPs |
| Neurons per layer | Width of network | 64-1024 |
| Learning rate | Step size | 0.001-0.01 |
| Batch size | Samples per update | 32-256 |
| Epochs | Training iterations | 10-1000 |

---

## Exercises

1. **Implement**: Build a perceptron that learns AND, OR gates
2. **XOR**: Show that single perceptron fails on XOR, but 2-layer MLP succeeds
3. **Architecture**: Train MLPs with 1, 2, 3 hidden layers. Compare learning curves
4. **Width vs Depth**: Compare [100] vs [50, 50] vs [33, 33, 34] architectures
5. **MNIST**: Train MLP on MNIST digit classification

---

## Key Takeaways

- Perceptrons are single neurons with linear decision boundaries
- MLPs stack layers to learn non-linear patterns
- Forward pass: input → weighted sums → activations → output
- Universal approximation: can learn any function with enough neurons
- Foundation for all deep learning

---

## Next Steps

→ Continue to [02-backpropagation.md](./02-backpropagation.md)
