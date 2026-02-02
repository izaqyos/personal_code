# ML and AI Knowledge Base

From classical machine learning fundamentals through deep learning to generative AI.

## Contents

### [01. Classical ML](01_classical_ml/)
Traditional machine learning algorithms and techniques.

- [Supervised Learning Overview](01_classical_ml/supervised_learning.md) - Regression vs classification
- [Linear Regression](01_classical_ml/linear_regression.md) - OLS, regularization, assumptions
- [Logistic Regression](01_classical_ml/logistic_regression.md) - Binary/multi-class classification
- [KNN](01_classical_ml/knn.md) - K-Nearest Neighbors, distance metrics
- [SVM](01_classical_ml/svm.md) - Support Vector Machines, kernels
- [Decision Trees](01_classical_ml/decision_trees.md) - Splitting criteria, pruning
- [Ensemble Methods](01_classical_ml/ensemble_methods.md) - Random Forest, Gradient Boosting, XGBoost
- [Unsupervised Learning](01_classical_ml/unsupervised_learning.md) - Clustering, dimensionality reduction
- [Model Evaluation](01_classical_ml/model_evaluation.md) - Metrics, cross-validation, bias-variance

### [02. Deep Learning](02_deep_learning/)
Neural networks and deep learning fundamentals.

- [Math Foundations](02_deep_learning/math_foundations.md) - Linear algebra, calculus refresher
- [Gradient Descent](02_deep_learning/gradient_descent.md) - SGD, Adam, learning rates
- [Neural Networks](02_deep_learning/neural_networks.md) - Perceptrons, MLPs, backpropagation
- [Activation Functions](02_deep_learning/activation_functions.md) - ReLU, sigmoid, softmax
- [CNNs](02_deep_learning/cnns.md) - Convolutional neural networks, image processing
- [RNNs](02_deep_learning/rnns.md) - Recurrent networks, LSTM, GRU
- [Regularization](02_deep_learning/regularization.md) - Dropout, batch norm, weight decay
- [Transformers](02_deep_learning/transformers.md) - Attention mechanism, architecture

### [03. Generative AI](03_generative_ai/)
Large language models and generative applications.

- [LLM Architecture](03_generative_ai/llm_architecture.md) - GPT, BERT, encoder-decoder
- [Tokenization](03_generative_ai/tokenization.md) - BPE, WordPiece, vocabulary
- [Fine-Tuning](03_generative_ai/fine_tuning.md) - LoRA, QLoRA, PEFT methods
- [Prompt Engineering](03_generative_ai/prompt_engineering.md) - Techniques, chain-of-thought
- [RAG](03_generative_ai/rag.md) - Retrieval-Augmented Generation, vector stores
- [Agents](03_generative_ai/agents.md) - LangChain, LangGraph, CrewAI
- [Evaluation](03_generative_ai/evaluation.md) - LLM metrics, benchmarks

## Learning Path

| Week | Focus | Topics |
|------|-------|--------|
| 1-2 | Classical ML | Regression, Classification |
| 3-4 | Classical ML | Clustering, Ensemble, Evaluation |
| 5-6 | Deep Learning | Neural Networks, CNNs |
| 7-8 | Deep Learning | RNNs, Transformers |
| 9-10 | GenAI | LLMs, Fine-tuning |
| 11-12 | GenAI | RAG, Agents |

## Framework Progression

1. **scikit-learn** - Classical ML, preprocessing, evaluation
2. **PyTorch** - Deep learning, custom models
3. **Hugging Face** - Pre-trained transformers
4. **LangChain/LangGraph** - LLM applications
5. **CrewAI** - Multi-agent systems

## Related Resources

- [Practice Exercises](../../code/practice/ML_and_AI/) - Hands-on coding
- [Prompt Engineering Practice](../../code/practice/ai/prompts/) - Prompt challenges

## References

- Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow (Géron)
- Deep Learning (Goodfellow, Bengio, Courville)
- Natural Language Processing with Transformers (Tunstall et al.)
- Build a Large Language Model From Scratch (Raschka)
