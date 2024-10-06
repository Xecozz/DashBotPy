# Dashboard Project

Ce projet est une application web de tableau de bord intégrant des fonctionnalités d'authentification Discord et un bot Discord.

## Structure du projet

### Dossiers principaux

- **Dashboard/** : Contient les fichiers principaux de l'application web, y compris les modèles, les vues et les tests.
- **discordAuth/** : Gère l'authentification via Discord.
- **DiscordBot/** : Contient le code du bot Discord.
- **env/** : Environnement virtuel pour les dépendances Python.
- **media/** : Contient les fichiers médias téléchargés par les utilisateurs.
- **packages/** : Contient les packages supplémentaires utilisés par le projet.
- **src/** : Contient le code source supplémentaire.
- **templates/** : Contient les fichiers de templates HTML.
- **theme/** : Contient les fichiers de thème pour l'application.

## Prérequis

- Python 3.x
- pip (Python package installer)
- Un environnement virtuel (recommandé)

## Installation

1. Clonez le dépôt :

   ```sh
   git clone <URL_DU_DEPOT>
   cd <NOM_DU_DEPOT>
   ```

2. Créez et activez un environnement virtuel :

   ```sh
   python -m venv env
   source env/bin/activate  # Sur Windows, utilisez `env\Scripts\activate`
   ```

3. Installez les dépendances :

   ```sh
   pip install -r requirements.txt
   ```

4. Configurez les variables d'environnement en utilisant le fichier `.env`.

## Utilisation

1. Appliquez les migrations de la base de données :

   ```sh
   python manage.py migrate
   ```

2. Lancez le serveur de développement :

   ```sh
   python manage.py runserver
   ```

3. Accédez à l'application via `http://127.0.0.1:8000/`.
