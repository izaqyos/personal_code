# LDA Demo — Design Specification

> Dual-implementation LDA (from-scratch Gibbs + sklearn) for learning, with comprehensive tests and a React presentation.

---

## 1. Goals

- **Learn LDA step-by-step** by implementing the core algorithm (collapsed Gibbs sampling) from scratch using only NumPy
- **Validate understanding** by comparing the from-scratch implementation against sklearn's variational inference
- **Test rigorously** with unit, property-based, and integration tests that reinforce mathematical invariants
- **Present the work** via a React hybrid tutorial/interactive presentation (~12 slides)

---

## 2. Project Structure

```
LDA_Demo/
├── lda/                        # Core Python package
│   ├── __init__.py
│   ├── vectorizer.py           # From-scratch BOW vectorizer
│   ├── gibbs_sampler.py        # From-scratch collapsed Gibbs LDA
│   ├── sklearn_lda.py          # sklearn wrapper (same interface)
│   ├── mock_data.py            # Dataset generators (easy + hard)
│   └── comparison.py           # Run both, compare, export JSON
├── tests/
│   ├── test_vectorizer.py
│   ├── test_gibbs_sampler.py
│   ├── test_sklearn_lda.py
│   ├── test_mock_data.py
│   └── test_integration.py
├── presentation/               # React app (Vite + TypeScript + Recharts)
│   ├── src/
│   └── package.json
├── results/                    # Pre-computed JSON for presentation
├── run_comparison.py           # CLI entry point
├── requirements.txt
└── pyproject.toml
```

---

## 3. Core Modules

### 3.1 `vectorizer.py` — From-Scratch BOW

**Class**: `BowVectorizer`

**Interface**:
- `fit(documents: list[str]) -> self`
- `transform(documents: list[str]) -> np.ndarray`  (shape: `(n_docs, vocab_size)`)
- `fit_transform(documents: list[str]) -> np.ndarray`
- `get_feature_names() -> list[str]`

**Parameters**:
- `stop_words: list[str] | None` — words to exclude
- `min_df: int` — minimum document frequency to include a word (default 1)
- `max_df: float` — maximum document frequency ratio to include a word (default 1.0)

**Behavior**:
- `fit()` builds vocabulary mapping (word -> column index), applies stop_words/min_df/max_df filtering
- `transform()` converts documents to dense count matrix using the fitted vocabulary. Unknown words are silently ignored.
- Returns dense numpy arrays (not scipy sparse) for simplicity and learning clarity
- Comments explain where sklearn's `CountVectorizer` differs (sparse output, more tokenization options)

### 3.2 `gibbs_sampler.py` — Collapsed Gibbs Sampling LDA

**Class**: `GibbsLDA`

**Interface**:
- `fit(X: np.ndarray) -> self`
- `transform(X: np.ndarray) -> np.ndarray`  (shape: `(n_docs, n_topics)`)
- `phi() -> np.ndarray`  (shape: `(n_topics, vocab_size)`) — topic-word distributions
- `theta() -> np.ndarray`  (shape: `(n_docs, n_topics)`) — doc-topic distributions
- `log_likelihoods: list[float]` — tracked per iteration for convergence monitoring

**Parameters**:
- `n_topics: int` — number of topics K
- `alpha: float` — Dirichlet prior on doc-topic distributions (default 0.1)
- `beta: float` — Dirichlet prior on topic-word distributions (default 0.01)
- `n_iterations: int` — number of Gibbs sampling iterations (default 1000)
- `random_state: int | None` — for reproducibility

**Algorithm** (collapsed Gibbs sampling):
```
Initialize: randomly assign each word token to a topic

For each iteration:
  For each document d:
    For each word position n in document d:
      1. Decrement counts for current assignment z_dn
      2. Compute p(z_dn = k) ∝ (n_dk + α) × (n_kw + β) / (n_k + V×β)
         for all k ∈ {0..K-1}
      3. Normalize to get probabilities
      4. Sample new z_dn from this distribution
      5. Increment counts for new assignment

  Record log-likelihood for this iteration

Extract final distributions:
  φ_k[w] = (n_kw + β) / (n_k + V×β)       — topic-word
  θ_d[k] = (n_dk + α) / (N_d + K×α)       — doc-topic
```

**Count matrices maintained**:
- `n_dk` — shape `(D, K)`: how many words in doc d assigned to topic k
- `n_kw` — shape `(K, V)`: how many times word w assigned to topic k
- `n_k` — shape `(K,)`: total words assigned to topic k
- `z` — list of lists: topic assignment for each word token

**Comments note**: In production, use `np.random.dirichlet` for sampling from the Dirichlet distribution directly. The collapsed Gibbs approach avoids this by integrating out θ and φ analytically.

### 3.3 `sklearn_lda.py` — Thin Wrapper

**Class**: `SklearnLDA`

**Interface**: identical to `GibbsLDA` — `fit()`, `transform()`, `phi()`, `theta()`

**Internals**:
- Wraps `sklearn.decomposition.LatentDirichletAllocation`
- `phi()` normalizes `lda.components_` rows
- `theta()` returns `lda.transform(X)`
- Passes through `n_topics`, `alpha` (→ `doc_topic_prior`), `beta` (→ `topic_word_prior`), `random_state`

### 3.4 `mock_data.py` — Dataset Generators

**Function**: `generate_easy_dataset() -> tuple[list[str], list[str], list[str]]`
- 3 topics: sports, politics, technology
- ~30 documents (10 per topic)
- Each topic has a dedicated vocabulary pool with zero overlap
- Returns `(documents, labels, topic_names)` — labels for validation only

**Function**: `generate_hard_dataset() -> tuple[list[str], list[str], list[str]]`
- Same 3 base topics
- ~40 documents: 10 per pure topic + ~10 bridging documents
- Bridging documents blend vocabulary from 2 topics (e.g., "tech policy", "sports politics")
- Some shared noise words across all topics
- Returns `(documents, labels, topic_names)` — bridging docs get hyphenated labels like "sports-politics"

Both functions use a fixed random seed for reproducibility.

### 3.5 `comparison.py` — Orchestrator

**Function**: `run_comparison(dataset, n_topics, alpha, beta, n_iterations, random_state) -> ComparisonResult`
- Vectorizes the dataset using `BowVectorizer`
- Runs `GibbsLDA` and `SklearnLDA` with identical hyperparameters
- Aligns topics between implementations using cosine similarity on φ rows (Hungarian algorithm or greedy matching)
- Computes comparison metrics:
  - Cosine similarity between aligned φ rows
  - Per-document dominant topic agreement
  - θ correlation per document

**Function**: `export_results(results: list[ComparisonResult], output_dir: str)`
- Serializes to JSON files in `results/`:
  - `easy_dataset.json` — topics, distributions, comparison metrics
  - `hard_dataset.json` — same structure
  - `convergence.json` — log-likelihood per iteration from Gibbs sampler

### 3.6 `run_comparison.py` — CLI Entry Point

- Runs comparison on both datasets with default hyperparameters
- Prints summary table to terminal
- Exports JSON to `results/`
- Hyperparameters: K=3, α=0.1, β=0.01, n_iterations=1000

---

## 4. Testing Strategy

All tests use `pytest`. Property tests use `@pytest.mark.parametrize`.

### 4.1 `test_vectorizer.py` — Unit Tests
- `fit()` builds correct vocabulary from known input
- `transform()` produces correct count vectors for known documents
- Stop words are excluded from vocabulary
- `min_df` filtering removes rare words
- `max_df` filtering removes overly common words
- `transform()` on unseen words silently ignores them
- `fit_transform()` equals `fit()` then `transform()`
- Empty document produces zero vector

### 4.2 `test_gibbs_sampler.py` — Unit + Property Tests

**Unit tests**:
- Tiny 3-doc, 2-topic corpus with obvious separation converges to expected topics
- Output shapes are correct: φ is `(K, V)`, θ is `(D, K)`

**Property tests (mathematical invariants)**:
- All θ rows sum to 1.0 (within tolerance)
- All φ rows sum to 1.0 (within tolerance)
- All values in θ and φ are ≥ 0
- Higher α → higher entropy in θ (denser doc-topic distributions)
- Higher β → higher entropy in φ (denser topic-word distributions)
- Log-likelihood is non-decreasing on average (windowed average)
- Same `random_state` → identical results (determinism)

### 4.3 `test_sklearn_lda.py` — Unit Tests
- Wrapper produces same results as calling sklearn directly
- `phi()` returns correctly shaped, row-normalized array
- `theta()` returns correctly shaped array with rows summing to ~1.0
- Interface matches `GibbsLDA` (same method names, same output shapes)

### 4.4 `test_mock_data.py` — Unit Tests
- Easy dataset: no vocabulary overlap between topics
- Hard dataset: bridging documents exist with hyphenated labels
- Document counts match expectations (easy: 30, hard: ~40)
- Returned structure is correct tuple of `(docs, labels, topic_names)`
- Fixed seed produces identical output across runs

### 4.5 `test_integration.py` — Cross-Implementation Comparison
- On easy dataset: both implementations assign the same dominant topic to each document (after topic alignment)
- On easy dataset: cosine similarity between aligned φ rows > 0.7
- On hard dataset: both agree on dominant topic for pure (non-bridging) documents
- On hard dataset: bridging documents get mixed θ distributions from both (no single topic > 0.9)

---

## 5. React Presentation

### 5.1 Tech Stack
- **Vite + React + TypeScript** — build tooling
- **Recharts** — bar charts, line charts, heatmaps
- **Custom slide component** — minimal prev/next navigation with slide counter, keyboard arrow support

### 5.2 Slides (~12)

| # | Title | Content | Interactive Element |
|---|-------|---------|-------------------|
| 1 | Title | "LDA: Learning by Implementation" | — |
| 2 | What is LDA? | Core idea from generative model. Two key outputs: φ and θ | Animated diagram: doc → topics → words |
| 3 | Bag of Words | How text becomes numbers. What's lost (word order) | Toggle: show sentence with/without stop words, see BOW vector change |
| 4 | The Dirichlet Distribution | Distribution over distributions. The simplex. α controls shape | Slider: drag α, see bar chart of sampled probability vectors update (sparse ↔ dense) |
| 5 | The Generative Story | Full plate notation walkthrough | Step-through animation: pick θ → pick z → pick w |
| 6 | Gibbs Sampling | The update formula. How counts drive convergence | Highlight one word, show the probability calculation step by step |
| 7 | Our Implementation | Code architecture. Module → concept mapping | Architecture diagram with clickable modules |
| 8 | Easy Dataset Results | Side-by-side Gibbs vs sklearn on clearly separated topics | Top-10 words per topic (bar charts), doc-topic heatmap |
| 9 | Hard Dataset Results | Same layout, bridging documents highlighted | Highlight mixed θ for bridging docs, show agreement/disagreement |
| 10 | Convergence | What "converged" looks like | Line chart: log-likelihood over iterations with iteration slider |
| 11 | Comparison Metrics | How similar are the two implementations? | Cosine similarity bars, θ correlation scatter plot |
| 12 | Takeaways + Limits | Summary of what LDA can/can't do | — |

### 5.3 Data Flow
- `run_comparison.py` exports JSON to `results/`
- React app imports JSON files at build time (Vite JSON import)
- No backend — pure static build
- Interactive widgets (α slider on slide 4) compute values client-side using simple JS math

---

## 6. Dependencies

**Python** (`requirements.txt`):
- `numpy` — array operations, random sampling
- `scikit-learn` — sklearn LDA wrapper + CountVectorizer for validation
- `pytest` — test runner

**JavaScript** (`presentation/package.json`):
- `react`, `react-dom`
- `typescript`
- `vite`
- `recharts`

---

## 7. Build Order

Each step is independently testable before proceeding:

1. `mock_data.py` + `test_mock_data.py`
2. `vectorizer.py` + `test_vectorizer.py`
3. `gibbs_sampler.py` + `test_gibbs_sampler.py` (core learning step)
4. `sklearn_lda.py` + `test_sklearn_lda.py`
5. `comparison.py` + `test_integration.py`
6. `run_comparison.py` → generates JSON to `results/`
7. React presentation (`presentation/`)
