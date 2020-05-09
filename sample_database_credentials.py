def get_database_url():
    """Get the url for connecting to the MySQL database
    
    Args:
        None
    
    Returns:
        database_url (str): url used to connect to the database
    """

    credentials = {
        'username': 'user',
        'password': 'pass',
        'hostname': 'host',
        'database_name': 'turnip'
    }
    
    database_url = (
        'mysql+mysqlconnector://{0}:{1}@{2}/{3}'
        .format(
            credentials['username'],
            credentials['password'],
            credentials['hostname'],
            credentials['database_name']
        )
    )
    
    return database_url
