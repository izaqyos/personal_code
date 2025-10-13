"""
Run instructions:
Activate venv $ pyvenv_a
install libs
$ pip install numpy
$ pip install gensim
$ pip install sklearn
$ pip install scikit-learn
$ pip install matplotlib

Run $  python wordnet1.py
"""

from nltk.corpus import wordnet as wn
from numpy import dot
from numpy.linalg import norm
import numpy as np

import gensim.downloader as api
from gensim.models import KeyedVectors
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer

import time

all_hypernyms = list(set(wn.all_synsets(pos='n')))

# Print the taxonomy (hypernym hierarchy) for a given word. Default is noun 'n'
def print_taxonomy(word, pos='n'):
    """Prints the hypernym (is-a) taxonomy of a given word.

    This function takes a word and its part of speech, finds the corresponding synset 
    (concept) in WordNet, and then traverses up its hypernym hierarchy. The hypernyms
    are printed in a numbered format, starting from the most general (root) concept and 
    proceeding to the most specific (the original word), along with their definitions.

    Args:
        word (str): The word to analyze.
        pos (str, optional): The part of speech ('n' for noun, 'v' for verb, 'a' for 
                             adjective, 'r' for adverb). Defaults to 'n' (noun).

    Raises:
        IndexError: If the specified word is not found in WordNet for the given part of speech.
        NLTK Error: If the 'wordnet' corpus is not downloaded and available. 
    """
    synset = wn.synsets(word, pos=pos)[0]
    hyper = lambda s: s.hypernyms()
    taxonomy = list(synset.closure(hyper))
    
    print(f"Taxonomy for '{word}':")
    # Print each hypernym in reverse order (from most general to most specific)
    for i, hypernym in enumerate(reversed(taxonomy), 1):
        print(f"{i}. {hypernym.name().split('.')[0]} ({hypernym.definition()})")
    print(f"{len(taxonomy) + 1}. {synset.name().split('.')[0]} ({synset.definition()})")

"""
This following code aims to calculate the semantic similarity between two words using a technique called *cosine similarity* applied to their hypernym vectors (representations based on their more general categories in WordNet).

**Code Breakdown:**

1. **`get_vector` function:**
   - Takes a `word` as input.
   - Finds the first synset (set of synonyms representing a concept) for that word in WordNet.
   - Gets all hypernyms of the synset (all words representing more general concepts than the original word), including the synset itself.
   - Creates a binary vector where each element represents whether a hypernym from the global `all_hypernyms` list is present in the word's hypernym list (1 if present, 0 otherwise).  This creates a vector representation for each word where the presence or absence of hypernyms indicates a semantic relationship.

2. **`cosine_similarity` function:**
   - Takes two vectors (`vec1` and `vec2`) as input.
   - Calculates the cosine similarity between the vectors:
      - **Dot product:**  The sum of the element-wise products of the two vectors.
      - **Norm:** The magnitude (length) of each vector.
      - **Cosine similarity:** The dot product divided by the product of the norms. This results in a value between -1 (dissimilar) and 1 (similar), where 0 indicates no relationship.

3. **`show_similarity` function:**
   - Takes two words (`word1` and `word2`) as input.
   - Calls `get_vector` to obtain their hypernym vectors.
   - Calls `cosine_similarity` to compute the similarity between the vectors.
   - Prints the result in a formatted way.

**How It Works:**

1. **Word Representation:** Each word is converted into a vector based on its hypernym relationships. This captures a semantic aspect of the word's meaning.
2. **Similarity Calculation:** Cosine similarity measures the angle between the two vectors. A smaller angle (higher cosine value) means the words are more semantically related.
3. **Output:** The code prints the cosine similarity between the two words, providing a numerical estimate of their semantic relatedness.

**Example:**

If you run:
```python
show_similarity("car", "bicycle")
```

You might get output like this:

```
Cosine similarity between 'car' and 'bicycle': 0.6666666666666666
```

This indicates a moderate degree of similarity, as both are vehicles.
"""

"""
**What is Cosine Similarity?**

Cosine similarity is a metric used to measure how similar two non-zero vectors are. It's particularly useful when dealing with high-dimensional data like text documents or images, where traditional distance measures might not be as effective.

**The Intuition:**

* **Vectors as Directions:** Think of vectors as arrows pointing in space.  The direction of the arrow represents the vector's content (e.g., the words in a document or the features in an image). The length of the arrow can represent the magnitude or importance of the vector.
* **Angle as Similarity:** Cosine similarity focuses on the angle between the two vectors. If two vectors point in the same direction (small angle), they are considered very similar. If they are perpendicular (90-degree angle), they are considered dissimilar.

**Mathematical Definition:**

The cosine similarity between two vectors **a** and **b** is calculated as:

```
cosine_similarity(a, b) = (a · b) / (||a|| * ||b||) 
```

where:

* **a · b** is the dot product of vectors **a** and **b**.
* ||a|| and ||b|| are the magnitudes (lengths) of vectors **a** and **b** respectively.

**Why Cosine Similarity?**

* **Focus on Orientation:** Cosine similarity disregards the magnitude (length) of the vectors and focuses only on their orientation. This is often desirable when comparing documents or images, as you may want to focus on the content rather than the amount of content.
* **Normalized Values:** Cosine similarity results in a value between -1 and 1.  
    * -1: Vectors are exactly opposite (most dissimilar).
    * 0: Vectors are orthogonal (no relationship).
    * 1: Vectors are identical (most similar).
* **Effective in High Dimensions:** Cosine similarity works well even in high-dimensional spaces, where other distance measures might suffer from the "curse of dimensionality."

**Applications:**

* **Text Similarity:** Comparing documents based on the similarity of their word vectors.
* **Image Similarity:** Finding similar images based on feature vectors.
* **Recommendation Systems:** Recommending items (movies, products, etc.) to users based on the similarity of their preference vectors.
* **Information Retrieval:** Ranking search results based on their similarity to the query.
* **Natural Language Processing:** Comparing the semantic similarity of words or phrases.

**Example:**

Consider two word vectors:

* **a** = [1, 2, 0]
* **b** = [3, 6, 0]

These vectors point in the same direction but have different magnitudes. Their cosine similarity is 1, indicating they are perfectly similar in terms of direction.

**In the WordNet Code Example:**

This code uses cosine similarity to compare the hypernym vectors of two words. This is a way to estimate their semantic similarity based on their shared "is-a" relationships in WordNet's taxonomy.
"""

"""
**What is the Dot Product?**

The dot product (also called scalar product or inner product) is a mathematical operation on two vectors that produces a single scalar (a number). It's a fundamental concept in linear algebra and has various applications in physics, engineering, and computer science.

**Mathematical Definition:**

Given two vectors, **a** = [a₁, a₂, ..., aₙ] and **b** = [b₁, b₂, ..., bₙ], their dot product is calculated as:

**a · b** = a₁b₁ + a₂b₂ + ... + aₙbₙ

**Geometric Interpretation:**

The dot product has a geometric meaning:

* **Magnitude and Angle:** It's equal to the product of the magnitudes (lengths) of the two vectors and the cosine of the angle between them:
   **a · b** = ||**a**|| ||**b**|| cos θ

* **Projection:** The dot product of **a** and **b** is also the magnitude of the projection of **a** onto **b** (or vice versa), multiplied by the magnitude of **b**.

**Properties:**

* **Commutative:** **a · b** = **b · a**
* **Distributive:** **a · (b + c)** = **a · b** + **a · c**
* **Scalar Multiplication:** (k**a**) **· b** = k(**a · b**)
* **Self Dot Product:** **a · a** = ||**a**||² (the magnitude of **a** squared)

**Applications:**

The dot product is used in various areas, including:

* **Physics:**  To calculate work done (force dot displacement), power (force dot velocity), and more.
* **Computer Graphics:** For lighting calculations, determining surface normals, and backface culling.
* **Machine Learning:** In algorithms like cosine similarity (as you saw in the previous code), to find the similarity between vectors representing documents, images, or other data.

**Key Insights from the Cosine Similarity Example:**

In the context of this code, the dot product was used within the cosine similarity calculation.  Here's what it tells you:

* **Word Overlap:** A higher dot product implies that the two word vectors have more non-zero elements in common, meaning they share more hypernyms in their taxonomies.
* **Similarity Measure:** When combined with the normalization of the vectors (dividing by the magnitudes), the cosine similarity provides a normalized measure of how similar the words are in terms of their semantic relationships.

Let me know if you'd like more details on any of these aspects, or have any other questions!

"""
def get_vector(word):
    synset = wn.synsets(word)[0]
    hypernyms = list(synset.closure(lambda s: s.hypernyms()))
    return [1 if h in hypernyms else 0 for h in all_hypernyms]

# Compute dot product of the two vectors divided by the product of their norms
def cosine_similarity(vec1, vec2):
    return dot(vec1, vec2) / (norm(vec1) * norm(vec2))

def show_similarity(word1, word2):
    vec1 = get_vector(word1)
    vec2 = get_vector(word2)
    similarity = cosine_similarity(vec1, vec2)
    print(f"Cosine similarity between '{word1}' and '{word2}': {similarity}")


def loadw2v():
    # Download necessary NLTK data
    print("Downloading wordnet, omw-1.4 and PoS average perceptron tagger")
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)

    # Initialize the lemmatizer
    lemmatizer = WordNetLemmatizer()

    # Download and load the pre-trained Word2Vec model
    print("Downloading and loading the model... This may take a few minutes.")
    model = api.load('word2vec-google-news-300')
    print("Model loaded!")
    return model

def get_word_vector(word, model):
    """Retrieves the vector representation of a given word from a pre-trained word embedding model.

    This function searches for the word in the model's vocabulary in different case variations:
    1. Lowercase
    2. Uppercase
    3. Capitalized

    Args:
        word (str): The word for which the vector is to be retrieved.

    Returns:
        numpy.ndarray: The vector representation of the word.

    Raises:
        KeyError: If the word is not found in the model's vocabulary in any of the case variations.
    """
    if word.lower() in model.key_to_index:
        return model[word.lower()]
    elif word.upper() in model.key_to_index:
        return model[word.upper()]
    elif word.capitalize() in model.key_to_index:
        return model[word.capitalize()]
    else:
        raise KeyError(f"Word '{word}' not in vocabulary")

def play_with_word_vectors(model):
    """Retrieves and prints word vectors for a list of words, along with their dimensions.
    Args:
        model (gensim.models.keyedvectors.KeyedVectors): The loaded Word2Vec model.
    """
    words = ["apple", "banana", "cat", "dog", "elephant", "fish", "grape", "house", "ice", "jungle"]
    for word in words:
        try:
            vector = get_word_vector(word, model)  # Get the vector (assuming you have a get_word_vector function)
            print(f"\nRaw vector for '{word}':")
            print(vector)
            print(f"Vector dimensions: {len(vector)}")  # Print the length of the vector (its dimension)
        except KeyError:
            print(f"Word '{word}' not found in vocabulary")
    
    print("Now find similar words")
    for word in words:
        find_similar_words(word, model)


def is_valid_word(word):
    """Checks if a word is valid for processing.

    A valid word is non-empty, contains only alphabetic characters (no apostrophes or other punctuation),
    and doesn't start or end with an underscore.

    Args:
        word (str): The word to validate.

    Returns:
        bool: True if the word is valid, False otherwise.
    """
    return word and word.isalpha() and not (word.startswith('_') or word.endswith('_')) 


from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
lemmatizer = WordNetLemmatizer()
def process_word(word):
    """Lemmatizes a word (if valid) using its part of speech tag.
    Args:
        word (str): The word to process.
    Returns:
        str or None: The lemmatized word if valid, otherwise None.
    Raises:
        ValueError: If the word is empty or contains non-alphabetic characters.
        Exception: If the wordnet synsets lookup fails for an unknown reason.
    """
    if not word:  
        raise ValueError("Word cannot be empty")

    word = word.lower()
    if not word.isalpha():  
        raise ValueError("Word should only contain alphabetic characters")
    
    if word.startswith('_') or word.endswith('_') or '_' in word:
        return None  # Ignore words with underscores

    try:
        pos = pos_tag([word])[0][1][0].lower()  # Get POS tag, defaults to noun ('n')
        synsets = wordnet.synsets(word, pos=pos)  # Find synsets
        if not synsets:  # Word not found in WordNet
            return None

        lemma = lemmatizer.lemmatize(word, pos=pos)
        return lemma

    except Exception as e:  # Catch unexpected errors
        print(f"Error processing word '{word}': {e}")
        return None

def word_in_vocab(word, model):
    """Checks if a word (or its lemma) exists in a word embedding model's vocabulary.

    Args:
        word (str): The word to check.
        model (gensim.models.keyedvectors.KeyedVectors): The word embedding model.
    
    Returns:
        bool: True if the word or its lemma is in the vocabulary, False otherwise.
    """
    vocab_set = set(model.key_to_index)  # Convert vocabulary to a set for faster lookup
    lemma = process_word(word)
    return word.lower() in vocab_set or word.upper() in vocab_set or word.capitalize() in vocab_set or lemma in vocab_set

def find_similar_words(word, model, topn=5):
    if not word_in_vocab(word, model):
        print(f"'{word}' is not in the vocabulary.")
        return
    print(f"\nWords similar to '{word}':")
    original_word = process_word(word)
    similar_words = model.most_similar(positive=[get_word_vector(word, model)], topn=50)  # Get more words than needed
    valid_words = []
    for similar_word, score in similar_words[:3]:
        print(f"check similar word {similar_word}")
        if not is_valid_word(word):
            print(f"word {similar_word} is not valid. skipping")
            continue
        processed_word = process_word(similar_word.replace("'", ""))  #remove apostrophes
        #processed_word = process_word(similar_word)
        if processed_word and processed_word != original_word and processed_word not in [w for w, _ in valid_words]:
            valid_words.append((processed_word, score))
            if len(valid_words) == topn:
                break
    
    # If we don't have enough words, relax the filtering
    if len(valid_words) < topn:
        for similar_word, score in similar_words:
            if similar_word not in [w for w, _ in valid_words]:
                valid_words.append((similar_word, score))
                if len(valid_words) == topn:
                    break
    
    for similar_word, score in valid_words[:topn]:
        print(f"{similar_word}: {score:.2f}")


def main():
    print('-'*120)
    print("This is a demo of using WordNet and NLTK in Python")
    print("Lets check the taxonomy for 'king'")
    taxonomy_defenition = """
    In the context of words, taxonomy refers to a hierarchical classification system that organizes words based on their semantic relationships. It reveals how words relate to each other in terms of broader categories (hypernyms) and more specific instances (hyponyms), creating a structured overview of a word's meaning.
"""
    print(taxonomy_defenition)
    print_taxonomy("king")
    sleep_for(3)
    print('-'*120)
    print(f"lets show an example of calculating similarity between words, say {("car", "bicycle")}")
    show_similarity("car", "bicycle")
    print('-'*120)
    print(f"they are quite similar, as both are vehicles. now lets try {("rocket", "shark")}")
    show_similarity("rocket", "shark")
    print('-'*120)
    print("Now we get lower similarity as rocket and shark are not really related")
    print('-'*120)
    sleep_for(5)
    print("now load word2vec model")
    model = loadw2v()
    print('-'*120)
    print("Lets explore some word vectors...")
    play_with_word_vectors(model)
    sleep_for(5)

    
def sleep_for(seconds):
    for remaining in range(seconds, 0, -1):
        print(f"Sleep Time remaining: {remaining} seconds")
        time.sleep(1)
    print("Sleep finished!") 

if __name__ == '__main__':
    main()

