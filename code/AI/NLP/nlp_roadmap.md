# NLP Learning Roadmap

---

## PHASE 1 — Classical NLP (text as counts)

### 1.1 Bag of Words (BOW)
- concept: represent doc as word count vector. ignore order.
- build: vectorize a few sentences manually in numpy
- key limit 2 notice: no meaning. no order. "dog bites man" = "man bites dog"

### 1.2 TF-IDF
- concept: weight words by how unique they r 2 a doc vs corpus
- TF = how often word appears in doc. IDF = how rare it is across all docs
- build: implement from scratch. then compare w/ sklearn's version
- key limit: still no meaning. just better weighting

### 1.3 Naive Bayes Classifier
- concept: use BOW features + Bayes theorem 2 classify text
- build: spam classifier from scratch
- connects back 2: ur Dirichlet / conjugacy knowledge

### 1.4 LDA (Latent Dirichlet Allocation)
- concept: docs r mixtures of topics. topics r mixtures of words. both Dirichlet priors.
- build: use gensim on a small corpus. then read the original Blei 2003 paper.
- key insight: this is where ur Beta/Dirichlet/conjugacy work pays off
- key limit: topics r fixed upfront. words have no notion of meaning/similarity

---

## PHASE 2 — From Counts 2 Meaning

### 2.1 Word Embeddings — word2vec
- concept: words as dense vectors. meaning from context.
- "u shall know a word by the company it keeps"
- build: implement skip-gram from scratch in numpy
- yt: Karpathy makemore series
- key insight: similar words r close in vector space. king - man + woman ≈ queen

### 2.2 GloVe (optional but useful)
- concept: global co-occurrence counts → embeddings
- lighter stop. just understand how it differs from word2vec
- skip building. just use pretrained vectors and explore them.

---

## PHASE 3 — Sequences

### 3.1 RNNs
- concept: process words one at a time. hidden state carries memory.
- build: tiny character-level RNN from scratch in numpy
- yt: Karpathy "building makemore" pt 2-3
- key limit: memory fades. long sequences break.

### 3.2 LSTMs
- concept: gates control what 2 remember / forget. fixes vanishing gradient.
- build: implement in pytorch (not numpy. gates get messy)
- key limit: still sequential. can't parallelize. slow.

---

## PHASE 4 — Attention + Transformers

### 4.1 Attention Mechanism
- concept: instead of compressing everything into 1 vector — look back at all words. weight by relevance.
- build: implement scaled dot-product attention from scratch
- yt: 3Blue1Brown attention video. watch b4 anything else here.
- this is the most important concept in modern NLP. go slow.

### 4.2 Transformer Architecture
- concept: attention is all u need. no recurrence. fully parallelizable.
- build: follow Karpathy's nanoGPT. build it from scratch.
- read: "Attention Is All You Need" (Vaswani 2017). after u build it.
- understand: encoder (BERT) vs decoder (GPT) distinction

### 4.3 BERT
- concept: bidirectional. trained on masked language modeling. good 4 understanding tasks.
- build: fine-tune pretrained BERT on a classification task via HuggingFace
- use case: classification, NER, question answering

### 4.4 GPT
- concept: unidirectional. trained on next-token prediction. good 4 generation.
- build: use nanoGPT. train on tiny shakespeare or similar.
- use case: text generation, completion, instruction following

---

## PHASE 5 — Modern Practice

### 5.1 HuggingFace Ecosystem
- transformers library. datasets. tokenizers.
- learn: how 2 load, fine-tune, evaluate pretrained models
- build: pick a task (sentiment, summarization, QA). fine-tune a model end-2-end.

### 5.2 Fine-tuning + Transfer Learning
- concept: pretrain on huge data. fine-tune on ur task w/ small data.
- build: full pipeline. data → tokenize → fine-tune → evaluate

### 5.3 Prompt Engineering + LLMs (optional / practical)
- if ur goal is applied NLP this matters a lot
- concept: how 2 steer large models w/ prompts. few-shot learning.

---

## per-topic workflow (repeat every stage)
> concept (claude) → visual (yt) → build (python) → reflect on limits

## key builds by phase
- ph1: spam classifier, LDA on toy corpus
- ph2: word2vec skip-gram from scratch
- ph3: char-level RNN, LSTM in pytorch
- ph4: attention from scratch, nanoGPT
- ph5: fine-tuned BERT on real task

---

## yt playlist (in order)
1. 3Blue1Brown — neural networks series
2. Karpathy — makemore (pt 1-5)
3. Karpathy — nanoGPT
4. 3Blue1Brown — attention
5. Yannic Kilcher — "Attention Is All You Need" walkthrough
