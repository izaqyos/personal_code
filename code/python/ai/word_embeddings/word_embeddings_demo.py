#!/opt/homebrew/bin/python3

"""
pre-requisites:
    a. setup venv with python3
    [i500695@WYLQRXL9LQ:2024-07-16 15:23:24:~/work/code/python/ai/word_embeddings:]2003$ python3 -m venv .
[i500695@WYLQRXL9LQ:2024-07-16 15:24:06:~/work/code/python/ai/word_embeddings:]2004$ source bin/activate

    b. install gensim
     python3 -m pip install gensim
resolve ImportError: cannot import name 'triu' from 'scipy.linalg' 
$ pip install scipy==1.12
$ python3 -m pip install matplotlib
$ python3 -m pip install scikit-learn

    c. download wiki.en.vec 

    d. run this script 
$ python word_embeddings_demo.py 

"""
from gensim.models import KeyedVectors
from numpy import triu
import time
import matplotlib.pyplot as plt
#%matplotlib inline #for jupyter env
from sklearn.decomposition import PCA



def load_word2vec_model():
    wiki_en_embd = "wiki.en.vec"
    start_time = time.time()
    print(f"loading {wiki_en_embd}...")
    wv = KeyedVectors.load_word2vec_format("wiki.en.vec")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"{wiki_en_embd} loaded in {elapsed_time:.4f} seconds")
    
    print(f"Demo of word2vec using gensim. loading {len(wv)} words from {wiki_en_embd}...")
    
    print(f"To get a sense of the vectors dimensions: {wv.vectors.shape}")
    
    print(f" vector of word italy: {type(wv.get_vector('italy')), wv.get_vector('italy').shape}")
    print(" Note the 2519370 words and 300 dimensions per vector. ")
    return wv

def plot_pairs(wv, a, b):
    ndx_a = [wv.key_to_index[a_i] for a_i in a if a_i in wv.key_to_index] 
    ndx_b = [wv.key_to_index[b_i] for b_i in b if b_i in wv.key_to_index]

    pca = PCA(2)
    wv2 = pca.fit_transform(wv.vectors[ndx_a + ndx_b])

    wv_a = wv2[:len(ndx_a)]
    wv_b = wv2[len(ndx_a):]

    plt.title("Word Embeddings Vector Pairs")
    plt.figure(figsize=(10, 10))
    plt.scatter(wv_a[:, 0], wv_a[:, 1])
    plt.scatter(wv_b[:, 0], wv_b[:, 1])

    for i, (p_a, p_b) in enumerate(zip(a, b)):
        if p_a in wv.key_to_index and p_b in wv.key_to_index:
            plt.annotate(p_a, wv_a[i], xytext=(-20, -15), textcoords="offset pixels")
            plt.annotate(p_b, wv_b[i], xytext=(-20, -15), textcoords="offset pixels")

    for i in range(len(wv_a)):
        plt.arrow(wv_a[i, 0], wv_a[i, 1], wv_b[i, 0] - wv_a[i, 0], wv_b[i, 1] - wv_a[i, 1], shape="left")
    plt.show()

def rome_italy(wv):
    vec_rome = wv.get_vector("rome")
    vec_italy = wv.get_vector("italy")
    vec_france = wv.get_vector("france")
    print(wv.similar_by_vector(vec_rome - vec_italy + vec_france, topn=1))

def main():
    wv = load_word2vec_model()
    countries = ["china",   "russia", "japan", "turkey", "poland", "germany", "france", "italy", "greece", "spain",  "portugal"]
    capitals  = ["beijing", "moscow", "tokyo", "ankara", "warsaw", "berlin",  "paris",  "rome",  "athens", "madrid", "lisbon"]
    print('"rome" - "italy" + "france" is actually "paris", similar to the classic king - man + woman = queen')
    rome_italy(wv)
    print(f"Plotting pairs: {countries} and {capitals}")
    print('We can see that capitals and countries are well separated. Additionally, the vector that maps each country to each capital (i.e. country - capital) is approximately the same. That vector "encodes" the concept of "being a capital of')
    plot_pairs(wv, countries, capitals)

if __name__ == "__main__":
    main()

