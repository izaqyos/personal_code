# Neural Networks Introduction

From perceptrons to multi-layer networks.

## Overview

Neural networks are composed of interconnected nodes (neurons) organized in layers.

```
Input → Hidden Layer(s) → Output

Each connection has a weight.
Each neuron applies an activation function.
```

## The Perceptron

Simplest neural network: single neuron.

```python
import numpy as np

def perceptron(x, weights, bias):
    """
    Single neuron computation.
    """
    z = np.dot(x, weights) + bias
    return 1 if z > 0 else 0  # Step activation

# Example: AND gate
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([0, 0, 0, 1])

# Weights that implement AND
weights = np.array([0.5, 0.5])
bias = -0.7

for x, target in zip(X, y):
    prediction = perceptron(x, weights, bias)
    print(f"{x} → {prediction} (target: {target})")
```

### Perceptron Learning

```python
def train_perceptron(X, y, learning_rate=0.1, epochs=100):
    n_features = X.shape[1]
    weights = np.zeros(n_features)
    bias = 0
    
    for _ in range(epochs):
        for x, target in zip(X, y):
            prediction = 1 if np.dot(x, weights) + bias > 0 else 0
            error = target - prediction
            
            # Update weights
            weights += learning_rate * error * x
            bias += learning_rate * error
    
    return weights, bias
```

## Multi-Layer Perceptron (MLP)

Multiple layers enable learning non-linear patterns.

```
Input Layer     Hidden Layer     Output Layer
   (n)              (h)              (m)
   
   o  ─┐        ┌─  o  ─┐        ┌─  o
      ├──  W1  ─┼→     ├──  W2  ─┼→
   o  ─┤        ├─  o  ─┤        ├─  o
      ├────────┼→     ├────────┼→
   o  ─┘        └─  o  ─┘        └─  o
```

```python
from sklearn.neural_network import MLPClassifier, MLPRegressor

# Classification
mlp = MLPClassifier(
    hidden_layer_sizes=(100, 50),  # 2 hidden layers
    activation='relu',
    solver='adam',
    max_iter=500
)
mlp.fit(X_train, y_train)
predictions = mlp.predict(X_test)

# Regression
mlp_reg = MLPRegressor(
    hidden_layer_sizes=(100,),
    activation='relu',
    solver='adam'
)
```

## Activation Functions

```python
import numpy as np

# Sigmoid: Output between 0 and 1
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

# Tanh: Output between -1 and 1
def tanh(z):
    return np.tanh(z)

# ReLU: Most popular for hidden layers
def relu(z):
    return np.maximum(0, z)

# Softmax: For multi-class output
def softmax(z):
    exp_z = np.exp(z - np.max(z))  # Numerical stability
    return exp_z / exp_z.sum()
```

### When to Use Each

```
Hidden layers:
  - ReLU: Default choice, fast training
  - LeakyReLU: When dead neurons are a problem
  - Tanh: Sometimes for RNNs

Output layer:
  - Sigmoid: Binary classification
  - Softmax: Multi-class classification
  - Linear (none): Regression
```

## Forward Propagation

```python
def forward_propagation(X, weights, biases):
    """
    Forward pass through network.
    """
    activations = [X]
    
    for w, b in zip(weights[:-1], biases[:-1]):
        z = activations[-1] @ w + b
        a = relu(z)  # Hidden layer activation
        activations.append(a)
    
    # Output layer
    z = activations[-1] @ weights[-1] + biases[-1]
    output = sigmoid(z)  # For binary classification
    
    return output, activations
```

## Backpropagation (Conceptual)

```
1. Forward pass: Compute predictions
2. Compute loss: How wrong were we?
3. Backward pass: Compute gradients using chain rule
4. Update weights: Move in direction that reduces loss
```

```python
def backpropagation_step(X, y, weights, biases, learning_rate):
    """
    Simplified backpropagation for single layer.
    """
    # Forward pass
    z = X @ weights + biases
    predictions = sigmoid(z)
    
    # Compute loss gradient
    error = predictions - y
    
    # Compute gradients
    dw = X.T @ error / len(X)
    db = np.mean(error)
    
    # Update weights
    weights -= learning_rate * dw
    biases -= learning_rate * db
    
    return weights, biases
```

## Loss Functions

```python
# Binary Cross-Entropy (classification)
def binary_cross_entropy(y_true, y_pred, epsilon=1e-15):
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
    return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))

# Categorical Cross-Entropy (multi-class)
def categorical_cross_entropy(y_true, y_pred, epsilon=1e-15):
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
    return -np.mean(np.sum(y_true * np.log(y_pred), axis=1))

# Mean Squared Error (regression)
def mse(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)
```

## Weight Initialization

```python
# Xavier/Glorot (for tanh/sigmoid)
def xavier_init(n_in, n_out):
    return np.random.randn(n_in, n_out) * np.sqrt(2.0 / (n_in + n_out))

# He (for ReLU)
def he_init(n_in, n_out):
    return np.random.randn(n_in, n_out) * np.sqrt(2.0 / n_in)
```

## Regularization

### Dropout
Randomly zero out neurons during training.

```python
from sklearn.neural_network import MLPClassifier

# Sklearn uses alpha for L2 regularization
mlp = MLPClassifier(
    hidden_layer_sizes=(100,),
    alpha=0.001  # L2 penalty
)
```

### Early Stopping

```python
mlp = MLPClassifier(
    hidden_layer_sizes=(100,),
    early_stopping=True,
    validation_fraction=0.1,
    n_iter_no_change=10
)
```

## Complete Example with Sklearn

```python
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report

# Prepare data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Pipeline with scaling (essential for neural networks!)
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('mlp', MLPClassifier(max_iter=500, random_state=42))
])

# Hyperparameter tuning
param_grid = {
    'mlp__hidden_layer_sizes': [(50,), (100,), (50, 50), (100, 50)],
    'mlp__activation': ['relu', 'tanh'],
    'mlp__alpha': [0.0001, 0.001, 0.01],
    'mlp__learning_rate_init': [0.001, 0.01]
}

grid_search = GridSearchCV(pipeline, param_grid, cv=5, n_jobs=-1)
grid_search.fit(X_train, y_train)

print(f"Best parameters: {grid_search.best_params_}")
print(f"Best CV score: {grid_search.best_score_:.3f}")

# Evaluate
predictions = grid_search.predict(X_test)
print(classification_report(y_test, predictions))
```

## From Scratch: Simple Network

```python
class SimpleNeuralNetwork:
    def __init__(self, layer_sizes):
        self.weights = []
        self.biases = []
        
        for i in range(len(layer_sizes) - 1):
            w = np.random.randn(layer_sizes[i], layer_sizes[i+1]) * 0.1
            b = np.zeros((1, layer_sizes[i+1]))
            self.weights.append(w)
            self.biases.append(b)
    
    def relu(self, z):
        return np.maximum(0, z)
    
    def relu_derivative(self, z):
        return (z > 0).astype(float)
    
    def sigmoid(self, z):
        return 1 / (1 + np.exp(-np.clip(z, -500, 500)))
    
    def forward(self, X):
        self.activations = [X]
        self.z_values = []
        
        for i, (w, b) in enumerate(zip(self.weights, self.biases)):
            z = self.activations[-1] @ w + b
            self.z_values.append(z)
            
            if i == len(self.weights) - 1:
                a = self.sigmoid(z)  # Output layer
            else:
                a = self.relu(z)  # Hidden layers
            
            self.activations.append(a)
        
        return self.activations[-1]
    
    def backward(self, y, learning_rate=0.01):
        m = len(y)
        
        # Output layer error
        delta = self.activations[-1] - y.reshape(-1, 1)
        
        # Backpropagate through layers
        for i in range(len(self.weights) - 1, -1, -1):
            dw = self.activations[i].T @ delta / m
            db = np.sum(delta, axis=0, keepdims=True) / m
            
            if i > 0:
                delta = delta @ self.weights[i].T * self.relu_derivative(self.z_values[i-1])
            
            self.weights[i] -= learning_rate * dw
            self.biases[i] -= learning_rate * db
    
    def fit(self, X, y, epochs=1000, learning_rate=0.01):
        losses = []
        for _ in range(epochs):
            predictions = self.forward(X)
            self.backward(y, learning_rate)
            loss = -np.mean(y * np.log(predictions + 1e-15) + 
                          (1-y) * np.log(1 - predictions + 1e-15))
            losses.append(loss)
        return losses
    
    def predict(self, X):
        return (self.forward(X) > 0.5).astype(int).flatten()
```

## Quick Reference

```python
# Sklearn MLP
MLPClassifier(
    hidden_layer_sizes=(100,),  # One hidden layer with 100 neurons
    activation='relu',          # 'relu', 'tanh', 'logistic'
    solver='adam',              # 'adam', 'sgd', 'lbfgs'
    alpha=0.0001,               # L2 regularization
    learning_rate='constant',   # 'adaptive', 'invscaling'
    learning_rate_init=0.001,
    max_iter=200,
    early_stopping=True
)

# Key points:
# - Always scale features
# - Start with one hidden layer
# - ReLU activation for hidden layers
# - Use early_stopping to prevent overfitting
```

## Related Topics
- [Gradient Descent](gradient_descent.md)
- [Deep Learning](../02_deep_learning/neural_networks.md)
- [Backpropagation](../02_deep_learning/backpropagation.md)
