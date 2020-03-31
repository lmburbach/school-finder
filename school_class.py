"""
Create school class
"""

from math import radians, cos


class School():
    '''
    Class for representing a School object
    '''

    def __init__(self, obs, d, prop_df, salary_df):
        '''
        Create instance of the school class

        Input:
            obs (pandas series): one row of data from the school dataframe
            d (float or int): distance used to create bounding square
            prop_df (pandas dataframe): processed property sales information
                from Assessor's Office request
            salary_df (pandas dataframe): processed salary information from
                Chigago Public Schools dataset
            prop_med (int): median sale price of all properties in prop_df
            sal_med (int): median teacher salary of all teachers in salary_df
        '''

        self.id = obs.school_id
        self.name = obs.long_name
        self.network = obs.network
        self.longitude = obs.school_longitude
        self.latitude = obs.school_latitude
        self.d = d

        self.prop_stats = self.get_property_stats(prop_df)
        self.salary_stats = self.get_salary_stats(salary_df)

    def filter_by_distance(self, prop_df):
        '''
        Filter prop_df to propeties within a bounding square of length 2d
            centered at the school

        Inputs:
            prop_df (pandas dataframe): processed property sales information
                from Assessor's Office request
            d (float or int): distance used to create bounding square
        Returns:
            filtered_df (panda dataframe): datframe of properties within the
                bounning square
        '''

        # One degree of lattitude corresponds to approximately 70 miles
        vertical = self.d / 70

        # One degree of longitude varies in miles by latitidue, corresponding
        # to cosine of the latitude * 69.172, 69.172 representing the number of
        #miles corresponding to one degree of longitude at the equator
        lat_radians = radians(self.latitude)
        horizontal = self.d / (cos(lat_radians) * 69.172)

        max_lat = self.latitude + vertical
        min_lat = self.latitude - vertical
        max_lon = self.longitude + horizontal
        min_lon = self.longitude- horizontal

        filtered_df = prop_df[(prop_df['centroid_x'] >= min_lon) & \
                              (prop_df['centroid_x'] <= max_lon) & \
                              (prop_df['centroid_y'] >= min_lat) & \
                              (prop_df['centroid_y'] <= max_lat)]

        return filtered_df

    def get_property_stats(self, prop_df):
        '''
        Generate descriptive summary statistics for proeprties within d miles of
            the school

        Input:
            prop_df (pandas dataframe): processed property sales information
                from Assessor's Office request

        Output:
            sumary (pandas series): summary statistics for properties within
                d miles of the school
        '''

        filtered_df = self.filter_by_distance(prop_df)
        summary = filtered_df['sale_price'].describe()
        if filtered_df.empty:
            return 'No property data available within {} miles of {}'.format(
                self.d, self.name)

        return summary.astype(int)

    def get_salary_stats(self, salary_df):
        '''
        Generate descriptive summary statistics for teacher salaries at school

        Input:
            salary_df (pandas dataframe): processed salary information
                from Chicago Public School's dataset

        Output:
            sumary (pandas series): summary statistics for salaries at school
        '''

        filtered_df = salary_df[salary_df['school_id'] == self.id]
        if filtered_df.empty:
            return 'Salary data is not available for school: ' + self.name
        summary = filtered_df['annual_salary'].describe()

        return summary.astype(int)

    def get_property_label(self, prop_med):
        '''
        Create verbose description of property data to be returned in the
            application terminal

        Input:
            prop_med (int): median sale price for all properties in dataset

        Output:
            No output; prints string to terminal when called
        '''

        if isinstance(self.prop_stats, str):
            print('No property data available within {} miles of {}.\nPlease ' \
                  'start again using a larger distance.'.format(
                    self.d, self.name))
            return True

        else:
            diff = self.prop_stats['50%'] - prop_med
            if diff < 0:
                comp = 'lower'
            else:
                comp = 'higher'

            mean = 'The median sale price for properties within {} miles of ' \
                    '{} is ${}, which is ${} {} than the median for all ' \
                    'Cook County properties, ${}.'.format(self.d, self.name,
                     self.prop_stats['50%'], int(abs(diff)), comp, prop_med)

            more_stats = '\n\nMore property value statistics within {} ' \
                         'miles of {}:'.format(self.d, self.name)

            for measure, stat in self.prop_stats.items():
                if measure != 'count':
                    more_stats = more_stats + '\n\t{}: ${}'.format(
                        measure.title(), stat)

            count = '\n\n\t(Data from {} properties)'.format(
                self.prop_stats['count'])

            print(mean + more_stats + count + '\n')

    def get_salary_label(self, sal_med):
        '''
        Create verbose description of salary data to be returned in the
            application terminal

        Input:
            sal_med (int): median anid
            nual salary for all teachers in dataset

        Output:
            No output; prints string to terminal when called
        '''

        if isinstance(self.salary_stats, str):
            print('No salary data available for {}.'.format(self.name))
            print('Certain schools, like charter schools, ' \
                  'do not report salary information.')

        else:
            diff = self.salary_stats['50%'] - sal_med
            if diff < 0:
                comp = 'lower'
            else:
                comp = 'higher'

            mean = 'The median teacher salary at {} is ${}, which is ${} {} ' \
                        'than the median for all CPS teachers, ${}.'.format(
                            self.name, self.salary_stats['50%'],
                            int(abs(diff)), comp, sal_med)

            more_stats = '\n\nMore salary statistics for {}:'.format(self.name)

            for measure, stat in self.salary_stats.items():
                if measure != 'count':
                    more_stats = more_stats + '\n\t{}: ${}'.format(
                        measure.title(), stat)

            count = '\n\n\t(Data from {} teachers)'.format(
                self.salary_stats['count'])

            print(mean + more_stats + count + '\n')

    def get_ratio_label(self, prop_med, sal_med):
        '''
        Caculate ratio of home price to salary and create verbose description of
            salary data to be returned in the application terminal

        Input:
            prop_med (int): median sale price for all properties in dataset
            sal_med (int): median annual salary for all teachers in dataset

        Output:
            No output; prints string to terminal when called
        '''

        if isinstance(self.prop_stats, str) or \
           isinstance(self.salary_stats, str):
            print('Both property data and salary data are needed to ' \
                  ' calculate this ratio.'.format(self.name))

        else:
            ratio = round(self.prop_stats['50%'] / self.salary_stats['50%'], 2)
            global_ratio = round(prop_med / sal_med, 2)

            if ratio < 2:
                rec = 'lower than'
            elif ratio > 2.5:
                rec = 'higher than'
            else:
                rec = 'within'

            diff = round((ratio - global_ratio) / global_ratio, 2)
            if diff < 0:
                comp = 'lower'
            else:
                comp = 'higher'

            print('The ratio of median property value to median teacher ' \
                  'salary within {} miles of {} is {}. This ratio is {} the ' \
                  'recommended range of 2.0-2.5.\n\nThis ratio is {}% {} ' \
                  'than the ratio of the median sale price of all Cook  ' \
                  'County properties to the median salary of all Chicago ' \
                  'Public Schools teachers, which is {}.'.format(self.d,
                   self.name, ratio, rec, diff, comp, global_ratio))

    def __repr__(self):
        '''
        Simple string representaiton of school object
        '''
        return '{} ({}) located at ({}, {})'.format(
            self.name, self.id, self.latitude, self.longitude)


def get_global_stats(prop_df, salary_df):
    '''
    Generate median sale price for all properties in the processed property
        dataset and the median annual salary for all teachers in the processed
        salary dataset

    Inputs:
        prop_df (pandas dataframe): processed property sales information
            from Assessor's Office request
        salary_df (pandas dataframe): processed salary information from
            CPS dataset

    Returns:
        a tuple: median sale price, median annual salary, both as integers
            for readability
    '''

    prop_med = prop_df['sale_price'].median()
    sal_med = salary_df['annual_salary'].median()

    return int(prop_med), int(sal_med)
