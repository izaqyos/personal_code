#!/usr/bin/env python3
"""Loss Functions Reference"""


def show_reference():
    """Display loss functions reference."""
    print("\n" + "=" * 60)
    print("LOSS FUNCTIONS REFERENCE")
    print("=" * 60)
    
    print("""
╔═══════════════════╦═════════════════════════════════════════════╗
║ Loss Function     ║ Formula / Use Case                          ║
╠═══════════════════╬═════════════════════════════════════════════╣
║                   ║  REGRESSION                                 ║
╠═══════════════════╬═════════════════════════════════════════════╣
║ MSE               ║ (1/n) Σ(y - ŷ)²                            ║
║                   ║ Standard regression, sensitive to outliers  ║
╠═══════════════════╬═════════════════════════════════════════════╣
║ MAE               ║ (1/n) Σ|y - ŷ|                              ║
║                   ║ Robust to outliers                          ║
╠═══════════════════╬═════════════════════════════════════════════╣
║ Huber             ║ MSE if |e| < δ, else MAE                    ║
║                   ║ Best of both worlds                         ║
╠═══════════════════╬═════════════════════════════════════════════╣
║                   ║  CLASSIFICATION                             ║
╠═══════════════════╬═════════════════════════════════════════════╣
║ Binary CE         ║ -[y·log(ŷ) + (1-y)·log(1-ŷ)]               ║
║                   ║ Binary classification                       ║
╠═══════════════════╬═════════════════════════════════════════════╣
║ Cross-Entropy     ║ -Σ yᵢ·log(ŷᵢ)                               ║
║                   ║ Multiclass classification                   ║
╠═══════════════════╬═════════════════════════════════════════════╣
║ Focal Loss        ║ -(1-pₜ)^γ log(pₜ)                           ║
║                   ║ Imbalanced datasets, hard examples          ║
╚═══════════════════╩═════════════════════════════════════════════╝
    """)
    
    print("\nPyTorch Loss Classes:")
    print("-" * 60)
    print("nn.MSELoss()        - Mean Squared Error")
    print("nn.L1Loss()         - Mean Absolute Error")
    print("nn.SmoothL1Loss()   - Huber Loss")
    print("nn.BCELoss()        - Binary Cross-Entropy (after sigmoid)")
    print("nn.BCEWithLogitsLoss() - BCE with built-in sigmoid")
    print("nn.CrossEntropyLoss()  - CE with built-in softmax")
    print("nn.NLLLoss()        - Negative Log Likelihood")
    
    print("\nTips:")
    print("-" * 60)
    print("• Use CrossEntropyLoss with raw logits (no softmax needed)")
    print("• Use BCEWithLogitsLoss with raw logits (no sigmoid needed)")
    print("• For imbalanced classes, use class weights or focal loss")
    print("• Monitor both train and val loss to detect overfitting")


if __name__ == "__main__":
    show_reference()
