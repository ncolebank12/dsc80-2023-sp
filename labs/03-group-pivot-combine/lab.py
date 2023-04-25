# lab.py


import os
import io
import pandas as pd
import numpy as np


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def clean_universities(df):
    copy = df.copy()
    copy['institution'] = copy['institution'].replace('\n',', ')
    copy['broad_impact'] = copy['broad_impact'].astype(int)
    copy[['nation','national_rank_cleaned']] = copy['national_rank'].str.split(', ', expand=True)
    copy['national_rank_cleaned'] = copy['national_rank_cleaned'].astype(int)
    copy = copy.drop(columns=['national_rank'])
    to_replace  ={'Czechia': 'Czech Republic', 'UK': 'United Kingdom', 'USA': 'United States'}
    copy['nation'] = copy['nation'].replace(to_replace)
    copy['is_r1_public'] = ~copy['city'].isna() & ~copy['state'].isna() & (copy['control'] == 'Public')
    return copy


def university_info(cleaned):
    by_state = cleaned.groupby('state').aggregate({'institution': 'count', 'score': 'mean'})
    three_or_more = by_state[by_state['institution'] >= 3]
    lowest_mean = three_or_more['score'].idxmin()

    top_100 = cleaned[cleaned['world_rank'] <= 100]
    faculty_in_top = top_100['quality_of_faculty'] <= 100

    proportion_private = 1 - cleaned.groupby('state')['is_r1_public'].mean()
    num_states = proportion_private[proportion_private >= 0.5].size

    national_1s = cleaned[cleaned['national_rank_cleaned'] == 1]
    lowest = national_1s[national_1s['world_rank'] == national_1s['world_rank'].max()].iloc[0]
    return [lowest_mean, faculty_in_top.mean(), num_states, lowest['institution']]



# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def std_scores_by_nation(cleaned):
    subset = cleaned[['institution', 'nation','score']].copy()
    subset['score'] = subset.groupby('nation')['score'].transform(lambda x: (x - x.mean()) / x.std(ddof=0))
    return subset
    

def su_and_spread():
    return [2, 'United States']


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def read_linkedin_survey(dirname):
    files = os.listdir(dirname)
    out = pd.DataFrame(columns=['first name', 'last name', 'current company', 'job title', 'email', 'university'])
    for fn in files:
        if fn.startswith('survey') == False:
            continue
        path = os.path.join(dirname, fn)
        curr_survey = pd.read_csv(path)
        curr_survey.columns = curr_survey.columns.str.lower().str.replace('_', ' ')
        out = pd.concat([out, curr_survey], ignore_index=True)
    return out

def com_stats(df):
    proportion = df[df['university'].str.contains('Ohio') & df['job title'].str.contains('Nurse')].shape[0] / df.shape[0]
    engineer_titles_count = df[df['job title'].str.endswith('Engineer').fillna(False)]['job title'].nunique()
    longest_idx = df['job title'].str.len().idxmax()
    manager_count = df[df['job title'].str.lower().str.contains('manager').fillna(False)].shape[0]
    return [proportion, engineer_titles_count, df['job title'].loc[longest_idx], manager_count]



# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def read_student_surveys(dirname):
    files = os.listdir(dirname)
    first_path = os.path.join(dirname, 'favorite1.csv')
    out = pd.read_csv(first_path)
    
    for fn in files:
        if fn.startswith('favorite') == False:
            continue
        if fn == 'favorite1':
            continue
        curr_favorite = pd.read_csv(os.path.join(dirname, fn))
        out = out.merge(curr_favorite)
    out = out.set_index('id')
    return out


def check_credit(df):
    out = pd.DataFrame(index=df.index)
    class_ec = 0
    out['name'] = df['name']
    wo_names = df.drop(columns=['name'])
    class_proportions = wo_names.count() / wo_names.shape[0]
    class_ec = min(class_proportions[class_proportions >= 0.8].size,2)
    student_proportions = wo_names.count(axis=1) / wo_names.shape[1]
    out['ec'] = class_ec + np.where(student_proportions >= 0.5, 5, 0)
    return out


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def most_popular_procedure(pets, procedure_history):
    merged = procedure_history.merge(pets)
    return merged['ProcedureType'].mode().iloc[0]

def pet_name_by_owner(owners, pets):
    merged = owners.merge(pets, left_on='OwnerID', right_on='OwnerID')
    merged = merged.groupby('OwnerID').agg({'Name_y': lambda x : x.iloc[0] if x.size == 1 else x.tolist(), 'Name_x': 'first'})
    merged = merged.set_index('Name_x')
    return merged['Name_y']



def total_cost_per_city(owners, pets, procedure_history, procedure_detail):
    with_pets = owners.merge(pets, left_on='OwnerID', right_on='OwnerID')
    with_procedures = procedure_history.merge(with_pets, left_on='PetID', right_on='PetID')
    with_prices = with_procedures.merge(procedure_detail, left_on=['ProcedureSubCode', 'ProcedureType'], right_on=['ProcedureSubCode', 'ProcedureType'])
    by_city = with_prices.groupby('City')['Price'].sum()
    return by_city


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def average_seller(sales):
    by_name =  sales.groupby('Name').mean()
    return by_name.rename(columns={'Total': 'Average Sales'})

def product_name(sales):
    pivoted = sales.pivot_table(index='Name', columns='Product', values='Total', aggfunc='sum')
    return pivoted

def count_product(sales):
    pivoted = sales.pivot_table(index=['Product', 'Name'], columns='Date', values='Total', aggfunc='count').fillna(0)
    return pivoted


def total_by_month(sales):
    with_month = sales.assign(Month= pd.to_datetime(sales['Date']).apply(lambda x : x.strftime('%B')))
    pivoted = with_month.pivot_table(index=['Name', 'Product'], columns='Month', values='Total', aggfunc='sum').fillna(0)
    return pivoted
