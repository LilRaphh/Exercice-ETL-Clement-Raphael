FROM mysql:latest

# Ajoute le script SQL pour l'initialisation de la base de données
ADD init.sql /docker-entrypoint-initdb.d/

# Optionnel : définissez la variable d'environnement pour le mot de passe root
# Cela est nécessaire si vous n'utilisez pas de volume persistant pour les données.
ENV MYSQL_ROOT_PASSWORD=admin
