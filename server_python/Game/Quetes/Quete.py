
class Quete:
    """classe d'une quete

    Cet objet est créé lorsqu'un joueur accepte une quete (ou est forcé d'en faire une)

    Attributs :

     - id(int) : l'identifiant de la quete (unique parmi toutes les quetes du jeu)
     - nom(string) : nom de la quete
     - description(string) : description de la quete
     - compteur(int) : valeur de l'action de la quete (exemple: nombre de goblins tués)
     - nb_a_faire(int) : nombre d'actions a faire (exemple: 15 goblins a tuer)
     - etat(string) : l'état de la quete ("en cours","réussi","échec")
     - perso(Perso) : le joueur qui a accepté la quete
     - quete_suivante(Quete) : Si la quete a une suite 

    Il faudra donc penser à une fonction pour chaque objet du jeu ou ennemi ou pnj et voire meme perso qui lorsqu'une action est effectuée, vérifie s'il n'y a pas eu de changements dans les quetes

    """
    def __init__(self):
        self.id=0
        self.nom="Nom"
        self.description="Description"
        self.compteur=0
        self.nb_a_faire=0
        self.etat="en cours"
        self.perso=None
        self.quete_suivante=None
        #TODO
        pass
    
    def finir(self):
        #TODO
        pass

    def affichage(self):
        """lorsque le joueur souhaite afficher son journal de quete
        on appelera cette fonction pour chaque quete du joueur
        """
        #TODO
        pass
