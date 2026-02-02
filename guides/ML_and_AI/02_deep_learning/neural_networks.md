# Deep Neural Networks

Building and training deep learning models.

## Overview

Deep neural networks have multiple hidden layers, enabling hierarchical feature learning.

```
Input → Layer1 → Layer2 → ... → LayerN → Output

Each layer learns increasingly abstract representations.
```

## PyTorch Basics

### Tensors

```python
import torch

# Create tensors
x = torch.tensor([[1, 2], [3, 4]], dtype=torch.float32)
zeros = torch.zeros(3, 4)
ones = torch.ones(3, 4)
random = torch.randn(3, 4)  # Normal distribution

# GPU support
if torch.cuda.is_available():
    x = x.cuda()
# Or use device-agnostic code
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
x = x.to(device)

# Operations
y = x + 2
z = x @ x.T  # Matrix multiplication
w = x * y    # Element-wise multiplication
```

### Automatic Differentiation

```python
# Tensors with gradients
x = torch.tensor([2.0], requires_grad=True)
y = x ** 2 + 3 * x + 1

# Compute gradients
y.backward()
print(f"dy/dx at x=2: {x.grad}")  # 2*2 + 3 = 7
```

## Building Neural Networks

### Using nn.Module

```python
import torch.nn as nn

class SimpleNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.2)
    
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.fc3(x)
        return x

# Create model
model = SimpleNet(input_size=784, hidden_size=256, output_size=10)
```

### Using nn.Sequential

```python
model = nn.Sequential(
    nn.Linear(784, 256),
    nn.ReLU(),
    nn.Dropout(0.2),
    nn.Linear(256, 128),
    nn.ReLU(),
    nn.Dropout(0.2),
    nn.Linear(128, 10)
)
```

## Training Loop

```python
import torch.optim as optim

# Setup
model = SimpleNet(784, 256, 10)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
def train_epoch(model, dataloader, criterion, optimizer, device):
    model.train()
    total_loss = 0
    correct = 0
    total = 0
    
    for batch_x, batch_y in dataloader:
        batch_x, batch_y = batch_x.to(device), batch_y.to(device)
        
        # Forward pass
        outputs = model(batch_x)
        loss = criterion(outputs, batch_y)
        
        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        # Track metrics
        total_loss += loss.item()
        _, predicted = outputs.max(1)
        correct += (predicted == batch_y).sum().item()
        total += batch_y.size(0)
    
    return total_loss / len(dataloader), correct / total

# Validation loop
def validate(model, dataloader, criterion, device):
    model.eval()
    total_loss = 0
    correct = 0
    total = 0
    
    with torch.no_grad():
        for batch_x, batch_y in dataloader:
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)
            outputs = model(batch_x)
            loss = criterion(outputs, batch_y)
            
            total_loss += loss.item()
            _, predicted = outputs.max(1)
            correct += (predicted == batch_y).sum().item()
            total += batch_y.size(0)
    
    return total_loss / len(dataloader), correct / total
```

## Data Loading

```python
from torch.utils.data import DataLoader, TensorDataset

# From numpy arrays
X_tensor = torch.from_numpy(X_train).float()
y_tensor = torch.from_numpy(y_train).long()
dataset = TensorDataset(X_tensor, y_tensor)

train_loader = DataLoader(
    dataset,
    batch_size=32,
    shuffle=True,
    num_workers=4
)

# Iterate
for batch_x, batch_y in train_loader:
    # Process batch
    pass
```

## Layer Types

### Fully Connected (Linear)
```python
nn.Linear(in_features, out_features, bias=True)
```

### Convolutional
```python
nn.Conv2d(in_channels, out_channels, kernel_size, stride=1, padding=0)
nn.Conv1d(in_channels, out_channels, kernel_size)
```

### Recurrent
```python
nn.LSTM(input_size, hidden_size, num_layers=1, batch_first=True)
nn.GRU(input_size, hidden_size, num_layers=1, batch_first=True)
```

### Normalization
```python
nn.BatchNorm1d(num_features)
nn.LayerNorm(normalized_shape)
```

### Pooling
```python
nn.MaxPool2d(kernel_size, stride=None)
nn.AvgPool2d(kernel_size, stride=None)
nn.AdaptiveAvgPool2d(output_size)
```

## Activation Functions

```python
nn.ReLU()           # max(0, x)
nn.LeakyReLU(0.1)   # x if x > 0 else 0.1*x
nn.ELU()            # x if x > 0 else alpha*(exp(x)-1)
nn.GELU()           # Gaussian Error Linear Unit (popular in transformers)
nn.Sigmoid()        # 1 / (1 + exp(-x))
nn.Tanh()           # (exp(x) - exp(-x)) / (exp(x) + exp(-x))
nn.Softmax(dim=1)   # Normalized exponential
```

## Loss Functions

```python
# Classification
nn.CrossEntropyLoss()       # Multi-class (includes softmax)
nn.BCEWithLogitsLoss()      # Binary (includes sigmoid)
nn.NLLLoss()                # Negative log likelihood

# Regression
nn.MSELoss()                # Mean squared error
nn.L1Loss()                 # Mean absolute error
nn.SmoothL1Loss()           # Huber loss
```

## Optimizers

```python
optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
optim.Adam(model.parameters(), lr=0.001, betas=(0.9, 0.999))
optim.AdamW(model.parameters(), lr=0.001, weight_decay=0.01)
optim.RMSprop(model.parameters(), lr=0.01)
```

## Learning Rate Scheduling

```python
from torch.optim.lr_scheduler import (
    StepLR, ExponentialLR, CosineAnnealingLR, ReduceLROnPlateau
)

# Step decay
scheduler = StepLR(optimizer, step_size=10, gamma=0.1)

# Cosine annealing
scheduler = CosineAnnealingLR(optimizer, T_max=100)

# Reduce on plateau
scheduler = ReduceLROnPlateau(optimizer, mode='min', patience=5)

# In training loop
for epoch in range(epochs):
    train_loss = train_epoch(model, train_loader, ...)
    val_loss = validate(model, val_loader, ...)
    
    scheduler.step()  # or scheduler.step(val_loss) for ReduceLROnPlateau
```

## Regularization

### Dropout
```python
nn.Dropout(p=0.5)       # Randomly zero elements
nn.Dropout2d(p=0.5)     # Zero entire channels (for conv)
```

### Weight Decay (L2)
```python
optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-4)
```

### Batch Normalization
```python
nn.BatchNorm1d(num_features)
nn.BatchNorm2d(num_features)
```

## Saving and Loading

```python
# Save entire model
torch.save(model, 'model.pth')
model = torch.load('model.pth')

# Save only weights (recommended)
torch.save(model.state_dict(), 'weights.pth')

# Load weights
model = SimpleNet(784, 256, 10)
model.load_state_dict(torch.load('weights.pth'))

# Save checkpoint (for resuming training)
checkpoint = {
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss
}
torch.save(checkpoint, 'checkpoint.pth')
```

## Complete Training Example

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# Model
class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(784, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 10)
        )
    
    def forward(self, x):
        return self.layers(x)

# Setup
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = MLP().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=3)

# Training
best_val_acc = 0
for epoch in range(50):
    # Train
    model.train()
    train_loss = 0
    for x, y in train_loader:
        x, y = x.to(device), y.to(device)
        
        optimizer.zero_grad()
        output = model(x)
        loss = criterion(output, y)
        loss.backward()
        optimizer.step()
        
        train_loss += loss.item()
    
    # Validate
    model.eval()
    val_loss = 0
    correct = 0
    with torch.no_grad():
        for x, y in val_loader:
            x, y = x.to(device), y.to(device)
            output = model(x)
            val_loss += criterion(output, y).item()
            correct += (output.argmax(1) == y).sum().item()
    
    val_acc = correct / len(val_loader.dataset)
    scheduler.step(val_loss)
    
    print(f"Epoch {epoch}: Train Loss={train_loss/len(train_loader):.4f}, "
          f"Val Loss={val_loss/len(val_loader):.4f}, Val Acc={val_acc:.4f}")
    
    # Save best model
    if val_acc > best_val_acc:
        best_val_acc = val_acc
        torch.save(model.state_dict(), 'best_model.pth')
```

## Quick Reference

```python
# Model pattern
class MyModel(nn.Module):
    def __init__(self):
        super().__init__()
        # Define layers
    
    def forward(self, x):
        # Define forward pass
        return x

# Training pattern
model.train()
for x, y in loader:
    optimizer.zero_grad()
    output = model(x)
    loss = criterion(output, y)
    loss.backward()
    optimizer.step()

# Evaluation pattern
model.eval()
with torch.no_grad():
    output = model(x)
```

## Related Topics
- [Backpropagation](backpropagation.md)
- [CNNs](cnn.md)
- [RNNs](rnn.md)
