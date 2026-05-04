# Guide de Déploiement - BarberPro sur Render

## Fichiers de déploiement créés

✅ `render.yaml` - Configuration Render avec service web et base de données PostgreSQL
✅ `Procfile` - Commande de démarrage pour Gunicorn
✅ `runtime.txt` - Version Python 3.11.9
✅ `deploy.sh` - Script de vérification pré-déploiement

## Variables d'environnement configurées

- `SECRET_KEY` - Généré automatiquement par Render
- `DEBUG=false` - Mode production
- `ALLOWED_HOSTS` - Défini automatiquement par Render
- `DATABASE_URL` - Fourni automatiquement par la base de données Render

## Étapes de déploiement

### 1. Préparation
```bash
# Vérifier que tout est en ordre
./deploy.sh
```

### 2. Sur Render.com
1. Connectez votre compte GitHub
2. Cliquez sur "New +" → "Blueprint"
3. Sélectionnez votre repository
4. Render détectera `render.yaml` automatiquement

### 3. Configuration Blueprint
- **Nom du service** : barberpro
- **Branche** : main
- **Commande de build** : `pip install -r requirements.txt`
- **Commande de démarrage** : `python manage.py migrate && gunicorn gestion_coiffure.wsgi:application --bind 0.0.0.0:$PORT`

### 4. Base de données
- PostgreSQL sera créée automatiquement
- Les migrations s'exécuteront au premier démarrage

### 5. Déploiement
- Cliquez sur "Create Blueprint"
- Attendez 5-10 minutes
- Votre app sera accessible à l'URL fournie

## Après déploiement

1. **Testez l'application** à l'URL Render
2. **Connectez-vous avec le superuser automatique** :
   - **Username** : `admin`
   - **Password** : `admin123456`
   - **Email** : `admin@barberpro.app`
3. **Le superuser a automatiquement un salon "Salon BarberPro"**
4. **Vous pouvez approuver les comptes utilisateur depuis l'interface admin**

## Dépannage

### Erreur de build
- Vérifiez `requirements.txt`
- Assurez-vous que toutes les dépendances sont listées

### Erreur de base de données
- Vérifiez que `DATABASE_URL` est défini
- Les migrations doivent s'exécuter automatiquement

### Erreur d'application
- Vérifiez les logs Render
- Testez localement avec `python manage.py check`

## Support

Si vous rencontrez des problèmes :
1. Vérifiez les logs détaillés sur Render
2. Testez localement avec les mêmes variables d'environnement
3. Consultez la documentation Render pour les déploiements Django