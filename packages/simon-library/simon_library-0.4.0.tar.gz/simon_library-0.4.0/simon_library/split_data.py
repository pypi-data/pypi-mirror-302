
from sklearn.model_selection import train_test_split

def split_data(df, features=None, target='diabetes_mellitus', test_size=0.2, random_state=42):
    """
    Splits the DataFrame into training and testing sets.
    
    Parameters:
    -----------
    df : pd.DataFrame
        The DataFrame containing the data to split.
        
    features : list, optional (default=None)
        The list of feature columns to use. If None, uses default feature set.
        
    target : str
        The name of the target column.
        
    test_size : float
        The proportion of the data to be used as the test set.
        
    random_state : int
        Random seed for reproducibility.
        
    Returns:
    --------
    X_train, X_test, y_train, y_test : pd.DataFrame, pd.DataFrame, pd.Series, pd.Series
        The training and test feature sets and their corresponding target values.
    """
    if features is None:
        features = ['age', 'height', 'weight', 'aids', 'cirrhosis', 'hepatic_failure',
                    'immunosuppression', 'leukemia', 'lymphoma', 'solid_tumor_with_metastasis']
    
    X = df[features]
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    
    return X_train, X_test, y_train, y_test
