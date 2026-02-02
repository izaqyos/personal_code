# Random Forests

Ensemble of decision trees using bagging.

## Concepts Covered

- **Bagging**: Bootstrap Aggregating
- **Random Subspace**: Feature sampling per split
- **Out-of-Bag (OOB)**: Built-in validation
- **Feature Importance**: Aggregated from all trees

## How It Works

1. Create N bootstrap samples from training data
2. Train a decision tree on each sample
3. At each split, only consider sqrt(features) random features
4. Aggregate predictions (voting for classification, averaging for regression)

## Usage

```bash
python train.py
python train.py --n-estimators 100 --max-depth 10
python inference.py
```

## Key Takeaways

1. **Reduces Overfitting**: Averaging reduces variance
2. **Parallelizable**: Trees are independent
3. **OOB Score**: Free validation without holdout set
4. **Feature Importance**: More reliable than single tree
