import os
import sys
import json
from Game.Etres.Etre import Etre

# triés par leurs id
data_pnjs = [
    "Data/pnjs/paysan_tergaron_vieu1.json"
]


class Pnj(Etre):
    """Classe des PNJ.

    Attributes:
        index(int): Identifiant unique du PNJ
        dialogue(str ???): Dialogue tenu par le PNJ quand on l'interpelle.

    """

    def __init__(self, index, game):
        """Instancie le PNJ.

        Args:
            index(int): Identiant unique du PNJ

        Auteur: Nathan

        """
        Etre.__init__(self, game)
        self.index = index
        self.dialogue = None
        if self.index > len(data_pnjs) - 1:
            raise IndexError("Problème avec pnj, mauvais index :", self.index)
        self.load()

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
                print("PPPPPPNNNNNNNNNJJJJJJJJ : ",nom)
            if "description" in dk:
                self.description = data["description"]
            if "race" in dk:
                self.race = data["race"]
            if "dialogue" in dk:
                self.dialogue = data["dialogue"]
