# project.py


import numpy as np
import pandas as pd
import os

# If this import errors, run `pip install plotly` in your Terminal with your conda environment activated.
import plotly.express as px


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def count_monotonic(arr):
    diffs = np.diff(arr)
    return diffs[diffs < 0].size

def monotonic_violations_by_country(vacs):    
    by_country = vacs.groupby('Country_Region').agg({'Doses_admin': count_monotonic, 'People_at_least_one_dose': count_monotonic})
    return by_country.rename(columns={'Doses_admin': 'Doses_admin_monotonic', 'People_at_least_one_dose': 'People_at_least_one_dose_monotonic'})


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def robust_totals(vacs):
    percentiled = vacs.groupby('Country_Region').agg({'Doses_admin': lambda x : np.percentile(x, 97), \
'People_at_least_one_dose': lambda x : np.percentile(x, 97)})
    return percentiled


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def fix_dtypes(pops_raw):
    ...


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def missing_in_pops(tots, pops):
    ...

    
def fix_names(pops):
    ...


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def draw_choropleth(tots, pops_fixed):
    ...


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def clean_israel_data(df):
    copy = df.copy()
    copy['Age'] = df['Age'].replace('-', np.NaN).astype(float)
    copy['Vaccinated'] = df['Vaccinated'].astype(bool)
    copy['Severe Sickness'] = df['Severe Sickness'].astype(bool)
    return copy


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def mcar_permutation_tests(df, n_permutations=100):
    ...
    
    
def missingness_type():
    ...


# ---------------------------------------------------------------------
# QUESTION 8
# ---------------------------------------------------------------------


def effectiveness(df):
    by_vaccinated = df.groupby('Vaccinated').mean()
    pu = by_vaccinated.loc[False]['Severe Sickness']
    pv = by_vaccinated.loc[True]['Severe Sickness']
    return (pu - pv) / pu


# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------


AGE_GROUPS = [
    '12-15',
    '16-19',
    '20-29',
    '30-39',
    '40-49',
    '50-59',
    '60-69',
    '70-79',
    '80-89',
    '90-'
]

def stratified_effectiveness(df):
    ...


# ---------------------------------------------------------------------
# QUESTION 10
# ---------------------------------------------------------------------
def calc_effectiveness(pu, pv):
    return (pu - pv) / pu

def effectiveness_calculator(
    *,
    young_vaccinated_prop,
    old_vaccinated_prop,
    young_risk_vaccinated,
    young_risk_unvaccinated,
    old_risk_vaccinated,
    old_risk_unvaccinated
):
    out = {}
    out['Young'] = calc_effectiveness(young_risk_unvaccinated, young_risk_vaccinated)
    out['Old'] = calc_effectiveness(old_risk_unvaccinated, old_risk_vaccinated)
    out['Overall'] = calc_effectiveness((1-young_vaccinated_prop)*young_risk_unvaccinated + (1-old_vaccinated_prop)*old_risk_unvaccinated, \
young_vaccinated_prop*young_risk_vaccinated + old_vaccinated_prop*old_risk_vaccinated)
    return out



# ---------------------------------------------------------------------
# QUESTION 11
# ---------------------------------------------------------------------


def extreme_example():
    return {'young_vaccinated_prop': 0.56, 'old_vaccinated_prop': 0.99, 'young_risk_vaccinated': 0.01, 'young_risk_unvaccinated': 0.2, \
'old_risk_vaccinated': 0.1, 'old_risk_unvaccinated': 0.59}
