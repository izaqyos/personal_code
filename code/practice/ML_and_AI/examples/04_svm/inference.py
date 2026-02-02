#!/usr/bin/env python3
"""SVM Inference Script"""

from pathlib import Path
import joblib
import numpy as np
import pandas as pd

SCRIPT_DIR = Path(__file__).parent
MODEL_DIR = SCRIPT_DIR / "model"
DATA_DIR = SCRIPT_DIR.parent / "data"


def load_model():
    return (
        joblib.load(MODEL_DIR / "model.joblib"),
        joblib.load(MODEL_DIR / "scaler.joblib"),
        joblib.load(MODEL_DIR / "label_encoder.joblib"),
        joblib.load(MODEL_DIR / "features.joblib"),
    )


def demo_predictions():
    print("\n" + "=" * 60)
    print("SVM INFERENCE DEMO")
    print("=" * 60)
    
    model, scaler, le, features = load_model()
    print(f"Model: SVM with {model.kernel} kernel, C={model.C}")
    print(f"Support Vectors: {sum(model.n_support_)}")
    
    samples = [
        [5.0, 3.4, 1.5, 0.2],
        [5.9, 2.8, 4.3, 1.3],
        [6.6, 3.0, 5.6, 2.0],
    ]
    
    print("\nSample Predictions:")
    print("-" * 60)
    
    for sample in samples:
        X = scaler.transform([sample])
        pred = model.predict(X)
        proba = model.predict_proba(X)
        
        print(f"Input: {sample}")
        print(f"  -> {le.inverse_transform(pred)[0]}")
        print(f"  -> Probabilities: {dict(zip(le.classes_, proba[0].round(3)))}\n")
    
    # Batch
    df = pd.read_csv(DATA_DIR / "iris.csv").head()
    X = scaler.transform(df[features])
    df["predicted"] = le.inverse_transform(model.predict(X))
    df["correct"] = df["species"] == df["predicted"]
    
    print("Batch Prediction:")
    print(df[["sepal_length", "petal_length", "species", "predicted", "correct"]].to_string(index=False))


if __name__ == "__main__":
    demo_predictions()
