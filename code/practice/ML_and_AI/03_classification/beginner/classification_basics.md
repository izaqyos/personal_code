# Classification Basics - Beginner

Predict discrete categories with classification models.

## Learning Objectives
- Understand binary and multi-class classification
- Train logistic regression and decision trees
- Interpret classification metrics

## Setup

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
```

---

## Exercise 1: Binary Classification

Predict whether a customer will churn.

```python
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression

# Generate binary classification data
X, y = make_classification(
    n_samples=1000, n_features=10, n_informative=5,
    n_redundant=2, n_classes=2, random_state=42
)

# TODO: Split into train/test (80/20)

# TODO: Train LogisticRegression

# TODO: Make predictions

# TODO: Print accuracy

# TODO: Print confusion matrix
```

<details>
<summary>Solution</summary>

```python
from sklearn.linear_model import LogisticRegression

X, y = make_classification(
    n_samples=1000, n_features=10, n_informative=5,
    n_redundant=2, n_classes=2, random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

predictions = model.predict(X_test)

print(f"Accuracy: {accuracy_score(y_test, predictions):.2%}")

cm = confusion_matrix(y_test, predictions)
print("\nConfusion Matrix:")
print(cm)
print("\nInterpretation:")
print(f"  True Negatives:  {cm[0,0]}")
print(f"  False Positives: {cm[0,1]}")
print(f"  False Negatives: {cm[1,0]}")
print(f"  True Positives:  {cm[1,1]}")
```
</details>

---

## Exercise 2: Classification Metrics

Calculate and interpret precision, recall, and F1.

```python
from sklearn.metrics import precision_score, recall_score, f1_score

# Using predictions from Exercise 1

# TODO: Calculate precision
# (Of predicted positives, how many are actually positive?)

# TODO: Calculate recall
# (Of actual positives, how many did we catch?)

# TODO: Calculate F1 score
# (Harmonic mean of precision and recall)

# TODO: Print classification report
```

<details>
<summary>Solution</summary>

```python
from sklearn.metrics import precision_score, recall_score, f1_score, classification_report

precision = precision_score(y_test, predictions)
recall = recall_score(y_test, predictions)
f1 = f1_score(y_test, predictions)

print("Classification Metrics:")
print(f"Precision: {precision:.2%}")
print(f"  → Of all predicted churners, {precision:.0%} actually churned")
print(f"Recall:    {recall:.2%}")
print(f"  → Of all actual churners, we caught {recall:.0%}")
print(f"F1 Score:  {f1:.2%}")
print(f"  → Balanced metric between precision and recall")

print("\nFull Classification Report:")
print(classification_report(y_test, predictions, target_names=['No Churn', 'Churn']))
```
</details>

---

## Exercise 3: Probability Predictions

Get probability estimates instead of just class labels.

```python
# TODO: Get probability predictions
# Hint: Use predict_proba()

# TODO: Print first 10 probabilities

# TODO: Change threshold from 0.5 to 0.3
# Re-classify based on new threshold

# TODO: Compare accuracy, precision, recall at both thresholds
```

<details>
<summary>Solution</summary>

```python
# Get probabilities
probabilities = model.predict_proba(X_test)

print("First 10 samples:")
print("Prob(No Churn) | Prob(Churn) | Predicted | Actual")
print("-" * 55)
for i in range(10):
    print(f"     {probabilities[i,0]:.3f}     |    {probabilities[i,1]:.3f}    |"
          f"     {predictions[i]}     |    {y_test[i]}")

# Custom threshold
threshold = 0.3
predictions_30 = (probabilities[:, 1] >= threshold).astype(int)

print(f"\nThreshold 0.5:")
print(f"  Accuracy:  {accuracy_score(y_test, predictions):.2%}")
print(f"  Precision: {precision_score(y_test, predictions):.2%}")
print(f"  Recall:    {recall_score(y_test, predictions):.2%}")

print(f"\nThreshold 0.3:")
print(f"  Accuracy:  {accuracy_score(y_test, predictions_30):.2%}")
print(f"  Precision: {precision_score(y_test, predictions_30):.2%}")
print(f"  Recall:    {recall_score(y_test, predictions_30):.2%}")

print("\nObservation:")
print("Lower threshold → More predicted positives → Higher recall, lower precision")
```
</details>

---

## Exercise 4: Decision Tree Classifier

Train and visualize a decision tree.

```python
from sklearn.tree import DecisionTreeClassifier, plot_tree

# Use Iris dataset for visualization
from sklearn.datasets import load_iris
iris = load_iris()
X, y = iris.data, iris.target

# TODO: Split data

# TODO: Train DecisionTreeClassifier with max_depth=3

# TODO: Print accuracy

# TODO: Visualize the tree
# Hint: Use plot_tree(model, feature_names=iris.feature_names, 
#                     class_names=iris.target_names, filled=True)

# TODO: Print feature importances
```

<details>
<summary>Solution</summary>

```python
from sklearn.tree import DecisionTreeClassifier, plot_tree

iris = load_iris()
X, y = iris.data, iris.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

tree = DecisionTreeClassifier(max_depth=3, random_state=42)
tree.fit(X_train, y_train)

predictions = tree.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, predictions):.2%}")

# Visualize
plt.figure(figsize=(20, 10))
plot_tree(tree, 
          feature_names=iris.feature_names, 
          class_names=iris.target_names, 
          filled=True,
          rounded=True,
          fontsize=10)
plt.title('Decision Tree for Iris Classification')
plt.tight_layout()
plt.show()

# Feature importance
print("\nFeature Importances:")
for name, importance in sorted(zip(iris.feature_names, tree.feature_importances_), 
                                key=lambda x: -x[1]):
    print(f"  {name}: {importance:.4f}")
```
</details>

---

## Exercise 5: Multi-Class Classification

Handle more than 2 classes.

```python
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression

# Load digits dataset (0-9)
digits = load_digits()
X, y = digits.data, digits.target

# TODO: Split data

# TODO: Train LogisticRegression (multi-class)

# TODO: Print accuracy

# TODO: Print classification report for all 10 classes

# TODO: Visualize some predictions
```

<details>
<summary>Solution</summary>

```python
from sklearn.datasets import load_digits

digits = load_digits()
X, y = digits.data, digits.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LogisticRegression(max_iter=5000)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, predictions):.2%}")

print("\nClassification Report:")
print(classification_report(y_test, predictions))

# Visualize predictions
fig, axes = plt.subplots(2, 5, figsize=(12, 5))
for i, ax in enumerate(axes.flat):
    ax.imshow(X_test[i].reshape(8, 8), cmap='gray')
    ax.set_title(f'Pred: {predictions[i]}, True: {y_test[i]}')
    ax.axis('off')
plt.suptitle('Sample Predictions')
plt.tight_layout()
plt.show()
```
</details>

---

## Exercise 6: Imbalanced Classification

Handle datasets with unequal class distribution.

```python
# Create imbalanced dataset (95% class 0, 5% class 1)
X, y = make_classification(
    n_samples=1000, n_features=10, n_informative=3,
    n_redundant=0, weights=[0.95, 0.05], random_state=42
)

# TODO: Check class distribution

# TODO: Train model without handling imbalance

# TODO: Train model WITH class_weight='balanced'

# TODO: Compare precision, recall, F1 for both

# TODO: Which is better for catching the minority class?
```

<details>
<summary>Solution</summary>

```python
X, y = make_classification(
    n_samples=1000, n_features=10, n_informative=3,
    n_redundant=0, weights=[0.95, 0.05], random_state=42
)

print("Class Distribution:")
print(pd.Series(y).value_counts())
print(f"Class 1 is only {y.mean():.1%} of data\n")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Without handling imbalance
model_default = LogisticRegression()
model_default.fit(X_train, y_train)
pred_default = model_default.predict(X_test)

# With class_weight='balanced'
model_balanced = LogisticRegression(class_weight='balanced')
model_balanced.fit(X_train, y_train)
pred_balanced = model_balanced.predict(X_test)

print("Without class_weight:")
print(f"  Accuracy:  {accuracy_score(y_test, pred_default):.2%}")
print(f"  Precision: {precision_score(y_test, pred_default):.2%}")
print(f"  Recall:    {recall_score(y_test, pred_default):.2%}")
print(f"  F1:        {f1_score(y_test, pred_default):.2%}")

print("\nWith class_weight='balanced':")
print(f"  Accuracy:  {accuracy_score(y_test, pred_balanced):.2%}")
print(f"  Precision: {precision_score(y_test, pred_balanced):.2%}")
print(f"  Recall:    {recall_score(y_test, pred_balanced):.2%}")
print(f"  F1:        {f1_score(y_test, pred_balanced):.2%}")

print("\nConclusion:")
print("class_weight='balanced' improves recall (catching minority class)")
print("at the cost of some precision and overall accuracy")
```
</details>

---

## Key Takeaways

1. **Confusion matrix** shows TP, TN, FP, FN
2. **Precision** = TP / (TP + FP) — "Of predicted positive, how many correct?"
3. **Recall** = TP / (TP + FN) — "Of actual positive, how many caught?"
4. **F1 Score** = Balance between precision and recall
5. **Probability thresholds** trade off precision vs recall
6. **Class imbalance** requires special handling (weights, sampling)

## Quick Reference

```python
# Logistic Regression
from sklearn.linear_model import LogisticRegression
model = LogisticRegression(max_iter=1000, class_weight='balanced')

# Decision Tree
from sklearn.tree import DecisionTreeClassifier
model = DecisionTreeClassifier(max_depth=5)

# Metrics
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions)
recall = recall_score(y_test, predictions)
f1 = f1_score(y_test, predictions)

# Probabilities
proba = model.predict_proba(X_test)[:, 1]  # Probability of class 1
```

## Next Steps
- Try [Intermediate: ROC Curves and AUC](../intermediate/roc_auc.md)
- Learn about [Clustering](../../04_clustering/beginner/kmeans.md)
