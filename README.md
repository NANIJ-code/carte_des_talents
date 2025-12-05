# Carte des talents

Résumé
-------
Application Django pour indexer et visualiser les profils de collaborateurs — recherche, cartes de talents et gestion de profils utilisateurs.

Principales fonctionnalités
---------------------------
- Inscription / connexion utilisateurs
- Création et édition de profil (bio, compétences, langues, passions, liens)
- Recherche de collaborateurs avec filtres
- Visualisation "talent map" par profil
- Interface responsive avec animations légères

Arborescence clé
----------------
- talent-map-app/ — application Django principale
  - talent_map_app/models.py — modèles (UserProfile, Collaboration)
  - talent_map_app/forms.py — formulaires (inscription, profil, recherche)
  - talent_map_app/views.py — vues
  - talent_map_app/urls.py — routes locales
  - templates/ — templates HTML
  - static/ — CSS / JS (style.css, talent-map.js)
- talent_map_project/ — configuration du projet (settings, urls)
- db.sqlite3 — base de données SQLite (local/dev)

Prérequis
---------
- Python 3.10+ (projet testé avec Python 3.13)
- pip
- virtualenv recommandé

Installation locale (développement)
----------------------------------
1. Cloner le repo
   git clone <url-du-repo>
   cd d:\GENIE_INFORMATIQUE\nuit\carte_des_talents\talent-map-app

2. Créer et activer un virtualenv (Windows PowerShell)
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

3. Installer les dépendances
   pip install -r requirements.txt

4. Appliquer les migrations
   python manage.py migrate

5. (Optionnel) Créer un superutilisateur
   python manage.py createsuperuser

6. Lancer le serveur de développement
   python manage.py runserver

Configuration et variables d'environnement
------------------------------------------
- Les secrets (SECRET_KEY, configurations DB, etc.) doivent être stockés dans un fichier .env ou dans des variables d'environnement.
- /talent_map_project/settings.py lit la configuration. Ne commitez pas de clés secrètes en clair.

Données et médias
-----------------
- db.sqlite3 est utilisé en local. Faire une sauvegarde avant toute suppression.
- Les fichiers médias/avatars doivent être exclus du repo (voir .gitignore).

Bonnes pratiques
----------------
- Respecter `prefers-reduced-motion` pour l'accessibilité (déjà pris en compte dans le CSS).
- Tester sur mobile/tablette pour les interactions tactiles (tilt/animations peuvent être désactivés sur petits écrans).

Tests
-----
- Ajouter des tests unitaires dans talent_map_app/tests.py.
- Exécuter :
  python manage.py test

Contribuer
----------
- Fork → branche feature → PR.
- Décrire les changements dans le message de commit.
- Ajouter ou mettre à jour la documentation / tests selon besoin.

Fichiers utiles
---------------
- templates/profile/create.html — formulaire création/édition profil
- templates/search/search.html — recherche et affichage des résultats
- static/js/talent-map.js — logique front (animations, gestion skills)
- static/css/style.css — styles globaux et carte profil ludique

Licence & contact
-----------------
- Licence : préciser la licence du projet (ex : MIT) dans un fichier LICENSE.
- Contact : créer un issue ou ouvrir une PR pour toute question ou amélioration.