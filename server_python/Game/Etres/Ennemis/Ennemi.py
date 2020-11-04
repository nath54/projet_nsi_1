import os
import json
import random
from Game.Etres.Combattant import Combattant

pathd = "Data/ennemis/"
data_ens = [pathd + f for f in os.listdir(pathd)]


class Ennemi(Combattant):
    """Classe de base de l'Ennemi.

    Attributes:
        index(int): Identifiant unique de l'ennemi

    """

    def __init__(self, id_, game, nb=-1):
        """Instancie l'ennemi.

        Args:
            index(int): Identifiant unique de l'ennemi

        Auteur: Nathan

        """
        Combattant.__init__(self, game)
        self.index = id_
        if self.index > len(data_ens) - 1:
            raise IndexError("Mauvais index d'ennemi :", self.index)
        # region LOAD
        datas = game.client_db.get_data_Ennemi_DB(self.index)
        self.nom = datas["nom"]
        self.type_ = datas["type"]
        self.description = datas["description"]
        self.attaque = datas["attaque"]
        self.vie = random.randint(datas["vie"][0], datas["vie"][1])
        self.effets_attaque = datas["attaque_effets"]
        # endregion
        if nb != -1:
            self.nom += "-"+str(nb)        

    def __str__(self):
        """Renvoie une description de l'ennemi."""
        return f"""Ennemi :
        - nom : {self.nom}
        - description : {self.description}"""

    def load(self):
        """Crée un Ennemi à partir de son ID.

        Les infos du Ennemi sont récupérées à partir d'un fichier .json

        Auteur : Nathan

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
                self.vie_totale = random.randint(data["vie"][0],
                                                 data["vie"][1])
                self.vie = self.vie_totale
            if "attaque" in dk:
                self.attaque = random.randint(data["attaque"][0],
                                              data["attaque"][1])
            if "attaque_effets" in dk:
                self.attaque_effets = data["attaque_effets"]
