import os
import sys
import json
from Game.Etres.Etre import Etre

# triés par leurs id
data_pnjs = "Data/pnjs/"
data_ens = [pathd + f for f in os.listdir(pathd)]


class Pnj(Etre):
    """Classe des PNJ.

    Attributes:
        index(int): Identifiant unique du PNJ
        dialogue(str ???): Dialogue tenu par le PNJ quand on l'interpelle.

    """

    def __init__(self, id_, game):
        """Instancie le PNJ.

        Args:
            id_(int): Identiant unique du PNJ

        Auteur: Hugo

        """
        Etre.__init__(self, game)
        self.index = id_
        datas = game.client_db.get_data_Pnj_DB(id_)
        if datas is None:
            raise IndexError("Problème avec pnj, mauvais index :", self.index)
        self.nom = datas.get("nom", "Personnage Non Joueur. PNJ pour les intimes.")
        self.description = datas.get("desc", "")
        self.race = datas.get("race", "humain")
        self.dialogue = datas.get("dialogue", {})

    def __str__(self):
        """Renvoie une description du PNJ."""
        return f"""
Pnj :
  - nom : {self.nom}
  - description : {self.description}
  - race : {self.race}"""

    def load(self):
        """Crée un PNJ à partir de son ID.

        Les infos du PNJ sont récupérées à partir d'un fichier .json

        Auteur : Nathan

        """
        if os.path.exists(data_pnjs[self.index]):
            f = open(data_pnjs[self.index])
            data = json.loads(f.read())
            f.close()

            dk = data.keys()
            if "type" in dk:
                self.type = data["type"]
            if "nom" in dk:
                self.nom = data["nom"]
            if "description" in dk:
                self.description = data["description"]
            if "race" in dk:
                self.race = data["race"]
            if "dialogue" in dk:
                self.dialogue = data["dialogue"]
