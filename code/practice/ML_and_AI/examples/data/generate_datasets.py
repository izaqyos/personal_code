#!/usr/bin/env python3
"""
Generate sample datasets for ML/AI examples.

Run this script to create all sample CSV files:
    python generate_datasets.py

Datasets created:
- housing.csv: Housing prices for regression
- churn.csv: Customer churn for binary classification
- iris.csv: Iris flowers for multiclass classification
- customers.csv: Customer data for clustering
- text_samples.csv: Text data for NLP examples
- sentiment.csv: Sentiment analysis data
- time_series.csv: Time series data
"""

import numpy as np
import pandas as pd
from pathlib import Path

# Reproducibility
np.random.seed(42)

DATA_DIR = Path(__file__).parent


def generate_housing_data(n_samples: int = 500) -> pd.DataFrame:
    """Generate synthetic housing price data."""
    # Features
    sqft = np.random.uniform(800, 4000, n_samples)
    bedrooms = np.random.randint(1, 6, n_samples)
    bathrooms = np.random.randint(1, 4, n_samples)
    age = np.random.randint(0, 50, n_samples)
    garage = np.random.randint(0, 3, n_samples)
    
    # Price with some noise (linear combination + noise)
    price = (
        50000 +
        100 * sqft +
        15000 * bedrooms +
        10000 * bathrooms -
        1000 * age +
        20000 * garage +
        np.random.normal(0, 30000, n_samples)
    )
    price = np.maximum(price, 50000)  # Minimum price
    
    return pd.DataFrame({
        'sqft': sqft.astype(int),
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'age': age,
        'garage': garage,
        'price': price.astype(int)
    })


def generate_churn_data(n_samples: int = 1000) -> pd.DataFrame:
    """Generate synthetic customer churn data."""
    # Features
    tenure = np.random.randint(1, 72, n_samples)  # months
    monthly_charges = np.random.uniform(20, 100, n_samples)
    total_charges = tenure * monthly_charges + np.random.normal(0, 100, n_samples)
    total_charges = np.maximum(total_charges, 0)
    
    contract = np.random.choice(['month-to-month', 'one_year', 'two_year'], n_samples, p=[0.5, 0.3, 0.2])
    internet_service = np.random.choice(['dsl', 'fiber', 'none'], n_samples, p=[0.4, 0.4, 0.2])
    
    # Churn probability based on features
    churn_prob = (
        0.3 +
        0.3 * (contract == 'month-to-month') -
        0.2 * (tenure / 72) +
        0.1 * (monthly_charges / 100) -
        0.15 * (contract == 'two_year')
    )
    churn_prob = np.clip(churn_prob, 0.05, 0.95)
    churn = (np.random.random(n_samples) < churn_prob).astype(int)
    
    return pd.DataFrame({
        'tenure': tenure,
        'monthly_charges': monthly_charges.round(2),
        'total_charges': total_charges.round(2),
        'contract': contract,
        'internet_service': internet_service,
        'churn': churn
    })


def generate_iris_data() -> pd.DataFrame:
    """Generate iris-like flower data."""
    n_per_class = 50
    
    # Setosa
    setosa = pd.DataFrame({
        'sepal_length': np.random.normal(5.0, 0.35, n_per_class),
        'sepal_width': np.random.normal(3.4, 0.38, n_per_class),
        'petal_length': np.random.normal(1.5, 0.17, n_per_class),
        'petal_width': np.random.normal(0.2, 0.1, n_per_class),
        'species': 'setosa'
    })
    
    # Versicolor
    versicolor = pd.DataFrame({
        'sepal_length': np.random.normal(5.9, 0.52, n_per_class),
        'sepal_width': np.random.normal(2.8, 0.31, n_per_class),
        'petal_length': np.random.normal(4.3, 0.47, n_per_class),
        'petal_width': np.random.normal(1.3, 0.2, n_per_class),
        'species': 'versicolor'
    })
    
    # Virginica
    virginica = pd.DataFrame({
        'sepal_length': np.random.normal(6.6, 0.64, n_per_class),
        'sepal_width': np.random.normal(3.0, 0.32, n_per_class),
        'petal_length': np.random.normal(5.6, 0.55, n_per_class),
        'petal_width': np.random.normal(2.0, 0.27, n_per_class),
        'species': 'virginica'
    })
    
    df = pd.concat([setosa, versicolor, virginica], ignore_index=True)
    return df.round(2)


def generate_customer_data(n_samples: int = 300) -> pd.DataFrame:
    """Generate customer data for clustering (RFM-style)."""
    # Recency (days since last purchase)
    recency = np.random.exponential(30, n_samples)
    recency = np.clip(recency, 1, 365).astype(int)
    
    # Frequency (number of purchases)
    frequency = np.random.poisson(5, n_samples) + 1
    
    # Monetary (average purchase value)
    monetary = np.random.lognormal(4, 0.8, n_samples)
    monetary = np.clip(monetary, 10, 5000).round(2)
    
    # Age
    age = np.random.normal(40, 12, n_samples)
    age = np.clip(age, 18, 80).astype(int)
    
    return pd.DataFrame({
        'customer_id': range(1, n_samples + 1),
        'recency': recency,
        'frequency': frequency,
        'monetary': monetary,
        'age': age
    })


def generate_text_samples() -> pd.DataFrame:
    """Generate sample text data for NLP examples."""
    samples = [
        # Positive
        ("I love this product! It's amazing and works perfectly.", "positive"),
        ("Best purchase I've ever made. Highly recommend!", "positive"),
        ("Excellent quality and fast shipping. Very happy!", "positive"),
        ("This exceeded my expectations. Wonderful!", "positive"),
        ("Great value for money. Will buy again.", "positive"),
        ("Fantastic experience from start to finish.", "positive"),
        ("Absolutely brilliant. Couldn't be happier.", "positive"),
        ("Top notch quality. Five stars!", "positive"),
        ("Perfect fit and great design. Love it!", "positive"),
        ("Outstanding service and product. Thank you!", "positive"),
        
        # Negative
        ("Terrible product. Complete waste of money.", "negative"),
        ("Broke after one day. Very disappointed.", "negative"),
        ("Poor quality and slow delivery. Avoid!", "negative"),
        ("Not as described. Requesting refund.", "negative"),
        ("Worst purchase ever. Do not recommend.", "negative"),
        ("Cheap materials and bad construction.", "negative"),
        ("Customer service was unhelpful and rude.", "negative"),
        ("Arrived damaged and missing parts.", "negative"),
        ("Completely useless. Total disappointment.", "negative"),
        ("Overpriced garbage. Save your money.", "negative"),
        
        # Neutral
        ("It's okay. Does what it's supposed to do.", "neutral"),
        ("Average product. Nothing special.", "neutral"),
        ("Meets basic expectations. Adequate.", "neutral"),
        ("Fair quality for the price point.", "neutral"),
        ("Standard product. No complaints, no praise.", "neutral"),
    ]
    
    return pd.DataFrame(samples, columns=['text', 'sentiment'])


def generate_sentiment_data(n_samples: int = 200) -> pd.DataFrame:
    """Generate larger sentiment dataset for training."""
    positive_words = ['great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'best', 'perfect']
    negative_words = ['terrible', 'awful', 'horrible', 'worst', 'hate', 'disappointing', 'poor', 'bad']
    neutral_words = ['okay', 'fine', 'average', 'normal', 'standard', 'acceptable', 'fair', 'decent']
    
    templates = [
        "This product is {}.",
        "I think it's {}.",
        "The quality is {}.",
        "My experience was {}.",
        "Overall, it's {}."
    ]
    
    data = []
    for _ in range(n_samples):
        sentiment = np.random.choice(['positive', 'negative', 'neutral'], p=[0.4, 0.4, 0.2])
        template = np.random.choice(templates)
        
        if sentiment == 'positive':
            word = np.random.choice(positive_words)
        elif sentiment == 'negative':
            word = np.random.choice(negative_words)
        else:
            word = np.random.choice(neutral_words)
        
        text = template.format(word)
        data.append((text, sentiment))
    
    return pd.DataFrame(data, columns=['text', 'sentiment'])


def generate_time_series(n_points: int = 500) -> pd.DataFrame:
    """Generate synthetic time series data."""
    t = np.arange(n_points)
    
    # Trend + seasonality + noise
    trend = 0.05 * t
    seasonality = 10 * np.sin(2 * np.pi * t / 50)
    noise = np.random.normal(0, 2, n_points)
    
    value = 100 + trend + seasonality + noise
    
    # Create dates
    dates = pd.date_range(start='2023-01-01', periods=n_points, freq='D')
    
    return pd.DataFrame({
        'date': dates,
        'value': value.round(2)
    })


def main():
    """Generate all datasets."""
    print("Generating datasets...")
    
    # Housing data
    housing = generate_housing_data()
    housing.to_csv(DATA_DIR / 'housing.csv', index=False)
    print(f"  housing.csv: {len(housing)} samples")
    
    # Churn data
    churn = generate_churn_data()
    churn.to_csv(DATA_DIR / 'churn.csv', index=False)
    print(f"  churn.csv: {len(churn)} samples")
    
    # Iris data
    iris = generate_iris_data()
    iris.to_csv(DATA_DIR / 'iris.csv', index=False)
    print(f"  iris.csv: {len(iris)} samples")
    
    # Customer data
    customers = generate_customer_data()
    customers.to_csv(DATA_DIR / 'customers.csv', index=False)
    print(f"  customers.csv: {len(customers)} samples")
    
    # Text samples
    text = generate_text_samples()
    text.to_csv(DATA_DIR / 'text_samples.csv', index=False)
    print(f"  text_samples.csv: {len(text)} samples")
    
    # Sentiment data
    sentiment = generate_sentiment_data()
    sentiment.to_csv(DATA_DIR / 'sentiment.csv', index=False)
    print(f"  sentiment.csv: {len(sentiment)} samples")
    
    # Time series
    ts = generate_time_series()
    ts.to_csv(DATA_DIR / 'time_series.csv', index=False)
    print(f"  time_series.csv: {len(ts)} samples")
    
    print("\nAll datasets generated successfully!")


if __name__ == '__main__':
    main()
