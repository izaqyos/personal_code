# Convolutional Neural Networks (CNN)

Neural networks specialized for image and spatial data.

## Concepts Covered

- **Convolution**: Sliding filter over input
- **Kernels/Filters**: Learned feature detectors
- **Pooling**: Downsample spatial dimensions
- **Feature Maps**: Activated outputs from convolutions

## Architecture Components

```
Input -> Conv2d -> ReLU -> Pool -> Conv2d -> ReLU -> Pool -> Flatten -> FC -> Output
```

## Key Parameters

- **Kernel Size**: Filter dimensions (e.g., 3x3)
- **Stride**: How much the filter moves
- **Padding**: Zeros added to borders
- **Channels**: Number of filters (output depth)

## Usage

```bash
python train.py
python train.py --epochs 10
python inference.py
```

## Key Takeaways

1. **Translation Invariance**: Detects features anywhere in image
2. **Parameter Sharing**: Same filter across all positions
3. **Hierarchical Features**: Early = edges, Later = objects
4. **Pooling**: Reduces size, adds invariance
