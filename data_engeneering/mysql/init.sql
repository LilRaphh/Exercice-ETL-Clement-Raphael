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

-- Création de la table meteo_rennes si elle n'existe pas déjà
CREATE TABLE IF NOT EXISTS meteo_rennes (
    date DATETIME PRIMARY KEY,
    Temperature DECIMAL(10, 1),
    Pluie DECIMAL(10, 1),
    Vent DECIMAL(10, 1),
    Humidite DECIMAL(10, 1),
    Point_rose DECIMAL(10, 1),
    Pression DECIMAL(10, 1),
    Visibilite DECIMAL(10, 1)
);

-- Création de la table velo_pieton si elle n'existe pas déjà
CREATE TABLE IF NOT EXISTS velo_pieton (
    date DATETIME PRIMARY KEY,
    counts INT,
    name VARCHAR(255)
);
