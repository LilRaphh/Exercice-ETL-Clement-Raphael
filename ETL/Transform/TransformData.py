import pandas as pd

class TransformData:

    def __init__(self):
        pass

    def convert_json_to_df(self, json):
        """
        Récupère un fichier json pour le convertir en dataframe avec pandas.

        Args:
        - json: Fichier json qui contient les datas.

        Returns:
        - Return le dataframe.
        """
        df = pd.DataFrame(json)
        
        df.reset_index(drop=True, inplace=True)
        
        return df
    
    def rename_column(self, df, column, new_column):
        """
        Renomme une colonne d'un dataframe avec pandas.

        Args:
        - df: Le sataframe que l'on veut modifier
        - columns: La colonne que l'on veut remplacer
        - new_column: Le nom de la nouvelle colonne

        Returns:
        - Return le dataframe avec les colonnes 
        """
        df = df.rename(columns={column: new_column})

        return df

    
    def remove_column(self, df, column: list):
        """
        Supprime une colonne du dataframe

        Args:
        - df: Le dataframe pandas contenant les données.
        - column (str): Le nom de la colonne à supprimer 

        Returns:
        - Return le dataframe avec la colonne supprimer
        """

        new_df = df.drop(columns=column)
        return new_df
    
    def remove_currency_symbols(self, df, columns: list):
        """
        Supprime les symboles monétaires et convertit les valeurs en type float.
        
        Args:
        - df (pd.DataFrame): Le DataFrame Pandas contenant les données.
        - columns (list): Liste des noms de colonnes à transformer.
        
        Returns:
        - pd.DataFrame: Le DataFrame mis à jour avec les colonnes transformées.
        """
        for column in columns:
            print(f"Traitement de la colonne: {column}")

            # Convertir en string si nécessaire
            df[column] = df[column].astype(str)

            # Supprimer les symboles monétaires et convertir les nombres
            df[column] = df[column] \
                .str.replace('[€,$,£,hPa,km,%]', '', regex=True) \
                .str.replace(',', '.') \
                .str.split(' ').str[0] 

        return df


    def to_lowercase(self, df, column):
        """
        Convertit toutes les chaînes de caractères d'une colonne en minuscules.
        
        Args:
        - df (pd.DataFrame): Le DataFrame Pandas contenant les données.
        - column (str): Le nom de la colonne à transformer.
        
        Returns:
        - pd.DataFrame: DataFrame avec la colonne modifiée.
        """
        df[column] = df[column].str.lower()
        return df

    def fill_missing_with_value(self, df, column, value):
        """
        Remplace les valeurs manquantes (NaN) dans une colonne par une valeur spécifiée.
        
        Args:
        - df (pd.DataFrame): Le DataFrame Pandas contenant les données.
        - column (str): Le nom de la colonne à transformer.
        - value (any): La valeur avec laquelle remplacer les NaN.
        
        Returns:
        - pd.DataFrame: DataFrame avec la colonne modifiée.
        """
        df[column].fillna(value, inplace=True)
        return df

    def strip_whitespace(self, df, column):
        """
        Supprime les espaces blancs avant et après les chaînes de caractères dans une colonne.
        
        Args:
        - df (pd.DataFrame): Le DataFrame Pandas contenant les données.
        - column (str): Le nom de la colonne à transformer.
        
        Returns:
        - pd.DataFrame: DataFrame avec la colonne modifiée.
        """
        df[column] = df[column].str.strip()
        return df

    def convert_to_datetime(self, df, column, format=None):
        """
        Convertit une colonne en format datetime.
        
        Args:
        - df (pd.DataFrame): Le DataFrame Pandas contenant les données.
        - column (str): Le nom de la colonne à transformer.
        - format (str, optional): Le format de la date, si nécessaire.
        
        Returns:
        - pd.DataFrame: DataFrame avec la colonne transformée en datetime.
        """
        df[column] = pd.to_datetime(df[column], format=format, errors='coerce')
        return df

    def drop_duplicates(self, df):
        """
        Supprime les lignes dupliquées dans le DataFrame.
        
        Args:
        - df (pd.DataFrame): Le DataFrame Pandas contenant les données.
        
        Returns:
        - pd.DataFrame: DataFrame sans doublons.
        """
        df.drop_duplicates(inplace=True)
        return df

    def normalize_column_names(self, df):
        """
        Normalise les noms de colonnes en les mettant en minuscules et en remplaçant les espaces par des underscores.
        
        Args:
        - df (pd.DataFrame): Le DataFrame Pandas contenant les données.
        
        Returns:
        - pd.DataFrame: DataFrame avec les noms de colonnes normalisés.
        """
        df.columns = df.columns.str.lower().str.replace(' ', '_')
        return df
