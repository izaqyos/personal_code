# Convolutional Neural Networks (CNNs)

> Neural networks designed for spatial data - images, video, and more.

---

## Why CNNs?

Fully connected networks for images are impractical:

```
Image: 224 × 224 × 3 = 150,528 input neurons
Hidden layer: 1000 neurons
Parameters: 150,528 × 1000 = 150 million!

Problems:
1. Too many parameters (overfitting)
2. Ignores spatial structure
3. Not translation invariant
```

CNNs solve these with:
- **Local connectivity**: Each neuron sees only a small region
- **Parameter sharing**: Same filter applied everywhere
- **Translation invariance**: Detect features regardless of position

---

## Convolution Operation

Slide a filter (kernel) across the image:

```
Input (5×5):              Filter (3×3):           Output:
┌─────────────────┐       ┌───────────┐
│ 1  1  1  0  0   │       │ 1  0  1   │
│ 0  1  1  1  0   │   *   │ 0  1  0   │   =   ?
│ 0  0  1  1  1   │       │ 1  0  1   │
│ 0  0  1  1  0   │       └───────────┘
│ 0  1  1  0  0   │
└─────────────────┘

Step 1 (top-left):
│ 1  1  1 │       │ 1  0  1 │
│ 0  1  1 │   ⊙   │ 0  1  0 │  = 1×1+1×0+1×1+0×0+1×1+1×0+0×1+0×0+1×1 = 4
│ 0  0  1 │       │ 1  0  1 │

Slide right, down... → Output feature map
```

### Mathematical Definition

```
(I * K)[i,j] = Σₘ Σₙ I[i+m, j+n] × K[m, n]

Where:
- I: Input image
- K: Kernel/filter
- *: Convolution operation
```

---

## Key Parameters

### Filter Size

```
Common sizes: 3×3, 5×5, 7×7

3×3 is most popular:
- Two 3×3 filters = one 5×5 receptive field
- But fewer parameters and more non-linearity!
```

### Stride

```
Stride = 1:                    Stride = 2:
Move 1 pixel at a time         Move 2 pixels at a time
Output similar size            Output halved

┌─┬─┬─┬─┐                      ┌───┬───┐
│░│░│ │ │  ← window positions  │░░░│   │
├─┼─┼─┼─┤                      │░░░│   │
│░│░│ │ │                      ├───┼───┤
├─┼─┼─┼─┤                      │   │   │
│ │ │ │ │                      │   │   │
└─┴─┴─┴─┘                      └───┴───┘
```

### Padding

```
No padding (valid):      Same padding:
Input shrinks            Output = Input size

Input: 5×5               Input: 5×5
Filter: 3×3              Filter: 3×3, Pad: 1
Output: 3×3              Output: 5×5

┌─────────┐              ┌─┬─────────┬─┐
│ ┌───┐   │              │0│0 0 0 0 0│0│
│ │   │   │              ├─┼─────────┼─┤
│ └───┘   │              │0│ image   │0│
│         │              │0│         │0│
└─────────┘              ├─┼─────────┼─┤
                         │0│0 0 0 0 0│0│
                         └─┴─────────┴─┘
```

### Output Size Formula

```
Output = (Input - Filter + 2×Padding) / Stride + 1

Example:
Input: 32×32, Filter: 3×3, Padding: 1, Stride: 1
Output = (32 - 3 + 2×1) / 1 + 1 = 32×32

Example:
Input: 32×32, Filter: 3×3, Padding: 0, Stride: 2
Output = (32 - 3 + 0) / 2 + 1 = 15×15
```

---

## CNN Architecture Components

### Convolutional Layer

```
Input: H × W × C_in    (height, width, channels)
Filters: K filters of size F × F × C_in
Output: H' × W' × K

Each filter produces one output channel
```

### Pooling Layer

Downsample spatial dimensions:

```
Max Pooling (2×2, stride 2):

┌───┬───┐      ┌───┐
│ 1 │ 3 │      │   │
├───┼───┤  →   │ 4 │   (take maximum)
│ 2 │ 4 │      │   │
└───┴───┘      └───┘

Average Pooling: Take mean instead of max

Purpose:
- Reduce computation
- Increase receptive field
- Add translation invariance
```

### Fully Connected Layer

```
After convolutions, flatten and use MLPs:

Feature maps: 7 × 7 × 512
Flatten: 7 × 7 × 512 = 25,088
FC: 25,088 → 4096 → 1000 (classes)
```

---

## Classic CNN Architecture

```
INPUT → [CONV → RELU → CONV → RELU → POOL] × N → [FC → RELU] × M → OUTPUT

Example (simplified VGG):

Input: 224×224×3
├── Conv3-64  → 224×224×64
├── Conv3-64  → 224×224×64
├── MaxPool   → 112×112×64
├── Conv3-128 → 112×112×128
├── Conv3-128 → 112×112×128
├── MaxPool   → 56×56×128
├── Conv3-256 → 56×56×256
├── Conv3-256 → 56×56×256
├── MaxPool   → 28×28×256
├── ... more conv blocks ...
├── Flatten   → 25088
├── FC-4096   → 4096
├── FC-4096   → 4096
└── FC-1000   → 1000 (softmax)
```

---

## Implementation

### PyTorch

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()

        # Convolutional layers
        self.conv1 = nn.Conv2d(
            in_channels=3,
            out_channels=32,
            kernel_size=3,
            stride=1,
            padding=1
        )
        self.conv2 = nn.Conv2d(32, 64, 3, 1, 1)
        self.conv3 = nn.Conv2d(64, 128, 3, 1, 1)

        # Pooling
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)

        # Batch normalization
        self.bn1 = nn.BatchNorm2d(32)
        self.bn2 = nn.BatchNorm2d(64)
        self.bn3 = nn.BatchNorm2d(128)

        # Fully connected
        # After 3 pools: 32 → 16 → 8 → 4
        self.fc1 = nn.Linear(128 * 4 * 4, 512)
        self.fc2 = nn.Linear(512, num_classes)

        # Dropout
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        # Conv block 1
        x = self.pool(F.relu(self.bn1(self.conv1(x))))  # 32→16

        # Conv block 2
        x = self.pool(F.relu(self.bn2(self.conv2(x))))  # 16→8

        # Conv block 3
        x = self.pool(F.relu(self.bn3(self.conv3(x))))  # 8→4

        # Flatten
        x = x.view(x.size(0), -1)

        # Fully connected
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)

        return x

# Usage
model = SimpleCNN(num_classes=10)
input_tensor = torch.randn(1, 3, 32, 32)  # Batch, Channels, H, W
output = model(input_tensor)
print(output.shape)  # [1, 10]
```

### Data Augmentation

```python
from torchvision import transforms

train_transform = transforms.Compose([
    transforms.RandomCrop(32, padding=4),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])
```

---

## Famous CNN Architectures

| Architecture | Year | Key Innovation |
|--------------|------|----------------|
| **LeNet-5** | 1998 | First successful CNN |
| **AlexNet** | 2012 | ReLU, Dropout, GPU training |
| **VGGNet** | 2014 | Very deep (16-19 layers), 3×3 filters |
| **GoogLeNet** | 2014 | Inception modules (parallel paths) |
| **ResNet** | 2015 | Skip connections (residual learning) |
| **DenseNet** | 2017 | Dense connections (all-to-all) |
| **EfficientNet** | 2019 | Compound scaling |
| **ConvNeXt** | 2022 | Modernized CNN (competes with ViT) |

---

## Receptive Field

The region of input that affects a neuron:

```
Layer 1 (3×3 conv): Receptive field = 3×3
Layer 2 (3×3 conv): Receptive field = 5×5
Layer 3 (3×3 conv): Receptive field = 7×7

Deeper layers "see" larger regions:

Input image:
┌─────────────────────┐
│ ┌───────────────┐   │  ← Layer 3 sees this (7×7)
│ │ ┌─────────┐   │   │
│ │ │ ┌───┐   │   │   │  ← Layer 2 sees this (5×5)
│ │ │ │ ■ │   │   │   │  ← Layer 1 sees this (3×3)
│ │ │ └───┘   │   │   │
│ │ └─────────┘   │   │
│ └───────────────┘   │
└─────────────────────┘
```

---

## Exercises

1. **Calculate**: What's the output size of 64×64 input with 5×5 filter, stride 2, padding 2?
2. **Implement**: Build a CNN for MNIST from scratch
3. **Visualize**: Plot learned filters from first conv layer
4. **Compare**: MLP vs CNN on CIFAR-10. Compare accuracy and parameters
5. **Transfer Learning**: Fine-tune pretrained ResNet on custom dataset

---

## Key Takeaways

- CNNs exploit spatial structure with local filters
- Parameter sharing drastically reduces parameters
- Convolution → ReLU → Pool is the basic building block
- Deeper networks = larger receptive field
- Modern architectures use skip connections (ResNet)
- Pretrained models are powerful starting points

---

## Next Steps

→ Continue to [05-rnns-lstms.md](./05-rnns-lstms.md)
