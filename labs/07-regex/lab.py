# lab.py


import pandas as pd
import numpy as np
import os
import re


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def match_1(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_1("abcde]")
    False
    >>> match_1("ab[cde")
    False
    >>> match_1("a[cd]")
    False
    >>> match_1("ab[cd]")
    True
    >>> match_1("1ab[cd]")
    False
    >>> match_1("ab[cd]ef")
    True
    >>> match_1("1b[#d] _")
    True
    """
    pattern = r'^..\[..\].*'

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_2(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_2("(123) 456-7890")
    False
    >>> match_2("858-456-7890")
    False
    >>> match_2("(858)45-7890")
    False
    >>> match_2("(858) 456-7890")
    True
    >>> match_2("(858)456-789")
    False
    >>> match_2("(858)456-7890")
    False
    >>> match_2("a(858) 456-7890")
    False
    >>> match_2("(858) 456-7890b")
    False
    """
    pattern = r'^\(858\) \d{3}-\d{4}$'

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_3(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_3("qwertsd?")
    True
    >>> match_3("qw?ertsd?")
    True
    >>> match_3("ab c?")
    False
    >>> match_3("ab   c ?")
    True
    >>> match_3(" asdfqwes ?")
    False
    >>> match_3(" adfqwes ?")
    True
    >>> match_3(" adf!qes ?")
    False
    >>> match_3(" adf!qe? ")
    False
    """
    pattern = r'^[a-zA-Z0-9 ?]{5,9}\?$'

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_4(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_4("$$AaaaaBbbbc")
    True
    >>> match_4("$!@#$aABc")
    True
    >>> match_4("$a$aABc")
    False
    >>> match_4("$iiuABc")
    False
    >>> match_4("123$$$Abc")
    False
    >>> match_4("$$Abc")
    True
    >>> match_4("$qw345t$AAAc")
    False
    >>> match_4("$s$Bca")
    False
    >>> match_4("$!@$")
    False
    """
    pattern = r'^\$[^abc$]*\$(A|a)+(B|b)+(C|c)+$'

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_5(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_5("dsc80.py")
    True
    >>> match_5("dsc80py")
    False
    >>> match_5("dsc80..py")
    False
    >>> match_5("dsc80+.py")
    False
    """
    pattern = r'^[A-Za-z0-9_]+\.py$'

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string.lower()) is not None


def match_6(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_6("aab_cbb_bc")
    False
    >>> match_6("aab_cbbbc")
    True
    >>> match_6("aab_Abbbc")
    False
    >>> match_6("abcdef")
    False
    >>> match_6("ABCDEF_ABCD")
    False
    """
    pattern = r'^[a-z]+_[a-z]+$'

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_7(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_7("_abc_")
    True
    >>> match_7("abd")
    False
    >>> match_7("bcd")
    False
    >>> match_7("_ncde")
    False
    """
    pattern = r'^_.*_$'

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None



def match_8(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_8("ASJDKLFK10ASDO")
    False
    >>> match_8("ASJDKLFK0ASDo!!!!!!! !!!!!!!!!")
    True
    >>> match_8("JKLSDNM01IDKSL")
    False
    >>> match_8("ASDKJLdsi0SKLl")
    False
    >>> match_8("ASDJKL9380JKAL")
    True
    """
    pattern = r'^[^Oi1]+$'

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None



def match_9(string):
    '''
    DO NOT EDIT THE DOCSTRING!
    >>> match_9('NY-32-NYC-1232')
    True
    >>> match_9('ca-23-SAN-1231')
    False
    >>> match_9('MA-36-BOS-5465')
    False
    >>> match_9('CA-56-LAX-7895')
    True
    >>> match_9('NY-32-LAX-0000') # If the state is NY, the city can be any 3 letter code, including LAX or SAN!
    True
    >>> match_9('TX-32-SAN-4491')
    False
    '''
    pattern = r'^(NY-\d{2}-[A-Z]{3}|CA-\d{2}-(SAN|LAX))-\d{4}$'

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_10(string):
    '''
    DO NOT EDIT THE DOCSTRING!
    >>> match_10('ABCdef')
    ['bcd']
    >>> match_10(' DEFaabc !g ')
    ['def', 'bcg']
    >>> match_10('Come ti chiami?')
    ['com', 'eti', 'chi']
    >>> match_10('and')
    []
    >>> match_10('Ab..DEF')
    ['bde']
    
    '''
    string = string.lower()
    string = re.sub(r'(\W|a)+', '', string)
    return re.findall(r'.{3}', string)


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def extract_personal(s):
    emails = re.findall(r'[\|, 	\b]([A-Za-z0-9]+@[A-Za-z0-9.]+)[| ,\b*	]',s)
    numbers = re.findall(r'ssn:(\d{3}-\d{2}-\d{4})', s)
    b_addresses = re.findall(r'bitcoin:([A-Za-z0-9]*)', s)
    s_addresses = re.findall(r'[0-9]+ [A-Za-z]+ [A-Za-z]+', s)
    return (emails, numbers, b_addresses, s_addresses)

# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def tfidf_data(reviews_ser, review):
    unique_words = set(re.findall(r'\b\w+\b', review))
    data = []
    for word in unique_words:
        count = len(re.findall(fr'\b{word}\b', review))
        tf = count / len(unique_words)
        idf = np.log(reviews_ser.size / reviews_ser.str.contains(word).sum())
        data.append({'cnt': count, 'tf': tf, 'idf': idf, 'tfidf': tf*idf})
    return pd.DataFrame(index=unique_words, data=data)

def relevant_word(out):
    return out['tfidf'].idxmax()


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def hashtag_list(tweet_text):
    return tweet_text.apply(lambda text : re.findall(r'#(\S+)', text) or [])

def get_most_common(hashtags, all_hashtags):
    if len(hashtags) == 0:
        return np.NAN
    elif len(hashtags) == 1:
        return hashtags[0]
    else:
        max_index = 0
        max_count = 0
        for i, hashtag in enumerate(hashtags):
            occurences = all_hashtags.count(hashtag)
            if occurences > max_count:
                max_count = occurences
                max_index = i
        return hashtags[max_index]


    

def most_common_hashtag(tweet_lists):
    return tweet_lists.apply(lambda hashtags : get_most_common(hashtags, tweet_lists.sum()))


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------




    
def clean_tweet(tweet):
    tweet = re.sub(r'@\S+|http:\/\/\S+|https:\/\/\S+|^RT|#\S+', '', tweet)
    tweet = re.sub(r'[^A-Za-z0-9 ]+', ' ', tweet)
    tweet = tweet.lower()
    tweet = re.sub(r' +', ' ', tweet.strip())
    return tweet

def create_features(ira):
    out = pd.DataFrame(index=ira.index)
    as_lists = hashtag_list(ira['text'])
    out['text'] = ira['text'].apply(clean_tweet)
    out['num_hashtags'] = as_lists.apply(lambda x : len(x))
    out['mc_hashtags'] = most_common_hashtag(as_lists)
    out['num_tags'] = ira['text'].apply(lambda x : len(re.findall(r'@\S+', x)))
    out['num_links'] = ira['text'].apply(lambda x : len(re.findall(r'http:\/\/\S+|https:\/\/\S+', x)))
    out['is_retweet'] = ira['text'].apply(lambda x : bool(re.search(r'^RT', x)))
    return out