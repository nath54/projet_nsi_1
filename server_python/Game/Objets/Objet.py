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

    def __init__(self, index, game):
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

        self.nom = datas[0]
        self.description = datas[1]
        self.type = datas[2]
        self.effet_utilise = datas[3]
        self.contenu = json.loads(datas[4])
        self.verrouille = datas[5]
        self.ouvert = datas[6]

    # def load(self, important=True):
    #     """Charge l'objet.

    #     Args:
    #         important(bool):  True: L'absence de l'objet provoque une erreur
    #                          False: L'absence de l'objet provoque un print

    #     Auteur: Hugo (d'une idée originale de Nathan)

    #     """
    #     self = self.game.client_db.get_obj_from_DB(self.index)
    #     if datas is not None:
    #         self.nom = datas[0]
    #         self.description = datas[1]
    #         self.type = datas[2]
    #         self.effet_utilise = datas[3]
    #     else:
    #         err = f"L'indice {self.index} ne correspond à aucun objet"
    #         if important:
    #             raise IndexError(err)
    #         else:
    #             print(err)

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
