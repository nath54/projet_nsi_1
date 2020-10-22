# Perso : 

## Attributs : 

 - nom:str,              le nom du personnage
 - race:str,             la race du personnage
 - classe:str,           la classe du personnage
 - vie_totale:int,       la vie totale du perso
 - vie:int,              la vie actuelle du perso
 - energie_totale:int,   l'énergie totale du perso (rassemblement du mana et de l'endurance traditionnels)
 - energie:int,          l'énergie actuelle du perso
 - force:int,            la force des personnages, permet par exemple de mettre en force minimale pour manier une arme correctement
 - intelligence:int,     l'intelligence du personnage, permet par exemple de lire des livres, recevoir des astuces
 - charme:int,           le niveau de charme, de charisme du personnage, permet d'avoir des avantages dans des discussions, des prix plus faibles dans les boutiques...
 - discretion:int,       permet de dérober des objets/de s'infiltrer (orientation voleur)
 - équipements:dict,     l'équipement du personnage {arme,armure tete, armure torse, armure jambes, armure bras, collier, bague droit, bague gauche} (Est-ce qu'on fait vraiment AUTANT d'équipement ?)
 - inventaire:list,      la liste des possessions du personnage
 - lieu:int/Lieu,        l'id ou l'instance de la classe lieu du personnage (utilisation de CONSTANTE)
 - effets:list,          liste des effets sur le personnage

## méthodes



