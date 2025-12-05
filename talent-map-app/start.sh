#!/bin/bash

# Attendre que la base de données soit prête (si PostgreSQL)
if [ "$DATABASE_URL" != "" ]; then
  echo "En attente de la base de données..."
  sleep 2
fi

# Appliquer les migrations
echo "Application des migrations..."
python manage.py migrate --noinput

# Collecter les fichiers statiques
echo "Collecte des fichiers statiques..."
python manage.py collectstatic --noinput --clear

# Créer un superutilisateur si nécessaire (optionnel, peut être fait manuellement)
# python manage.py createsuperuser --noinput || true

# Utiliser le port fourni par Render ou 8000 par défaut
PORT=${PORT:-8000}

# Démarrer le serveur Gunicorn
echo "Démarrage du serveur sur le port $PORT..."
exec gunicorn talent_map_project.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120

