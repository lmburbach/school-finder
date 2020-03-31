'''
Get assessment data from Cook County Assessor's Office
'''

import pandas as pd
import numpy as np
import socrata_request as sr

def clean_df(df):
    '''
    Perform pandas operations to clean assessor data

    Inputs:
        df: a pandas dataframe containing assessor sales data

    Returns:
        a clean and filtered pandas dataframe
    '''

    df['sale_date'] = pd.to_datetime(df['sale_date'])
    # Some values all the way down to 0, 1, etc. Avoiding outliers.
    # Filtering to sales greater than or equal to 10000 to remove outliers
    df = df[df.sale_price >= 10000]

    # Filter out observations with NaN values in both apts and n_units
    df = df[(df['n_units'].notnull()) | (df['apts'].notnull())]

    # Clean observations with negative apts and 0 apts to be equal to 1
    df.loc[:, 'clean_apts'] = np.where(df['apts'] == 0.0, 1.0,
                                       np.abs(df['apts']))
    del df['apts']
    df.loc[:, 'apts'] = df['clean_apts']
    del df['clean_apts']

    # Keep the most recent sale for a given pin
    df = df[df['most_recent_sale'] == 1]
    # Note that to remove 30000 other duplicates, deduping to get most recent
    # sale date for any pin
    df = df.sort_values('sale_date', ascending=False) \
           .groupby('pin', sort=False) \
           .first() \
           .reset_index()

    # Filter to single family homes and condominiums
    df = df[(df['class'] == 299) | \
            ((df['class'].between(202, 210, inclusive=True)) & \
             (df['apts'] == 1))]

    return df


def get_assessor(link, request, app_token, increment):
    '''
    Get the assessor data into a clean and filtered dataframe

    Inputs:
        link: a string representing the path containing the dataset
        request: a string representing the request to pull
        app_token: a string representing the token to pull data from Socrata API
        increment: an integer specifying how to batch pull data

    Returns:
        a cleaned Pandas dataframe
    '''

    # List of columns to select
    cols = ['pin', 'class', 'town_code', 'type_resd', \
            'n_units', 'apts', 'addr', 'centroid_x', \
            'centroid_y', 'sale_price', 'tractce', \
            'sale_date', 'sale_year', 'most_recent_sale']

    # List of columns to convert to numeric
    num_cols = ['apts', 'centroid_x', 'centroid_y', 'class', 'n_units'] + \
               ['sale_price', 'town_code', 'type_resd', 'sale_year'] + \
               ['most_recent_sale']

    df = sr.get_clean_socrata_df(link, request, app_token, cols, increment,
                                 num_cols)
    df = clean_df(df)

    return df
