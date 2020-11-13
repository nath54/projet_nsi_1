# Instructions

## Avoir une installation propre qui marche de mariadb

Il faut avoir mariadb d'installé, et il faut qu'il soit lancé lors de l'éxecution du programme


## Installer les dépendances python

Vous devez installer les librairies suivantes : `socket`, `mariadb`
et optionnellement `websockets` si vous voulez jouer au jeu sur un navigateur web.

`py -m pip install socket mariadb` ou `pip install socket mariadb`

## Initialisation de la base de donnée :

Vous pouvez essayer lancer le programme python `init_projet.py` avec python au premier lancement du programme.
Il va crééer le compte `pyuser` et la database `projet_nsi_1`.
Vous devrez juste rentrer le compte et le mot de passe root, ne vous inquietez pas,
le programme va juste créer un compte et une database, il ne va rien faire d'autre,
Vous pouvez meme regarder dans le programme si vous voulez vraiment en être sûr.

Si le programme ne marche pas, ou que vous voulez faire les commandes manuellement,
vous pouvez suivre les instructions ci dessous.
Si le programme a bien marché, vous pouvez directement passer à la suite [ici](#lancer-le-serveur) (Lancer le serveur)

## Initialisation de la base de donnée (manuellement) :

### Créer un compte `pyuser`

(note sur windows avec wamp64) : Sur windows vous pouvez trouver le programme mysql.exe à l'emplacement suivant : `C:\wamp64\bin\mariadb\mariadb[version]\bin` ou a une autre version de mariadb suivant celle que vous avez installé.

Pour commencer, il faut avoir un terminal à portée de main, c'est plus facile.
Sur windows, du coup, il faut faire `cd C:\wamp64\bin\mariadb\mariadb[version]\bin` avant de pouvoir faire la suite.

Il faut que vous vous connectiez ensuite à mysql en tant que root : `mysql -u root -p`
Puis il faut que vous créiez le compte qui sera utilisé par le programme : `CREATE USER pyuser@localhost IDENTIFIED BY "pypassword";`

### Créer la database `projet_nsi_1`

IL faut ensuite créer la database : `CREATE DATABASE projet_nsi_1;`

### Accorder tous les droits à `pyuser` sur cette derniere

Il faut ensuite s'y connecter : `USE projet_nsi_1;`
Et donner tous les droits à l'utilisateur pyuser : `GRANT ALL PRIVILEGES ON * TO pyuser@localhost;`
Vous pouvez ensuite vous déconnecter de mysql.

## Lancer le serveur

### Rapidement

Windows :
 - Vous pouvez directement executer le fichier `start_server.bat` [ici](start_server.bat)

Linux :
 - Vous pouvez directement executer le fichier `start_server.sh` [ici](start_server.sh)

### Manuellement :

Il faut que vous alliez dans le dossier `server_python`
et que vous lanciez le serveur grâce à : `py main_server.py` ou bien `python main_server.py`

## Lancer le client

### Rapidement

Windows :
 - Vous pouvez directement executer le fichier `start_client.bat` [ici](start_client.bat)

Linux :
 - Vous pouvez directement executer le fichier `start_client.sh` [ici](start_client.sh)

### Manuellement :

Il faut que vous alliez dans le dossier `client_python`
et que vous lanciez le serveur grâce à : `py main_client.py` ou bien `python main_client.py`

# Informations supplémentaires :

Le jeu n'est pas encore fini, il manque des fonctionnalités dans le jeu comme la magie et les différents sorts,
que je rajouterai plus tard.
Et il y a sans doute d'autres fonctionnalités que je rajouterai plus tard,
c'est pour cela que des fois, dans le code, il y a des variables inutilisées pour l'instant,
ou des valeurs dans les tableaux inutilisés ou voire meme des fonctions inutilisées.

*Enjoy :)*
