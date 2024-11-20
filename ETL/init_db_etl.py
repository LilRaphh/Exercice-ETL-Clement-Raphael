from Extract.API import API
from Extract.Scrapping import Scrapping
from Transform.TransformData import TransformData   
import pandas as pd
from sqlalchemy import create_engine

# Utiliser l'API pour récupérer les données vélo/piéton
api = API()

# Lien de l'API qui retourne un CSV
lien_api_velo_pieton = (
    "https://data.rennesmetropole.fr/api/explore/v2.1/catalog/datasets/"
    "eco-counter-data/exports/csv?lang=fr&timezone=Europe%2FBerlin&"
    "use_labels=true&delimiter=%3B"
)

# Récupérer toutes les données au format CSV
try:
    csv_pieton_velo_rennes = api.get_api_data(lien_api_velo_pieton)
except Exception as e:
    print(f"Erreur lors de la récupération des données : {e}")

df_velo_piton = pd.DataFrame(csv_pieton_velo_rennes)

# Importation de notre class de scraping 
scrap = Scrapping()

# Importation des datas qui ont été scrap
df_meteo = pd.read_csv("./dataset/meteo_rennes.csv")

transform = TransformData()

df_meteo = transform.remove_currency_symbols(df_meteo, ['Humidité', 'Pression', 'Visibilité', 'Température', 'Pluie', 'Vent', 'Pt. de rosée'])

df_meteo = transform.rename_column(df_meteo, 'Heure locale\naccess_time\n30mn\nMETAR', 'date')
df_meteo = transform.rename_column(df_meteo, 'Température', 'Temperature')
df_meteo = transform.rename_column(df_meteo, 'Humidité', 'Humidite')
df_meteo = transform.rename_column(df_meteo, 'Pt. de rosée', 'Point_rose')
df_meteo = transform.rename_column(df_meteo, 'Pression', 'Pression')
df_meteo = transform.rename_column(df_meteo, 'Visibilité', 'Visibilite')

df_meteo = transform.remove_column(df_meteo, ['Unnamed: 0', 'Unnamed: 2', 'Temps', 'Bio-météo'])
df_velo_piton = transform.remove_column(df_velo_piton, ['status', 'ID', 'geo', 'counter', 'sens', 'isoDate'])

# Convertir les colonnes 'date' en format datetime sans décalage horaire pour les deux DataFrames
df_velo_piton['date'] = pd.to_datetime(df_velo_piton['date'], utc=True).dt.tz_convert(None)
df_meteo['date'] = pd.to_datetime(df_meteo['date'], utc=True).dt.tz_convert(None)

# Effectuer la jointure
df_merged = pd.merge(df_velo_piton, df_meteo, on='date', how='left')

# Suppression des lignes où la colonne 'Température (°C)' a une valeur NaN
df_cleaned = df_merged.dropna(subset=['Temperature'])
df_cleaned_all = df_cleaned.drop_duplicates(subset=['date'])

# Clear les datas indésirables
df_cleaned_all = df_cleaned_all.drop(df_cleaned_all[df_cleaned_all['Temperature'] == 'nn'].index)
df_cleaned_all = df_cleaned_all.drop(df_cleaned_all[df_cleaned_all['Pluie'] == 'nn'].index)
df_cleaned_all = df_cleaned_all.drop(df_cleaned_all[df_cleaned_all['Humidite'] == 'nn'].index)
df_cleaned_all = df_cleaned_all.drop(df_cleaned_all[df_cleaned_all['Point_rose'] == 'nn'].index)
df_cleaned_all = df_cleaned_all.drop(df_cleaned_all[df_cleaned_all['Visibilite'] == 'nn'].index)
df_meteo = df_meteo.drop(df_meteo[df_meteo['Temperature'] == 'nn'].index)
df_meteo = df_meteo.drop(df_meteo[df_meteo['Pluie'] == 'nn'].index)
df_meteo = df_meteo.drop(df_meteo[df_meteo['Humidite'] == 'nn'].index)
df_meteo = df_meteo.drop(df_meteo[df_meteo['Point_rose'] == 'nn'].index)
df_meteo = df_meteo.drop(df_meteo[df_meteo['Visibilite'] == 'nn'].index)

df_cleaned_all['Temperature'] = df_cleaned_all['Temperature'].astype(float)
df_cleaned_all['Pluie'] = df_cleaned_all['Pluie'].astype(float)
df_cleaned_all['Vent'] = df_cleaned_all['Vent'].astype(float)
df_cleaned_all['Humidite'] = df_cleaned_all['Humidite'].astype(float)
df_cleaned_all['Point_rose'] = df_cleaned_all['Point_rose'].astype(float)

# Informations de connexion
DB_USER = 'root'
DB_PASSWORD = 'admin'
DB_HOST = 'localhost'
DB_PORT = 3306
DB_NAME = 'ETL'

# Créer une connexion à MySQL
engine = create_engine(f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

dict_bdd = {
    'weather_pieton_count_data': df_cleaned_all,
    'meteo_rennes': df_meteo,
    'velo_pieton': df_velo_piton
    }

for bdd, df in dict_bdd.items():

    # Insérer les données dans MySQL
    try:
        with engine.connect() as connection:  # Assure que la connexion reste ouverte
            df.to_sql(bdd, con=connection, if_exists='append', index=False)
        print(f"Données insérées avec succès pour: {bdd}")
    except Exception as e:
        print(f"Erreur lors de l'insertion des données : {e}")

