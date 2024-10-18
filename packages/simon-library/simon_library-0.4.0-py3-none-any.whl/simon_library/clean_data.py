
import logging


def clean_data(df):
    """
    Clean the data by removing unnecessary columns and rows.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame with columns that need cleaning ('age', 'gender', 'ethnicity', 'height', 'weight').
    
    Returns:
    --------
    df : pd.DataFrame
        DataFrame with cleaned data.
    """     
    try:
        logging.info(f"Rows before cleaning: {len(df)}")
        logging.info(f"Null values before cleaning: {len(df)}")
        df_cleaned = df.dropna(subset=['age', 'gender', 'ethnicity'])
        df_cleaned.loc[:, 'height'] = df_cleaned['height'].fillna(df_cleaned['height'].mean())
        df_cleaned.loc[:, 'weight'] = df_cleaned['weight'].fillna(df_cleaned['weight'].mean())
        logging.info(f"Rows after cleaning: {len(df)}")
        logging.info(f"Null values after cleaning: {len(df)}")
    except KeyError:
        logging.error("The DataFrame does not contain the required columns.")
        return None
    return df_cleaned
