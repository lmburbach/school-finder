'''
Get teacher salary and school data from Chicago Public Schools
'''
import csv
import pandas as pd
from socrata_request import get_clean_socrata_df, convert_cols_to_num

def get_clean_teacher_salary_data(file_name):
    '''
    Return a clean data frame with Chicago public teacher salary data

    Inputs:
        file_name: a string representing the path containing the CSV file

    Outputs:
        A cleaned pandas dataframe
    '''
    col_names = ['pos_num', 'dept_id', 'department', 'fte', 'clsindc',
                 'annual_salary', 'fte_annual_salary',
                 'annual_benefit_cost', 'job_code', 'job_title', 'name']

    cols_to_use = ['dept_id', 'department', 'fte', 'annual_salary',
                   'annual_benefit_cost', 'job_title']

    num_cols = ['fte', 'annual_salary', 'annual_benefit_cost']

    salaries = pd.read_csv(file_name, names=col_names,
                           usecols=cols_to_use, skiprows=[0])

    salaries = convert_cols_to_num(salaries, num_cols)

    salaries = salaries[salaries['fte'] == 1]

    incl_job_filt = salaries['job_title'].str.contains('Teacher')

    excl_job_filt = ~salaries['job_title'].str.contains(('Assistant|Asst|'
                                                         'Specialist|'
                                                         'Analyst|Recruitment|'
                                                         'Part-Time'))

    return salaries[incl_job_filt & excl_job_filt]


def write_to_csv(df, csv_name):
    '''
    Create CSV from columns of pandas df

    Inputs:
        df: A pandas df
        csv_name: the name for the CSV

    Outputs:
        A CSV file
    '''
    with open(csv_name, 'w') as f:
        writer = csv.writer(f, delimiter=',')

        writer.writerow(['School Name', 'School Code', 'School Network'])
        for i, row in df.iterrows():
            writer.writerow((row['long_name'], row['school_id'],
                             row['network']))

    return csv_name


def get_teacher_data(link, prof_request, app_token, salary_file_name,
                     increment):
    '''
    Return a cleaned dataframe with teacher salaries, school_ids,
        and school locations

    Inputs:
        link: a string representing the path containing the CSV file
        prof_request: a string representing the request to pull for
            the school profile data
        app_token: a string representing the token to pull data from Socrata
            API
        salary_file_name: a string representing the location of the teacher
            salary flat file
        increment: an integer specifying how to batch pull data

    Outputs:
        A cleaned pandas dataframe
    '''
    school_cols = ['school_id', 'finance_id', 'short_name', 'long_name',
                   'school_latitude', 'school_longitude', 'network']
    school_num_cols = ['finance_id', 'school_id', 'school_latitude',
                       'school_longitude']

    salaries = get_clean_teacher_salary_data(salary_file_name)

    school_info = get_clean_socrata_df(link, prof_request, app_token,
                                       school_cols, increment, school_num_cols)

    # Drops 633 observations - any teacher not assigned
    # to a particular school
    salaries = salaries.merge(school_info, left_on='dept_id',
                              right_on='finance_id')

    write_to_csv(school_info, 'data/school_codes.csv')

    return school_info, salaries
