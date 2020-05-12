import numpy as np
import pandas as pd

def drop_features(data):
    """Drop features not related to turnip prices with
    the exception of In-Game Name and Island
    
    Args: 
        data (dataframe): 
            original data from Maddox Knight's Turnip Mafia
    
    Returns:
        data (dataframe): 
            contains In-Game Name, Island along with the 
            buying and selling prices of turnips
    """
    
    column_names = [
        'In-Game Name', 'Island', 'Buy Price', 'Mon AM', 
        'Mon PM', 'Tue AM', 'Tue PM', 'Wed AM', 'Wed PM', 
        'Thu AM', 'Thu PM', 'Fri AM','Fri PM','Sat AM','Sat PM'
    ]
    data = data[column_names]
    return data

def mask_invalid_names(data):
    """Mask rows in which In-Game Name or Island are invalid
    
    Args: 
        data (dataframe): 
            contains data associated with invalid In-Game Names 
            or Island
    
    Returns:
        data (dataframe): 
            contains data associated with both a valid In-Game Name 
            and Island
    """
    
    invalid_ign_mask = data['In-Game Name'].notna()
    invalid_island_mask = data['Island'].notna()
    valid_data = data[invalid_ign_mask & invalid_island_mask].copy()
    valid_data.reset_index(drop=True, inplace=True)
    return valid_data

def convert_entry_to_float(entry):
    """Convert a price entry to float while replacing invalid
    prices with NaN
    
    Args:
        entry (str/float):
            entry to be converted
    
    Returns:
        convert_entry (float): 
            entry as a float or np.nan 
    """
    
    try: 
        converted_entry = float(entry)
    except:
        converted_entry = np.nan
    return converted_entry

def preprocess(data):
    """Preprocess data by dropping features, masking invalid 
    In-game Name and Islands along with formatting turnip prices
    
    Args: 
        data (dataframe): 
            original data from Maddox Knight's Turnip Mafia
        
    Returns:
        preprocessed_data (dataframe): 
            contains In-Game Name, Island along with the 
            buying and selling prices of turnips
    """
    
    preprocessed_data = drop_features(data)
    preprocessed_data = mask_invalid_names(preprocessed_data)
    # week 4 Lala Hyazinth duplicated, drop duplicates
    preprocessed_data.drop_duplicates(
        subset=['In-Game Name', 'Island'], 
        keep='last', 
        inplace=True
    )
    
    price_columns = preprocessed_data.columns[2:]
    preprocessed_data[price_columns] = (
        preprocessed_data[price_columns].applymap(convert_entry_to_float)
    )
        
    return preprocessed_data
