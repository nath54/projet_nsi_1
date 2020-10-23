
import os
import json


data_objs=[
    "Data/objets/pomme.json"
]




class Objet:
    """Classe définissant les objets

    Attributes:
        nom(str): Nom de l'objet
        description(str): Description de l'objet (Lore/renseignement)
        type(str): Type de l'objet (Consommable, Équipement, Objet-Clé)
        effet(str): Écrit comme du code Python, effet de l'objet consommé

    """
    def __init__(self, index):
        """Créer un objet

        Args:
            nom(str): Le nom de l'objet
            description(str): Description de l'objet
            type_(str): Le type de l'objet
            effet_utilise(list/None): Effet qu'aura l'action d'utiliser l'objet
            note : on pourra imaginer rajouter d'autres actions qui auront d'autres effets
            note : si un effet_utilise est None, on ne peut pas utiliser l'objet

        Author: Hugo,Nathan

        """
        self.index=index
        if self.index > len(data_objs)-1:
            raise IndexError("Problème avec objet, mauvais index :", self.index)

        self.nom = "Objet"
        self.description = "Un objet"
        self.type = "objet"
        self.effet_utilise = None
        #on charge l'objet
        self.load()

    def load(self):
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
            
            # il faudra sans doute rajouter d'autres effets dans le futur


    def __repr__(self):
        """Permet d'afficher une description de l'objet

        Author: Hugo

        """
        n = "\n"
        return f"{2 * n}{self.nom} ({self.type}){n}{self.description}{2 * n}"

