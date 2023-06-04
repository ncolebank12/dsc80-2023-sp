# lab.py


import pandas as pd
import numpy as np
import plotly.express as px
import statsmodels.api as sm
import os
import itertools
from sklearn.preprocessing import Binarizer, QuantileTransformer, FunctionTransformer

import warnings
warnings.filterwarnings('ignore')


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def best_transformation():
    return 4


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------

def determine_ordinal(val, order):
    return order.index(val)

def create_ordinal(df):
    out = pd.DataFrame(index = df.index)
    out['ordinal_cut'] = df['cut'].apply(lambda x : determine_ordinal(x, ['Fair', 'Good', 'Very Good', 'Premium', 'Ideal']))
    out['ordinal_color'] = df['color'].apply(lambda x : determine_ordinal(x, ['J', 'I', 'H', 'G', 'F', 'E', 'D']))
    out['ordinal_clarity'] = df['clarity'].apply(lambda x : determine_ordinal(x, ['I1', 'SI2', 'SI1', 'VS2', 'VS1', 'VVS2', 'VVS1', 'IF']))
    return out


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def create_one_hot_col(df, col):
    out = pd.DataFrame(index=df.index)
    vals = df[col].unique()
    for val in vals:
        out['one_hot_' + col + '_' + val] = (df[col] == val).astype(int)
    return out

def create_one_hot(df):
    out = create_one_hot_col(df, 'cut')
    return pd.concat([out, create_one_hot_col(df, 'color'), create_one_hot_col(df, 'clarity')], axis=1)


def create_proportions_col(df, col):
    proportions = df[col].value_counts() / len(df)
    return df[col].map(proportions)

def create_proportions(df):
    out = pd.DataFrame(index=df.index)
    out['proportion_cut'] = create_proportions_col(df, 'cut')
    out['proportion_color'] = create_proportions_col(df, 'color')
    out['proportion_clarity'] = create_proportions_col(df, 'clarity')
    return out



# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def create_quadratics(df):
    out = pd.DataFrame(index=df.index)
    numeric_columns = df.select_dtypes(include=np.number).drop(columns=['price'])
    combinations = itertools.combinations(numeric_columns.columns, 2)
    for combination in combinations:
        out[combination[0] + ' * ' + combination[1]] = df[combination[0]] * df[combination[1]]
    return out


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------



def comparing_performance():
    # create a model per variable => (variable, R^2, RMSE) table
    return [0.8493305264355833, 1548.5331930613177, 'x', 'carat * x', 'ordinal_color', 1434.8400089047332]


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


class TransformDiamonds(object):
    
    def __init__(self, diamonds):
        self.data = diamonds
        
    # Question 6.1
    def transform_carat(self, data):
        bi = Binarizer(threshold=1)
        return bi.transform(data[['carat']])
    
    # Question 6.2
    def transform_to_quantile(self, data):
        quantile = QuantileTransformer(n_quantiles=100)
        fitted = quantile.fit(self.data[['carat']])
        return fitted.transform(data[['carat']])
    
    def calc_depth_pct(self, data):
        return 100 * ((2 * data['z']) / (data['x'] + data['y']))
    
    # Question 6.3
    def transform_to_depth_pct(self, data):
        f = FunctionTransformer(self.calc_depth_pct)
        return f.transform(data[['x', 'y', 'z']])