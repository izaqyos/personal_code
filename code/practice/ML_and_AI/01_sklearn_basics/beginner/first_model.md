# First ML Model - Beginner

Build your first machine learning model with scikit-learn.

## Learning Objectives
- Load and explore a dataset
- Split data into train/test sets
- Train a simple classifier
- Evaluate model performance

## Setup

```bash
pip install scikit-learn pandas numpy matplotlib
```

---

## Exercise 1: Load and Explore Data

Load the Iris dataset and understand its structure.

```python
from sklearn.datasets import load_iris
import pandas as pd

# Load dataset
iris = load_iris()

# TODO: Create a DataFrame with the data
# Hint: Use pd.DataFrame(iris.data, columns=iris.feature_names)

# TODO: Add target column
# Hint: df['target'] = iris.target

# TODO: Print first 5 rows

# TODO: Print shape of the data

# TODO: Print class distribution
# Hint: Use value_counts()
```

<details>
<summary>Solution</summary>

```python
from sklearn.datasets import load_iris
import pandas as pd

iris = load_iris()

df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['target'] = iris.target
df['species'] = df['target'].map({0: 'setosa', 1: 'versicolor', 2: 'virginica'})

print("First 5 rows:")
print(df.head())

print(f"\nShape: {df.shape}")

print("\nClass distribution:")
print(df['species'].value_counts())
```
</details>

---

## Exercise 2: Split Data

Split data into training and testing sets.

```python
from sklearn.model_selection import train_test_split

# TODO: Separate features (X) and target (y)
# X should have shape (150, 4)
# y should have shape (150,)

# TODO: Split into train (80%) and test (20%) sets
# Hint: Use train_test_split with test_size=0.2

# TODO: Print shapes of all splits

# TODO: Verify class balance in train and test
```

<details>
<summary>Solution</summary>

```python
from sklearn.model_selection import train_test_split

X = iris.data  # Features
y = iris.target  # Target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    random_state=42,
    stratify=y  # Maintain class proportions
)

print(f"X_train shape: {X_train.shape}")
print(f"X_test shape: {X_test.shape}")
print(f"y_train shape: {y_train.shape}")
print(f"y_test shape: {y_test.shape}")

print(f"\nTrain class distribution: {pd.Series(y_train).value_counts().sort_index().tolist()}")
print(f"Test class distribution: {pd.Series(y_test).value_counts().sort_index().tolist()}")
```
</details>

---

## Exercise 3: Train a Model

Train a K-Nearest Neighbors classifier.

```python
from sklearn.neighbors import KNeighborsClassifier

# TODO: Create a KNN classifier with k=3

# TODO: Fit the model on training data

# TODO: Make predictions on test data

# TODO: Print first 10 predictions vs actual values
```

<details>
<summary>Solution</summary>

```python
from sklearn.neighbors import KNeighborsClassifier

# Create model
knn = KNeighborsClassifier(n_neighbors=3)

# Train model
knn.fit(X_train, y_train)

# Predict
predictions = knn.predict(X_test)

# Compare
print("First 10 predictions:")
for i in range(10):
    pred = iris.target_names[predictions[i]]
    actual = iris.target_names[y_test[i]]
    match = "✓" if predictions[i] == y_test[i] else "✗"
    print(f"  Predicted: {pred:12} Actual: {actual:12} {match}")
```
</details>

---

## Exercise 4: Evaluate Model

Calculate accuracy and examine the confusion matrix.

```python
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# TODO: Calculate accuracy score

# TODO: Print confusion matrix

# TODO: Print classification report
```

<details>
<summary>Solution</summary>

```python
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Accuracy
accuracy = accuracy_score(y_test, predictions)
print(f"Accuracy: {accuracy:.2%}")

# Confusion Matrix
cm = confusion_matrix(y_test, predictions)
print("\nConfusion Matrix:")
print(cm)

# Classification Report
print("\nClassification Report:")
print(classification_report(y_test, predictions, target_names=iris.target_names))
```
</details>

---

## Exercise 5: Try Different Models

Compare multiple algorithms on the same data.

```python
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC

# TODO: Create a list of models to try
models = [
    ("KNN", KNeighborsClassifier(n_neighbors=3)),
    # Add more models...
]

# TODO: Train each model and print accuracy
# for name, model in models:
#     ...
```

<details>
<summary>Solution</summary>

```python
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC

models = [
    ("KNN (k=3)", KNeighborsClassifier(n_neighbors=3)),
    ("KNN (k=5)", KNeighborsClassifier(n_neighbors=5)),
    ("Logistic Regression", LogisticRegression(max_iter=200)),
    ("Decision Tree", DecisionTreeClassifier(max_depth=3)),
    ("SVM", SVC(kernel='rbf')),
]

print("Model Comparison:")
print("-" * 40)
for name, model in models:
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"{name:25} Accuracy: {accuracy:.2%}")
```
</details>

---

## Exercise 6: Cross-Validation

Use cross-validation for more robust evaluation.

```python
from sklearn.model_selection import cross_val_score

# TODO: Perform 5-fold cross-validation on the KNN model

# TODO: Print mean and standard deviation of scores

# TODO: Compare with train/test split accuracy
```

<details>
<summary>Solution</summary>

```python
from sklearn.model_selection import cross_val_score

knn = KNeighborsClassifier(n_neighbors=3)

# 5-fold cross-validation
cv_scores = cross_val_score(knn, X, y, cv=5, scoring='accuracy')

print("Cross-Validation Results:")
print(f"Scores: {cv_scores}")
print(f"Mean accuracy: {cv_scores.mean():.2%}")
print(f"Std deviation: {cv_scores.std():.2%}")

# Single train/test split for comparison
knn.fit(X_train, y_train)
test_accuracy = knn.score(X_test, y_test)
print(f"\nSingle split accuracy: {test_accuracy:.2%}")
```
</details>

---

## Key Takeaways

1. **Load data** → Understand its structure and features
2. **Split data** → Always separate train and test sets
3. **Train model** → Fit on training data only
4. **Evaluate** → Measure performance on test data
5. **Compare** → Try multiple algorithms
6. **Cross-validate** → Get robust performance estimates

## Complete Workflow

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report

# 1. Load data
iris = load_iris()
X, y = iris.data, iris.target

# 2. Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 3. Train model
model = KNeighborsClassifier(n_neighbors=3)
model.fit(X_train, y_train)

# 4. Evaluate
predictions = model.predict(X_test)
print(f"Test Accuracy: {accuracy_score(y_test, predictions):.2%}")

# 5. Cross-validate
cv_scores = cross_val_score(model, X, y, cv=5)
print(f"CV Accuracy: {cv_scores.mean():.2%} (+/- {cv_scores.std()*2:.2%})")
```

## Next Steps
- Try [Intermediate: Feature Engineering](../intermediate/feature_engineering.md)
- Learn about [Regression](../../02_regression/beginner/linear_regression.md)
