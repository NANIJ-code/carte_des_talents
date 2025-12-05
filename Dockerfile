# Utiliser une image Python officielle comme base
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copier le fichier requirements.txt depuis talent-map-app
COPY talent-map-app/requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code de l'application depuis talent-map-app
COPY talent-map-app/ .

# Créer un répertoire pour les fichiers statiques
RUN mkdir -p /app/staticfiles

# Exposer le port 8000 (port par défaut de Django)
EXPOSE 8000

# Script de démarrage
COPY talent-map-app/start.sh /start.sh
RUN chmod +x /start.sh

# Commande par défaut
CMD ["/start.sh"]

