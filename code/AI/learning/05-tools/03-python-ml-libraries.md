# Python ML Libraries Guide

> Essential libraries for machine learning with code examples.

---

## Overview

This guide covers the most important Python libraries for ML/AI development, with practical code snippets.

---

## Data Manipulation

### NumPy

```python
"""
NumPy: Foundation for numerical computing
- N-dimensional arrays
- Broadcasting
- Linear algebra
- Random sampling
"""
import numpy as np

# Array creation
arr = np.array([1, 2, 3])
zeros = np.zeros((3, 4))
ones = np.ones((2, 3))
range_arr = np.arange(0, 10, 2)  # [0, 2, 4, 6, 8]
linspace = np.linspace(0, 1, 5)  # [0, 0.25, 0.5, 0.75, 1]
random = np.random.randn(3, 4)  # Normal distribution

# Array operations
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])
print(a + b)        # Element-wise addition
print(a @ b)        # Matrix multiplication
print(a.T)          # Transpose
print(np.dot(a, b)) # Dot product

# Indexing and slicing
arr = np.arange(12).reshape(3, 4)
print(arr[0, 1])      # Single element
print(arr[:, 1])      # Column
print(arr[1, :])      # Row
print(arr[arr > 5])   # Boolean indexing

# Broadcasting
a = np.array([[1], [2], [3]])  # (3, 1)
b = np.array([4, 5, 6])         # (3,)
print(a + b)  # Broadcasts to (3, 3)

# Linear algebra
eigenvalues, eigenvectors = np.linalg.eig(a)
inverse = np.linalg.inv(a)
determinant = np.linalg.det(a)
```

### Pandas

```python
"""
Pandas: Data manipulation and analysis
- DataFrames and Series
- Data cleaning
- Grouping and aggregation
- File I/O
"""
import pandas as pd

# Creating DataFrames
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'score': [85.5, 90.0, 78.5]
})

# Reading data
df = pd.read_csv('data.csv')
df = pd.read_json('data.json')
df = pd.read_parquet('data.parquet')

# Basic operations
print(df.head())
print(df.describe())
print(df.info())
print(df.shape)

# Selection
df['name']              # Column
df[['name', 'age']]     # Multiple columns
df.loc[0]               # Row by label
df.iloc[0:5]            # Rows by position
df[df['age'] > 25]      # Boolean filter

# Data manipulation
df['new_col'] = df['age'] * 2
df = df.drop('new_col', axis=1)
df = df.rename(columns={'name': 'full_name'})
df = df.sort_values('age', ascending=False)

# Grouping and aggregation
grouped = df.groupby('category').agg({
    'value': ['mean', 'sum', 'count'],
    'score': 'max'
})

# Missing data
df.isna().sum()
df.fillna(0)
df.dropna()

# Merge and join
merged = pd.merge(df1, df2, on='key', how='left')
concatenated = pd.concat([df1, df2], axis=0)
```

---

## Deep Learning Frameworks

### PyTorch

```python
"""
PyTorch: Deep learning framework
- Dynamic computation graphs
- GPU acceleration
- Automatic differentiation
- Rich ecosystem
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader

# Tensors
x = torch.tensor([1, 2, 3])
x = torch.zeros(3, 4)
x = torch.randn(3, 4)
x = torch.from_numpy(np_array)

# GPU operations
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
x = x.to(device)

# Autograd
x = torch.randn(3, requires_grad=True)
y = x ** 2
y.sum().backward()
print(x.grad)  # Gradient

# Neural network module
class MLP(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, output_dim)
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x

# Dataset
class CustomDataset(Dataset):
    def __init__(self, data, labels):
        self.data = data
        self.labels = labels

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]

# Training loop
model = MLP(784, 256, 10).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

for epoch in range(epochs):
    for batch_x, batch_y in dataloader:
        batch_x, batch_y = batch_x.to(device), batch_y.to(device)

        optimizer.zero_grad()
        outputs = model(batch_x)
        loss = criterion(outputs, batch_y)
        loss.backward()
        optimizer.step()

# Save and load
torch.save(model.state_dict(), 'model.pth')
model.load_state_dict(torch.load('model.pth'))
```

### TensorFlow/Keras

```python
"""
TensorFlow/Keras: Deep learning framework
- Production-ready
- TensorFlow Serving
- Keras high-level API
"""
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Sequential model
model = keras.Sequential([
    layers.Dense(128, activation='relu', input_shape=(784,)),
    layers.Dropout(0.5),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')
])

# Functional API
inputs = keras.Input(shape=(784,))
x = layers.Dense(128, activation='relu')(inputs)
x = layers.Dropout(0.5)(x)
outputs = layers.Dense(10, activation='softmax')(x)
model = keras.Model(inputs, outputs)

# Compile and train
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.fit(
    x_train, y_train,
    epochs=10,
    batch_size=32,
    validation_split=0.2,
    callbacks=[
        keras.callbacks.EarlyStopping(patience=3),
        keras.callbacks.ModelCheckpoint('best_model.h5')
    ]
)

# Save and load
model.save('model.h5')
model = keras.models.load_model('model.h5')
```

---

## Scikit-learn

```python
"""
Scikit-learn: Classical ML library
- Preprocessing
- Model selection
- Evaluation metrics
- Pipelines
"""
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.pipeline import Pipeline

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Preprocessing
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Model training
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Predictions
y_pred = model.predict(X_test_scaled)
y_prob = model.predict_proba(X_test_scaled)

# Evaluation
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))

# Cross-validation
scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
print(f"CV Scores: {scores.mean():.4f} (+/- {scores.std():.4f})")

# Hyperparameter tuning
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(
    RandomForestClassifier(),
    param_grid,
    cv=5,
    scoring='accuracy',
    n_jobs=-1
)
grid_search.fit(X_train, y_train)
print(f"Best params: {grid_search.best_params_}")

# Pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', LogisticRegression())
])
pipeline.fit(X_train, y_train)
```

---

## NLP Libraries

### Hugging Face Transformers

```python
"""
Transformers: State-of-the-art NLP
- Pretrained models
- Easy fine-tuning
- Multiple frameworks
"""
from transformers import (
    AutoTokenizer,
    AutoModel,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
    pipeline
)

# Quick inference with pipelines
classifier = pipeline("sentiment-analysis")
result = classifier("I love this product!")
print(result)  # [{'label': 'POSITIVE', 'score': 0.99}]

generator = pipeline("text-generation", model="gpt2")
text = generator("Once upon a time", max_length=50)

# Load model and tokenizer
model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Tokenization
text = "Hello, how are you?"
inputs = tokenizer(
    text,
    return_tensors="pt",
    padding=True,
    truncation=True,
    max_length=512
)

# Get embeddings
with torch.no_grad():
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state

# Fine-tuning with Trainer
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=64,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="./logs",
    evaluation_strategy="epoch"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    compute_metrics=compute_metrics
)

trainer.train()
```

### spaCy

```python
"""
spaCy: Industrial-strength NLP
- Fast and efficient
- Named entity recognition
- Dependency parsing
- Custom pipelines
"""
import spacy

# Load model
nlp = spacy.load("en_core_web_sm")

# Process text
doc = nlp("Apple is looking at buying U.K. startup for $1 billion")

# Tokenization
for token in doc:
    print(token.text, token.pos_, token.dep_)

# Named entities
for ent in doc.ents:
    print(ent.text, ent.label_)

# Similarity
doc1 = nlp("I like cats")
doc2 = nlp("I love dogs")
print(doc1.similarity(doc2))

# Custom pipeline component
@spacy.Language.component("custom_component")
def custom_component(doc):
    # Process doc
    return doc

nlp.add_pipe("custom_component")
```

---

## Computer Vision

### OpenCV

```python
"""
OpenCV: Computer vision library
- Image processing
- Video capture
- Feature detection
"""
import cv2
import numpy as np

# Read and display image
img = cv2.imread('image.jpg')
cv2.imshow('Image', img)
cv2.waitKey(0)

# Convert color spaces
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Resize
resized = cv2.resize(img, (224, 224))

# Image transformations
blurred = cv2.GaussianBlur(img, (5, 5), 0)
edges = cv2.Canny(img, 100, 200)
thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1]

# Drawing
cv2.rectangle(img, (10, 10), (100, 100), (0, 255, 0), 2)
cv2.circle(img, (50, 50), 20, (0, 0, 255), -1)
cv2.putText(img, 'Hello', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

# Video capture
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
```

### torchvision

```python
"""
torchvision: PyTorch computer vision
- Datasets
- Transforms
- Pretrained models
"""
import torchvision
import torchvision.transforms as T
from torchvision import models

# Transforms
transform = T.Compose([
    T.Resize(256),
    T.CenterCrop(224),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Datasets
train_dataset = torchvision.datasets.ImageFolder(
    root='data/train',
    transform=transform
)

# Data augmentation
aug_transform = T.Compose([
    T.RandomResizedCrop(224),
    T.RandomHorizontalFlip(),
    T.ColorJitter(brightness=0.2, contrast=0.2),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Pretrained models
model = models.resnet50(pretrained=True)

# Feature extraction
model.fc = nn.Identity()  # Remove classifier
features = model(images)  # Extract features

# Fine-tuning
model.fc = nn.Linear(2048, num_classes)
for param in model.parameters():
    param.requires_grad = False
for param in model.fc.parameters():
    param.requires_grad = True
```

---

## Experiment Tracking

### Weights & Biases

```python
"""
wandb: Experiment tracking
- Logging metrics
- Hyperparameter sweeps
- Model versioning
"""
import wandb

# Initialize
wandb.init(
    project="my-project",
    config={
        "learning_rate": 0.001,
        "epochs": 10,
        "batch_size": 32
    }
)

# Log metrics
for epoch in range(epochs):
    train_loss = train()
    val_loss = validate()

    wandb.log({
        "epoch": epoch,
        "train_loss": train_loss,
        "val_loss": val_loss
    })

# Log images
wandb.log({"images": [wandb.Image(img, caption="Sample")]})

# Log model
wandb.save("model.pth")

# Finish
wandb.finish()

# Hyperparameter sweep
sweep_config = {
    "method": "bayes",
    "metric": {"name": "val_loss", "goal": "minimize"},
    "parameters": {
        "learning_rate": {"min": 0.0001, "max": 0.1},
        "batch_size": {"values": [16, 32, 64]}
    }
}
sweep_id = wandb.sweep(sweep_config, project="my-project")
wandb.agent(sweep_id, train_func, count=10)
```

---

## Utility Libraries

### tqdm (Progress Bars)

```python
from tqdm import tqdm, trange

# Basic usage
for i in tqdm(range(100)):
    process(i)

# With description
for batch in tqdm(dataloader, desc="Training"):
    train_step(batch)

# Nested loops
for epoch in trange(epochs, desc="Epochs"):
    for batch in tqdm(dataloader, desc="Batches", leave=False):
        train_step(batch)
```

### einops (Tensor Operations)

```python
"""
einops: Readable tensor operations
- Rearrange, reduce, repeat
- Framework agnostic
"""
from einops import rearrange, reduce, repeat

# Rearrange dimensions
x = rearrange(x, 'b c h w -> b (h w) c')  # Flatten spatial
x = rearrange(x, 'b (h w) c -> b c h w', h=14, w=14)  # Unflatten

# Attention reshaping
q = rearrange(q, 'b n (h d) -> b h n d', h=num_heads)

# Reduce
x = reduce(x, 'b c h w -> b c', 'mean')  # Global average pooling

# Repeat
x = repeat(x, 'b c -> b c h w', h=7, w=7)  # Expand dims
```

### OmegaConf (Configuration)

```python
"""
OmegaConf: Hierarchical configuration
- YAML support
- Variable interpolation
- Type safety
"""
from omegaconf import OmegaConf

# Load config
config = OmegaConf.load("config.yaml")

# Access values
print(config.model.hidden_size)
print(config.training.learning_rate)

# Merge configs
base = OmegaConf.load("base.yaml")
override = OmegaConf.load("override.yaml")
config = OmegaConf.merge(base, override)

# Create from dict
config = OmegaConf.create({
    "model": {"hidden_size": 256},
    "training": {"lr": 0.001}
})

# Variable interpolation (in YAML)
# model:
#   hidden_size: 256
# ffn_size: ${model.hidden_size} * 4
```

---

## Library Summary Table

| Library | Purpose | Key Use Cases |
|---------|---------|---------------|
| **NumPy** | Numerical computing | Arrays, linear algebra |
| **Pandas** | Data manipulation | DataFrames, I/O |
| **PyTorch** | Deep learning | Models, training |
| **TensorFlow** | Deep learning | Production, serving |
| **scikit-learn** | Classical ML | Preprocessing, models |
| **Transformers** | NLP models | BERT, GPT, fine-tuning |
| **spaCy** | NLP processing | NER, parsing |
| **OpenCV** | Computer vision | Image processing |
| **torchvision** | CV for PyTorch | Datasets, transforms |
| **wandb** | Experiment tracking | Logging, sweeps |
| **tqdm** | Progress bars | Training loops |
| **einops** | Tensor ops | Readable reshaping |
| **OmegaConf** | Configuration | YAML configs |

---

## Exercises

1. **NumPy**: Implement matrix multiplication from scratch
2. **Pandas**: Load, clean, and analyze a dataset
3. **PyTorch**: Build and train a CNN on CIFAR-10
4. **Transformers**: Fine-tune BERT for sentiment analysis
5. **scikit-learn**: Build a complete ML pipeline with cross-validation

---

## Key Takeaways

- NumPy/Pandas for data manipulation
- PyTorch/TensorFlow for deep learning
- scikit-learn for classical ML and preprocessing
- Hugging Face for NLP
- OpenCV/torchvision for computer vision
- wandb for experiment tracking
- einops for readable tensor operations
- Use the right tool for the job!
