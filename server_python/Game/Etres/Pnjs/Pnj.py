
import os
import sys
import json
# import ../Etre.py
from Etre import Etre

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# triés par leurs id
data_pnjs = [
    "../../../Data/pnjs/paysan_tergaron_vieu1.json"
]


class Pnj(Etre):
    def __init__(self, index):
        super.__init__(self)
        self.index = index
        self.dialogue = None
        if self.index > len(data_pnjs)-1:
            raise IndexError("Problème avec pnj, mauvais index :", self.index)
        self.load()

    def __str__(self):
        return f"""
Pnj :
  - nom : {self.nom}
  - description : {self.description}
  - race : {self.race}"""

    def load(self):
        """Crée un PNJ à partir de son ID

        Les infos du PNJ sont récupérées à partir d'un fichier .json

        Author : Nathan

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


if __name__ == "__main__":
    p = Pnj(0)
    print(p)
