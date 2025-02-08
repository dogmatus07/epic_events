# Epic Events CRM
### CRM sécurisé pour gérer les contrats et événements
Epic Events est une application en ligne de commande qui permet de gérer les contrats et les événements associés à une entreprise.
L'application est conçue avec **Python, SQLAlchemy et SQLite**

---
## Installation

### Clôner le dépôt

`git clone https://github.com/dogmatus07/epic_events.git`

`cd epic_events`

### Créer et activer un environnement virtuel
`python -m venv env`

#### Sous Windows
`env\Scripts\activate`

#### Sous Mac/Linux
`source env/bin/activate`

### Installer les dépendances
`pip install -r requirements.txt`

## Initialiser la base de données

### Générer la base de données
`python crm/db/init_db.py`

#### Notes
Ce que le script init_db.py va faire : 
1. Créer les tables (Utilisateurs, Rôles, Clients, Contrats et Événements)
2. Peupler la base avec des utilisateurs par défaut : 
   - admin1@epicevents.com
   - admin2@epicevents.com
   - commercial1@epicevents.com
   - commercial2@epicevents.com
   - support1@epicevents.com
   - support2@epicevents.com
3. Le mot de passe par défaut est : epic-evenTs2025 pour tous les utilisateurs.

## Lancer l'application
`python main.py`

L'application va demander une authentification afin d'accéder au menu principal.

Exemples : 
- Utilisateur Gestion : admin1@epicevents.com
- Utilisateur Commercial : commercial1@epicevents.com
- Utilisateur Support : support1@epicevents.com

## Fonctionnalités
- Authentification sécurisée
- Gestion des utilisateurs (CRUD)
- Gestion des clients (CRUD)
- Gestion des contrats (CRUD)
- Gestion des événements (CRUD)
- Assigner les événements à la team support
- Filtrage des événements

## Fonctionnement de l'application Epic Events CRM