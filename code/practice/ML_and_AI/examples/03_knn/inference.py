#!/usr/bin/env python3
"""KNN Inference Script"""

from pathlib import Path
import joblib
import numpy as np
import pandas as pd

SCRIPT_DIR = Path(__file__).parent
MODEL_DIR = SCRIPT_DIR / "model"
DATA_DIR = SCRIPT_DIR.parent / "data"


def load_model():
    model = joblib.load(MODEL_DIR / "model.joblib")
    scaler = joblib.load(MODEL_DIR / "scaler.joblib")
    le = joblib.load(MODEL_DIR / "label_encoder.joblib")
    features = joblib.load(MODEL_DIR / "features.joblib")
    return model, scaler, le, features


def predict(sepal_length: float, sepal_width: float, 
            petal_length: float, petal_width: float) -> str:
    model, scaler, le, features = load_model()
    X = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
    X_scaled = scaler.transform(X)
    pred = model.predict(X_scaled)
    return le.inverse_transform(pred)[0]


def demo_predictions():
    print("\n" + "=" * 60)
    print("KNN INFERENCE DEMO")
    print("=" * 60)
    
    model, scaler, le, features = load_model()
    print(f"Model: {model.n_neighbors}-NN with {model.metric} distance")
    
    samples = [
        [5.0, 3.4, 1.5, 0.2],  # Setosa-like
        [5.9, 2.8, 4.3, 1.3],  # Versicolor-like
        [6.6, 3.0, 5.6, 2.0],  # Virginica-like
    ]
    
    print("\nSample Predictions:")
    print("-" * 60)
    
    for sample in samples:
        X = np.array([sample])
        X_scaled = scaler.transform(X)
        pred = model.predict(X_scaled)
        proba = model.predict_proba(X_scaled)
        species = le.inverse_transform(pred)[0]
        
        print(f"Input: {sample}")
        print(f"  -> Predicted: {species}")
        print(f"  -> Probabilities: {dict(zip(le.classes_, proba[0].round(3)))}")
        print()
    
    # Batch from file
    print("-" * 60)
    print("Batch Prediction (first 5 from iris.csv)")
    print("-" * 60)
    
    df = pd.read_csv(DATA_DIR / "iris.csv").head()
    X = scaler.transform(df[features])
    preds = model.predict(X)
    df["predicted"] = le.inverse_transform(preds)
    df["correct"] = df["species"] == df["predicted"]
    
    print(df[["sepal_length", "petal_length", "species", "predicted", "correct"]].to_string(index=False))


if __name__ == "__main__":
    demo_predictions()
