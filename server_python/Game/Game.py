"""CECI EST LA PARTIE QUI GERE LE JEU."""

# Imports :
from Game.Map.Map import Map
from Game.Map.Lieux.Lieu import Lieu
from Game.Objets.Objet import Objet
from Game.Quetes.Quete import Quete
from Game.Etres.Perso import Perso
from Game.Etres.Pnjs.Pnj import Pnj
from Game.Etres.Ennemis.Ennemi import Ennemi

import os


class Game:
    """
    Classe de la partie.

    Attributes:
        map_(Map): Référence à la map du jeu

    """

    def __init__(self, jload):
        """Initie ce qui est essentiel pour le jeu (Map).

        Auteur: Nathan

        """
        self.jload = jload

        self.client_db = None
        self.races = {}
        self.classes = {}

        self.load_races_classes()

        self.Map = Map
        self.Lieu = Lieu
        self.Objet = Objet
        self.Quete = Quete
        self.Perso = Perso
        self.Pnj = Pnj
        self.Ennemi = Ennemi
        self.map_ = Map()

        self.server = None

    def start(self):
        """Lance le moteur de jeu.

        Auteur: Nathan

        """
        self.map_.load_from_bdd(self)
        print("Débuggage (on vérifie que ça a bien tout créé)")
        print("\nListe des lieux : ")
        print(self.map_.lieux)

    def load_races_classes(self):
        for fich in os.listdir("Data/races/"):
            data = self.jload("Data/races/" + fich)
            self.races[data["nom"]] = data

        for fich in os.listdir("Data/classes/"):
            data = self.jload("Data/classes/" + fich)
            self.classes[data["nom"]] = data

    def get_all_persos_lieu(self, id_lieu):
        persos = []
        for cl in self.server.clients.values():
            perso = cl["player"].perso
            if perso is not None and perso.lieu == id_lieu:
                persos.append(perso)
        return persos
