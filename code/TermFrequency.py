'''

author: Fateme Najafi
Term Frequency

'''

import numpy as np

class TermFrequency ():

    def __init__(self, data, data_type = 'product', word2index = False , index2word = False):
        self.word2index , self.index2word = word2index, index2word
        if (data_type == 'product'):
            self.word2index, self.index2word = self.create_dictionaries(data)
        self.dimension = len(self.word2index)
        self.corpus_TF = 0
        if (data_type == 'product'):
            self.corpus_TF = self.term_frequency_all(data, self.term_frequency_product)
        if (data_type == 'text'):
            self.corpus_TF = self.term_frequency_all(data, self.term_frequency_text)
        
    def create_dict(self, tokenized):
        '''
        It creates dictionary for a list of words.
        '''
        word_dict = {}
        for word in tokenized:
            if (word in word_dict.keys()):
                word_dict[word]+=1
            else:
                word_dict[word]=1
        return word_dict

    def corpus_words(self, corpus):
        '''
        It creates a sorted list of all the words in the given corpus.
        '''
        corpus_dict = [self.create_dict(product) for product in corpus]
        all_keys = list({word for product_dict in corpus_dict for word in list(product_dict.keys())})
        all_keys.sort(reverse=False)
        return all_keys

    def create_dictionaries(self, corpus):
        '''
        It creates 2 dictionaries:
            * word2index
            * index2word
        '''
        all_keys = self.corpus_words(corpus)
        word2index = {}
        index2word = {}
        for index, word in enumerate(all_keys):
            word2index[word]=index
            index2word[index]=word
        return word2index, index2word

    def term_frequency_product (self, tokenized_text):
        '''
        For given product, it returns a row of tf.
        '''
        tf = np.zeros(self.dimension).tolist()
        for word in tokenized_text:
            tf[self.word2index[word]]+=1
        return tf

    def term_frequency_text (self, tokenized_text):
        '''
        For given text, it returns a row of tf depends on words that occured in products.
        '''
        tf = np.zeros(self.dimension).tolist()
        for word in tokenized_text:
            if (word in self.word2index.keys()):
                tf[self.word2index[word]]+=1
        return tf
    
    def term_frequency_all (self, corpus, tf_func):
        '''
        It returns term frequency of given corpus
        '''
        return np.array([tf_func(text) for text in corpus]) 