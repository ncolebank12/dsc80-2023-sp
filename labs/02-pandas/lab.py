# lab.py


import pandas as pd
import numpy as np
import os


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def data_load(scores_fp):
    df = pd.read_csv(scores_fp, usecols=['name','tries','highest_score','sex'])
    df = df.drop(columns=['sex'])
    df = df.rename(columns={'name': 'firstname', 'tries': 'attempts'})
    df = df.set_index('firstname')
    return df

def calc_pass(attempts, highest_score):
    if attempts > 1 and highest_score < 60:
        return 'No'
    elif attempts > 4 and highest_score < 70:
        return 'No'
    elif attempts > 6 and highest_score < 90:
        return 'No'
    elif attempts > 8:
        return 'No'
    else:
        return 'Yes'

def pass_fail(scores):
    with_pass = scores.assign(**{'pass': scores.apply(lambda x: calc_pass(x['attempts'], x['highest_score']), axis=1)})
    return with_pass

# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def med_score(scores): ##TODO - Account for if there are no yes - see ed.
    return scores[scores['pass'] == 'Yes']['highest_score'].median()

def highest_score_name(scores):
    max_score = scores['highest_score'].max()
    students = scores[scores['highest_score'] == max_score].index.values
    return max_score, list(students)

# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def idx_dup():
    return 6


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def trick_me():
    data = [['tom', 'f', '2'],['tommy', 'g', '14'],['tomald', 't', '2'],['tomathan', 'y', '20'],['tomulus', 'a', '80']]
    tricky_1 = pd.DataFrame(columns=['Name','Name','Age'], data = data)
    tricky_1.to_csv('data/tricky_1.csv', index=False)
    tricky_2  = pd.read_csv('data/tricky_1.csv')
    return 3


def trick_bool():
    return [4,12, 13]


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def change(x):
    if pd.isnull(x):
        return 'MISSING'
    else:
        return x
    
def correct_replacement(df_with_nans):
    return df_with_nans.applymap(change)
    
def missing_ser():
    return 2
    
def fill_ser(df_with_nans):
    for col in df_with_nans:
        current_col = df_with_nans[col]
        current_col[current_col.isna()] = 'MISSING'
        df_with_nans[col] = current_col


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def population_stats(df):
    output = pd.DataFrame(columns=['num_nonnull','prop_nonnull','num_distinct','prop_distinct'])
    for col in df:
        as_ser = df[col]
        nonnull = as_ser[as_ser.isna() == False]
        output.loc[col] = [nonnull.size, nonnull.size / as_ser.size, nonnull.nunique(), nonnull.nunique() / nonnull.size]
    return output


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def most_common(df, N=10):
    out = pd.DataFrame(index = np.arange(N))
    for col in df:
        val_counts = df[col].value_counts()
        top_n = val_counts
        if val_counts.size > N:
            top_n = val_counts[:N]
        print(top_n)
        out[col + '_values'] = pd.Series(top_n.index)
        top_n.index = np.arange(top_n.size)
        out[col + '_counts'] = top_n
    return out


# ---------------------------------------------------------------------
# QUESTION 8
# ---------------------------------------------------------------------


def super_hero_powers(powers):
    indexed = powers.set_index('hero_names')
    sums = indexed.sum(axis=1)
    can_fly = indexed[indexed['Flight'] == True].drop(columns=['Flight'])
    can_fly_sums = can_fly.sum()
    only_one = indexed[sums == 1]
    only_one_sums = only_one.sum()
    return [sums.idxmax(), can_fly_sums.idxmax(), only_one_sums.idxmax()]
    


# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------

def clean_heroes(heroes):
    return heroes.replace(['-', -99],np.nan)


# ---------------------------------------------------------------------
# QUESTION 10
# ---------------------------------------------------------------------


def super_hero_stats():
    return ['Onslaught', 'George Lucas', 'bad', 'Marvel Comics', 'NBC - Heroes', 'Groot']
