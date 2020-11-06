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
        datas = game.client_db.get_data_Ennemi_DB(self.index)
        if datas is None:
            raise IndexError(f"Cet ennemi n'existe pas : {id_}")
        self.nom = datas["nom"]
        self.type_ = datas["type"]
        self.description = datas["description"]
        self.attaque = datas["attaque"]
        self.vie = random.randint(datas["vie"][0], datas["vie"][1])
        self.effets_attaque = datas["attaque_effets"]
        # endregion
        if nb != -1:
            self.nom += "-" + str(nb)

    def __str__(self):
        """Renvoie une description de l'ennemi."""
        return f"""Ennemi :
        - nom : {self.nom}
        - description : {self.description}"""

    def __repr__(self):
        """Renvoie une description plus détaillée de l'ennemi

        Author: Nathan
        """
        return f"""
Ennemi :
    - nom : {self.nom}
    - race : {self.race}
    - description : {self.description}
    - vie : {self.vie} / {self.vie_totale}
    - attaque : {self.attaque}
    - esquive : {self.esquive}"""
