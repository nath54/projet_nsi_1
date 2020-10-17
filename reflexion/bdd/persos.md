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
 - equipement : TEXT (on va utiliser un text de la forme (on dira que "|" et "&" sont des séparateurs) : "type de l'objet & nombre possédé(s) | type de l'objet2 & nombre possédé(s)" que l'on pourra donc split avec python)

## Commande pour créer la table :

`CREATE TABLE persos (id INT PRIMARY KEY AUTO_INCREMENT, nom TEXT, classe TEXT, race TEXT, niveau INT, force INT, intelligence INT, charme INT, discression INT, experience_totale INT, experience INT, vie_totale INT, vie INT, energie_totale INT, energie INT, equipement TEXT);`
