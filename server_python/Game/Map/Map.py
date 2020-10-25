import io
import json
import os


class Map:
    """Classe qui gérera la map du jeu"""
    def __init__(self):
        self.lieux = {}
        pass

    def load_from_json(self, Lieu, Objet, Pnj, Perso, Ennemi):
        """Permet de charger la map depuis un fichier .json

        Author: Nathan

        """
        emplacement = "Data/map/"
        for fichier in os.listdir(emplacement):
            f = io.open(emplacement+fichier, "r", encoding="utf-8")
            data = json.loads(f.read())
            self.create_lieu(data, Lieu, Objet, Pnj, Perso, Ennemi)
            f.close()

    def create_lieu(self, datalieu, Lieu, Objet, Pnj, Perso, Ennemi):
        """Instancie un lieu

        Args:
            datalieu(dict): ???

        Author: Nathan

        """
        lieu = Lieu()
        lieu.map_ = self
        dk = datalieu.keys()
        if "id" not in dk:
            # On pourrait aussi renvoyer une indexError
            return
        idl = datalieu["id"]
        if "nom" in dk:
            lieu.nom = datalieu["nom"]
        if "description" in dk:
            lieu.description = datalieu["description"]
        if "pnjs" in dk:
            for pid in datalieu["pnjs"]:
                lieu.pnjs.add(Pnj(pid))
        if "ennemis" in dk:
            for pid in datalieu["ennemis"]:
                if type(pid) == int:
                    lieu.ennemis.add(Ennemi(pid))
                # TODO : Trouver un système où il pourrait y avoir plusieurs
                #        fois le même objet, je pensais à un attribut nombre
                """
                elif type(pid)==list:
                    for _ in range(pid[1]):
                        lieu.ennemis.add(Ennemi(pid[0]))
                """
        if "objets" in dk:
            for pid in datalieu["objets"]:
                if type(pid) == int:
                    lieu.objets.add(Objet(pid))
                # TODO : Trouver un système où il pourrait y avoir plusieurs
                #        fois le même objet, je pensais à un attribut nombre
                """
                elif type(pid)==list:
                    for _ in range(pid[1]):
                        lieu.objets.add(Objet(pid[0]))
                """
        if "lieux" in dk:
            lieu.lieux_accessibles = datalieu["lieux"]
        self.lieux.append(lieu)
