import os
import json

data_objs = [
    "Data/objets/pomme.json"
]


class Objet:
    """Classe définissant les objets

    Attributes:
        nom(str): Le nom de l'objet
        description(str): Description de l'objet
        type_(str): Le type de l'objet
        effet_utilise(list/None): Effet qu'aura l'action d'utiliser l'objet

    Note:
        On pourra rajouter d'autres actions qui auront d'autres effets
        Si un effet_utilise est None, on ne peut pas utiliser l'objet

    """
    def __init__(self, index):
        """Créer un objet

        Args:
            index(int): Index de l'objet à utiliser

        Author: Hugo, Nathan

        """
        self.index = index
        if self.index > len(data_objs) - 1:
            raise IndexError(f"Index de l'objet trop grand : {self.index}")

        self.nom = "Objet"
        self.description = "Un objet"
        self.type = "objet"
        self.effet_utilise = None
        # on charge l'objet
        self.load()

    def load(self):
        """Charge l'objet

        Author: Nathan

        """
        if os.path.exists(data_objs[self.index]):
            f = open(data_objs[self.index])
            data = json.loads(f.read())
            f.close()

            dk = data.keys()
            if "type" in dk:
                self.type = data["type"]
            if "nom" in dk:
                self.nom = data["nom"]
            if "description" in dk:
                self.description = data["description"]
            if "effets_utilise" in dk:
                self.effet_utilise = data["effets_utilise"]

            # Il faudra sans doute rajouter d'autres effets dans le futur

    def __repr__(self):
        """Permet d'afficher une description de l'objet

        Author: Hugo

        """
        n = "\n"
        return f"{2 * n}{self.nom} ({self.type}){n}{self.description}{2 * n}"
