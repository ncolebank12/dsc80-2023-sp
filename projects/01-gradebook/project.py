# project.py


import pandas as pd
import numpy as np
import os

late_threshold = 10

# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def get_assignment_names(grades):
    names=  { 'lab': [], 'project': [], 'midterm': [], 'final': [], 'disc': [], 'checkpoint': [] }
    disc_num_length = 12
    num_index = -2
    checkpoint_full_len = 22
    checkpoint_len = -12
    for header in grades:
        if len(header) > 1:
            without_num = header[:num_index]
            num = header[num_index:]
            if without_num in names: #for lab and project
                names[without_num].append(header)
            elif header.lower() in names: #for midterm and final
                names[header.lower()].append(header)
            elif header.find('discussion') != -1 and len(header) == disc_num_length:
                names['disc'].append(header)
            elif len(header) == checkpoint_full_len and header[0:len('project')] == 'project' and header[checkpoint_len:] == 'checkpoint' + num:
                names['checkpoint'].append(header)
    return names


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def projects_total(grades):
    names = get_assignment_names(grades)
    projects = names['project']
    project_grades = np.zeros(grades.shape[0])
    max_string =  ' - Max Points'
    fr_string = '_free_response'
    for project in projects:
        numerator = np.nan_to_num(grades[project])
        denominator = grades[project + max_string]
        if project + fr_string in grades:
            numerator += np.nan_to_num(grades[project + fr_string])
            denominator += grades[project + fr_string + max_string]
        project_grades += numerator/denominator
    project_grades = project_grades/len(projects)
    return pd.Series(data=project_grades)



# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def hms_to_hours(time_string):
    times = time_string.split(':')
    hours = float(times[2])/60/60
    hours += float(times[1])/60
    hours += float(times[0])
    return hours

def last_minute_submissions(grades):    
    counts = {}
    for lab in get_assignment_names(grades)['lab']:
        times =grades[lab + ' - Lateness (H:M:S)'].apply(hms_to_hours)
        times = times[times != 0]
        times = times[times < late_threshold]
        counts[lab] = times.size
    return pd.Series(counts)



# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------

def determimne_lateness(time):
    wk_in_hours = 168
    if time <= late_threshold:
        return 1
    elif time <= wk_in_hours:
        return 0.9
    elif time <= 2*wk_in_hours:
        return 0.7
    else:
        return 0.4

def lateness_penalty(col):
    in_hours = col.apply(hms_to_hours)
    return in_hours.apply(determimne_lateness)




# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def process_labs(grades):
    ...


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def lab_total(processed):
    ...


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def total_points(grades):
    ...


# ---------------------------------------------------------------------
# QUESTION 8
# ---------------------------------------------------------------------


def final_grades(total):
    ...

def letter_proportions(total):
    ...


# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------


def raw_redemption(final_breakdown, question_numbers):
    ...
    
def combine_grades(grades, raw_redemption_scores):
    ...


# ---------------------------------------------------------------------
# QUESTION 10
# ---------------------------------------------------------------------


def z_score(ser):
    ...
    
def add_post_redemption(grades_combined):
    ...


# ---------------------------------------------------------------------
# QUESTION 11
# ---------------------------------------------------------------------


def total_points_post_redemption(grades_combined):
    ...
    
def proportion_improved(grades_combined):
    ...
