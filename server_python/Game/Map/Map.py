import io
import json
import os

class Map:
    """Classe qui gérera la map du jeu"""
    def __init__(self):
        self.lieux = []
        pass

    def load_from_json(self):
        """Permet de charger la map depuis un fichier .json

        Author: Nathan

        """
        emplacement = "Data/map/"
        for fichier in os.listdir(emplacement):
            f = io.open(emplacement+fichier, "r", encoding="utf-8")
            data = json.loads(f.read())
            print(data)
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
            #TODO
            pass
        if "ennemis" in dk:
            #TODO
            pass
        if "objets" in dk:
            #TODO
            pass
        if "lieux" in dk:
            #TODO
            pass
        self.lieux.append(lieu)


if __name__ == "__main__":
    map = Map()
    map.load_from_json()
