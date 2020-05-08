import matplotlib.pyplot as plt
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
    
    table = pd.pivot_table(
        data=data, 
        values='price', 
        index=['user_id', 'island_id'], 
        columns=['datetime_observed']
    )
    table.dropna(inplace=True)

    data = table.reset_index().melt(
        id_vars=['user_id', 'island_id'], 
        value_name='price'
    )
    return data

def plot_sell_data(data, plot_individuals=True):
    """Plot the sell price data for each individual or overall
    
    Args:
        data (dataframe): contains selling prices of turnips
        plot_individuals (bool): plot individual or overall data
    
    """
    
    earliest_sell_date = data['datetime_observed'].min()
    latest_sell_date = data['datetime_observed'].max() 
    
    user_island_id = zip(data['user_id'], data['island_id'])
    data['user_island_id'] = list(user_island_id)
    
    if (plot_individuals):
        hue='user_island_id'
    else:
        hue=None
    
    plt.figure(figsize=(12, 6))
    sell_price_plot = sns.lineplot(
        x='datetime_observed', 
        y='price', 
        data=data, 
        hue=hue, 
        legend=False
    )
    
    title='Date vs Turnip Selling Price {0} to {1}'.format(
        datetime.strftime(earliest_sell_date, '%Y-%m-%d'), 
        datetime.strftime(latest_sell_date, '%Y-%m-%d')
    )
    sell_price_plot.set(
        title=title,
        xlabel='Date',
        ylabel='Price'
    )
    
    plt.xlim(earliest_sell_date, latest_sell_date)
    plt.show()
