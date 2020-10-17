# Persos

Modèle incomplet, à compléter...

## Attributs :
 

 - id : INT PRIMARY KEY AUTO_INCREMENT
 - account_id : INT (la clé de la table perso correspondate)
 - nom : TEXT
 - classe : TEXT 
 - race : TEXT
 - niveau : INT

 - force : INT
 - intelligence : INT
 - charme : INT
 - discression : INT
 
 - experience_totale : INT (on va éviter les accents pour sql)
 - experience : INT
 - vie_totale : INT
 - vie : INT
 - energie_totale : INT
 - energie : INT
 - equipement : ??? (J'hésite à mettre un type TEXT et que ce soit le nom de la table qui va être créée et qui va contenir les informations sur son équipement)

## Commande pour créer la table :

`CREATE TABLE persos (id INT PRIMARY KEY AUTO_INCREMENT, nom TEXT, classe TEXT, race TEXT, niveau INT, force INT, intelligence INT, charme INT, discression INT, experience_totale INT, experience INT, vie_totale INT, vie INT, energie_totale INT, energie INT, equipement ???);`
