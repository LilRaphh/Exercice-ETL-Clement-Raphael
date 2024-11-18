-- Création de la table weather_pieton_count_data si elle n'existe pas déjà
CREATE TABLE IF NOT EXISTS weather_pieton_count_data (
    date INT PRIMARY KEY,
    timestamp TIMESTAMP,
    counts DECIMAL(10, 1),
    name VARCHAR(255),
    temperature DECIMAL(5, 2),
    pluie DECIMAL(5, 2),
    vent DECIMAL(5, 2),
    humidite DECIMAL(5, 2),
    point_rose DECIMAL(5, 2),
    pression DECIMAL(5, 2),
    visibilite DECIMAL(5, 2)
);