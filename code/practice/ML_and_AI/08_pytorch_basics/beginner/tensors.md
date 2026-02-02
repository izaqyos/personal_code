# PyTorch Tensors - Beginner

Foundation of deep learning with PyTorch.

## Learning Objectives
- Create and manipulate tensors
- Understand tensor operations
- Use GPU acceleration

## Setup

```bash
pip install torch torchvision
```

```python
import torch
import numpy as np
```

---

## Exercise 1: Creating Tensors

Create tensors in different ways.

```python
# TODO: Create a tensor from a Python list
x = # [1, 2, 3, 4]

# TODO: Create a 3x4 tensor of zeros

# TODO: Create a 3x4 tensor of ones

# TODO: Create a 3x4 tensor of random values (normal distribution)

# TODO: Create a tensor from a numpy array

# TODO: Print shape, dtype, and device for each
```

<details>
<summary>Solution</summary>

```python
import torch
import numpy as np

# From list
x_list = torch.tensor([1, 2, 3, 4])
print(f"From list: {x_list}")

# Zeros
x_zeros = torch.zeros(3, 4)
print(f"\nZeros (3x4):\n{x_zeros}")

# Ones
x_ones = torch.ones(3, 4)
print(f"\nOnes (3x4):\n{x_ones}")

# Random normal
x_random = torch.randn(3, 4)
print(f"\nRandom (3x4):\n{x_random}")

# From numpy
np_array = np.array([[1, 2], [3, 4]])
x_numpy = torch.from_numpy(np_array)
print(f"\nFrom numpy:\n{x_numpy}")

# Properties
print(f"\nProperties of random tensor:")
print(f"  Shape: {x_random.shape}")
print(f"  Dtype: {x_random.dtype}")
print(f"  Device: {x_random.device}")
```
</details>

---

## Exercise 2: Tensor Operations

Perform basic mathematical operations.

```python
a = torch.tensor([[1, 2], [3, 4]], dtype=torch.float32)
b = torch.tensor([[5, 6], [7, 8]], dtype=torch.float32)

# TODO: Element-wise addition

# TODO: Element-wise multiplication

# TODO: Matrix multiplication (2 ways: @ and torch.matmul)

# TODO: Transpose

# TODO: Sum all elements

# TODO: Sum along rows (axis=1)

# TODO: Mean along columns (axis=0)
```

<details>
<summary>Solution</summary>

```python
a = torch.tensor([[1, 2], [3, 4]], dtype=torch.float32)
b = torch.tensor([[5, 6], [7, 8]], dtype=torch.float32)

# Element-wise addition
print(f"a + b:\n{a + b}")

# Element-wise multiplication
print(f"\na * b:\n{a * b}")

# Matrix multiplication
print(f"\na @ b:\n{a @ b}")
print(f"\ntorch.matmul(a, b):\n{torch.matmul(a, b)}")

# Transpose
print(f"\na.T:\n{a.T}")

# Sum all elements
print(f"\na.sum(): {a.sum()}")

# Sum along rows
print(f"\na.sum(dim=1): {a.sum(dim=1)}")

# Mean along columns
print(f"\na.mean(dim=0): {a.mean(dim=0)}")
```
</details>

---

## Exercise 3: Reshaping Tensors

Change tensor shapes without changing data.

```python
x = torch.arange(12)  # [0, 1, 2, ..., 11]

# TODO: Reshape to 3x4

# TODO: Reshape to 2x2x3

# TODO: Flatten back to 1D

# TODO: Add a dimension (unsqueeze)

# TODO: Remove a dimension (squeeze)

# TODO: Reshape using view vs reshape
```

<details>
<summary>Solution</summary>

```python
x = torch.arange(12)
print(f"Original: {x.shape} = {x}")

# Reshape to 3x4
x_3x4 = x.reshape(3, 4)
print(f"\nReshaped to 3x4:\n{x_3x4}")

# Reshape to 2x2x3
x_2x2x3 = x.reshape(2, 2, 3)
print(f"\nReshaped to 2x2x3:\n{x_2x2x3}")

# Flatten
x_flat = x_2x2x3.flatten()
print(f"\nFlattened: {x_flat}")

# Unsqueeze (add dimension)
x_unsqueeze = x_3x4.unsqueeze(0)  # Add batch dimension
print(f"\nUnsqueezed: {x_unsqueeze.shape}")

# Squeeze (remove dimension)
x_squeeze = x_unsqueeze.squeeze(0)
print(f"Squeezed: {x_squeeze.shape}")

# view vs reshape
print("\nview vs reshape:")
print("- view: requires contiguous memory, shares data")
print("- reshape: may copy if not contiguous, safer")
```
</details>

---

## Exercise 4: Indexing and Slicing

Access specific elements and subsets.

```python
x = torch.arange(24).reshape(4, 6)
print(f"Original (4x6):\n{x}")

# TODO: Get element at row 1, column 2

# TODO: Get first row

# TODO: Get last column

# TODO: Get rows 1-2, columns 2-4

# TODO: Get every other row

# TODO: Boolean indexing (elements > 10)
```

<details>
<summary>Solution</summary>

```python
x = torch.arange(24).reshape(4, 6)
print(f"Original (4x6):\n{x}")

# Element at row 1, column 2
print(f"\nx[1, 2]: {x[1, 2]}")

# First row
print(f"\nx[0]: {x[0]}")

# Last column
print(f"\nx[:, -1]: {x[:, -1]}")

# Rows 1-2, columns 2-4
print(f"\nx[1:3, 2:5]:\n{x[1:3, 2:5]}")

# Every other row
print(f"\nx[::2]:\n{x[::2]}")

# Boolean indexing
mask = x > 10
print(f"\nx[x > 10]: {x[mask]}")
```
</details>

---

## Exercise 5: GPU Operations

Move tensors to GPU for acceleration.

```python
# TODO: Check if CUDA is available

# TODO: Create a tensor on GPU directly

# TODO: Move a CPU tensor to GPU

# TODO: Perform operations on GPU

# TODO: Move result back to CPU

# TODO: Time comparison: CPU vs GPU for large matrix multiply
```

<details>
<summary>Solution</summary>

```python
import time

# Check CUDA
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"CUDA device: {torch.cuda.get_device_name(0)}")
    device = torch.device('cuda')
else:
    print("Running on CPU")
    device = torch.device('cpu')

# Create on GPU
x_gpu = torch.randn(3, 3, device=device)
print(f"\nTensor on {x_gpu.device}:\n{x_gpu}")

# Move CPU tensor to GPU
x_cpu = torch.randn(3, 3)
x_moved = x_cpu.to(device)
print(f"Moved to: {x_moved.device}")

# GPU operations
y_gpu = x_gpu @ x_gpu.T
print(f"Result on: {y_gpu.device}")

# Move back to CPU
y_cpu = y_gpu.cpu()
print(f"Back to: {y_cpu.device}")

# Timing comparison
size = 1000
iterations = 100

# CPU timing
a_cpu = torch.randn(size, size)
b_cpu = torch.randn(size, size)
start = time.time()
for _ in range(iterations):
    c_cpu = a_cpu @ b_cpu
cpu_time = time.time() - start

print(f"\nCPU time ({iterations} iterations): {cpu_time:.3f}s")

# GPU timing (if available)
if torch.cuda.is_available():
    a_gpu = a_cpu.cuda()
    b_gpu = b_cpu.cuda()
    torch.cuda.synchronize()
    start = time.time()
    for _ in range(iterations):
        c_gpu = a_gpu @ b_gpu
    torch.cuda.synchronize()
    gpu_time = time.time() - start
    print(f"GPU time ({iterations} iterations): {gpu_time:.3f}s")
    print(f"Speedup: {cpu_time/gpu_time:.1f}x")
```
</details>

---

## Exercise 6: Automatic Differentiation

Track gradients for backpropagation.

```python
# TODO: Create a tensor with requires_grad=True

# TODO: Perform some operations

# TODO: Call backward() to compute gradients

# TODO: Access the gradients

# TODO: Verify gradient computation manually
```

<details>
<summary>Solution</summary>

```python
# Create tensor with gradient tracking
x = torch.tensor([2.0, 3.0], requires_grad=True)
print(f"x = {x}")

# Forward pass
y = x ** 2  # y = [4, 9]
z = y.sum()  # z = 13
print(f"y = x² = {y}")
print(f"z = sum(y) = {z}")

# Backward pass
z.backward()

# Access gradients
print(f"\nGradients (dz/dx):")
print(f"x.grad = {x.grad}")

# Manual verification
print(f"\nManual check:")
print(f"z = x₁² + x₂²")
print(f"dz/dx₁ = 2*x₁ = 2*2 = 4")
print(f"dz/dx₂ = 2*x₂ = 2*3 = 6")
print(f"Matches: {torch.allclose(x.grad, 2 * x)}")

# More complex example
print("\n--- More complex example ---")
x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
y = x * 2
z = y.mean()  # z = mean(2x) = (2*1 + 2*2 + 2*3) / 3 = 4
z.backward()
print(f"x = {x.data}")
print(f"y = 2x = {y.data}")
print(f"z = mean(y) = {z.item():.1f}")
print(f"dz/dx = {x.grad}")  # 2/3 for each element
```
</details>

---

## Key Takeaways

1. **Tensors** are the fundamental data structure in PyTorch
2. **Similar to NumPy** but with GPU support and autograd
3. **Shape operations**: reshape, view, squeeze, unsqueeze
4. **Device management**: `.to(device)`, `.cuda()`, `.cpu()`
5. **Gradients**: `requires_grad=True` enables automatic differentiation
6. **Operations** are similar to NumPy but return tensors

## Quick Reference

```python
import torch

# Creation
torch.tensor([1, 2, 3])
torch.zeros(3, 4)
torch.ones(3, 4)
torch.randn(3, 4)  # Normal distribution
torch.arange(10)
torch.from_numpy(np_array)

# Operations
a + b, a - b, a * b, a / b  # Element-wise
a @ b, torch.matmul(a, b)    # Matrix multiply
a.sum(), a.mean(), a.max()
a.T, a.transpose(0, 1)

# Reshaping
x.reshape(3, 4)
x.view(3, 4)
x.flatten()
x.unsqueeze(0), x.squeeze(0)

# GPU
x.to('cuda'), x.cuda()
x.to('cpu'), x.cpu()

# Gradients
x = torch.tensor([1.0], requires_grad=True)
y = x ** 2
y.backward()
print(x.grad)
```

## Next Steps
- Try [Intermediate: Building Neural Networks](../intermediate/neural_network.md)
- Learn about [Data Loading](../../09_neural_networks/beginner/data_loading.md)
