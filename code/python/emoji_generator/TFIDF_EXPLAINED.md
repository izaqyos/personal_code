# TF-IDF Step by Step

Using the emoji generator engine (`engine.py`) as the running example.

---

## The Analogy: A Librarian's Brain

Imagine a librarian who needs to find the right book when someone asks a vague
question like "pr got merged." She can't read minds -- she can only compare the
**words** in the question against the **words** on each book's index card.

But she's smart about it. She knows the word "the" appears on every card, so
it's useless. And she knows the word "canary" only appears on one card, so if
someone says "canary," that's a dead giveaway. TF-IDF is how she weights
these words.

---

## Step 0: The Raw Data

Three entries from `emojis.yaml`, after `searchable_text` combines
description + aliases:

```
Doc A (pr_approved_merged):
  "pull request approved and merged . pr merged . mr approved and merged .
   change landed . code merged to main . lgtm merged . pr got approved"

Doc B (deploying):
  "deploying to environment . deploying . deployment in progress .
   pushing to production . releasing . shipping . deploy started"

Doc C (merge_conflicts):
  "merge conflicts need resolution . merge conflicts . conflicts .
   conflict resolution . rebase needed . branch conflicts"
```

---

## Step 1: Tokenization

Break text into individual words (tokens). Lowercase everything.

```
Doc A tokens: ["pull", "request", "approved", "and", "merged", "pr", "merged",
               "mr", "approved", "and", "merged", "change", "landed", "code",
               "merged", "to", "main", "lgtm", "merged", "pr", "got", "approved"]

Doc B tokens: ["deploying", "to", "environment", "deploying", "deployment",
               "in", "progress", "pushing", "to", "production", "releasing",
               "shipping", "deploy", "started"]

Doc C tokens: ["merge", "conflicts", "need", "resolution", "merge", "conflicts",
               "conflicts", "conflict", "resolution", "rebase", "needed",
               "branch", "conflicts"]
```

**Analogy:** Tearing each index card into individual word tiles.

---

## Step 2: Stop Word Removal

> `engine.py:111` -- `stop_words="english"`

Remove words like "and", "to", "in", "the" -- they appear everywhere and
carry no meaning.

```
Doc A after: ["pull", "request", "approved", "merged", "pr", "merged",
              "mr", "approved", "merged", "change", "landed", "code",
              "merged", "main", "lgtm", "merged", "pr", "got", "approved"]

Doc B after: ["deploying", "environment", "deploying", "deployment",
              "progress", "pushing", "production", "releasing",
              "shipping", "deploy", "started"]

Doc C after: ["merge", "conflicts", "need", "resolution", "merge", "conflicts",
              "conflicts", "conflict", "resolution", "rebase", "needed",
              "branch", "conflicts"]
```

**Analogy:** The librarian ignoring filler words like "the", "a", "to" when
comparing cards. They appear on every card, so they help no one.

**Gotcha:** Query `"on it"` -- both words are stop words. After removal: `[]`.
Empty. Score = 0 for everything. The engine can't match it.

---

## Step 3: N-Gram Extraction

> `engine.py:97` -- `ngram_range=(1, 2)`

Extract both single words AND consecutive pairs.

```
Doc A features (sample):
  Unigrams: "pull", "request", "approved", "merged", "pr", "lgtm", ...
  Bigrams:  "pull request", "request approved", "approved merged",
            "pr merged", "pr got", "got approved", ...

Doc C features (sample):
  Unigrams: "merge", "conflicts", "resolution", "rebase", "branch", ...
  Bigrams:  "merge conflicts", "conflicts need", "need resolution",
            "conflict resolution", "rebase needed", "branch conflicts", ...
```

**Why bigrams matter:** Without bigrams, the query "merge queue" and "merge
conflicts" both match on "merge." With bigrams, "merge conflicts" as a
**phrase** becomes its own feature -- and Doc C gets a direct hit.

**Analogy:** The librarian doesn't just look for individual words. She also
checks if two words appear **side by side**. "Merge conflicts" as a phrase
is more specific than just "merge" alone.

---

## Step 4: Term Frequency (TF)

Count how often each word/bigram appears in each document.

```
Doc A:
  "merged"   -> appears 5 times
  "approved" -> appears 3 times
  "pr"       -> appears 2 times
  "lgtm"     -> appears 1 time

Doc C:
  "conflicts" -> appears 4 times
  "merge"     -> appears 2 times
  "rebase"    -> appears 1 time
```

> `engine.py:122` -- `sublinear_tf=True`

With sublinear TF, apply log scaling:

```
Doc A:
  "merged"   -> raw 5 -> 1 + log(5) = 2.61
  "approved" -> raw 3 -> 1 + log(3) = 2.10
  "lgtm"     -> raw 1 -> 1 + log(1) = 1.00

Doc C:
  "conflicts" -> raw 4 -> 1 + log(4) = 2.39
  "merge"     -> raw 2 -> 1 + log(2) = 1.69
```

**Why log?** Diminishing returns. A word appearing 5 times isn't 5x more
important than appearing once. It's maybe 2.6x more important.

**Analogy:** If a book's index card mentions "Python" once, it's probably
about Python. If it mentions "Python" 10 times, it's still about Python --
not 10x more about Python.

---

## Step 5: Inverse Document Frequency (IDF)

Compute how rare each word is across ALL documents. Rare words get higher weight.

```
Formula: idf(word) = log((1 + N) / (1 + df)) + 1
  N  = total documents (44 emoji entries)
  df = how many documents contain this word

                        df    IDF (approximate)
  "merged"              3     high-ish  (only in PR-related entries)
  "deploy"              2     high      (only in deployment entries)
  "lgtm"                1     very high (unique to pr_approved)
  "conflicts"           1     very high (unique to merge_conflicts)
```

If a word appeared in ALL 44 entries, its IDF would be ~1.0 (low).
If it appears in just 1 entry, IDF is ~4.8 (high).

**Analogy:** The librarian knows from experience:
- "code" appears on 20 cards -> not very helpful for finding a specific book
- "canary" appears on 1 card -> if someone says "canary," she knows EXACTLY
  which book

**This is the key insight of TF-IDF:** Common words are demoted. Distinctive
words are promoted.

---

## Step 6: TF x IDF = The Final Weight

Multiply each word's TF (how frequent in THIS doc) by its IDF (how rare
ACROSS all docs).

```
Doc A "pr_approved_merged":
  "merged"     -> TF 2.61 * IDF ~2.5 = 6.53   (frequent + somewhat rare)
  "lgtm"       -> TF 1.00 * IDF ~4.8 = 4.80   (infrequent but VERY rare)
  "approved"   -> TF 2.10 * IDF ~2.8 = 5.88

Doc C "merge_conflicts":
  "conflicts"  -> TF 2.39 * IDF ~4.8 = 11.47  (frequent + very rare = dominant)
  "merge"      -> TF 1.69 * IDF ~2.5 = 4.23
  "rebase"     -> TF 1.00 * IDF ~4.8 = 4.80   (unique word, high signal)
```

Each document is now a **vector** -- a list of numbers, one per word/bigram
in the vocabulary.

```
Vocabulary: ["approved", "branch", "code", "conflicts", "deploy", "lgtm", "merge", "merged", ...]
Doc A vec:  [  5.88,      0,        2.1,    0,           0,        4.80,   0,       6.53,   ...]
Doc B vec:  [  0,         0,        0,      0,           7.2,      0,      0,       0,      ...]
Doc C vec:  [  0,         3.1,      0,      11.47,       0,        0,      4.23,    0,      ...]
```

Most values are 0 (sparse). That's normal -- each entry only uses a handful
of words from the full vocabulary.

**This is `fit_transform()` at `engine.py:148`.** It builds the vocabulary,
computes IDF, and transforms all entries into vectors in one pass.

---

## Step 7: Query Vectorization

> `engine.py:182` -- `self.vectorizer.transform([query])`

When a user types `"pr got merged"`, transform it using the **same**
vocabulary and IDF weights.

```
Query: "pr got merged"
  After stop words: ["pr", "got", "merged"]
  Bigrams: ["pr got", "got merged"]

  Query vec: [0, 0, 0, 0, 0, 0, 0, 3.2, ...]
                                    ^ "merged" has weight
```

**Critical:** This uses `transform()`, NOT `fit_transform()`. The vocabulary
is frozen from Step 6. If the query contains a word not in the vocabulary
(e.g., "kubernetes"), it's silently ignored -- zero weight.

**Analogy:** A new visitor comes to the library and asks a question. The
librarian translates that question into the same "card system" she already
has. She doesn't reorganize her cards for every new visitor.

---

## Step 8: Cosine Similarity

> `engine.py:206` -- `cosine_similarity(query_vector, self.tfidf_matrix)`

Compare the query vector against every document vector.

```
                     query    Doc A     Doc B     Doc C
"merged"              3.2     6.53      0         0
"pr"                  2.1     3.40      0         0
"got"                 1.5     1.80      0         0
"pr got" (bigram)     1.8     2.10      0         0
"got merged" (bigram) 1.8     0         0         0
all other words        0      ...       ...       ...
```

Cosine similarity measures the **angle** between two vectors, not the distance:

```
cos(theta) = (A . B) / (|A| x |B|)

Query vs Doc A:  (3.2x6.53 + 2.1x3.40 + 1.5x1.80 + 1.8x2.10) / (|Q| x |A|)
               = high overlap -> score ~ 0.65

Query vs Doc B:  no shared words -> dot product = 0 -> score = 0.0

Query vs Doc C:  "merge" != "merged" (different tokens) -> score ~ 0.0
```

### Why Cosine, Not Euclidean Distance?

Imagine two arrows from the origin:

```
        Doc A (long description, many words)
       /
      /  <- small angle = similar topic
     /
    /
Query ---->

        Doc B (short description, few words)
        |
        |  <- 90 deg angle = unrelated topic
        |
Query ---->
```

Cosine only cares about **direction** (what topic), not **length** (how many
words). A long description about "merging" and a short query about "merging"
point the same way. Euclidean distance would penalize the length difference.

---

## Step 9: Rank and Filter

> `engine.py:210-214`

Sort by score descending, filter out anything below `MIN_CONFIDENCE` (0.15).

```
Results for "pr got merged":
  #1  pr_approved_merged   score: 0.65   <- winner
  #2  landed               score: 0.22   <- partial overlap ("merged to main")
  #3  in_merge_queue       score: 0.18   <- shares "merge"
  --- below MIN_CONFIDENCE (0.15) ---
  #4  merge_conflicts      score: 0.12   <- cut off
```

---

## The Full Pipeline

```
emojis.yaml                          User types: "pr got merged"
     |                                        |
     v                                        v
[ Load entries ]                     [ Tokenize + stop words ]
     |                                        |
     v                                        v
[ Tokenize + stop words ]            [ Extract n-grams ]
     |                                        |
     v                                        v
[ Extract n-grams (1,2) ]            [ transform() into SAME vector space ]
     |                                        |
     v                                        |
[ fit(): learn vocabulary + IDF ]             |
     |                                        |
     v                                        v
[ transform(): TF x IDF vectors ]   [ Query vector ]
     |                                        |
     v                                        v
[ 44x200 sparse matrix ]  -------->  [ cosine_similarity() ]
                                              |
                                              v
                                     [ Sort by score, filter > 0.15 ]
                                              |
                                              v
                                     [ pr_approved_merged  0.65 ]
```

**Left side** happens once at startup (`__init__`, line 57).
**Right side** happens every query (`search`, line 160).

---

## One Sentence Summary

TF-IDF turns text into numbers by asking: **"How important is this word to
THIS document, relative to ALL documents?"** -- then cosine similarity finds
which document's numbers point in the same direction as your query's numbers.

---

## Related Files

- `engine.py` -- Implementation with inline LEARN comments
- `BOW_LEARNING_PATH.md` -- What to learn next (build from scratch, blind spots, fixes)
- `registry.py` -- How emoji entries become `searchable_text`

---

**Last Updated:** 2026-02-15
