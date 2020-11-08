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
        self.vie_totale = random.randint(datas["vie"][0], datas["vie"][1])
        self.vie = self.vie_totale
        self.effets_attaque = datas.get("attaque_effets", {})
        self.agressivite = datas.get("agressivite", 0)
        # endregion
        if nb != -1:
            self.nom += "-" + str(nb)

    def tour(self, lieu):
        """Fonction appelée au tour de l'ennemi

        Auteur: Nathan

        """
        if random.randint(0, 100) <= self.agressivite:  # si l'ennemi attaque
            persos_l = self.game.get_all_persos_lieu(lieu)  # on recupere tous les persos dans ce lieu
            #
            if len(persos_l) >= 1:  # s'il y a des persos dans ce lieu
                # on va d'abord choisir le type d'attaque de l'ennemi
                # comme ca, si l'ennemi n'a pas d'attaques disponnibles,
                # on ne va pas aller chercher tous les persos d'un lieu inutiliement
                tp_att = "corps à corps"
                cac = self.get_attaque("corps à corps")
                dist = self.get_attaque("distance")
                if cac is None and dist is None:  # l'ennemi ne peut pas attaquer
                    return
                elif cac is None:
                    tp_att = "distance"
                elif dist is None:
                    tp_att = "corps à corps"
                else:
                    if self.moy_lst(cac) > self.moy_lst(dist):
                        tp_att = "corps à corps"
                    else:
                        tp_att = "distance"
                # on va chercher un personnage cible
                p_cible = None
                for p in persos_l:
                    if p.classe == "tank":  # on attaque en priorité les tanks
                        p_cible = p
                #
                if p_cible is None:  # s'il n'y a pas de tanks dans ce lieu, on prend la premiere perso dans ce lieu
                    p_cible = persos_l[0]
                # l'ennemi va attaquer le perso cible
                mess = self.attaque_cible(p_cible, tp_att)
                mess = json.dumps({"type": "message", "value": mess})
                self.game.server.send_all(mess)

    def __str__(self):
        """Renvoie une description de l'ennemi."""
        return f"""Ennemi :
        - nom : {self.nom}
        - description : {self.description}"""

    def __repr__(self):
        """Renvoie une description plus détaillée de l'ennemi

        Auteur: Nathan
        """
        return f"""
Ennemi :
    - nom : {self.nom}
    - race : {self.race}
    - description : {self.description}
    - vie : {self.vie} / {self.vie_totale}
    - attaque : {self.attaque}
    - esquive : {self.esquive}"""
