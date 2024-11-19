-- Création de la table weather_pieton_count_data si elle n'existe pas déjà
CREATE TABLE IF NOT EXISTS weather_pieton_count_data (
    date DATETIME PRIMARY KEY,
    timestamp TIMESTAMP,
    counts DECIMAL(10, 1),
    name VARCHAR(255),
    Temperature DECIMAL(10, 4),
    Pluie DECIMAL(10, 4),
    Vent DECIMAL(10, 4),
    Humidite DECIMAL(10, 4),
    Point_rose DECIMAL(10, 4),
    Pression DECIMAL(10, 4),
    Visibilite DECIMAL(10, 4)
);