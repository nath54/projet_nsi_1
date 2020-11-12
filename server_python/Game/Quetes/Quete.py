class Quete:
    """Classe d'une quête.

    Cet objet est créé lorsqu'un joueur accepte une quête
    (ou est forcé d'en faire une)

    Attributs :

     - id(int) : Identifiant unique de la quête
     - nom(str) : Nom de la quête
     - description(str) : Description de la quête
     - compteur(int) : Valeur de l'action de la quête
                       (exemple: nombre de gobelins tués)
     - nb_a_faire(int) : Nombre d'actions à faire (exemple: 15 gobelins à tuer)
     - etat(str) : État de la quête ("en cours","réussi","échec")
     - perso(Perso) : Joueur ayant accepté la quête
     - quete_suivante(Quete) : Si la quête a une suite

    TODO: Il faudra donc penser à une fonction pour chaque objet du jeu ou
    ennemi ou pnj et voire même perso qui, lorsqu'une action est effectuée,
    vérifie s'il n'y a pas eu de changements dans les quêtes

    """

    def __init__(self, game, id_):
        """Initialise la quête."""
        self.game = game
        self.id = id_
        self.index = id_
        data = game.client_db.get_data_quetes_DB(self.index)
        self.nom = data["nom"]
        self.description = data["description"]
        self.compteur = 0
        self.nb_a_faire = 0
        self.etat = "en cours"
        self.quete_suivante = None
        # TODO
        pass

    def finir(self):
        """Permet de mettre fin à une quête.

        Doit donner les récompenses au joueur et l'enlever de son journal de
        quête.

        Auteur : TODO

        """
        # TODO
        pass

    def affichage(self):
        """Affiche le contenu d'une quête.

        Auteur : TODO

        """
        pass
