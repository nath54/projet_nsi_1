# Instructions

## Avoir une installation propre qui marche de mariadb

Il faut avoir mariadb d'installé, et il faut qu'il soit lancé lors de l'éxecution du programme

## Créer un compte `pyuser`

(note sur windows avec wamp64) : Sur windows vous pouvez trouver le programme mysql.exe à l'emplacement suivant : `C:\wamp64\mariadb\mariadb10.5.4\bin` ou a une autre version de mariadb suivant celle que vous avez installé.

Pour commencer, il faut avoir un terminal à portée de main, c'est plus facile.
Sur windows, du coup, il faut faire `cd C:\wamp64\mariadb\mariadb10.5.4\bin` avant de pouvoir faire la suite.

Il faut que vous vous connectiez ensuite à mysql en tant que root : `mysql -u root -p`
Puis il faut que vous créiez le compte qui sera utilisé par le programme : `CREATE USER pyuser@localhost IDENTIFIED BY "pypassword";`

## Créer la database `projet_nsi_1`

IL faut ensuite créer la database : `CREATE DATABASE projet_nsi_1;`

## Accorder tous les droits à `pyuser` sur cette derniere

Il faut ensuite s'y connecter : `USE projet_nsi_1;`
Et donner tous les droits à l'utilisateur pyuser : `GRANT ALL PRIVILEGES ON * TO pyuser@localhost;`
Vous pouvez ensuite vous déconnecter de mysql.

## Installer les dépendances python

Vous devez installer les librairies suivantes : `socket`, `mariadb`
et optionnellement `websockets` si vous voulez jouer au jeu sur un navigateur web.

`py -m pip install socket mariadb` ou `pip install socket mariadb`

## Lancer le serveur

Il faut que vous alliez dans le dossier `server_python`
et que vous lanciez le serveur grâce à : `py main_server.py` ou bien `python main_server.py`

## Lancer le client

Il faut que vous alliez dans le dossier `client_python`
et que vous lanciez le serveur grâce à : `py main_client.py` ou bien `python main_client.py`s



Enjoy :)
