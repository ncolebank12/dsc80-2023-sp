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
        numerator = grades[project].fillna(0)
        denominator = grades[project + max_string].copy()
        if (project + fr_string) in grades:
            numerator += grades[project + fr_string].fillna(0)
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
    out = pd.DataFrame(index=grades.index)
    labs = get_assignment_names(grades)['lab']
    for lab in labs:
        out[lab] = ((grades[lab] / grades[lab + ' - Max Points']) * lateness_penalty(grades[lab + ' - Lateness (H:M:S)'])).fillna(0)
    return out
# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------

def calc_lab(row):
    wo_lowest = row.drop(row.idxmin())
    return wo_lowest.mean()

def lab_total(processed):
    return processed.apply(calc_lab, axis=1)


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------

def calc_disc_or_check(grades, names, category):
    sums = np.zeros(grades.shape[0])
    for x in names[category]:
        column_copy = grades[x].fillna(0)
        sums += column_copy / grades[x + ' - Max Points']
    return 0.025 * (sums / len(names[category]))


def total_points(grades):
    names = get_assignment_names(grades)
    lab_portion = 0.2 * lab_total(process_labs(grades))
    project_portion = 0.3 * projects_total(grades)
    checkpoints_portion = calc_disc_or_check(grades, names, 'checkpoint')
    discussions_portion = calc_disc_or_check(grades, names, 'disc')
    midterm_portion = 0.15 * (grades['Midterm'].fillna(0) / grades['Midterm - Max Points'])
    final_portion = 0.3 * (grades['Final'].fillna(0) / grades['Final - Max Points'])
    # print(lab_portion[0], project_portion[0], checkpoints_portion[0], discussions_portion[0], midterm_portion[0], final_portion[0])
    return lab_portion + project_portion + checkpoints_portion + discussions_portion + midterm_portion + final_portion


# ---------------------------------------------------------------------
# QUESTION 8
# ---------------------------------------------------------------------

def letter_calc(grade):
    if grade >= 0.9:
        return 'A'
    elif grade >= 0.8:
        return 'B'
    elif grade >= 0.7:
        return 'C'
    elif grade >= 0.6:
        return 'D'
    else:
        return 'F'

def final_grades(total):
    return total.apply(letter_calc)

def letter_proportions(total):
    letters = final_grades(total)
    return letters.value_counts().sort_values(ascending=False) / letters.size


# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------


def raw_redemption(final_breakdown, question_numbers):
    out = pd.DataFrame()
    out['PID'] = final_breakdown['PID']
    out['Raw Redemption Score'] = 0
    denominator = 0
    redemption_only = final_breakdown.iloc[:, question_numbers]
    for col in redemption_only:
        out['Raw Redemption Score'] += redemption_only[col].fillna(0)
        denominator += redemption_only[col].max()
    out['Raw Redemption Score'] = out['Raw Redemption Score'] / denominator
    return out 
    
def combine_grades(grades, raw_redemption_scores):
    return grades.merge(raw_redemption_scores)


# ---------------------------------------------------------------------
# QUESTION 10
# ---------------------------------------------------------------------


def z_score(ser):
    return (ser - ser.mean()) / ser.std(ddof=0)
    
def add_post_redemption(grades_combined):
    ...


# ---------------------------------------------------------------------
# QUESTION 11
# ---------------------------------------------------------------------


def total_points_post_redemption(grades_combined):
    ...
    
def proportion_improved(grades_combined):
    ...
