# Decision Trees

Interpretable tree-based classification and regression.

## Concepts Covered

- **Splitting Criteria**: Gini impurity, Entropy (Information Gain)
- **Tree Building**: Recursive partitioning (CART)
- **Pruning**: Pre-pruning (max_depth), Post-pruning
- **Feature Importance**: Based on impurity decrease

## The Math

### Gini Impurity
```
Gini(D) = 1 - Σ(pᵢ)²
```

### Entropy
```
H(D) = -Σ pᵢ log₂(pᵢ)
```

### Information Gain
```
IG(D, A) = H(D) - Σ (|Dᵥ|/|D|) × H(Dᵥ)
```

## Usage

```bash
python train.py
python train.py --max-depth 5 --criterion gini
python inference.py
```

## Key Takeaways

1. **Interpretability**: Can visualize and explain decisions
2. **No Feature Scaling**: Not required for trees
3. **Overfitting**: Use max_depth, min_samples_leaf to control
4. **Feature Importance**: Built-in feature ranking
