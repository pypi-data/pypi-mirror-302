
from sklearn.metrics import accuracy_score
import logging


def train_model(X_train, X_test, y_train, y_test, model, model_name):
    """
    Trains the given model on the provided training data and calculates accuracy on the test set.
    Also returns the predicted probabilities for both training and test sets.

    Parameters:
    -----------
    X_train : pd.DataFrame or np.ndarray
        Features for the training set.
    
    X_test : pd.DataFrame or np.ndarray
        Features for the test set.
    
    y_train : pd.Series or np.ndarray
        True labels for the training set.
    
    y_test : pd.Series or np.ndarray
        True labels for the test set.
    
    model : sklearn model instance
        The machine learning model to be trained (e.g., LogisticRegression or RandomForestClassifier).
    
    Returns:
    --------
    accuracy : float
        Accuracy score of the model on the test set.
    
    train_predictions_proba : np.ndarray
        Predicted probabilities for the training set (for class 1).
    
    test_predictions_proba : np.ndarray
        Predicted probabilities for the test set (for class 1).
    """

    logging.info(f"Model {model_name} Training...")
    # Train the model
    model.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = model.predict(X_test)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    logging.info(f"Model {model_name} Accuracy: {accuracy}")

    # Get predicted probabilities for the training set (for class 1)
    train_predictions_proba = model.predict_proba(X_train)[:, 1]

    # Get predicted probabilities for the test set (for class 1)
    test_predictions_proba = model.predict_proba(X_test)[:, 1]

    # Add predictions as new columns in training and testing sets (optional)
    X_train['predictions'] = train_predictions_proba
    X_test['predictions'] = test_predictions_proba

    return accuracy, train_predictions_proba, test_predictions_proba

