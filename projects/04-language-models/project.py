# project.py


import pandas as pd
import numpy as np
import os
import re
import requests
import time


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def get_book(url):
    res = requests.get(url)
    text = res.text
    pattern = r'\*\*\* START.*\*\*\*([\S\s]*)\*\*\* END.*\*\*\*'
    prog = re.compile(pattern)
    contents = prog.search(text).group(1)
    contents = contents.replace('\r\n','\n')
    time.sleep(5)
    return contents


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def tokenize(book_string):
    stripped = book_string.strip()
    with_markers = re.sub(r'\n{2,}', '\x03\x02', stripped)
    tokens = re.findall(r'\w+|[^\s\w]', stripped)
    tokens.insert(0, '\x02')
    tokens.append('\x03')
    return tokens


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


class UniformLM(object):


    def __init__(self, tokens):

        self.mdl = self.train(tokens)
        
    def train(self, tokens):
        uniques = set(tokens)
        return pd.Series(index=uniques, data = 1/len(uniques))
    
    def probability(self, words):
        prob = 1
        for word in words:
            if word in self.mdl.index:
                prob *= self.mdl[word]
            else:
                return 0
        return prob


        
    def sample(self, M):
        return ' '.join(self.mdl.sample(M, replace=True).index)


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


class UnigramLM(object):
    
    def __init__(self, tokens):

        self.mdl = self.train(tokens)
    
    def train(self, tokens):
        return pd.Series(tokens).value_counts() / len(tokens)
    
    def probability(self, words):
        prob = 1
        for word in words:
            if word in self.mdl.index:
                prob *= self.mdl[word]
            else:
                return 0
        return prob
        
    def sample(self, M):
        return ' '.join(self.mdl.sample(M, replace=True, weights=self.mdl).index)


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


class NGramLM(object):
    
    def __init__(self, N, tokens):
        # You don't need to edit the constructor,
        # but you should understand how it works!
        
        self.N = N

        ngrams = self.create_ngrams(tokens)

        self.ngrams = ngrams
        self.mdl = self.train(ngrams)

        if N < 2:
            raise Exception('N must be greater than 1')
        elif N == 2:
            self.prev_mdl = UnigramLM(tokens)
        else:
            self.prev_mdl = NGramLM(N-1, tokens)

    def create_ngrams(self, tokens):
        ...
        
    def train(self, ngrams):
        # N-Gram counts C(w_1, ..., w_n)
        ...
        
        # (N-1)-Gram counts C(w_1, ..., w_(n-1))
        ...

        # Create the conditional probabilities
        ...
        
        # Put it all together

        ...
        ...
    
    def probability(self, words):
        ...
    

    def sample(self, M):
        # Use a helper function to generate sample tokens of length `length`
        ...
        
        # Transform the tokens to strings
        ...
        ...
