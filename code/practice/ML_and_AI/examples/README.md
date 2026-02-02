# ML and AI Examples Library

A comprehensive collection of runnable Python examples covering all major Machine Learning and Generative AI concepts.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run any example
cd 01_linear_regression
python train.py
python inference.py
```

## Directory Structure

```
examples/
├── data/                         # Shared sample datasets
│
│   CLASSICAL ML - SUPERVISED
├── 01_linear_regression/         # Linear, Ridge, Lasso regression
├── 02_logistic_regression/       # Binary/multiclass classification
├── 03_knn/                       # K-Nearest Neighbors
├── 04_svm/                       # Support Vector Machines
├── 05_decision_trees/            # Decision tree classifier
├── 06_random_forests/            # Ensemble methods
│
│   CLASSICAL ML - UNSUPERVISED
├── 07_kmeans_clustering/         # K-Means clustering
├── 08_hierarchical_clustering/   # Agglomerative clustering
├── 09_pca_dimensionality/        # Principal Component Analysis
│
│   OPTIMIZATION FUNDAMENTALS
├── 10_gradient_descent/          # SGD, Mini-batch, Momentum
├── 11_neural_network_basics/     # MLP from scratch
├── 12_activation_functions/      # ReLU, Sigmoid, GELU, etc.
├── 13_loss_functions/            # MSE, CrossEntropy, Focal
│
│   DEEP LEARNING
├── 14_cnn/                       # Convolutional Neural Networks
├── 15_rnn_lstm/                  # Recurrent Networks, LSTM
│
│   TRANSFORMER COMPONENTS
├── 16_tokenization/              # Character, Word, BPE tokenizers
├── 17_embeddings/                # Word embeddings, similarity
├── 18_attention/                 # Scaled dot-product attention
├── 19_multi_head_attention/      # Multi-head attention
└── 20_transformer_block/         # Full transformer encoder
```

## Concept Map

```
                    ┌─────────────────────────────────────────┐
                    │         MACHINE LEARNING                │
                    └─────────────────────────────────────────┘
                                      │
            ┌─────────────────────────┼─────────────────────────┐
            ▼                         ▼                         ▼
    ┌───────────────┐         ┌───────────────┐         ┌───────────────┐
    │  SUPERVISED   │         │ UNSUPERVISED  │         │ DEEP LEARNING │
    └───────────────┘         └───────────────┘         └───────────────┘
            │                         │                         │
    ┌───────┴───────┐         ┌───────┴───────┐         ┌───────┴───────┐
    │               │         │               │         │               │
    ▼               ▼         ▼               ▼         ▼               ▼
Regression    Classification  Clustering    Dim.     Neural         Sequence
                                           Reduction Networks       Models
    │               │         │               │         │               │
    ▼               ▼         ▼               ▼         ▼               ▼
- Linear        - Logistic  - K-Means     - PCA     - MLP          - RNN
- Ridge         - KNN       - Hierarchical          - CNN          - LSTM
- Lasso         - SVM                               - Activations  - Transformer
                - Trees                             - Loss Funcs   - Attention
                - Forests
```

## Learning Path

### Phase 1: Classical ML - Supervised (Week 1-2)
1. **Linear Regression** - Start here! Understand the basics
2. **Logistic Regression** - Classification with probability
3. **KNN** - Instance-based learning
4. **SVM** - Maximum margin classifiers
5. **Decision Trees** - Interpretable models
6. **Random Forests** - Ensemble power

### Phase 2: Classical ML - Unsupervised (Week 3)
7. **K-Means** - Cluster discovery
8. **Hierarchical Clustering** - Dendrograms
9. **PCA** - Dimensionality reduction

### Phase 3: Optimization & NN Basics (Week 4)
10. **Gradient Descent** - The core algorithm
11. **Neural Networks** - Forward/backward pass
12. **Activations** - Non-linearity functions
13. **Loss Functions** - Optimization objectives

### Phase 4: Deep Learning (Week 5-6)
14. **CNN** - Image processing
15. **RNN/LSTM** - Sequence modeling

### Phase 5: Transformers (Week 7-8)
16. **Tokenization** - Text to tokens
17. **Embeddings** - Dense representations
18. **Attention** - The key mechanism
19. **Multi-Head Attention** - Parallel attention
20. **Transformer Block** - Putting it all together

## Each Example Contains

```
XX_concept_name/
├── README.md         # Concept explanation
├── data/
│   ├── train.csv     # Training data
│   └── test.csv      # Test data
├── train.py          # Training script
├── inference.py      # Prediction script
└── model/            # Saved models
```

## Running Examples

### Training
```bash
cd 01_linear_regression
python train.py
# Output: Trains model, saves to model/, prints metrics
```

### Inference
```bash
python inference.py
# Output: Loads saved model, makes predictions
```

### With Custom Data
```bash
python train.py --data-path /path/to/custom/data.csv
```

## Key Concepts by Example

| Example | Key Concepts |
|---------|--------------|
| 01 Linear Regression | MSE, R², regularization |
| 02 Logistic Regression | Sigmoid, BCE, threshold |
| 03 KNN | Distance metrics, k selection |
| 04 SVM | Kernels, margin, support vectors |
| 05 Decision Trees | Entropy, Gini, pruning |
| 06 Random Forests | Bagging, OOB, feature importance |
| 07 K-Means | Inertia, elbow, silhouette |
| 08 Hierarchical | Linkage, dendrogram |
| 09 PCA | Variance, components, reconstruction |
| 10 Gradient Descent | Learning rate, momentum, Adam |
| 11 NN Basics | Weights, bias, backprop |
| 12 Activations | ReLU, sigmoid, GELU derivatives |
| 13 Loss Functions | MSE, CE, focal loss |
| 14 CNN | Conv2d, pooling, feature maps |
| 15 RNN/LSTM | Hidden state, gates, sequences |
| 16 Tokenization | BPE, vocabulary, encoding |
| 17 Embeddings | Vector space, similarity |
| 18 Attention | Q, K, V, scaled dot-product |
| 19 MHA | Heads, concatenation |
| 20 Transformer | LayerNorm, FFN, residuals |

## Requirements

- Python 3.10+
- See `requirements.txt` for full list

## Tips

1. **Run in order** - Examples build on each other
2. **Read the code** - Comments explain the "why"
3. **Experiment** - Change hyperparameters
4. **Visualize** - Most examples include plots
5. **Compare** - Run multiple algorithms on same data
