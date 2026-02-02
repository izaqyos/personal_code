#!/usr/bin/env python3
"""Random Forest Inference Script"""

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
    print("RANDOM FOREST INFERENCE DEMO")
    print("=" * 60)
    
    model, le, features = load_model()
    print(f"Trees: {model.n_estimators}, OOB Score: {model.oob_score_:.4f}")
    
    print("\nFeature Importance:")
    for feat, imp in zip(features, model.feature_importances_):
        print(f"  {feat}: {imp:.4f}")
    
    samples = [[5.0, 3.4, 1.5, 0.2], [5.9, 2.8, 4.3, 1.3], [6.6, 3.0, 5.6, 2.0]]
    
    print("\nSample Predictions:")
    print("-" * 60)
    
    for sample in samples:
        X = np.array([sample])
        pred = model.predict(X)
        proba = model.predict_proba(X)
        
        # Show individual tree votes
        tree_preds = [tree.predict(X)[0] for tree in model.estimators_[:5]]
        
        print(f"Input: {sample}")
        print(f"  -> {le.inverse_transform(pred)[0]}")
        print(f"  -> Proba: {dict(zip(le.classes_, proba[0].round(3)))}")
        print(f"  -> First 5 tree votes: {tree_preds}")
        print()
    
    df = pd.read_csv(DATA_DIR / "iris.csv").head()
    df["predicted"] = le.inverse_transform(model.predict(df[features]))
    print("Batch Prediction:")
    print(df[["petal_length", "petal_width", "species", "predicted"]].to_string(index=False))


if __name__ == "__main__":
    demo_predictions()
