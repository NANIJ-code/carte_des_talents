# Guide de déploiement sur Render

Ce guide explique comment déployer l'application Carte des Talents sur Render avec Docker.

## Prérequis

- Un compte Render (gratuit disponible sur [render.com](https://render.com))
- Un dépôt Git (GitHub, GitLab, ou Bitbucket) contenant ce projet

## Étapes de déploiement

### 1. Préparer le dépôt Git

Assurez-vous que tous les fichiers sont commités et poussés vers votre dépôt :

```bash
git add .
git commit -m "Préparation pour déploiement Render avec Docker"
git push origin main
```

### 2. Créer la base de données PostgreSQL sur Render

1. Connectez-vous à votre tableau de bord Render
2. Cliquez sur "New +" → "PostgreSQL"
3. Configurez :
   - **Name**: `carte-des-talents-db`
   - **Database**: `carte_des_talents`
   - **User**: `carte_des_talents_user`
   - **Plan**: Free (ou un plan payant selon vos besoins)
4. Cliquez sur "Create Database"
5. Notez l'**Internal Database URL** (sera utilisé automatiquement)

### 3. Déployer l'application web

#### Option A : Utiliser render.yaml (Recommandé)

1. Dans votre tableau de bord Render, cliquez sur "New +" → "Blueprint"
2. Connectez votre dépôt Git
3. Render détectera automatiquement le fichier `render.yaml` à la racine
4. Cliquez sur "Apply" pour créer les services

#### Option B : Déploiement manuel

1. Dans votre tableau de bord Render, cliquez sur "New +" → "Web Service"
2. Connectez votre dépôt Git
3. Configurez le service :
   - **Name**: `carte-des-talents`
   - **Environment**: `Docker`
   - **Region**: Choisissez la région la plus proche
   - **Branch**: `main` (ou votre branche principale)
   - **Root Directory**: Laisser vide (le Dockerfile est dans `talent-map-app/`)
   - **Dockerfile Path**: `talent-map-app/Dockerfile`
   - **Docker Context**: `talent-map-app`
   - **Plan**: Free (ou un plan payant)

4. Configurez les variables d'environnement :
   - `SECRET_KEY`: Générez une clé secrète Django (vous pouvez utiliser `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: Votre domaine Render (ex: `carte-des-talents.onrender.com`)
   - `DATABASE_URL`: L'URL interne de la base de données créée à l'étape 2

5. Cliquez sur "Create Web Service"

### 4. Lier la base de données au service web

1. Dans les paramètres de votre service web, allez dans "Environment"
2. Ajoutez la variable `DATABASE_URL` avec l'URL interne de votre base de données PostgreSQL
3. Render peut aussi créer automatiquement cette variable si vous liez la base de données dans l'interface

### 5. Créer un superutilisateur

Une fois le déploiement terminé :

1. Ouvrez le shell de votre service web dans Render
2. Exécutez :
```bash
python manage.py createsuperuser
```
3. Suivez les instructions pour créer votre compte administrateur

## Configuration des variables d'environnement

Variables importantes à configurer dans Render :

| Variable | Description | Exemple |
|----------|-------------|---------|
| `SECRET_KEY` | Clé secrète Django (générer une nouvelle pour la production) | Généré automatiquement |
| `DEBUG` | Mode debug (toujours `False` en production) | `False` |
| `ALLOWED_HOSTS` | Domaines autorisés (séparés par des virgules) | `carte-des-talents.onrender.com` |
| `DATABASE_URL` | URL de connexion PostgreSQL | Auto-configuré par Render |

## Vérification du déploiement

1. Accédez à l'URL de votre service (ex: `https://carte-des-talents.onrender.com`)
2. Vérifiez que l'application se charge correctement
3. Testez la création de compte et la connexion
4. Accédez à `/admin` avec votre superutilisateur

## Notes importantes

- **Plan Free**: Les services gratuits s'endorment après 15 minutes d'inactivité. Le premier démarrage peut prendre 30-60 secondes.
- **Base de données**: Le plan gratuit PostgreSQL a des limitations (90 jours de rétention, pas de sauvegarde automatique). Pour la production, considérez un plan payant.
- **Fichiers statiques**: Les fichiers statiques sont servis via WhiteNoise, inclus dans le Dockerfile.
- **Migrations**: Les migrations sont appliquées automatiquement au démarrage via le script `start.sh`.

## Dépannage

### L'application ne démarre pas

1. Vérifiez les logs dans le tableau de bord Render
2. Assurez-vous que toutes les variables d'environnement sont configurées
3. Vérifiez que `DATABASE_URL` pointe vers la bonne base de données

### Erreur de connexion à la base de données

1. Vérifiez que la base de données est créée et active
2. Vérifiez que `DATABASE_URL` utilise l'URL interne (pas externe)
3. Assurez-vous que le service web et la base de données sont dans la même région

### Les fichiers statiques ne se chargent pas

1. Vérifiez que `collectstatic` s'exécute correctement (voir les logs)
2. Assurez-vous que WhiteNoise est correctement configuré dans `settings.py`

## Support

Pour plus d'informations, consultez :
- [Documentation Render](https://render.com/docs)
- [Documentation Django Deployment](https://docs.djangoproject.com/en/4.2/howto/deployment/)

