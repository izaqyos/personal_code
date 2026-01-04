# ML Fundamentals

> Core concepts that underpin all machine learning algorithms.

---

## What is Machine Learning?

Machine learning is a subset of artificial intelligence where systems learn patterns from data rather than being explicitly programmed.

### Types of Learning

| Type | Description | Examples |
|------|-------------|----------|
| **Supervised** | Learn from labeled data | Classification, Regression |
| **Unsupervised** | Find patterns in unlabeled data | Clustering, Dimensionality Reduction |
| **Reinforcement** | Learn through trial and reward | Game AI, Robotics |
| **Semi-supervised** | Mix of labeled and unlabeled | When labels are expensive |

---

## Key Concepts

### 1. Features and Labels

```
Features (X): Input variables used for prediction
Labels (y): Output variable we want to predict

Example - House Price Prediction:
Features: [sqft, bedrooms, location, age]
Label: price
```

### 2. Training, Validation, and Test Sets

```
┌─────────────────────────────────────────────┐
│              Full Dataset                    │
├──────────────────┬───────────┬──────────────┤
│   Training (60%) │ Val (20%) │  Test (20%)  │
│   Learn params   │ Tune      │  Final eval  │
└──────────────────┴───────────┴──────────────┘
```

- **Training set**: Model learns from this data
- **Validation set**: Tune hyperparameters, prevent overfitting
- **Test set**: Final unbiased evaluation (touch only once!)

### 3. Bias-Variance Tradeoff

```
Total Error = Bias² + Variance + Irreducible Noise

High Bias (Underfitting):
- Model too simple
- Misses patterns
- High training AND test error

High Variance (Overfitting):
- Model too complex
- Memorizes noise
- Low training error, HIGH test error
```

**Visual intuition:**
```
Underfitting          Good Fit           Overfitting
    |                   |                    |
  ──┼──               ──•──                ∿∿∿
   /                  /   \              /\/\/\
  /                  •     •            •     •
 •
```

### 4. Cross-Validation

K-Fold Cross-Validation provides robust model evaluation:

```
Fold 1: [VAL][TRAIN][TRAIN][TRAIN][TRAIN] → Score₁
Fold 2: [TRAIN][VAL][TRAIN][TRAIN][TRAIN] → Score₂
Fold 3: [TRAIN][TRAIN][VAL][TRAIN][TRAIN] → Score₃
Fold 4: [TRAIN][TRAIN][TRAIN][VAL][TRAIN] → Score₄
Fold 5: [TRAIN][TRAIN][TRAIN][TRAIN][VAL] → Score₅

Final Score = mean(Score₁...Score₅)
```

---

## Model Evaluation Metrics

### Classification Metrics

```
Confusion Matrix:
                  Predicted
              │  Pos  │  Neg  │
         ─────┼───────┼───────┤
Actual  Pos   │  TP   │  FN   │
        ─────┼───────┼───────┤
        Neg   │  FP   │  TN   │
```

| Metric | Formula | Use When |
|--------|---------|----------|
| **Accuracy** | (TP+TN)/(All) | Balanced classes |
| **Precision** | TP/(TP+FP) | Cost of FP is high |
| **Recall** | TP/(TP+FN) | Cost of FN is high |
| **F1 Score** | 2×(P×R)/(P+R) | Balance P and R |
| **AUC-ROC** | Area under ROC curve | Ranking quality |

### Regression Metrics

| Metric | Formula | Notes |
|--------|---------|-------|
| **MSE** | mean((y - ŷ)²) | Penalizes large errors |
| **RMSE** | √MSE | Same units as y |
| **MAE** | mean(\|y - ŷ\|) | Robust to outliers |
| **R²** | 1 - (SS_res/SS_tot) | Explained variance |

---

## The ML Pipeline

```
1. Problem Definition
   └─→ What are we predicting? What's the business goal?

2. Data Collection & Exploration
   └─→ Gather data, understand distributions, find issues

3. Data Preprocessing
   └─→ Handle missing values, encode categoricals, scale features

4. Feature Engineering
   └─→ Create meaningful features, select important ones

5. Model Selection
   └─→ Choose algorithm based on problem type and data

6. Training
   └─→ Fit model to training data

7. Evaluation
   └─→ Measure performance on validation/test sets

8. Hyperparameter Tuning
   └─→ Optimize model settings (grid search, random search)

9. Deployment & Monitoring
   └─→ Serve model, track performance drift
```

---

## Common Pitfalls

1. **Data Leakage**: Information from test set influencing training
2. **Imbalanced Classes**: Model predicts majority class only
3. **Feature Scaling**: Algorithms sensitive to magnitude differences
4. **Missing Data Handling**: Dropping vs imputing
5. **Overfitting to Validation**: Using test set too early/often

---

## Exercises

1. **Conceptual**: Explain why you should never touch the test set until final evaluation
2. **Calculate**: Given TP=90, FP=10, FN=20, TN=80, compute precision, recall, and F1
3. **Identify**: Is predicting spam email a classification or regression problem?
4. **Debug**: Model has 99% training accuracy but 60% test accuracy. What's wrong?

---

## Next Steps

→ Continue to [02-linear-regression.md](./02-linear-regression.md)
