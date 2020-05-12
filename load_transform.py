import pandas as pd
import seaborn as sns

from datetime import datetime, timedelta

def load_week_n_sell_data(week, connection):
    """Load the sell data for a given week
    
    Args:
        week (int): week number
        connection (sqlalchemy connection): MySQL database connection  
    
    Returns:
        week_n_sell_data (dataframe): 
            turnip selling data for a given week
    """
    
    first_week = datetime.strptime('2020-04-12', '%Y-%m-%d')
    week_lower_bound = first_week + timedelta(days=(7 * (week - 1)))
    week_lower_bound = datetime.strftime(week_lower_bound, '%Y-%m-%d')
    week_upper_bound = first_week + timedelta(days=(7 * week))
    week_upper_bound = datetime.strftime(week_upper_bound, '%Y-%m-%d')
    
    query = '''
        SELECT 
            *
        FROM 
            turnip.sell_data
        WHERE
            datetime_observed >= %(lower_bound)s AND
            datetime_observed < %(upper_bound)s;
    '''
    parameters = {
        'lower_bound': week_lower_bound,
        'upper_bound': week_upper_bound
    }
    week_n_sell_data = pd.read_sql(query, connection, params=parameters)
    
    return week_n_sell_data

def drop_incomplete_sell_data(data):
    """Drop data with any missing selling prices within the week
    
    Args:
        data (dataframe): 
            contains turnip selling prices loaded into 
            a dataframe using get_week_n_sell_data
    
    Returns:
        data (dataframe):
            contains turnip selling prices for the entire week
    """
    
    pivot_table = pd.pivot_table(
        data=data, 
        values='price', 
        index=['user_id', 'island_id'], 
        columns=['datetime_observed']
    )
    pivot_table.dropna(inplace=True)

    data = pivot_table.reset_index()
    data = data.melt(
        id_vars=['user_id', 'island_id'], 
        value_name='price'
    )
    return data

def date_to_weekday_am_pm(date):
    """Convert date to weekday followed by AM or PM
    
    Args:
        date (datetime): date when a given turnip price was observed
        
    Returns:
        weekday_am_pm (str): weekday AM/PM e.g. 'Monday AM'
    """
    
    weekday = date.strftime('%A')
    time_of_day = date.strftime('%p')
    
    weekday_am_pm = weekday + ' ' + time_of_day
    return weekday_am_pm

def datetime_to_weekday(data):
    """Use the column datetime_observed and function date_to_weekday_am_pm 
    to create the column weekday_observed
    
    Args:
        data (datetime): 
            contains turnip selling prices loaded into a dataframe using 
            get_week_n_sell_data
        
    Returns:
        data (dataframe): 
            contains the original data in addition to a column indicating 
            the weekday and time of day (AM/PM) for each price observation 
    """
    
    weekday_observed = data['datetime_observed'].apply(date_to_weekday_am_pm)
    data['weekday_observed'] = weekday_observed
    return data

def pivot(data, is_combined_data=True):
    """Pivot the data

    Args:
        data (dataframe):
            contains user_id, island_id, turnip selling prices along with 
            weekday_observed
    
    Returns:
        pivot_table (dataframe):
            pivot table of the data with incremented trend numbers in place 
            of user_id and island_id
             ______________________________________________________
            |     -    | Monday AM | Monday PM | ... | Saturday PM |
            | trend_id |     -     |     -     | ... |      -      |
            |     0    |   price   |   price   | ... |    price    |
    """
    
    not_combined_data = not(is_combined_data)
    if (not_combined_data):
        index=['user_id', 'island_id']
    else:
        index='trend_id'
        
    pivot_table = pd.pivot_table(
        data=data,
        values='price',
        index=index,
        columns='weekday_observed'
    )
    
    # correct weekday order
    column_names = data['weekday_observed'].unique()
    pivot_table = pivot_table.reindex(column_names, axis=1)
    
    if (not_combined_data):
        # drop user_id, island_id
        pivot_table.reset_index(drop=True, inplace=True)
    
    return pivot_table

def combine(list_of_data):
    """Combine weekly turnip prices
    
    Args:
        list_of_data (list): 
            contains price data for various weeks
        
    Returns:
        combined_data (dataframe): 
            contains turnip prices with each weekly trend identified
            by trend_id
    """
    
    pivot_tables = [
        pivot(data, is_combined_data=False) 
        for data in list_of_data
    ]
    
    combined_data = pd.concat(pivot_tables)
    combined_data.reset_index(drop=True, inplace=True)
    combined_data.reset_index(inplace=True)
    
    combined_data = combined_data.melt(id_vars='index', value_name='price')
    combined_data.reset_index(drop=True, inplace=True)
    combined_data.rename(columns={'index': 'trend_id'}, inplace=True)
    
    return combined_data

def load_transform_combine(num_weeks, connection):
    """Load weekly sell data, transform by dropping incomplete weeks,
    creating a column containing the weekday and time of day and then
    combining the data
    
    Args:
        num_week (int): number of weeks
        connection (sqlalchemy connection): MySQL database connection
        
    Returns:
        combined_data (dataframe): 
            contains turnip prices with each weekly trend identified
            by trend_id
    """
    
    weekly_data = [
        load_week_n_sell_data(week=week_num, connection=connection) 
        for week_num in range(1, num_weeks + 1)
    ]    
    
    weekly_data = [drop_incomplete_sell_data(data) for data in weekly_data]
    weekly_data = [datetime_to_weekday(data) for data in weekly_data]
    
    combined_data = combine(weekly_data)
    return combined_data
