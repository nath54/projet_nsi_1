# Persos_equipements 

Une table qui va être créée et attribuée à chaque nouveau perso, et qui va contenir les informations des objets que le perso possède

## Attributs : 

 - id : INT PRIMARY KEY AUTO_INCREMENT
 - type : INT (en fait ce sera juste l'index d'une liste en python qui contiendra toutes les informations relatives à tous les objets du jeu)
 - nombre : INT (le nombre d'objets possédés)


## Commande pour créer la table (à exécuter dans python au moment de la création du perso) :

`cursor.execute(f"CREATE TABLE {nom_de_la_variable_contenant_le_nom_de_la_table} (id INT PRIMARY KEY AUTO_INCREMENT, type INT, nombre INT);",)`
`cursor.commit()`
