#!/usr/bin/env python3
"""Decision Tree Inference Script"""

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
        joblib.load(MODEL_DIR / "label_encoder.joblib"),
        joblib.load(MODEL_DIR / "features.joblib"),
    )


def demo_predictions():
    print("\n" + "=" * 60)
    print("DECISION TREE INFERENCE DEMO")
    print("=" * 60)
    
    model, le, features = load_model()
    print(f"Tree Depth: {model.get_depth()}, Leaves: {model.get_n_leaves()}")
    
    # Feature importance
    print("\nFeature Importance:")
    for feat, imp in zip(features, model.feature_importances_):
        print(f"  {feat}: {imp:.4f}")
    
    samples = [
        [5.0, 3.4, 1.5, 0.2],
        [5.9, 2.8, 4.3, 1.3],
        [6.6, 3.0, 5.6, 2.0],
    ]
    
    print("\nSample Predictions:")
    print("-" * 60)
    
    for sample in samples:
        X = np.array([sample])
        pred = model.predict(X)
        proba = model.predict_proba(X)
        
        print(f"Input: {sample}")
        print(f"  -> {le.inverse_transform(pred)[0]}")
        print(f"  -> Leaf: {model.apply(X)[0]}")
        print()
    
    # Batch
    df = pd.read_csv(DATA_DIR / "iris.csv").head()
    df["predicted"] = le.inverse_transform(model.predict(df[features]))
    df["correct"] = df["species"] == df["predicted"]
    df["leaf_id"] = model.apply(df[features])
    
    print("Batch Prediction:")
    print(df[["petal_length", "petal_width", "species", "predicted", "leaf_id"]].to_string(index=False))


if __name__ == "__main__":
    demo_predictions()
