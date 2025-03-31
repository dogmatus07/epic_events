# Epic Events CRM
### CRM sécurisé pour gérer les contrats et événements
Epic Events est une application en ligne de commande qui permet de gérer les contrats et les événements associés à une entreprise.
L'application est conçue avec **Python, SQLAlchemy et SQLite**

---

## Fonctionnalités principales
- Authentification JWT sécurisée
- Rôles utilisateurs : Commercial, Support, Gestion
- Création, lecture, modification et suppression de :
  - Clients 👤 
  - Contrats 📄 (avec filtres : signé, payé...)
  - Evénements 🗓️ (réservés aux contrats existants)
- Interface colorée et lisible grâce à Rich
- Journalisation des erreurs avec Sentry
- Tests automatisés avec Pytest et rapports de couverture

## Stack
|                 Composants | Techno ou Librairie |
|-----------------------|---------------------|
|               Langage | Python 3.9.6        |
|                        ORM | SQLAlchemy          |
|            Base de données | SQLite              |
|           Authentification | JWT                 |
| Journalisation des erreurs | Sentry              |
|          Tests automatisés | Pytest              |
|      Interface utilisateur | Rich                |

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
3. Etant donné qu'il s'agit d'un projet dans le cadre d'une formation, toutes les données ici sont factices et ne sont pas réels. Il a donc été défini un mot de passe par défaut qui est : epic-evenTs2025 pour tous les utilisateurs. 

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
L'application Epic Events CRM est une application en ligne de commande qui permet de gérer les contrats et les événements associés à une entreprise.
Elle est conçue pour être utilisée par trois types d'utilisateurs : les gestionnaires, les commerciaux et le support. Chaque type d'utilisateur a des droits d'accès différents et peut effectuer des actions spécifiques dans l'application.

### Utilisateurs
L'application dispose de trois types d'utilisateurs :
1. **Gestionnaire** : 
   - Peut créer, modifier et supprimer des utilisateurs, des clients et des contrats.
   - Peut assigner des événements à la team support.
   - Peut filtrer les événements par date, client ou statut.
   - Peut afficher la liste des événements.
   - Peut afficher la liste des utilisateurs.
   - Peut afficher la liste des clients.
   - Peut afficher la liste des contrats.

2. **Commercial** :
   - Peut créer et mettre à jour des clients.
   - Peut mettre à jour des contrats.
   - Peut créer des événements.
   - Peut afficher la liste des événements.
   - Peut afficher la liste des clients.
   - Peut afficher la liste des contrats.

3. **Support** :
   - Peut afficher la liste des événements.
   - Peut mettre à jour ses propres événements.

### Authentification
L'application utilise une authentification sécurisée pour garantir que seuls les utilisateurs autorisés peuvent accéder aux fonctionnalités de l'application. Lors de la connexion, l'utilisateur doit entrer son adresse e-mail et son mot de passe. Si les informations d'identification sont valides, l'utilisateur est redirigé vers le menu principal de l'application.
### Menu principal
Le menu principal de l'application est affiché après la connexion réussie. Il présente les options disponibles en fonction du type d'utilisateur connecté. Les utilisateurs peuvent naviguer dans le menu en entrant le numéro de l'option souhaitée.
### Gestion des utilisateurs
Les gestionnaires peuvent créer, modifier et supprimer des utilisateurs. Ils peuvent également afficher la liste des utilisateurs existants. Les commerciaux et le support ne peuvent pas gérer les utilisateurs.
### Gestion des clients
Les commerciaux peuvent créer et mettre à jour des clients. Ils peuvent également afficher la liste des clients existants. Les gestionnaires peuvent également gérer les clients.
### Gestion des contrats
Les commerciaux peuvent mettre à jour des contrats. Ils peuvent également afficher la liste des contrats existants. Les gestionnaires peuvent également gérer les contrats.
### Gestion des événements
Les gestionnaires peuvent assigner des événements à la team support. Les commerciaux peuvent créer des événements et afficher la liste des événements existants. Le support peut mettre à jour ses propres événements.
### Filtrage des événements
Les gestionnaires peuvent filtrer les événements par date, client ou statut. Ils peuvent également afficher la liste des événements existants.
### Mise à jour des événements
Les gestionnaires assignent les événements au support. Le support peut ensuite mettre à jour leurs propres événements.
### Affichage des événements
Les gestionnaires, les commerciaux et le support peuvent afficher la liste des événements existants. Les événements sont affichés avec leurs détails, y compris le client associé, la date de l'événement et le statut.
### Gestion des erreurs
L'application gère les erreurs courantes, telles que les entrées invalides ou les tentatives de connexion échouées. Des messages d'erreur appropriés sont affichés pour aider l'utilisateur à corriger ses erreurs.

### Organisation du projet

Le projet est organisé de la manière suivante :
```
crm/
├── controllers/
├── repositories/
├── utils/
├── views/
├── models/
├── db/
├── utils/
main.py
.env
requirements.txt
tests/
```

### Sécurité & Journalisation
- Toutes les erreurs critiques sont remontées automatiquement à Sentry
- Les exceptions sont capturées dans les controllers et les vues critiques
- Le code suit les recommandations OWASP de base :
  - Validation des données utilisateur
  - Pas de mot de passe stocké en clair
  - Utilisation d'ORM pour éviter les injections SQL


### Contribuer
Si vous souhaitez contribuer à l'application Epic Events CRM, n'hésitez pas à soumettre des demandes de tirage (pull requests) ou à signaler des problèmes (issues) sur le dépôt GitHub.
### Auteurs
Steve RAHARISON