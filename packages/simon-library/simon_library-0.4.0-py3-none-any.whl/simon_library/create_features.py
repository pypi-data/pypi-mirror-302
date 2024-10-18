
import pandas as pd
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_features(df):
    """
    Create new features from existing columns, including encoding categorical variables 
    and adding new binary features, with logging and copy handling to avoid warnings.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame with columns that need feature engineering (e.g., 'ethnicity', 'gender').
    
    Returns:
    --------
    df : pd.DataFrame
        DataFrame with new and transformed features.
    """
    try:
        # Log starting the feature engineering process
        logging.info("Starting feature engineering...")

        # Create dummy variables for the 'ethnicity' column
        df = pd.get_dummies(df, columns=['ethnicity'], drop_first=True)
        logging.info(f"Dummy variables created for 'ethnicity'. New columns: {list(df.columns)}")
        
        # Creating a copy to avoid SettingWithCopyWarning
        df = df.copy()

        # Map gender column to binary values ('M' -> 1, 'F' -> 0)
        df.loc[:, 'gender_binary'] = df.loc[:, 'gender'].map({'M': 1, 'F': 0})
        logging.info("Binary encoding applied to 'gender' column.")

        return df

    except KeyError as e:
        # Log if expected columns are missing
        logging.error(f"KeyError: Column not found in DataFrame - {e}")
        return None

    except Exception as e:
        # Log any other unexpected errors
        logging.error(f"An error occurred during feature engineering: {e}")
        return None

