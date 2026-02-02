# Convolutional Neural Networks (CNNs)

Neural networks for image and spatial data.

## Overview

CNNs use convolution operations to extract spatial features hierarchically.

```
Image → Conv → Pool → Conv → Pool → Flatten → FC → Output

Lower layers: Edges, textures
Middle layers: Parts, patterns
Higher layers: Objects, concepts
```

## Convolution Operation

```python
import torch
import torch.nn as nn

# 2D Convolution
conv = nn.Conv2d(
    in_channels=3,      # RGB input
    out_channels=32,    # 32 filters
    kernel_size=3,      # 3x3 kernel
    stride=1,           # Move 1 pixel at a time
    padding=1           # Maintain spatial size
)

# Input shape: (batch, channels, height, width)
x = torch.randn(16, 3, 224, 224)  # Batch of 16 RGB images
output = conv(x)  # Shape: (16, 32, 224, 224)
```

### Convolution Parameters

```
Output Size = (Input - Kernel + 2*Padding) / Stride + 1

Example:
  Input: 224x224
  Kernel: 3x3
  Padding: 1
  Stride: 1
  Output: (224 - 3 + 2*1) / 1 + 1 = 224x224 (same size)
```

## Pooling

Reduce spatial dimensions while keeping important features.

```python
# Max Pooling
maxpool = nn.MaxPool2d(kernel_size=2, stride=2)
# 224x224 → 112x112

# Average Pooling
avgpool = nn.AvgPool2d(kernel_size=2, stride=2)

# Adaptive (output size independent of input)
adaptive = nn.AdaptiveAvgPool2d((1, 1))  # Global average pooling
```

## Basic CNN Architecture

```python
class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        
        # Feature extractor
        self.features = nn.Sequential(
            # Block 1
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),  # 224 → 112
            
            # Block 2
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),  # 112 → 56
            
            # Block 3
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),  # 56 → 28
        )
        
        # Classifier
        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            nn.Linear(128, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes)
        )
    
    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x

model = SimpleCNN(num_classes=10)
```

## Popular Architectures

### LeNet-5 (1998)
```python
class LeNet5(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 6, 5)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 4 * 4, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)
    
    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = nn.functional.max_pool2d(x, 2)
        x = torch.relu(self.conv2(x))
        x = nn.functional.max_pool2d(x, 2)
        x = x.view(-1, 16 * 4 * 4)
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)
```

### VGG-style (2014)
```python
def make_vgg_block(in_ch, out_ch, num_convs):
    layers = []
    for i in range(num_convs):
        layers.append(nn.Conv2d(in_ch if i == 0 else out_ch, out_ch, 3, padding=1))
        layers.append(nn.ReLU())
    layers.append(nn.MaxPool2d(2, 2))
    return nn.Sequential(*layers)
```

### ResNet-style (2015)
```python
class ResidualBlock(nn.Module):
    def __init__(self, channels):
        super().__init__()
        self.conv1 = nn.Conv2d(channels, channels, 3, padding=1)
        self.bn1 = nn.BatchNorm2d(channels)
        self.conv2 = nn.Conv2d(channels, channels, 3, padding=1)
        self.bn2 = nn.BatchNorm2d(channels)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        residual = x
        x = self.relu(self.bn1(self.conv1(x)))
        x = self.bn2(self.conv2(x))
        x = x + residual  # Skip connection
        return self.relu(x)
```

## Transfer Learning

Use pre-trained models for new tasks.

```python
from torchvision import models

# Load pre-trained model
resnet = models.resnet50(pretrained=True)

# Freeze feature layers
for param in resnet.parameters():
    param.requires_grad = False

# Replace classifier
num_features = resnet.fc.in_features
resnet.fc = nn.Linear(num_features, num_classes)

# Only train new classifier
optimizer = optim.Adam(resnet.fc.parameters(), lr=0.001)
```

### Fine-tuning
```python
# Unfreeze last few layers
for param in resnet.layer4.parameters():
    param.requires_grad = True

# Use different learning rates
optimizer = optim.Adam([
    {'params': resnet.fc.parameters(), 'lr': 1e-3},
    {'params': resnet.layer4.parameters(), 'lr': 1e-4}
])
```

## Data Augmentation

```python
from torchvision import transforms

train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                        std=[0.229, 0.224, 0.225])
])

val_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                        std=[0.229, 0.224, 0.225])
])
```

## Image Classification Example

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader

# Data
train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

train_data = datasets.ImageFolder('data/train', transform=train_transform)
train_loader = DataLoader(train_data, batch_size=32, shuffle=True)

# Model
model = models.resnet18(pretrained=True)
model.fc = nn.Linear(model.fc.in_features, len(train_data.classes))
model = model.cuda()

# Training
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

for epoch in range(10):
    model.train()
    for images, labels in train_loader:
        images, labels = images.cuda(), labels.cuda()
        
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
```

## Common CNN Tasks

### Object Detection
```python
# Using pre-trained Faster R-CNN
from torchvision.models.detection import fasterrcnn_resnet50_fpn

model = fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()

with torch.no_grad():
    predictions = model(images)
# Returns: boxes, labels, scores
```

### Semantic Segmentation
```python
# Using pre-trained DeepLabV3
from torchvision.models.segmentation import deeplabv3_resnet50

model = deeplabv3_resnet50(pretrained=True)
model.eval()

with torch.no_grad():
    output = model(images)['out']
# Output shape: (batch, num_classes, height, width)
```

## Tips and Best Practices

### Architecture Design
```
1. Start with proven architectures (ResNet, EfficientNet)
2. Use BatchNorm after convolutions
3. Use dropout before FC layers
4. Global average pooling instead of flatten
5. Start small, scale up
```

### Training Tips
```
1. Use data augmentation
2. Use pre-trained weights when possible
3. Start with learning rate 1e-3 or 1e-4
4. Use learning rate scheduling
5. Monitor overfitting on validation set
```

## Quick Reference

```python
# Convolution: Extract features
nn.Conv2d(in_ch, out_ch, kernel_size, stride=1, padding=0)

# Pooling: Reduce size
nn.MaxPool2d(kernel_size, stride)
nn.AdaptiveAvgPool2d(output_size)

# Normalization: Stabilize training
nn.BatchNorm2d(num_features)

# Output size formula
output = (input - kernel + 2*padding) // stride + 1

# Common pattern
Conv → BatchNorm → ReLU → Pool
```

## Related Topics
- [Neural Networks](neural_networks.md)
- [Transfer Learning](transfer_learning.md)
- [RNNs](rnn.md)
