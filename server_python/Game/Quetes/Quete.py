class Quete:
    """Classe d'une quête

    Cet objet est créé lorsqu'un joueur accepte une quête
    (ou est forcé d'en faire une)

    Attributs :

     - id(int) : Identifiant unique de la quête
     - nom(string) : Nom de la quête
     - description(string) : Description de la quête
     - compteur(int) : Valeur de l'action de la quête
                       (exemple: nombre de gobelins tués)
     - nb_a_faire(int) : Nombre d'actions à faire (exemple: 15 gobelins à tuer)
     - etat(string) : État de la quête ("en cours","réussi","échec")
     - perso(Perso) : Joueur ayant accepté la quête
     - quete_suivante(Quete) : Si la quête a une suite

    TODO: Il faudra donc penser à une fonction pour chaque objet du jeu ou
    ennemi ou pnj et voire même perso qui, lorsqu'une action est effectuée,
    vérifie s'il n'y a pas eu de changements dans les quêtes

    """
    def __init__(self):
        """Initialise la quête"""
        self.id = 0
        self.nom = "Nom"
        self.description = "Description"
        self.compteur = 0
        self.nb_a_faire = 0
        self.etat = "en cours"
        self.perso = None
        self.quete_suivante = None
        # TODO
        pass

    def finir(self):
        # TODO
        pass

    def affichage(self):
        """Affiche le contenu d'une quête.

        Fonction qui permettra d'afficher une présentation de la quête.

        """
        # TODO
        pass
