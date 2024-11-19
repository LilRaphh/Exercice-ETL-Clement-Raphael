import os
import psycopg2
from psycopg2 import sql

class DataBaseConnection:

    def __init__(self):
         pass

    def connection(self, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME):
        """
        connecte le projet au serveur postgres

        Arg:
        en paramètre les données de connexion au serveur

        Return:
        retourne la connexion au serveur
        """
        try:
            conn = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )
            print("Connexion réussie à la base de données")    
            return conn
        except Exception as e:
            print(f"Erreur de connexion : {e}")

