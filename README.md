# Projet Intégré : Évaluation de la Corélation entre la météo et le passage dans les rues de Rennes

## Technologies Utilisées

### Langage

![Python](https://img.shields.io/badge/Python-3.12.7-blue?logo=python&logoColor=white)

### Framework et outils de développement

![Docker](https://img.shields.io/badge/Docker-20.10.7-blue?logo=docker&logoColor=white)


### Bibliothèques de Données & Machine Learning

![Pandas](https://img.shields.io/badge/Pandas-1.5.2-brightgreen?logo=pandas&logoColor=white)

### Outils de Visualisation

![Superset](https://img.shields.io/badge/SuperSet-version-blue?logo=Superset$logoColor=white)

## Introduction au Projet
---

Ces outils ont été utilisé pour le developpement du Projet Exercice-ETL-Clement-Raphael. Ce dernier vise à récupérer des données provenant de diverses sources, comme une API et un site internet, afin de de les transformer, pour ensuite les analyser. Tout cela de manière à pouvoir en tirer des insights et potentiellement, par la suite, en faire des prédictions.

## Objectif du Projet 
---
Ce projet vise à combiner les données d'un site météo (infoclimat) ainsi que les données fournies par une API Rennes Metropoles. Cete démarche permet de pouvoir détécter des biais de comportements, que ce soit vis-à-vis de la météo mais aussi de périodes de l'années, ou des événements. Et cela afin de pouvoir au long terme donner des voies d'amélioration quant à la circulation au sein de la métropole de Rennes.

## Architecture du Projet
---

<img width="725" alt="Capture d’écran 2024-11-15 à 15 15 31" src="https://github.com/user-attachments/assets/a07471d4-3756-4139-9e65-8cde17b39086">

## Workflow et schéma d'architecture

1. **Récupération des données (API et scrapping)** :

  - Exctration des données à partir de la page météo, à l'aide d'un script Python.
  - Récupération des données de l'API pour les transformer sous le même format que le scrapping.

2. **Traitement des données**

  - **Transformation des données / Simplification :** Une fois la récupération de toutes les données, à travers le scrapping de toutes les pages depuis le 1er janvier 2023, nettouage de toutes les données à l'aide d'un second script python.
  - **merging des données :** merging des deux sources des données par la date.

3. **Envoie des données vers la base de donnée**

  - Envoie des données vers la base de données Postgres SQL à partir de scripts Python.

4. **Visualisation et Analyse**

  - Superset récupére les données pour créer une visualisation

# **Guide d'Installation**

## **Prérequis**
Avant de commencer, assurez-vous d'avoir les outils suivants installés sur votre machine :
1. **Python 3.12.7** ou une version compatible.
   - Vérifiez en exécutant : `python --version` ou `python3 --version`.
2. **Docker** (version 20.10.7 ou ultérieure).
   - Vérifiez en exécutant : `docker --version`.
3. **Git** pour cloner le dépôt.
   - Vérifiez en exécutant : `git --version`.

---

## **Étape 1 : Cloner le dépôt**
Téléchargez le code source de ce projet depuis le dépôt GitHub :
```bash

git clone https://github.com/votre-utilisateur/Exercice-ETL-Clement-Raphael.git

cd Exercice-ETL-Clement-Raphael
```
---

## **Étape 2 : Configurer l'environnement Python**

1. **Créer un environnement virtuel** (recommandé pour isoler les dépendances du projet) :
   - Sur Unix/macOS :
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - Sur Windows :
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

2. **Mettre à jour `pip` et installer les dépendances** :
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
---

## **Étape 3 : Configurer Docker pour les services**
Certains services, comme les bases de données ou les outils de visualisation, peuvent être exécutés à l'aide de Docker.

1. **Configurer le fichier `docker-compose.yml`** (si applicable) :
   - Modifiez les paramètres si nécessaire, par exemple, les ports ou les chemins des volumes.
   - Exemple :
     ```yaml
     version: '3.8'
     services:
       database:
         image: postgres:latest
         container_name: my_postgres_db
         ports:
           - "5432:5432"
         environment:
           POSTGRES_USER: admin
           POSTGRES_PASSWORD: password
           POSTGRES_DB: my_database
         volumes:
           - db_data:/var/lib/postgresql/data
       superset:
         image: apache/superset:latest
         container_name: superset_app
         ports:
           - "8088:8088"
         environment:
           SUPERSET_CONFIG_PATH: /app/pythonpath/superset_config.py
         volumes:
           - ./superset_config:/app/pythonpath
     volumes:
       db_data:
     ```

2. **Lancer Docker** :
   ```bash
   docker-compose up -d
   ```

## **Étape 4 : Configurer les Variables d’Environnement**

Certaines fonctionnalités nécessitent des clés ou des configurations spécifiques. Celles-ci peuvent être centralisées dans un fichier .env.

**Créer un fichier .env:**
   ```bash
   touch .env
   ```

=======
# 📜 Conclusion

---

L’application développée dans le cadre de ce projet met en lumière l’interaction entre les conditions météorologiques et les flux de passage en différents points de la ville de Rennes. Grâce à l’exploitation combinée de données issues d’un site météo scrappé et d’une API dédiée aux flux de passage, nous avons pu établir des liens de corrélation intéressants tout au long de l’année.

En s’appuyant sur des techniques de web scraping et d’intégration d’API, l’application offre une analyse approfondie et quantifiée de la manière dont les variations climatiques influencent les déplacements urbains. Ces résultats peuvent fournir des insights précieux pour les gestionnaires urbains, les commerçants, ou toute entité cherchant à anticiper les comportements liés aux flux de population en fonction des conditions climatiques.

Les visualisations générées permettent d’explorer ces corrélations de manière intuitive et interactive, ouvrant la voie à une meilleure compréhension des dynamiques urbaines. Ce projet pourrait également servir de base pour des développements futurs, tels que l’intégration de modèles prédictifs ou l’analyse de flux dans d’autres contextes géographiques.

En conclusion, cette solution démontre comment des données disparates peuvent être combinées et analysées pour révéler des tendances utiles et exploitables. Elle représente une avancée vers une gestion des flux urbains plus proactive, tout en soulignant le rôle clé des conditions environnementales dans la planification et la prise de décision.

🚧 Difficultés Rencontrées

  texte


## Amélioration future
---
  


## Contributeurs

  - Clément Metois (@Skyane) : Apprenti Data Scientist -**skayne.pro@gmail.com**-
  - Colnot Raphaël (@LilRaphh) : Apprenti Data Scientist -**colnotraphael@gmail.com**-


## Licence

Ce projet a été réaslisé pour rendu en école.









