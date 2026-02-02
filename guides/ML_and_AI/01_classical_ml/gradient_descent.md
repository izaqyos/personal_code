# Gradient Descent

Optimization algorithm for finding minimum of a function.

## Overview

Gradient descent iteratively moves toward the minimum by following the negative gradient.

```
w_new = w_old - learning_rate × gradient

Where:
  gradient = ∂Loss/∂w (direction of steepest increase)
  learning_rate = step size (α)
```

## Intuition

```
Imagine standing on a hill in fog:
1. Feel the slope at your feet
2. Take a step downhill
3. Repeat until flat (minimum)

The gradient tells you which way is uphill.
The negative gradient tells you which way is downhill.
```

## Basic Implementation

```python
import numpy as np

def gradient_descent(gradient_func, initial_w, learning_rate=0.01, iterations=1000):
    """
    Generic gradient descent.
    
    Args:
        gradient_func: Function that computes gradient at w
        initial_w: Starting point
        learning_rate: Step size
        iterations: Number of steps
    """
    w = initial_w
    history = [w]
    
    for _ in range(iterations):
        gradient = gradient_func(w)
        w = w - learning_rate * gradient
        history.append(w)
    
    return w, history

# Example: Minimize f(w) = w²
# Gradient: df/dw = 2w
gradient_func = lambda w: 2 * w
optimal_w, history = gradient_descent(gradient_func, initial_w=5.0)
print(f"Optimal w: {optimal_w}")  # Should be close to 0
```

## Linear Regression with Gradient Descent

```python
def linear_regression_gd(X, y, learning_rate=0.01, iterations=1000):
    """
    Linear regression using gradient descent.
    """
    m, n = X.shape
    w = np.zeros(n)
    b = 0
    losses = []
    
    for _ in range(iterations):
        # Forward pass
        y_pred = X @ w + b
        
        # Compute loss (MSE)
        loss = np.mean((y_pred - y) ** 2)
        losses.append(loss)
        
        # Compute gradients
        error = y_pred - y
        dw = (2/m) * X.T @ error
        db = (2/m) * np.sum(error)
        
        # Update parameters
        w = w - learning_rate * dw
        b = b - learning_rate * db
    
    return w, b, losses

# Example
X = np.random.randn(100, 3)
true_w = np.array([2, -1, 0.5])
y = X @ true_w + np.random.randn(100) * 0.1

w, b, losses = linear_regression_gd(X, y)
print(f"Learned weights: {w}")
print(f"True weights: {true_w}")
```

## Variants

### Batch Gradient Descent
Uses entire dataset for each update.

```python
for epoch in range(epochs):
    gradient = compute_gradient(X, y)  # All data
    w = w - learning_rate * gradient
```

**Pros:** Stable, guaranteed convergence (for convex)
**Cons:** Slow for large datasets

### Stochastic Gradient Descent (SGD)
Uses one sample per update.

```python
for epoch in range(epochs):
    indices = np.random.permutation(len(X))
    for i in indices:
        gradient = compute_gradient(X[i:i+1], y[i:i+1])  # One sample
        w = w - learning_rate * gradient
```

**Pros:** Fast updates, can escape local minima
**Cons:** Noisy, may never converge exactly

### Mini-Batch Gradient Descent
Uses small batches (best of both worlds).

```python
batch_size = 32

for epoch in range(epochs):
    indices = np.random.permutation(len(X))
    for start in range(0, len(X), batch_size):
        batch_indices = indices[start:start+batch_size]
        X_batch = X[batch_indices]
        y_batch = y[batch_indices]
        
        gradient = compute_gradient(X_batch, y_batch)
        w = w - learning_rate * gradient
```

**Pros:** Balances speed and stability, GPU efficient
**Cons:** Batch size is hyperparameter

## Learning Rate

Critical hyperparameter that controls step size.

```
Too small: Very slow convergence
Too large: May overshoot, diverge
Just right: Fast, stable convergence
```

### Finding Good Learning Rate

```python
# Learning rate finder (1cycle policy inspiration)
def find_learning_rate(model, X, y, start_lr=1e-7, end_lr=10, num_steps=100):
    lrs = np.exp(np.linspace(np.log(start_lr), np.log(end_lr), num_steps))
    losses = []
    
    initial_weights = model.get_weights()
    
    for lr in lrs:
        model.set_weights(initial_weights)
        # Train for a few steps
        loss = train_step(model, X, y, lr)
        losses.append(loss)
    
    # Plot and find where loss starts decreasing fastest
    # Good LR is usually 1/10 of where loss starts exploding
    return lrs, losses
```

## Advanced Optimizers

### Momentum
Accumulates gradient to accelerate convergence.

```python
def sgd_momentum(gradient_func, w, learning_rate=0.01, momentum=0.9, iterations=1000):
    velocity = np.zeros_like(w)
    
    for _ in range(iterations):
        gradient = gradient_func(w)
        velocity = momentum * velocity - learning_rate * gradient
        w = w + velocity
    
    return w
```

### RMSprop
Adapts learning rate per parameter.

```python
def rmsprop(gradient_func, w, learning_rate=0.01, decay=0.9, epsilon=1e-8, iterations=1000):
    cache = np.zeros_like(w)
    
    for _ in range(iterations):
        gradient = gradient_func(w)
        cache = decay * cache + (1 - decay) * gradient**2
        w = w - learning_rate * gradient / (np.sqrt(cache) + epsilon)
    
    return w
```

### Adam (Recommended)
Combines momentum and adaptive learning rates.

```python
def adam(gradient_func, w, learning_rate=0.001, beta1=0.9, beta2=0.999, 
         epsilon=1e-8, iterations=1000):
    m = np.zeros_like(w)  # First moment
    v = np.zeros_like(w)  # Second moment
    
    for t in range(1, iterations + 1):
        gradient = gradient_func(w)
        
        # Update moments
        m = beta1 * m + (1 - beta1) * gradient
        v = beta2 * v + (1 - beta2) * gradient**2
        
        # Bias correction
        m_hat = m / (1 - beta1**t)
        v_hat = v / (1 - beta2**t)
        
        # Update parameters
        w = w - learning_rate * m_hat / (np.sqrt(v_hat) + epsilon)
    
    return w
```

## Practical Tips

### Feature Scaling
Essential for gradient descent to work well.

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Now features have mean=0, std=1
# Gradients are more balanced across features
```

### Early Stopping
Prevent overfitting by monitoring validation loss.

```python
best_val_loss = float('inf')
patience = 10
patience_counter = 0

for epoch in range(max_epochs):
    train_loss = train_one_epoch(model, X_train, y_train)
    val_loss = evaluate(model, X_val, y_val)
    
    if val_loss < best_val_loss:
        best_val_loss = val_loss
        best_weights = model.get_weights()
        patience_counter = 0
    else:
        patience_counter += 1
        
    if patience_counter >= patience:
        print(f"Early stopping at epoch {epoch}")
        model.set_weights(best_weights)
        break
```

### Learning Rate Schedules

```python
# Step decay
def step_decay(epoch, initial_lr=0.01, drop=0.5, epochs_drop=10):
    return initial_lr * (drop ** (epoch // epochs_drop))

# Exponential decay
def exp_decay(epoch, initial_lr=0.01, decay_rate=0.01):
    return initial_lr * np.exp(-decay_rate * epoch)

# Cosine annealing
def cosine_anneal(epoch, initial_lr=0.01, min_lr=0.0001, total_epochs=100):
    return min_lr + (initial_lr - min_lr) * (1 + np.cos(np.pi * epoch / total_epochs)) / 2
```

## Convergence Visualization

```python
import matplotlib.pyplot as plt

def visualize_gd(losses, title="Gradient Descent Convergence"):
    plt.figure(figsize=(10, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(losses)
    plt.xlabel('Iteration')
    plt.ylabel('Loss')
    plt.title('Loss over iterations')
    
    plt.subplot(1, 2, 2)
    plt.plot(losses[:min(100, len(losses))])
    plt.xlabel('Iteration')
    plt.ylabel('Loss')
    plt.title('First 100 iterations')
    
    plt.tight_layout()
    plt.show()
```

## Quick Reference

```
Optimizer Selection:
  Default: Adam (lr=0.001)
  Simple: SGD with momentum (lr=0.01, momentum=0.9)
  Fine-tuning: SGD with lower lr

Learning Rate Guidelines:
  Adam: 0.001 (default)
  SGD: 0.01 - 0.1 (depends on problem)
  
Batch Size Guidelines:
  32-128: Good default
  Larger: More stable, slower per epoch
  Smaller: More noise, faster per epoch

Essential Preprocessing:
  - Normalize features (StandardScaler)
  - Initialize weights properly
  - Shuffle data each epoch
```

## Related Topics
- [Linear Regression](linear_regression.md)
- [Neural Networks](../02_deep_learning/neural_networks.md)
- [Backpropagation](../02_deep_learning/backpropagation.md)
