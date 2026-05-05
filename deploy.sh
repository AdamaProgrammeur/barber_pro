#!/bin/bash

echo "🚀 Déploiement de BarberPro sur Render"
echo "======================================"

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f "manage.py" ]; then
    echo "❌ Erreur: manage.py non trouvé. Assurez-vous d'être dans le répertoire du projet Django."
    exit 1
fi

# Vérifier que les fichiers de déploiement existent
if [ ! -f "render.yaml" ]; then
    echo "❌ Erreur: render.yaml non trouvé."
    exit 1
fi

if [ ! -f "Procfile" ]; then
    echo "❌ Erreur: Procfile non trouvé."
    exit 1
fi

echo "✅ Fichiers de déploiement présents"

# Vérifier la configuration Django
echo "🔍 Vérification de la configuration Django..."
python manage.py check
if [ $? -ne 0 ]; then
    echo "❌ Erreur dans la configuration Django"
    exit 1
fi

echo "✅ Configuration Django valide"

# Instructions pour le déploiement
echo ""
echo "📋 Instructions de déploiement sur Render:"
echo "=========================================="
echo ""
echo "1. Allez sur https://render.com"
echo "2. Connectez votre compte GitHub"
echo "3. Cliquez sur 'New +' > 'Blueprint'"
echo "4. Sélectionnez ce repository"
echo "5. Render détectera automatiquement render.yaml"
echo "6. Configurez les variables d'environnement si nécessaire:"
echo "   - SECRET_KEY: laissez Render générer une clé"
echo "   - DEBUG: false"
echo "   - ALLOWED_HOSTS: sera défini automatiquement"
echo "7. Cliquez sur 'Create Blueprint'"
echo ""
echo "🎯 L'application sera déployée avec:"
echo "   - Base de données PostgreSQL automatique"
echo "   - Migrations exécutées automatiquement"
echo "   - Superuser créé automatiquement (admin/admin123456)"
echo "   - Gunicorn comme serveur WSGI"
echo ""
echo "⏱️  Le déploiement prend généralement 5-10 minutes."
echo ""
echo "🔗 Après déploiement, votre app sera accessible à l'URL fournie par Render."