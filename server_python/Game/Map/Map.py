import io
import json
import os


class Map:
    """Classe qui gérera la map du jeu.

    Attributes:
        lieux(dict<Lieu>): ???

    """

    def __init__(self):
        """Instancie la map du jeu."""
        self.lieux = {}
        pass

    def load_from_bdd(self, game):
        """Charge la map depuis la DB.

        Auteur : Nathan

        """
        id_lieux = game.client_db.get_lieux()
        for idl in id_lieux:
            lieu = game.Lieu(game, idl)
            lieu.map_ = self
            self.lieux[idl] = lieu

    def load_from_json(self, game):
        """Charge la map depuis un fichier `.json`.

        Auteur : Nathan

        """
        emplacement = "Data/map/"
        for fichier in os.listdir(emplacement):
            if fichier.endswith("json"):
                f = io.open(emplacement + fichier, "r", encoding="utf-8")
                data = json.loads(f.read())
                self.create_lieu(data, game)
                f.close()

    def create_lieu(self, datalieu, game):
        """Instancie un lieu.

        Args:
            datalieu(dict<???>): ???

        Auteur : Nathan

        """
        lieu = game.Lieu(game, datalieu["id"])
        lieu.map_ = self
        # dk = datalieu.keys()
        # if "id" not in dk:
        #     # On pourrait aussi renvoyer une indexError
        #     return
        # idl = datalieu["id"]
        # if "nom" in dk:
        #     lieu.nom = datalieu["nom"]
        # if "description" in dk:
        #     lieu.description = datalieu["description"]
        # if "pnjs" in dk:
        #     for pid in datalieu["pnjs"]:
        #         lieu.pnjs.append(game.Pnj(pid, game))
        # if "ennemis" in dk:
        #     for pid in datalieu["ennemis"]:
        #         if type(pid) == int:
        #             lieu.ennemis.append(game.Ennemi(pid, game))
        #         elif type(pid) == list:
        #             for _ in range(pid[1]):
        #                 lieu.ennemis.append(game.Ennemi(pid[0], game))

        #         # TODO : Trouver un système où il pourrait y avoir plusieurs
        #         #        fois le même objet

        # if "objets" in dk:
        #     for pid in datalieu["objets"]:
        #         if type(pid) == int:
        #             obj = Objet(pid, game)
        #             lieu.objets.append(obj)
        #         # TODO : Trouver un système où il pourrait y avoir plusieurs
        #         #        fois le même objet
        #         elif type(pid) == list:
        #             for x in range(pid[1]):
        #                 obj = Objet(pid[0], game, num=x + 1)
        #                 lieu.objets.append(obj)

        # if "lieux" in dk:
        #     lieu.lieux_accessibles = datalieu["lieux"]
        self.lieux[idl] = lieu
