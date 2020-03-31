"""
Main file to run and compile full analysis
"""

import argparse
import pandas as pd
import assessors_request as ar
import cps_request as cr
from school_class import School, get_global_stats


APP_TOKEN = 'R3vyxUCRVSSYEjvpNaip8fbu2'
LINK = 'datacatalog.cookcountyil.gov'
CPS_LINK = 'data.cityofchicago.org'
AR_REQUEST = '5pge-nu6u'
CR_PROF_REQUEST = 'kh4r-387c'
TEACHER_SALARIES_FILE = 'data/teacher_salaries_20191231.csv'

SCHOOL_DF = pd.read_pickle('data/schools.pk1')
PROP_DF = pd.read_pickle('data/assessor.pk1')
SALARY_DF = pd.read_pickle('data/salaries.pk1')

MENU = '''

********************** SCHOOL FINDER **********************

Welcome to the school finder application!

This application summarizes teacher salary and property
values within a specified distance of a selected school.

***********************************************************

To view school names and codes, open data/school_codes.csv
from a new terminal window.
'''

def retrieve_code():
    '''
    Request and validate user input for school code

    Takes no input in function call, returns school code as integer
    '''

    while True:
        code = input('\nEnter the six-digit school code of interest: ')
        if code.isdigit() and len(code) == 6:
            break
        else:
            print('\nERROR: School code must be six digits.' \
                  '\nPlease try again.\n')

    return int(code)


def select_distance():
    '''
    Request and validate user input for distance

    Takes no input in function call, returns distance as float
    '''

    while True:
        d = input('\nHow many miles around the school would you like ' \
                  'to search? ')
        try:
            return float(d)
        except ValueError:
            print('ERROR: Please enter a numerical value in miles.\n')


def retrieve_school(school_df, prop_df, salary_df):
    '''
    Create school object based on user input

    Inputs:
        school_df (pandas dataframe): processed school information from Chicago
            Data Portal request
        prop_df (pandas dataframe): processed property sales information
            from Assessor's Office request
        salary_df (pandas dataframe): processed salary information from
            Chigago Public Schools dataset

    Returns:
        school (School class object) - school object created from user input
    '''

    while True:
        code = retrieve_code()
        obs = school_df[school_df.school_id == code]
        if obs.empty:
            print('\nERROR: School code {} cannot be found.'.format(code) +
                  '\nRefer to data/school_codes.csv to view school names and ' +
                  'codes.\n')
        else:
            print('\nLooking at school: {} ({})\n'.format(
                  obs.iloc[0]['long_name'], code))
            print('\nIs this correct?')
            confirm = confirm_selection()
            if confirm == 'y':
                d = select_distance()
                school = School(obs.iloc[0], d, prop_df, salary_df)
                print('\nGenerating data for {}...'.format(school.name))
                break

    return school


def confirm_selection():
    '''
    Request and validate user input for yes/no questions

    Takes no input in function call, returns user input as lowercase (yes or no)
    '''

    while True:
        confirm = input('Please enter (Yes/No): ')
        valid = ['no', 'yes', 'y', 'n']
        if confirm.lower() in valid:
            confirm = confirm.lower()[0]
            break
        else:
            print('ERROR: {} is not a valid option. Please enter (Yes/No): ' \
                  .format(confirm))

    return confirm


def display_stats(school_df, prop_df, salary_df):
    '''
    Display menu and summary information from school object to user

    Inputs:
        school_df (pandas dataframe): processed school information from Chicago
            Data Portal request
        prop_df (pandas dataframe): processed property sales information
            from Assessor's Office request
        salary_df (pandas dataframe): processed salary information from
            Chigago Public Schools dataset

    Returns:
        nothing, prints informaiton to terminal
    '''

    prop_med, sal_med = get_global_stats(prop_df, salary_df)
    while True:
        print(MENU)
        school = retrieve_school(school_df, prop_df, salary_df)
        print('\n*****PROPERTY DATA*****')
        if school.get_property_label(prop_med):
            continue
        input('Press ENTER to continue to salary data.')
        print('\n*****SALARY DATA*****')
        school.get_salary_label(sal_med)
        input('Press ENTER to continue to property/salary ratio.')
        print('\n*****PROPERTY VALUE TO SALARY RATIO*****')
        school.get_ratio_label(prop_med, sal_med)

        print('\nWould you like to view another school or distance?')
        new = confirm_selection()
        if new == 'n':
            break


def menu_wrapper(school_df, prop_df, salary_df):
    '''
    Run application until user quits

    Inputs:
        school_df (pandas dataframe): processed school information from Chicago
            Data Portal request
        prop_df (pandas dataframe): processed property sales information
            from Assessor's Office request
        salary_df (pandas dataframe): processed salary information from
            Chigago Public Schools dataset

    Returns:
        nothing, prints informaiton to terminal
    '''

    display_stats(school_df, prop_df, salary_df)
    print('\n************* QUITTING APPLICATION *************\n')


def go():
    '''
    Run full analysis
    '''

    parser = argparse.ArgumentParser(description='School finder')
    parser.add_argument('-a',
                        default=False,
                        action='store_true',
                        help='Use archived version of files')

    args = parser.parse_args()
    if args.a:
        print('Using archived files instead of pulling data via API')
        school_df = SCHOOL_DF
        prop_df = PROP_DF
        salary_df = SALARY_DF
    else:
        prop_df = ar.get_assessor(LINK, AR_REQUEST, APP_TOKEN, 100000)
        school_df, salary_df = cr.get_teacher_data(CPS_LINK, CR_PROF_REQUEST,
                               APP_TOKEN, TEACHER_SALARIES_FILE, 1000)

    menu_wrapper(school_df, prop_df, salary_df)


if __name__ == '__main__':
    go()
