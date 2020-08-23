import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def get_sample_trends(data, trend_ids, n_samples):
    """Return the a sample of trends from the given trend_ids
    
    Args:
        data (dataframe): 
            contains turnip prices with each weekly trend identified
            by trend_id
            
        trend_ids (array): 
            contains the trend_ids from which random samples are
            selected
    
    Returns:
        sample_trends (dataframe): 
            contains the sample of trends
    """
    
    num_trend_ids = trend_ids.shape[0]
    n_samples = min(num_trend_ids, n_samples)
    
    sample_trend_ids = np.random.choice(
        trend_ids, 
        replace=False, 
        size=(n_samples)
    )
    sample_trend_indices = data['trend_id'].isin(sample_trend_ids)
    sample_trends = data.loc[sample_trend_indices, :]
    
    return sample_trends

def plot_trend_samples(data, labels, num_clusters, display_sample_ids=False):
    """Plot samples of all trends
    
    Args:
        data (dataframe): 
            contains turnip prices with each weekly trend identified
            by trend_id
            
        labels (array): 
            contains the cluster numbers for each trend_id

        num_clusters (int):
            the number of unique labels/clusters
    
    Returns:
        None
    """


    cluster_numbers = range(1, num_clusters + 1)
    xticks = data['weekday_observed'].unique()
    
    # find occurences 
    # adapted from https://stackoverflow.com/questions/6294179/
    trend_id_clusters = [
        np.where(labels == cluster_number)[0]
        for cluster_number in cluster_numbers
    ]
    
    for trend_ids, cluster_number in zip(trend_id_clusters, cluster_numbers):
        sample_trends = get_sample_trends(data, trend_ids, 10)
        sample_ids = sample_trends['trend_id'].unique()
        
        plt.figure(figsize=(12, 6))
        trend_plot = sns.lineplot(
            x='weekday_observed', 
            y='price', 
            hue='trend_id',
            data=sample_trends, 
            sort=False,
            palette=sns.color_palette('Set1', n_colors=len(sample_ids)),
            legend=False
        )
        trend_plot.set(
            title='Trend Cluster Number {0}'.format(cluster_number),
            xlabel='Weekday and Time of Day',
            ylabel='Price of Turnips (Bells)'
        )
        trend_plot.set_xticklabels(xticks, rotation=30, ha='right')
        plt.xlim(0, 11)
        plt.show()

        if (display_sample_ids):
            print("Sample IDs for Cluster Number", cluster_number)
            print(sample_ids)
