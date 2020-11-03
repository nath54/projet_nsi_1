import os
import json

data_objs = [
    "Data/objets/pomme.json"
]


class Objet:
    """Classe définissant les objets.

    Attributes:
        index(int): Identifiant unique d'un objet.
        nom(str): Le nom de l'objet
        description(str): Description de l'objet
        type(str): Le type de l'objet
        effet_utilise(list/None): Effet qu'aura l'action d'utiliser l'objet
        contenu(list<Objet>): Liste des objets si c'est un contenant
        est_ouvert(bool): Est-ce que l'objet est ouvert ?

    Note:
        On pourra rajouter d'autres actions qui auront d'autres effets
        Si un effet_utilise est None, on ne peut pas utiliser l'objet

    """

    def __init__(self, index, game, num=0):
        """Créer un objet.

        Args:
            game(Game): Référence à la partie
            id(int): Index de l'objet à utiliser

        Auteur: Hugo, Nathan

        """
        self.index = index
        self.game = game
        datas = self.game.client_db.get_data_obj_DB(self.index)

        if datas is None:
            raise IndexError(f"Index de l'objet trop grand : {self.index}")

        self.nom = datas["nom"]
        if num != 0:
            self.nom += str(num)
        self.description = datas["description"]
        self.type = datas["type"]
        self.effets = datas["effets"]
        self.contenu = datas["contenu"]
        self.verrouille = datas["verrouille"]
        self.ouvert = datas["ouvert"]

    def __repr__(self):
        """Permet d'afficher une description de l'objet.

        Auteur: Hugo

        """
        n = "\n"
        if self.type == "décor":
            r = f"{2 * n}{self.nom}{n}{self.description}{2 * n}"
        else:
            r = f"{2 * n}{self.nom} ({self.type}){n}{self.description}{2 * n}"
        return r

    def format_contenu(self):
        """Formate le contenu d'un objet

        Auteur: Hugo

        """
        if len(self.contenu) > 0:
            res = f"Dans ce {self.nom}, vous trouvez :\n"
            for obj in self.contenu:
                res += f"\t- {obj.nom}\n"
        else:
            res = f"Dans ce {self.nom}, vous trouvez... À vrai dire pas grand chose."
        return res
