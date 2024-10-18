
from sklearn.model_selection import train_test_split


def split_data(df):
    X = df[['age', 'height', 'weight', 'aids', 'cirrhosis', 'hepatic_failure',
                'immunosuppression', 'leukemia', 'lymphoma', 'solid_tumor_with_metastasis']]
    y = df['diabetes_mellitus']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

