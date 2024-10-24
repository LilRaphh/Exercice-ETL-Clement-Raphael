import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

class DataBaseConnection:

    def __init__(self):
        self.conn = self.connection("postgres", "Colnot36", "localhost", 5432, "postgres")
        self.cursor = self.conn.cursor()

    def connection(self, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME):
        """
        connecte le projet au serveur postgres

        Arg:
        en paramètre les données de connexion au serveur

        Return:
        retourne la connexion au serveur
        """
        load_dotenv()  
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

    def createBdd(self, nameTable, ListePara):
        """
        en paramètre le nom de la table ainsi que la liste sur laquelle on va avoir toutes les données

        Prend le premier élément de la liste pour créer ue clé, puis boucle sur les éléments de la liste pour récupérer toutes les datas
        
        
        """
        query = f"CREATE TABLE {nameTable} ({ListePara[0]} DATE PRIMARY KEY," 
        for i in ListePara: 
            query += ListePara[i+1] + format.ListePara[i+1] + ","
        query += ");"
        self.cursor.execute(query)
        # Fermer le curseur
        self.cursor.close()

    def createB(self, nameTable):
        try:
            query = f"""CREATE TABLE IF NOT EXISTS {nameTable} (
            client_id INT PRIMARY KEY,
            client_name VARCHAR(100),
            contact_email VARCHAR(100),
            phone_number VARCHAR(20),
            address VARCHAR(255)
            );"""
            self.cursor.execute(query)
        except Exception as e:
            print(f"Erreur de connexion : {e}")

    def selectSQL(self, table):
        # Créer un curseur pour exécuter des requêtes
        query = f"SELECT * FROM {table}"
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        # Afficher les enregistrements
        for row in records:
            print(row)


    def closecursor(self):
        # Fermer le curseur
            self.cursor.close()

    def stopconnexion(conn):
        conn.close()
        print("Connexion fermée")

db = DataBaseConnection()
db.createB("test1")
db.selectSQL( "clients")