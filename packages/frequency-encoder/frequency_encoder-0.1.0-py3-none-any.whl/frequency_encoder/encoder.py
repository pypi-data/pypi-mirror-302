import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class FrequencyEncoder(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.encoding_maps = {}
    
    def fit(self, X, y=None):
        """
        Aprende el mapeo de frecuencias para las columnas especificadas.
        
        Args:
        X (pd.DataFrame): DataFrame de entrenamiento.
        y: Ignorado (compatibilidad con scikit-learn).

        Returns:
        self
        """
        for column in X.columns:
            freq_encoding = X[column].value_counts() / len(X)
            self.encoding_maps[column] = freq_encoding.to_dict()
        return self

    def transform(self, X):
        """
        Aplica la codificación de frecuencia a las columnas del DataFrame.
        
        Args:
        X (pd.DataFrame): DataFrame a transformar.

        Returns:
        pd.DataFrame: DataFrame transformado.
        """
        X_transformed = X.copy()
        for column in X.columns:
            encoding_map = self.encoding_maps.get(column, {})
            X_transformed[column] = X_transformed[column].map(lambda x: encoding_map.get(x, -1))
        return X_transformed
