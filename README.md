<<<<<<< HEAD
# BarberPro

Application de gestion de salon de coiffure (back-office) construite avec Django + Django REST Framework.
Elle permet de gérer les clients, services, file d'attente, paiements, utilisateurs du salon et tableau de bord.

## Fonctionnalités

- Authentification JWT (connexion, profil, rôles)
- Création d'un salon et gestion des membres (`admin`, `receptionniste`)
- Gestion des clients
- Gestion des services
- Gestion de la file d'attente
- Gestion des paiements
- Dashboard pour suivi des activités
- Mode démo (connexion test rapide)

## Stack technique

- Backend: Django 4.2, Django REST Framework
- Base de données: PostgreSQL
- Frontend: templates Django + assets statiques (et dossier frontend pour ressources UI)

## Arborescence utile

```text
.
├── backend/gestion_coiffure/
│   ├── manage.py
│   ├── .env.example
│   ├── accounts/
│   ├── clients/
│   ├── services/
│   ├── file_attente/
│   ├── paiements/
│   ├── dashbord/
│   ├── salon/
│   └── gestion_coiffure/settings.py
├── frontend/
├── requirements.txt
└── README.md
```

## Prérequis

- Python 3.10+ (recommandé: 3.12)
- PostgreSQL 13+
- `pip` et environnement virtuel Python

## Installation

1. Cloner le projet:
```bash
git clone <URL_DU_REPO>
cd coiffures
```

2. Créer et activer un environnement virtuel:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Installer les dépendances:
```bash
pip install -r requirements.txt
```

4. Créer la base PostgreSQL (exemple):
```sql
CREATE DATABASE coiffure_db;
CREATE USER postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE coiffure_db TO postgres;
```

## Configuration

1. Copier le fichier d'exemple:
```bash
cp backend/gestion_coiffure/.env.example backend/gestion_coiffure/.env
```

2. Modifier `backend/gestion_coiffure/.env`:
```env
DEBUG=True
SECRET_KEY=change-me-in-production
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=coiffure_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

## Lancement

1. Appliquer les migrations:
```bash
cd backend/gestion_coiffure
python manage.py migrate
```

2. (Optionnel) Créer un superuser:
```bash
python manage.py createsuperuser
```

3. Démarrer le serveur:
```bash
python manage.py runserver
```

4. Ouvrir:
- Application: `http://127.0.0.1:8000/`
- Admin Django: `http://127.0.0.1:8000/admin/`

## Mode démo

Si `DEMO_LOGIN_ENABLED=True`, un bouton de connexion démo est disponible sur la page login.

Variables associées:
- `DEMO_USERNAME`
- `DEMO_PASSWORD`
- `DEMO_EMAIL`
- `DEMO_SALON_NAME`

## Tests

Depuis `backend/gestion_coiffure`:

```bash
python manage.py check
python manage.py test
```

## Bonnes pratiques Git (sécurité)

- Ne jamais committer `.env`
- Ne pas committer `venv/`, `node_modules/`, `media/`, `staticfiles/`, logs ou dumps SQL
- Utiliser `.env.example` comme modèle partageable

## Préparer un push GitHub propre

1. Vérifier l'état:
```bash
git status
```

2. Retirer du tracking Git les fichiers sensibles/dérivés déjà suivis:
```bash
git rm -r --cached --ignore-unmatch venv .venv env ENV
git rm -r --cached --ignore-unmatch backend/gestion_coiffure/media backend/gestion_coiffure/staticfiles
git rm --cached --ignore-unmatch backend/gestion_coiffure/.env
```

3. Ajouter les fichiers utiles:
```bash
git add .gitignore requirements.txt README.md backend/gestion_coiffure/.env.example backend/gestion_coiffure/gestion_coiffure/settings.py
git add .
```

4. Commit:
```bash
git commit -m "chore: secure env config, cleanup gitignore, and improve project documentation"
```

5. Initialiser le dépôt si nécessaire:
```bash
git init
git branch -M main
```

6. Connecter GitHub et pousser:
```bash
git remote add origin https://github.com/<USER>/<REPO>.git
git push -u origin main
```

Si `origin` existe déjà:
```bash
git remote set-url origin https://github.com/<USER>/<REPO>.git
git push -u origin main
```
=======
# BarberPro - Application de Gestion de Salon

[![Python Version](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/)
[![Django Version](https://img.shields.io/badge/django-5.2-green)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)

BarberPro est une application web complète pour la gestion des salons de coiffure.  
Elle permet aux propriétaires et au personnel de gérer les clients, les services, les paiements, les files d'attente et plus encore.

---

## **Fonctionnalités**

- Gestion des utilisateurs avec rôles : **Propriétaire, Coiffeur, Réceptionniste**  
- Gestion des clients et de leurs informations  
- Gestion des services proposés par le salon  
- Gestion des paiements et suivi des transactions  
- Gestion des files d’attente et planning des rendez-vous  
- Tableau de bord pour visualiser les statistiques du salon  
- Mode **Démo** pour tester l’application sans créer de compte réel

---

## **Technologies Utilisées**

- **Backend** : Python 3.12, Django 5.2, Django REST Framework  
- **Base de données** : PostgreSQL  
- **Frontend** : HTML, CSS, JavaScript, Bootstrap
- **Authentification** : Custom User Model Django  
- **Outils supplémentaires** : Git, GitHub, Virtualenv

---

## **Installation**

### 1️⃣ Cloner le projet

```bash
git clone https://github.com/AdamaProgrammeur/BarberPro.git
cd BarberPro/backend/gestion_coiffure
>>>>>>> 7bb2ef2db54aef8f0825a9e6bdd464ace979bcc6
