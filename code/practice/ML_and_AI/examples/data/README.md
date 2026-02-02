# Shared Datasets

Sample datasets for ML/AI examples.

## Regenerate Datasets

```bash
python generate_datasets.py
```

## Available Datasets

### housing.csv
Housing price regression data.
- **Samples**: 500
- **Features**: sqft, bedrooms, bathrooms, age, garage
- **Target**: price
- **Use case**: Linear regression, Ridge, Lasso

### churn.csv
Customer churn binary classification.
- **Samples**: 1000
- **Features**: tenure, monthly_charges, total_charges, contract, internet_service
- **Target**: churn (0/1)
- **Use case**: Logistic regression, classification

### iris.csv
Flower species multiclass classification.
- **Samples**: 150 (50 per class)
- **Features**: sepal_length, sepal_width, petal_length, petal_width
- **Target**: species (setosa, versicolor, virginica)
- **Use case**: KNN, SVM, decision trees

### customers.csv
Customer segmentation data (RFM-style).
- **Samples**: 300
- **Features**: customer_id, recency, frequency, monetary, age
- **Use case**: K-Means, hierarchical clustering

### text_samples.csv
Sample text for NLP examples.
- **Samples**: 25
- **Features**: text, sentiment
- **Use case**: Tokenization, embeddings demos

### sentiment.csv
Larger sentiment analysis dataset.
- **Samples**: 200
- **Features**: text, sentiment (positive/negative/neutral)
- **Use case**: Text classification, RNN/LSTM

### time_series.csv
Synthetic time series with trend and seasonality.
- **Samples**: 500
- **Features**: date, value
- **Use case**: Time series forecasting, RNN
