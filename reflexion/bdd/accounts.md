# Accounts

## Attributs :
 
 - id : INT PRIMARY KEY AUTO_INCREMENT
 - pseudo : TEXT
 - email : TEXT (si jamais l'utilisateur perd sont mot de passe, faudra réussir a envoyer un mail grâce à python à l'email)
 - password : TEXT
 - perso_id : INT (la clé de la table perso correspondate)

## Commande pour créer la table :

`CREATE TABLE accounts (id INT PRIMARY KEY AUTO_INCREMENT, pseudo TEXT, email TEXT, password TEXT, perso_id INT);`
