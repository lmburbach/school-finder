'''
Get and clean a Socrata request dataframe
'''

import pandas as pd
from sodapy import Socrata

def get_socrata_df(link, request, app_token, cols, increment):
    '''
    Return a Pandas dataframe from Socrata request

    Inputs:
        link: a string representing the path containing the dataset
        request: a string representing the request to pull
        app_token: a string representing the token to pull data from Socrata API
        cols: a list of column names
        increment: an integer specifying how to batch pull data

    Returns:
        a Pandas dataframe
    '''

    client = Socrata(link, app_token)

    off = 0
    results_list = []
    cols_str = ', '.join(cols)

    while True:
        result = client.get(request,
                            select=cols_str,
                            limit=increment,
                            offset=off)

        if not result:
            break

        results_list.extend(result)
        off += increment

    return pd.DataFrame.from_records(results_list)


def convert_cols_to_num(df, num_cols):
    '''
    Convert list of columns to numeric in a Pandas dataframe

    Inputs:
        df: a pandas dataframe
        num_cols: a list of columns to convert to numeric

    Returns:
        a Pandas dataframe with selected columns converted to numeric
    '''

    df[num_cols] = df[num_cols].apply(pd.to_numeric)
    return df


def get_clean_socrata_df(link, request, app_token, cols, increment, num_cols):
    '''
    Return a Pandas dataframe from Socrata request and converts designated
    columns to numeric

    Inputs:
        link: a string representing the path containing the dataset
        request: a string representing the request to pull
        app_token: a string representing the token to pull data from Socrata API
        cols: a list of column names
        increment: an integer specifying how to batch pull data
        num_cols: a list of columns to convert to numeric
    '''

    df = get_socrata_df(link, request, app_token, cols, increment)
    return convert_cols_to_num(df, num_cols)
