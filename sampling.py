import numpy as np

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
