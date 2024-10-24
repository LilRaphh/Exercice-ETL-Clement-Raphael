import requests
import pandas as pd
from io import StringIO

class API:
    def __init__(self):
        self.records = None

    def get_api_data(self, link: str, delimiter: str = ';'):
        """
        Récupère les données de l'API au format CSV et les convertit en DataFrame.

        Args:
        - link (str): Lien de l'API qui retourne les données en CSV.
        - delimiter (str): Délimiteur utilisé dans le fichier CSV (par défaut, ';').

        Returns:
        - pd.DataFrame: DataFrame contenant les données récupérées.
        """
        try:
            # Effectuer la requête à l'API
            response = requests.get(link)
            response.raise_for_status()  # Lève une erreur si la requête échoue
        except requests.exceptions.RequestException as e:
            # Gérer les erreurs de connexion ou HTTP
            print(f"Erreur lors de la requête à l'API : {e}")
            return None

        try:
            # Le contenu de la réponse est du texte CSV
            csv_data = response.content.decode('utf-8')

            # Lire le CSV directement en DataFrame
            df = pd.read_csv(StringIO(csv_data), delimiter=delimiter)

            if not df.empty:
                print("Les données ont été chargées avec succès.")
                self.records = df
                return self.records
            else:
                print("Le fichier CSV est vide ou n'a pas été correctement récupéré.")
                return None
        except Exception as e:
            # Gérer les erreurs de lecture du CSV
            print(f"Erreur lors de la lecture du CSV : {e}")
            return None
