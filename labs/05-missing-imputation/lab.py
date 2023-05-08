# lab.py


import os
import pandas as pd
import numpy as np
from scipy import stats


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def after_purchase():
    return ['NMAR', 'MD', 'MAR', 'NMAR', 'MAR']


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def multiple_choice():
    return ['MAR', 'MAR', 'MAR', 'NMAR', 'MCAR']


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------



def first_round():
    return [0.1743, 'NR']


def second_round():
    return [0.017, 'R', 'D']


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def verify_child(heights):
    just_x = heights.iloc[:, 2:]
    data = []
    for col in just_x:
        data.append(stats.ks_2samp(heights.loc[heights[col].isna(), 'father'], heights.loc[~heights[col].isna(), 'father']).pvalue)
    return pd.Series(data, index=just_x.columns)




# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def cond_single_imputation(new_heights):
    categorical = new_heights.assign(father=pd.qcut(new_heights['father'], 4))
    return categorical.groupby('father')['child'].transform(lambda ser: ser.fillna(ser.mean()))


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def quantitative_distribution(child, N):
    hist, bins = np.histogram(child[child.isna() == False], 10, density=True)
    hist = hist / hist.sum()
    vals = []
    for _ in range(N):
        bin_index = np.random.choice(10, p=hist)
        vals.append(np.random.uniform(bins[bin_index], bins[bin_index + 1]))
    return np.array(vals)


def impute_height_quant(child):
    n_missing = child.isna().sum()
    child.loc[child.isna()] = quantitative_distribution(child, n_missing)
    return child


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def answers():
    return ([1, 2, 2, 1], ['netflix.com', 'reddit.com'])
