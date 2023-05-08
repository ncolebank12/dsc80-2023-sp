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
    copy = pops_raw.copy()
    copy['World Percentage'] = pd.to_numeric(copy['World Percentage'].str.replace('%', '')) / 100
    copy['Population in 2023'] = (copy['Population in 2023'] * 1000).astype(int)
    copy['Area (Km²)'] = pd.to_numeric(copy['Area (Km²)'].str.replace(' Km²', '').str.replace('_','').str.replace(',',''))
    copy['Density (P/Km²)'] = pd.to_numeric(copy['Density (P/Km²)'].str.replace('/Km²', ''))

    return copy


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def missing_in_pops(tots, pops):
    return set(tots.index) - set(pops['Country (or dependency)'])

    
def fix_names(pops):
    copy = pops.copy()
    copy['Country (or dependency)'] = copy['Country (or dependency)'].replace({'Cape Verde': 'Cabo Verde', 'Myanmar': 'Burma', \
'Republic of the Congo': 'Congo (Brazzaville)', 'DR Congo': 'Congo (Kinshasa)', 'South Korea': 'Korea, South', 'United States': 'US', \
'Ivory Coast': "Cote d'Ivoire", 'Czech Republic': 'Czechia', 'Palestine': 'West Bank and Gaza'})
    return copy


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def draw_choropleth(tots, pops_fixed):
    merged = tots.merge(pops_fixed, left_index=True, right_on='Country (or dependency)')
    merged['dpp'] = merged['Doses_admin'] / merged['Population in 2023']
    fig = px.choropleth(merged, locations="ISO", hover_name='Country (or dependency)', color="dpp", labels={'dpp': 'Doses Per Person'}, \
color_continuous_scale=px.colors.sequential.Blues, title='COVID Vaccine Doses Per Person by Country, As of January 20th, 2023')
    return fig


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

def abs_diff(grouped, col):
    return abs(grouped.loc[False, col] - grouped.loc[True, col])


def mcar_permutation_tests(df, n_permutations=100):
    w_null_age = df.assign(null_age=df['Age'].isna())
    stats_1 = []
    stats_2 = []
    for _  in range(n_permutations):
        shuffled = w_null_age.assign(null_age=np.random.permutation(w_null_age['null_age']))
        by_age = shuffled.groupby('null_age').mean()
        stats_1.append(abs_diff(by_age, 'Vaccinated'))
        stats_2.append(abs_diff(by_age, 'Severe Sickness'))
    return (np.asarray(stats_1), np.asarray(stats_2))

    
    
def missingness_type():
    return 1


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

def determine_group(age):
    if age <= 15:
        return '12-15'
    elif age <= 19:
        return '16-19'
    elif age <= 29:
        return '20-29'
    elif age <= 39:
        return '30-39'
    elif age <= 49:
        return '40-49'
    elif age <= 59:
        return '50-59'
    elif age <= 69:
        return '60-69'
    elif age <= 79:
        return '70-79'
    elif age <= 89:
        return '80-89'
    else:
        return '90-'
    

def stratified_effectiveness(df):
    with_groups = df.assign(Group=df['Age'].apply(determine_group))
    out = with_groups.groupby('Group').apply(effectiveness)
    return out


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
