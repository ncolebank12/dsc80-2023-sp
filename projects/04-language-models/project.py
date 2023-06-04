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
        n = self.N
        i = 0
        out = []
        while i < len(tokens) - n + 1:
            out.append(tuple(tokens[i] for i in range(i,i+n)))
            i += 1
        return out

        
    def train(self, ngrams):
        # N-Gram counts C(w_1, ..., w_n)
        ngram_series = pd.Series(ngrams)
        ngram_counts = ngram_series.value_counts()
        
        # (N-1)-Gram counts C(w_1, ..., w_(n-1))
        n1gram_counts = ngram_series.apply(lambda x : x[:-1]).value_counts()
        last_n1gram = ngrams[-1]
        last_n1gram = last_n1gram[-self.N + 1:]
        if last_n1gram in set(n1gram_counts.index):
            n1gram_counts[last_n1gram] += 1
        # Create the conditional probabilities
        data = []
        for ngram, count in ngram_counts.items():
            n1gram = ngram[:-1]
            n1gram_count = n1gram_counts[n1gram]
            prob = count / n1gram_count
            data.append((ngram, n1gram, prob))

        return pd.DataFrame(data, columns=['ngram', 'n1gram', 'prob'])
    
    def get_prob(self, mdl, ngram):
        if isinstance(mdl, pd.Series): #is unigram model
            if ngram[0] in set(mdl.index):
                return mdl[ngram[0]]
            else:
                return 0
        else:
            if mdl['ngram'].isin([tuple(ngram)]).any():
                return mdl[mdl['ngram'] == tuple(ngram)].iloc[0]['prob']
            else:
                return 0
        
    def probability(self, words):
        prob = 1
        prev_mdl = self.prev_mdl
        for i in range(self.N - 1, 0, -1):
            if (i < len(words) + 1):
                res = self.get_prob(prev_mdl.mdl, words[0:i])
                prob *= res

            if (i != 1):
                prev_mdl = prev_mdl.prev_mdl
        for i in range(len(words) - self.N + 1):
            res = self.get_prob(self.mdl, words[i:i+self.N])
            prob *= res
        return prob
                

    def generate_tokens(self, m, tokens):
        if m == 0:
            return
        if self.N - 1 > len(tokens):
            self.prev_mdl.generate_tokens(m-1, tokens)
        prev = tuple(tokens[-self.N + 1:])
        if str(prev) in self.mdl['n1gram'].astype(str).values:
            possibilities = self.mdl[self.mdl['n1gram'] == prev]
            tokens.append(possibilities['ngram'].sample().iloc[0][-1])
        else:
            tokens.append('\x03')
        self.generate_tokens(m-1, tokens)


    def sample(self, M):
        # Use a helper function to generate sample tokens of length `length`
        tokens = ['\x02']
        self.generate_tokens(M-1, tokens)
        tokens.append('\x03')
        
        # Transform the tokens to strings
        return ' '.join(tokens)
