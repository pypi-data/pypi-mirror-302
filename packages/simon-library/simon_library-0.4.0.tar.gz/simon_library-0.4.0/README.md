# simon_library

`simon_library` is a Python package designed for data preprocessing and model evaluation. The library contains a set of utilities for cleaning data, feature engineering, splitting data, training models, and evaluating performance using ROC AUC. This package is especially useful for data science and machine learning tasks.

## Installation

You can install the `simon_library` package via `pip`:

pip install simon_library


## Available Functions

1. get_data(path)
Loads a CSV file into a pandas DataFrame with error handling and logging.

Parameters:

path (str): The path to the CSV file to be loaded.
Returns:

pd.DataFrame: The loaded DataFrame if successful, otherwise None.

2. clean_data(df)
Cleans the data by handling missing values and preparing it for further analysis.

Parameters:

df (pd.DataFrame): The DataFrame to clean.
Returns:

pd.DataFrame: The cleaned DataFrame.

3. create_features(df)
Generates additional features from existing columns, including encoding categorical variables and adding new binary features.

Parameters:

df (pd.DataFrame): The DataFrame to create features from.
Returns:

pd.DataFrame: The DataFrame with new and transformed features.

4. split_data(df, target, test_size=0.2, random_state=42)
Splits the DataFrame into training and testing sets.

Parameters:

df (pd.DataFrame): The DataFrame to split.
target (str): The target column to predict.
test_size (float): Proportion of the data to be used as the test set.
random_state (int): Random seed for reproducibility.
Returns:

X_train, X_test, y_train, y_test: Split training and test sets.

5. train_model(X_train, X_test, y_train, y_test, model)
Trains the provided model on the training set and evaluates it on the test set.

Parameters:

X_train, X_test: Feature sets for training and testing.
y_train, y_test: Target values for training and testing.
model: A scikit-learn model to train.
Returns:

accuracy: Accuracy score on the test set.
train_predictions_proba, test_predictions_proba: Predicted probabilities for training and testing sets.

6. get_roc_auc(y_train, y_test, train_predictions, test_predictions)
Calculates the ROC AUC score for both training and test sets.

Parameters:

y_train, y_test: True target values for the training and test sets.
train_predictions, test_predictions: Predicted probabilities for the training and test sets.
Returns:

roc_auc_train, roc_auc_test: ROC AUC scores for training and test sets.

