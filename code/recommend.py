'''

author: Fateme Najafi

Recommend products and evaluate

'''
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import jaccard_score
from TermFrequency import TermFrequency
from clean_data import *

jaccard_sim = lambda x, y: jaccard_score(x, y, average='macro')
cosine_sim  = lambda x, y: cosine_similarity(x.reshape(1, len(x)), y.reshape(1, len(x)))[0][0]


def calculate_similarity(corpus_product, corpus_text, similarity_function):
    sims = np.array([similarity_function(product, text) for index_t, text in enumerate(corpus_text) for index_p, product in enumerate(corpus_product) ])
    return sims.reshape(len(corpus_text), len(corpus_product))

def predict (similarity_matrix, top_n):
    return [arr.argsort()[-top_n:][::-1] for arr in similarity_matrix]
    