# Dev Emoji Generator

Find the perfect emoji combo for software development concepts using natural language.

Type what you mean in plain English, and the tool finds the best emoji match using a two-stage engine: **Stage 1** catches dev lingo and typos via exact/fuzzy alias lookup (Levenshtein distance), **Stage 2** handles natural language via TF-IDF cosine similarity. No hardcoded if/else, no API keys, no heavy ML models.

```
$ devmoji "pr approved and merged"

  Results for: "pr approved and merged"
  ┌───┬──────────┬──────────────────────────────────┬───────┐
  │ # │  Emoji   │ Description                      │ Score │
  ├───┼──────────┼──────────────────────────────────┼───────┤
  │ 1 │  ✅🔀   │ pull request approved and merged  │   82% │
  │ 2 │  ✅👀   │ pull request approved             │   54% │
  │ 3 │  🛬✅   │ change landed in main branch      │   31% │
  └───┘──────────┴──────────────────────────────────┴───────┘

  Pick a number (or Enter for #1, 'q' to skip): 1

  Copied to clipboard: ✅🔀
```

---

## Install

```bash
cd code/python/emoji_generator

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install in editable mode (registers the `devmoji` command)
pip install -e .

# Optional: install dev dependencies for tests
pip install -e ".[dev]"
```

## Usage

### CLI Mode (one-shot)

```bash
# Search and pick
devmoji "pr merged"

# Auto-select top result (no prompt)
devmoji -1 "deploying to prod"

# Show more results
devmoji --top 10 "code review"

# Print only, don't copy to clipboard
devmoji --no-copy "hotfix"

# List all available emojis
devmoji --list
```

### REPL Mode (interactive)

```bash
devmoji --repl
```

In REPL mode:
- Type any phrase to search
- Pick a number to copy to clipboard
- Type `list` to see all emojis
- Type `quit` to exit
- When no match is found, you can add a new emoji entry on the spot

### Run without installing

```bash
python -m emoji_generator "merge queue"
python -m emoji_generator --repl
```

---

## Adding Your Own Emojis

### Option 1: Edit the YAML file directly

Open `emoji_generator/data/emojis.yaml` and add an entry:

```yaml
- emoji: "🎯🔥"
  name: "on_target"
  description: "on target hitting the goal"
  aliases:
    - "on target"
    - "hitting the mark"
    - "nailed it"
```

Restart the tool (or in REPL mode, the engine hot-reloads after adding).

### Option 2: Use the "no match" flow

When you search for something that doesn't match, the tool gives you a ready-to-paste YAML snippet:

```
No good match found for: "standup meeting running long"

To add this, paste the following into emojis.yaml:

  - emoji: "PUT_EMOJI_HERE"
    name: "standup_meeting_running_long"
    description: "standup meeting running long"
    aliases:
      - "standup meeting running long"
```

In REPL mode, you can press `a` to add the entry interactively.

---

## How It Works -- Deep Dive

This section teaches the core algorithms from the ground up, using real examples from the emoji registry. See also `emoji_generator/engine.py` which is annotated with `# LEARN:` comments inline.

---

### Two-Stage Matching Strategy

Different types of queries need different tools:

| Query type | Example | Best tool |
|---|---|---|
| Short dev lingo | "on it", "lgtm" | Exact alias match |
| Abbreviations | "ooo", "wip", "ack" | Exact alias match |
| Typos | "ship ti", "deploiying" | Fuzzy string match (Levenshtein) |
| Natural language | "pr got merged" | TF-IDF + cosine similarity |
| Long descriptions | "the build is broken" | TF-IDF + cosine similarity |

#### Why not just TF-IDF for everything?

TF-IDF **breaks** on short dev lingo:

1. **Stop word problem**: "on it" -- both "on" and "it" are English stop words. TF-IDF removes them, producing an **empty query vector**. Zero features = no match possible.
2. **Abbreviation problem**: "lgtm" has no IDF signal. TF-IDF works on word frequency -- "lgtm" doesn't decompose into meaningful sub-words. It's an opaque token.
3. **Short query problem**: TF-IDF needs enough words to build a meaningful vector. A 1-2 word query produces a very sparse vector where random noise dominates.

#### The Pipeline

```
User query: "on it"
    │
    ▼
┌─────────────────────────────────┐
│  Stage 1: LingoLookup           │
│  Exact match → aliases dict     │
│  Fuzzy match → Levenshtein      │
│                                 │
│  "on it" == alias "on it"? YES  │──→ Return 🫡 (score: 1.0)
└─────────────────────────────────┘

User query: "the pull request was approved and merged"
    │
    ▼
┌─────────────────────────────────┐
│  Stage 1: LingoLookup           │
│  No exact match. Fuzzy? No.     │
└──────────────┬──────────────────┘
               │ (no results)
               ▼
┌─────────────────────────────────┐
│  Stage 2: TF-IDF Engine         │
│  Vectorize → cosine similarity  │
│  "merged" has high IDF weight   │──→ Return ✅🔀 (score: 0.82)
└─────────────────────────────────┘
```

Stage 1 catches lingo, abbreviations, and typos. Stage 2 handles natural language. Each stage does what it's best at, and stop words can safely stay in TF-IDF without worrying about "on it" breaking -- because Stage 1 catches it before TF-IDF ever sees it.

---

### Levenshtein Distance -- The Typo Catcher

Stage 1's fuzzy matching is powered by **Levenshtein distance** -- a classic dynamic programming algorithm you may have seen before (e.g., as the "edit distance" problem in CS courses).

#### What it measures

The minimum number of **single-character edits** (insertions, deletions, substitutions) to transform one string into another.

```
"lgtm" → "lgmt"     1 substitution (swap t↔m)     distance = 2*
"ship it" → "ship ti"  1 substitution              distance = 2*
"deploy" → "deploiy"   1 substitution + 1 insert   distance = 2
"ack" → "acknowledged" 10 insertions               distance = 10

* Note: raw Levenshtein counts each position change as a substitution,
  not a transposition. "lgtm"→"lgmt" requires 2 subs (t→m at pos 3, m→t at pos 4).
```

#### The Algorithm (Dynamic Programming)

Build a matrix `D` where `D[i][j]` = edit distance between the first `i` characters of string `A` and the first `j` characters of string `B`.

**Example: `"ship it"` vs `"ship ti"`** (spaces included):

```
         ""  s  h  i  p     t  i
    ""  [ 0  1  2  3  4  5  6  7 ]   ← base: transform "" into "ship ti"
    s   [ 1  0  1  2  3  4  5  6 ]   s==s: free (diagonal)
    h   [ 2  1  0  1  2  3  4  5 ]   h==h: free
    i   [ 3  2  1  0  1  2  3  4 ]   i==i: free
    p   [ 4  3  2  1  0  1  2  3 ]   p==p: free
        [ 5  4  3  2  1  0  1  2 ]    == : free
    i   [ 6  5  4  3  2  1  1  1 ]   i!=t: min(0+1, 1+1, 1+1) = 1; then i==i: 1
    t   [ 7  6  5  4  3  2  1  2 ]   t==t: 1; then t!=i: min(1+1, 1+1, 1+1) = 2

    Final: D[7][7] = 2
```

#### The Recurrence Relation

```
If A[i] == B[j]:
    D[i][j] = D[i-1][j-1]              # chars match, no edit needed (diagonal)
Else:
    D[i][j] = 1 + min(
        D[i-1][j],        # delete from A      (↑ move up)
        D[i][j-1],        # insert into A      (← move left)
        D[i-1][j-1],      # substitute in A    (↖ move diag)
    )
```

**Complexity**: O(n × m) time and space, where n and m are string lengths. For our short aliases (3-20 chars), this is trivially fast.

#### From Distance to Similarity Ratio

Raw distance isn't directly comparable across different-length strings. A 2-edit distance between 4-char strings (50% different) is much worse than between 20-char strings (10% different).

`rapidfuzz` normalizes to a 0-100 **similarity ratio**:

```
ratio ≈ (1 - distance / max(len(A), len(B))) × 100

"lgtm" vs "lgmt":     (1 - 2/4)  × 100 = 50    → below threshold (85)
"ship it" vs "ship ti": (1 - 2/7) × 100 = 71    → below threshold
"roger that" vs "roger tht": (1 - 2/10) × 100 = 80 → close!
```

(In practice, `rapidfuzz` uses a more sophisticated optimal alignment score that's slightly more generous than the naive formula above.)

We use a **threshold of 85** -- meaning the query must be at least 85% similar to a known alias. This catches common typos without producing false positives.

#### Why `rapidfuzz` over `difflib`?

Python's stdlib `difflib.SequenceMatcher` computes a similar ratio, but:
- `rapidfuzz` is implemented in C and is **~10x faster**
- It uses the same Levenshtein-based algorithm under the hood
- For our ~200 aliases, the difference is microseconds, but the API is also cleaner

---

### The TF-IDF Analogy

Think of TF-IDF like a **detective ranking suspects**. If someone yells "merge!" in a crowded office, that's not very helpful -- lots of people deal with merges (low signal). But if someone yells "canary!", only one person turns around -- that's a strong signal. TF-IDF is a formula that automatically figures out which words are "merge" (common, low value) vs "canary" (distinctive, high value).

---

### TF-IDF Step by Step (with real data)

Using 3 entries from `emojis.yaml`:

| Doc # | Emoji | Searchable Text |
|---|---|---|
| D1 | `✅🔀` | "pull request approved and merged . pr merged . lgtm merged" |
| D2 | `🚦⏳` | "in the merge queue waiting . merge queue . queued for merge" |
| D3 | `💥⚠️` | "merge conflicts need resolution . merge conflicts . rebase needed" |

#### Step 1: Term Frequency (TF) -- count words per document

After stop-word removal ("the", "in", "and", "for", "need" are dropped):

| Word | D1 (pr merged) | D2 (merge queue) | D3 (conflicts) |
|---|---|---|---|
| "merge" | 1 | 3 | 2 |
| "merged" | 3 | 0 | 0 |
| "pull" | 1 | 0 | 0 |
| "request" | 1 | 0 | 0 |
| "queue" | 0 | 2 | 0 |
| "conflicts" | 0 | 0 | 2 |
| "rebase" | 0 | 0 | 1 |

TF just counts. Notice "merge" is everywhere -- it's not distinctive.

#### Step 2: Inverse Document Frequency (IDF) -- how rare is each word?

Formula: `IDF(word) = log(total docs / docs containing word)`

| Word | Appears in # docs | IDF = log(3/n) |
|---|---|---|
| "merge" | 3 (all of them) | log(3/3) = **0.0** |
| "merged" | 1 (only D1) | log(3/1) = **1.1** |
| "queue" | 1 (only D2) | log(3/1) = **1.1** |
| "conflicts" | 1 (only D3) | log(3/1) = **1.1** |
| "rebase" | 1 (only D3) | log(3/1) = **1.1** |

The key insight: **"merge" gets IDF = 0** because it appears in every document. It's useless for distinguishing between entries. Meanwhile "queue", "conflicts", and "merged" each appear in only one document, so they have high IDF -- they're distinctive.

#### Step 3: TF-IDF = TF x IDF

| Word | D1 = TF x IDF | D2 = TF x IDF | D3 = TF x IDF |
|---|---|---|---|
| "merge" | 1 x 0.0 = **0** | 3 x 0.0 = **0** | 2 x 0.0 = **0** |
| "merged" | 3 x 1.1 = **3.3** | 0 | 0 |
| "queue" | 0 | 2 x 1.1 = **2.2** | 0 |
| "conflicts" | 0 | 0 | 2 x 1.1 = **2.2** |

"merge" is completely eliminated. Each document is now characterized only by its *distinctive* words.

#### Step 4: Query time -- "merge queue"

The query "merge queue" gets vectorized using the same vocabulary:

| Word | Query TF | x IDF | = TF-IDF |
|---|---|---|---|
| "merge" | 1 | x 0.0 | = **0** |
| "queue" | 1 | x 1.1 | = **1.1** |

Now cosine similarity compares this query vector against each document:

- vs D1 (`✅🔀`): query has "queue"=1.1, D1 has "queue"=0 --> **no overlap** --> score ~ 0
- vs D2 (`🚦⏳`): query has "queue"=1.1, D2 has "queue"=2.2 --> **strong overlap** --> score ~ 0.8
- vs D3 (`💥⚠️`): query has "queue"=1.1, D3 has "queue"=0 --> **no overlap** --> score ~ 0

Result: D2 (`🚦⏳` merge queue) wins decisively -- even though all three entries contain "merge".

---

### Why Bigrams Matter

This is the `ngram_range=(1, 2)` parameter in `engine.py`.

Without bigrams, the query "merge queue" produces two features: `"merge"` and `"queue"`. With bigrams, it produces three: `"merge"`, `"queue"`, **and** `"merge queue"` as a single unit.

Why it matters -- imagine you had a 4th entry:

| D4 | `🔀❓` | "queue management merge strategy" |

D4 contains both "merge" and "queue" separately, but NOT the phrase "merge queue". Without bigrams, D4 would score the same as D2. With bigrams, D2 has the bigram feature `"merge queue"` and D4 doesn't -- so D2 wins.

```
Query: "merge queue"

Features extracted (with bigrams):
  unigrams:  ["merge", "queue"]
  bigrams:   ["merge queue"]

D2 text: "merge queue . queued for merge"
  Has bigram "merge queue" --> BONUS match

D4 text: "queue management merge strategy"
  Has "merge" and "queue" separately, but NOT "merge queue" --> no bonus
```

---

### fit_transform() vs transform() -- Why the Distinction Matters

Think of it like **studying for a test** vs **taking the test**.

**`fit()` = Study the material.** The vectorizer reads ALL emoji descriptions and learns:
1. The **vocabulary** -- every unique word and bigram (~400 features).
2. The **IDF weights** -- how rare each word is across all entries.

**`transform()` = Take the test.** Using the learned vocabulary and IDF weights, convert text into a numerical vector.

**`fit_transform()` = Both at once** (optimization -- single pass instead of two).

```python
# In __init__ (line 148): registry gets fit_transform
# -- learn vocabulary FROM these entries, then vectorize them
texts = [entry.searchable_text for entry in self.entries]
self.tfidf_matrix = self.vectorizer.fit_transform(texts)

# In search() (line 182): query gets only transform
# -- use the vocabulary ALREADY learned, just convert this new text
query_vector = self.vectorizer.transform([query])
```

**What would go wrong with `fit_transform()` on the query?**

```
Registry vocabulary (learned during fit):
  ["merge", "queue", "pull", "request", "deploy", "hotfix", ...]
  400 columns

Registry vector for "merge queue":
  [0.0, 0.8, 0, 0, 0, 0, ...]   <-- positions in 400-column space

Query "merge queue" with transform():          <-- CORRECT
  [0.0, 1.1, 0, 0, 0, 0, ...]   <-- SAME 400 columns --> comparison works!

Query "merge queue" with fit_transform():      <-- WRONG
  Learns a NEW vocabulary: ["merge", "queue"]  (only 2 words!)
  [0.0, 1.1]                     <-- 2-column vector
  Cannot compare against 400-column registry matrix!
```

It's like two people taking a test -- but one has a 400-question answer sheet and the other has a 2-question answer sheet. You can't grade them the same way. `transform()` ensures everyone uses the same answer sheet.

**Matrix shapes in the engine:**

```
Registry (fit_transform):   45 x 400   (45 emoji entries, ~400 features)
Query    (transform):        1 x 400   (1 query, same 400 features)
```

Most of the query's 400 values are zero -- because "merge queue" only uses a few words out of the ~400 in the vocabulary. That's why the matrix is stored in sparse format (only non-zero values are kept).

---

### Cosine Similarity as Matrix Multiplication

Cosine similarity is a **normalized dot product**, which boils down to matrix multiplication with a transpose:

```
cosine_similarity(Q, R) = Q_normalized  *  R_normalized^T
```

Where each row is scaled to unit length (L2-normalized) before multiplying.

#### Worked example

Simplified vocabulary with 5 features:

```
Columns:  "merged"  "queue"  "merge_queue"  "conflicts"  "pull_request"
```

**Registry matrix R (3 entries x 5 features), after L2 normalization:**

```
              merged  queue  merge_queue  conflicts  pull_request
D1  ✅🔀   [  0.8    0.0      0.0          0.0        0.6     ]
D2  🚦⏳   [  0.0    0.61     0.79         0.0        0.0     ]
D3  💥⚠️   [  0.0    0.0      0.0          1.0        0.0     ]
```

**Query vector Q, normalized:**

```
Q  "merge queue"  [  0.0    0.6      0.8          0.0        0.0     ]
```

**Step 1: Transpose R (flip rows into columns):**

```
R = [3 x 5]                         R^T = [5 x 3]

     c0   c1   c2   c3   c4              D1    D2    D3
D1 [ 0.8  0.0  0.0  0.0  0.6 ]    c0 [ 0.8   0.0   0.0 ]
D2 [ 0.0  0.61 0.79 0.0  0.0 ]    c1 [ 0.0   0.61  0.0 ]
D3 [ 0.0  0.0  0.0  1.0  0.0 ]    c2 [ 0.0   0.79  0.0 ]
                                   c3 [ 0.0   0.0   1.0 ]
                                   c4 [ 0.6   0.0   0.0 ]
```

**Step 2: Matrix multiply Q x R^T:**

```
Q * R^T  =  [1 x 5] * [5 x 3]  =  [1 x 3]

Score D1:  (0.0*0.8) + (0.6*0.0) + (0.8*0.0) + (0.0*0.0) + (0.0*0.6)  =  0.0
Score D2:  (0.0*0.0) + (0.6*0.61)+ (0.8*0.79)+ (0.0*0.0) + (0.0*0.0)  =  0.37 + 0.63 = 1.0
Score D3:  (0.0*0.0) + (0.6*0.0) + (0.8*0.0) + (0.0*1.0) + (0.0*0.0)  =  0.0

Result: [ 0.0,  1.0,  0.0 ]
          D1    D2    D3
         ✅🔀   🚦⏳  💥⚠️
```

D2 (`🚦⏳` merge queue) scores 1.0 -- perfect match. The others score 0.

**Why angles instead of distances?** Cosine similarity is **scale-invariant**. A long description with many words has a larger vector magnitude than a short one -- Euclidean distance would penalize short descriptions unfairly. Cosine only cares about the *direction* the vectors point, not their length:

- **Score = 1.0**: Vectors point in the same direction (identical topic)
- **Score = 0.0**: Vectors are perpendicular (completely unrelated)

**In the actual engine:**

```
[1 x 400]  *  [400 x 45]  =  [1 x 45]
 query          registry^T     one score per emoji entry
```

One matrix multiplication, 45 similarity scores. That's all `cosine_similarity(query_vector, self.tfidf_matrix)` does on line 206 of `engine.py`.

---

### The LEARN Comments

Open `emoji_generator/engine.py` for inline explanations on every technical decision:
- Two-stage strategy: why short lingo needs lookup, not TF-IDF
- Levenshtein distance: the DP recurrence, matrix walkthrough, and ratio normalization
- TF-IDF theory and parameter choices
- Why `ngram_range=(1, 2)` and not (1, 3)
- Why `stop_words="english"` is safe now (Stage 1 handles the edge cases)
- What `sublinear_tf=True` does (logarithmic TF scaling)
- Sparse matrices and why they matter
- The confidence threshold and what scores mean intuitively
- `rapidfuzz.fuzz.ratio` vs raw Levenshtein distance

---

## Running Tests

```bash
# From the project root, with venv activated
pytest tests/ -v
```

## Project Structure

```
emoji_generator/
  emoji_generator/
    __init__.py          # Package init
    __main__.py          # python -m entry point
    cli.py               # CLI + REPL interface
    engine.py            # Two-stage engine: LingoLookup + TF-IDF (annotated with LEARN comments)
    registry.py          # YAML loader + EmojiEntry dataclass
    data/
      emojis.yaml        # The emoji dictionary (human-editable)
  tests/
    test_engine.py       # Engine matching accuracy tests
  pyproject.toml         # Package config + devmoji script entry
  requirements.txt       # Dependencies
  README.md              # This file
```

## Dependencies

| Package | Purpose |
|---|---|
| scikit-learn | TF-IDF vectorizer + cosine similarity (Stage 2) |
| rapidfuzz | Levenshtein-based fuzzy string matching (Stage 1) |
| pyyaml | Load emoji registry from YAML |
| pyperclip | Cross-platform clipboard |
| prompt_toolkit | REPL with history + auto-suggestions |
| rich | Pretty terminal output (tables, panels, colors) |
