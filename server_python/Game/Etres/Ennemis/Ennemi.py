
import os
import json
import random
from Game.Etres.Etre import Etre

data_ens=[
    "Data/ennemis/rat.json"
]

class Ennemi(Etre):
    """Classe de base de l'Ennemi

    Attributes:

    """
    def __init__(self,index):
        Etre.__init__(self)
        self.index=index
        if self.index > len(data_ens)-1:
            raise IndexError("Problème avec pnj, mauvais index :", self.index)
        self.load()

    def __str__(self):
        return f"""
Pnj :
  - nom : {self.nom}
  - description : {self.description}"""

    def load(self):
        """Crée un Ennemi à partir de son ID

        Les infos du Ennemi sont récupérées à partir d'un fichier .json

        Author : Nathan

        """
        if os.path.exists(data_ens[self.index]):
            f = open(data_ens[self.index])
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
            if "vie" in dk:
                self.vie_totale = random.randint(data["vie"][0],data["vie"][1])
                self.vie = self.vie_totale
            if "attaque" in dk:
                self.attaque = random.randint(data["attaque"][0],data["attaque"][1])
            if "attaque_effets" in dk:
                self.attaque_effets = data["attaque_effets"]
