# lab.py


import pandas as pd
import numpy as np
import io
import os


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def prime_time_logins(login):
    out = login.copy()
    out['Time'] = pd.to_datetime(out['Time']).dt.hour
    out['Time'] = (out['Time'] >= 16) & (out['Time'] < 20)
    return out.groupby('Login Id').sum()




# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------

def get_days_active(times):
    times = pd.to_datetime(times).sort_values()
    first_login = times.iloc[0]
    today = pd.Timestamp(year=2023,month=1,day=31)
    return (today - first_login).days + 1    

def count_frequency(login):

    by_id = login.groupby('Login Id').agg(['count',get_days_active])
    return by_id['Time', 'count'] / by_id['Time', 'get_days_active']


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def most_expensive_per_customer(customers, products):
    merged = customers.merge(products, how='cross')
    merged = merged[merged['Balance'] >= merged['Price']]
    merged = merged.sort_values(['Price']).groupby('Name').tail(1).reset_index()
    merged = merged[['Name', 'Email', 'Model', 'Price']]
    return merged


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def suits_null_hyp():
    return [1,2]

def simulate_suits_null():
    # 0 is defeective, 1 is non-defective
    return np.random.choice([0,1], 250, replace=True, p=[0.02,0.98])

def estimate_suits_p_val(N):
    count = 0
    for i in np.arange(N):
        res = 250 - simulate_suits_null().sum()
        if res >= 10:
            count += 1
    return count / N



# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def car_null_hypoth():
    return [1, 4]

def car_alt_hypoth():
    return [2, 6]

def car_test_stat():
    return [1, 4]

def car_p_value():
    return 5


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def bhbe_col(heroes):
    return (heroes['Hair color'].str.lower() == 'blond') & (heroes['Eye color'].str.lower() == 'blue')

def superheroes_observed_stat(heroes):
    bhbe = heroes[bhbe_col(heroes)]
    non_bhbe = heroes[~bhbe_col(heroes)]
    return (bhbe['Alignment'].str.lower() == 'good').mean() - (non_bhbe['Alignment'.str.lower() == 'good']).mean()

def simulate_bhbe_null(n):
    ...

def superheroes_calc_pval():
    ...


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def diff_of_means(data, col='orange'):
    ...


def simulate_null(data, col='orange'):
    ...


def pval_color(data, col='orange'):
    ...


# ---------------------------------------------------------------------
# QUESTION 8
# ---------------------------------------------------------------------


def ordered_colors():
    ...


# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------



def same_color_distribution():
    ...


# ---------------------------------------------------------------------
# QUESTION 10
# ---------------------------------------------------------------------


def perm_vs_hyp():
    ...
