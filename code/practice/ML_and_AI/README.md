# ML and AI Practice

Hands-on exercises from classical machine learning through deep learning to generative AI.

## Structure

Each topic directory contains:
- `beginner/` - Basic implementations, single concepts
- `intermediate/` - Integration, tuning, evaluation
- `advanced/` - Production concerns, optimization, custom solutions

## Topics

### Phase 1: scikit-learn (Classical ML)

| # | Topic | Focus |
|---|-------|-------|
| 01 | [sklearn Basics](01_sklearn_basics/) | Data loading, preprocessing, pipelines |
| 02 | [Regression](02_regression/) | Linear, polynomial, regularized |
| 03 | [Classification](03_classification/) | Logistic, KNN, SVM, decision trees |
| 04 | [Clustering](04_clustering/) | K-means, hierarchical, DBSCAN |
| 05 | [Dimensionality](05_dimensionality/) | PCA, t-SNE, feature selection |
| 06 | [Ensemble](06_ensemble/) | Random Forest, Gradient Boosting, XGBoost |
| 07 | [Model Evaluation](07_model_evaluation/) | Metrics, cross-validation, hyperparameter tuning |

### Phase 2: PyTorch (Deep Learning)

| # | Topic | Focus |
|---|-------|-------|
| 08 | [PyTorch Basics](08_pytorch_basics/) | Tensors, autograd, datasets |
| 09 | [Neural Networks](09_neural_networks/) | MLP, training loops, optimization |
| 10 | [CNN Basics](10_cnn_basics/) | Convolutions, image classification |
| 11 | [RNN Basics](11_rnn_basics/) | Sequences, LSTM, text processing |

### Phase 3: Generative AI

| # | Topic | Focus |
|---|-------|-------|
| 12 | [Transformers](12_transformers/) | Attention, Hugging Face, pre-trained models |
| 13 | [Fine-Tuning](13_fine_tuning/) | LoRA, QLoRA, PEFT |
| 14 | [RAG](14_rag/) | Embeddings, vector stores, retrieval |
| 15 | [Agents](15_agents/) | LangGraph, CrewAI, tool use |

## Framework Progression

```
scikit-learn → PyTorch → Hugging Face → LangChain/LangGraph → CrewAI
   (Weeks 1-4)   (Weeks 5-8)   (Weeks 9-10)    (Weeks 11-12)
```

## Environment Setup

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Phase 1: Classical ML
pip install scikit-learn pandas numpy matplotlib seaborn

# Phase 2: Deep Learning
pip install torch torchvision

# Phase 3: GenAI
pip install transformers datasets peft accelerate
pip install langchain langchain-community langgraph
pip install chromadb sentence-transformers
pip install crewai crewai-tools
```

## Exercise Format

Each exercise includes:
- **Objective** - What to build/learn
- **Dataset** - Data to use
- **Tasks** - Step-by-step requirements
- **Hints** - Implementation guidance
- **Solution** - Reference implementation (collapsed)

## Progress Tracking

Use the [LEARNING_ROADMAP.md](LEARNING_ROADMAP.md) for a structured weekly schedule.

## Related Resources

- [ML/AI KB](../../../guides/ML_and_AI/) - Theory and concepts
- [Prompt Engineering](../ai/prompts/) - Prompt crafting practice
