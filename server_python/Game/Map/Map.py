import io
import json
import os


class Map:
    """Classe qui gérera la map du jeu"""
    def __init__(self):
        self.lieux = []
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
        dk = datalieu.keys()
        if "nom" in dk:
            lieu.nom = datalieu["nom"]
        if "description" in dk:
            lieu.description = datalieu["description"]
        if "pnjs" in dk:
            for pid in datalieu["pnjs"]:
                lieu.pnjs.add(Pnj(pid))
        if "ennemis" in dk:
            # TODO
            pass
        if "objets" in dk:
            for pid in datalieu["objets"]:
                lieu.objets.add(Objet(pid))
        if "lieux" in dk:
            # TODO
            pass
        self.lieux.append(lieu)
