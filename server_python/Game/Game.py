"""CECI EST LA PARTIE QUI GERE LE JEU."""

# Imports :
from Game.Map.Map import Map
from Game.Map.Lieux.Lieu import Lieu
from Game.Objets.Objet import Objet
from Game.Quetes.Quete import Quete
from Game.Etres.Perso import Perso
from Game.Etres.Pnjs.Pnj import Pnj
from Game.Etres.Ennemis.Ennemi import Ennemi


class Game:
    """
    Classe de la partie.

    Attributes:
        map_(Map): Référence à la map du jeu

    """

    def __init__(self):
        """Initie ce qui est essentiel pour le jeu (Map).

        Auteur: Nathan

        """
        self.client_db = None

        self.Map = Map
        self.Lieu = Lieu
        self.Objet = Objet
        self.Quete = Quete
        self.Perso = Perso
        self.Pnj = Pnj
        self.Ennemi = Ennemi
        self.map_ = Map()
        # TODO
        pass

    def start(self):
        """???.

        Auteur: Nathan

        """
        self.map_.load_from_json(self)
        print("Débuggage (on vérifie que ça a bien tout créé)")
        print("\nListe des lieux : ")
        print(self.map_.lieux)
