import logging 
import pandas as pd


def get_data(path):
    """
    Load a CSV file into a pandas DataFrame with error handling and logging.
    
    Parameters:
    -----------
    path : str
        The path to the CSV file to be loaded.
    
    Returns:
    --------
    df : pd.DataFrame or None
        Returns the loaded DataFrame if successful, None otherwise.
    """
    try:
        # Logging the start of data loading
        logging.info(f"Loading data from file: {path}")
        
        # Load the data
        df = pd.read_csv(path)

        # Logging the success of data loading
        logging.info(f"Data successfully loaded. Number of rows: {len(df)}, number of columns: {len(df.columns)}")
        
        return df

    except FileNotFoundError:
        # Logging an error if the file is not found
        logging.error(f"File not found: {path}")
        return None

    except pd.errors.EmptyDataError:
        # Logging an error if the file is empty
        logging.error(f"File is empty: {path}")
        return None

    except pd.errors.ParserError:
        # Logging an error if there are issues with parsing the CSV
        logging.error(f"Error parsing the file: {path}")
        return None

    except Exception as e:
        # Logging any other error
        logging.error(f"An error occurred while loading data from the file: {path}. Error: {e}")
        return None
    
    