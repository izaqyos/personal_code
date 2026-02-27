# LDA — Latent Dirichlet Allocation
> full summary: concepts · math · code · diagrams

---

## 1. core idea

LDA is a **generative probabilistic model**. it assumes every doc was "written" by:
1. picking a **mixture of topics**
2. for each word — picking a topic from that mix, then picking a word from that topic

u observe the words. LDA reverse-engineers everything else.

two key outputs:
- `φ` — **topic → word** distributions. what words define each topic
- `θ` — **doc → topic** distributions. how much each doc belongs to each topic

---

## 2. bag of words (BOW)

LDA starts w/ BOW — word order thrown away, only counts survive.

```
"the cat sat on the mat"  →  {the:2, cat:1, sat:1, on:1, mat:1}
```

`CountVectorizer` does this in sklearn. produces a sparse matrix `X` of shape `(n_docs, vocab_size)`.

```python
vec = CountVectorizer(stop_words="english")
X = vec.fit_transform(docs)   # fit = build vocab. transform = count words
vocab = vec.get_feature_names_out()
```

**`fit_transform` breakdown:**

| step | what happens |
|------|-------------|
| `fit` | scans all docs. assigns each unique word a column index |
| `transform` | converts each doc into a count vector using that index |
| combined | does both in one pass |

**critical rule:** on new docs, use `transform` only — never `fit_transform` again.

```python
X_train = vec.fit_transform(train_docs)   # builds vocab HERE
X_new   = vec.transform(new_docs)         # reuses same vocab ✓
X_new   = vec.fit_transform(new_docs)     # rebuilds vocab — WRONG ✗
```

**reading a sparse row:**

```python
doc0 = X[0].toarray()[0]
#      ^         ^    ^
#   row 0    2D→dense  2D→1D
```

- `X[0]` — sparse row. stores only non-zero positions
- `.toarray()` — converts to dense 2D numpy array. all zeros shown
- `[0]` — strips outer wrapper. 2D `(1, vocab_size)` → 1D `(vocab_size,)`

---

## 3. the Dirichlet distribution

a **distribution over distributions**. instead of sampling a number, u sample a probability vector.

### the simplex

4 K=3 topics, all valid mixtures live on a 2-simplex (triangle):

```
         [1,0,0]
         pure topic 0
             △
            / \
           /   \
          /     \
  [0,1,0] ——————— [0,0,1]
pure t1          pure t2
```

every interior point = a valid topic mixture. Dirichlet = probability mass over that triangle.

### the PDF

```
Dir(x | α)  =  (1/B(α)) · ∏ xᵢ^(αᵢ - 1)

x    = probability vector being scored   e.g. [0.7, 0.2, 0.1]
α    = concentration parameter vector
B(α) = normalising constant  =  ∏Γ(αᵢ) / Γ(Σαᵢ)
```

the `αᵢ - 1` exponent controls shape:

| αᵢ | exponent | effect |
|----|----------|--------|
| `< 1` | negative | rewards extremes (0 or 1). sparse |
| `= 1` | 0 → flat | no preference. uniform |
| `> 1` | positive | rewards middle values. dense |

### α — the concentration parameter

```
α = [α₁, α₂, ..., αK]    one value per topic (or word)
```

| α value | distribution shape | practical meaning |
|---------|-------------------|-------------------|
| `α < 1` | mass at corners | docs dominated by 1-2 topics |
| `α = 1` | uniform | any mixture equally likely |
| `α > 1` | mass at center | docs blend topics evenly |
| `α = [2, 8]` | skewed | topic 1 dominates most docs |

concrete samples:
```
α=[0.1, 0.1]  →  [0.97, 0.03], [0.02, 0.98]   ← sparse
α=[1.0, 1.0]  →  [0.60, 0.40], [0.30, 0.70]   ← uniform
α=[5.0, 5.0]  →  [0.51, 0.49], [0.48, 0.52]   ← dense
α=[2.0, 8.0]  →  [0.18, 0.82], [0.22, 0.78]   ← skewed
```

### 2 Dirichlets in LDA

```
Dirichlet(α)  →  samples θ_d   →  topic mix per doc
                 e.g. doc 4 = [0.85 sports, 0.15 politics]

Dirichlet(β)  →  samples φ_k   →  word mix per topic
                 e.g. topic 0 = {goal:0.22, match:0.18, senate:0.01 ...}
```

same math. different role. acts as a **regulariser** — anchors dists to a prior belief, prevents overfitting.

---

## 4. the generative model

```
Given:
  K   = num topics          (u set this)
  V   = vocab size
  D   = num docs
  α   = Dirichlet prior on doc→topic dist
  β   = Dirichlet prior on topic→word dist

For each topic k ∈ {1..K}:
  φ_k ~ Dirichlet(β)          ← word dist for topic k.  shape: (V,)

For each doc d ∈ {1..D}:
  θ_d ~ Dirichlet(α)          ← topic mix for doc d.    shape: (K,)

  For each word position n ∈ {1..Nd}:
    z_dn ~ Categorical(θ_d)   ← sample a topic
    w_dn ~ Categorical(φ_z)   ← sample a word from that topic
```

u observe `w`. everything else — `θ`, `φ`, `z` — is **latent**. LDA infers them.

---

## 5. joint probability

```
p(w, z, θ, φ | α, β)

=  ∏_k p(φ_k | β)                     ← topic→word priors
×  ∏_d p(θ_d | α)                     ← doc→topic priors
×  ∏_d ∏_n p(z_dn | θ_d)             ← topic assignments
×  ∏_d ∏_n p(w_dn | φ_{z_dn})        ← word likelihoods
```

problem: `p(w | α, β)` requires summing over **all possible z assignments** → intractable. approximation required.

---

## 6. inference

### Gibbs sampling

marginalise out θ and φ analytically. sample only topic assignments `z`.

```
for each word w_dn:
  p(z_dn = k | z_-dn, w)
    ∝  (n_{dk} + α)          ← how much doc d uses topic k
     × (n_{kw} + β)          ← how much topic k uses word w
     / (n_{k}  + Vβ)         ← total words assigned to topic k

  where:
    n_{dk}  = # times doc d assigned to topic k  (excl. current word)
    n_{kw}  = # times topic k generated word w
    n_{k}   = total words in topic k

repeat until convergence. extract φ and θ from final counts.
```

### variational inference (sklearn default)

faster than Gibbs. less exact. optimises the **ELBO**:

```
true objective: maximise log p(w | α, β)  ← intractable

variational approach:
  approximate posterior p(z,θ,φ | w)
  with simpler dist     q(z,θ,φ | λ,γ,φ)

  maximise ELBO:
    L = E_q[log p(w,z,θ,φ)] - E_q[log q(z,θ,φ)]
      = likelihood term      - KL divergence term

  KL = how far q is from true posterior.
  maximising ELBO = tightening lower bound on log p(w).
```

two forces: **likelihood** (fit the words) vs **KL term** (stay close to prior). sklearn stops when ELBO improvement `< tol` or after `max_iter` iterations.

---

## 7. full python example

```python
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

# --- docs ---
docs = [
    "the goalkeeper saved the match with a brilliant goal kick",
    "the striker scored two goals in the final football match",
    "the senate voted on the new tax bill today",
    "politicians debate the new budget and tax reform policy",
    "the election results changed the balance of power in senate",
    "football fans celebrate after team wins the championship match",
]

# --- BOW ---
# fit = build vocab from all docs
# transform = convert each doc to word count vector
vec = CountVectorizer(stop_words="english")
X = vec.fit_transform(docs)          # sparse matrix (6, vocab_size)
vocab = vec.get_feature_names_out()

# inspect BOW for doc 0
# X[0]          → sparse row (non-zero positions only)
# .toarray()    → dense 2D array (all zeros shown)
# [0]           → strip outer wrapper. 2D→1D
doc0 = X[0].toarray()[0]
nonzero = [(vocab[i], doc0[i]) for i in doc0.nonzero()[0]]
print("BOW doc 0:", nonzero)
# e.g. [('brilliant',1), ('goal',1), ('goalkeeper',1), ('kick',1), ('match',1)]

# --- LDA ---
K = 2                                # num topics — u pick this
lda = LatentDirichletAllocation(
    n_components=K,                  # K topics
    random_state=42,
    max_iter=20,                     # variational inference iterations
    learning_method="batch",
)
lda.fit(X)

# --- φ: topic → word distribution ---
# lda.components_ shape: (K, vocab_size)
# values are unnormalized. normalize by row sum to get probs.
N_TOP = 5
print("\n=== topics (φ) ===")
for i, topic_vec in enumerate(lda.components_):
    topic_probs = topic_vec / topic_vec.sum()          # normalize
    top_idx = topic_probs.argsort()[-N_TOP:][::-1]
    top = [(vocab[j], round(topic_probs[j], 3)) for j in top_idx]
    print(f"topic {i}: {top}")
# topic 0: [('match',0.08), ('goal',0.07), ('football',0.06), ...]
# topic 1: [('senate',0.09), ('tax',0.08), ('election',0.07), ...]

# --- θ: doc → topic distribution ---
# lda.transform(X) shape: (n_docs, K)
# each row sums to ~1.0
doc_topics = lda.transform(X)
print("\n=== doc topic mix (θ) ===")
for i, mix in enumerate(doc_topics):
    dominant = mix.argmax()
    print(f"doc {i} → topic {dominant} ({mix.round(2)})  \"{docs[i][:45]}...\"")

# --- inference on new doc ---
# MUST use same fitted vec (same vocab). unknown words silently dropped.
new_doc = ["the team captain lobbied the government for sports funding"]
X_new   = vec.transform(new_doc)          # transform only — NOT fit_transform
mix_new = lda.transform(X_new)[0]
print(f"\nnew doc: {mix_new.round(3)}")   # mixed → expect something like [0.45, 0.55]
```

---

## 8. key variables — reference

| symbol | shape | meaning | sklearn location |
|--------|-------|---------|-----------------|
| `X` | `(D, V)` | BOW matrix. word counts per doc | `vec.fit_transform()` |
| `φ_k` | `(K, V)` | word dist per topic | `lda.components_` (normalize rows) |
| `θ_d` | `(D, K)` | topic mix per doc | `lda.transform(X)` |
| `z_dn` | scalar | topic assignment per word | latent. never exposed |
| `α` | scalar or `(K,)` | Dirichlet prior on θ | `doc_topic_prior` param |
| `β` | scalar or `(V,)` | Dirichlet prior on φ | `topic_word_prior` param |
| `ELBO` | scalar | lower bound on log-likelihood | `lda.bound_` after fit |

---

## 9. limits

- **BOW = no word order.** "not good" ≠ "good not"
- **K is manual.** no auto-detection of num topics
- **topics are unlabeled.** u interpret what they mean
- **rare words = noise.** use `min_df` in CountVectorizer to filter
- **new vocab ignored.** words not seen during `fit` are silently dropped at inference

---

## 10. tldr

```
LDA = "given these word counts, what hidden topics explain the patterns?"

Dirichlet(α)  →  prior on doc→topic mixtures    (θ)
Dirichlet(β)  →  prior on topic→word mixtures   (φ)
Gibbs/VI      →  infer θ and φ from observed words
ELBO          →  what's actually optimised. proxy for log-likelihood

low α  →  sparse docs (1-2 topics dominate)
high α →  dense docs  (topics blend evenly)
```
