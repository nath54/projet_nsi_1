
from Game.Etres.Perso import Perso


class Player:
    """Classe du joueur.

    Attributes:
        pseudo(str): Pseudo du compte
        password(str): Mot de passe du compte
        perso(Perso): Référence au personnage du compte
        id(int) : l'identifiant du player dans la table comptes

    """

    def __init__(self, pseudo, game, id_, ):
        """Initie le compte du joueur."""
        self.pseudo = pseudo
        self.perso = None
        self.game = game
        self.id_ = id_

    def load_perso(self, data_perso):
        """Fonction qui crée un perso au joueur et qui lui charge les infos.

        Auteur: Nathan
        """
        self.perso = Perso(self.game)
        self.player = self

        self.perso.nom = data_perso["nom"]
        self.perso.genre = data_perso["genre"]
        self.perso.race = data_perso["race"]
        self.perso.classe = data_perso["classe"]

        self.perso.experience = data_perso["experience"]
        self.perso.inventaire = data_perso["inventaire"]
        self.perso.equipement = data_perso["equipement"]
        self.perso.lieu = data_perso["lieu"]
        self.perso.quetes = data_perso["quetes"]
        self.perso.argent = data_perso["argent"]

        self.perso.vie = data_perso["vie"]
        self.perso.vie_totale = data_perso["vie_totale"]
        self.perso.energie = data_perso["energie"]
        self.perso.energie_totale = data_perso["energie_totale"]

        self.perso.charme = data_perso["charme"]
        self.perso.discretion = data_perso["discretion"]
        self.perso.force = data_perso["force_"]
        self.perso.agilite = data_perso["agilite"]
        self.perso.magie = data_perso["magie"]
        self.perso.effets_attaque = data_perso["effets_attaque"]
        self.perso.bonus_esquive = data_perso["bonus_esquive"]
        self.perso.sorts = data_perso["sorts"]
        self.perso.resistances = data_perso["resistances"]
        self.perso.faiblesses = data_perso["faiblesses"]

    def creation(self, data_creation):
        self.perso = Perso(self.game)
        #
        self.perso.nom = data_creation["nom"]
        self.perso.genre = data_creation["genre"]
        self.perso.race = data_creation["race"]
        self.perso.classe = data_creation["classe"]
        self.perso.experience = {
            "force": [0, 100],
            "charme": [0, 100],
            "agilite": [0, 100],
            "discretion": [0, 100],
            "magie": [0, 100],
            "vie": [0, 100],
        }
        self.perso.lieu = 0
        self.perso.quetes = {}
        # on met en place la base des valeurs
        valeurs = {
            "argent": 100,
            "charme": 5,
            "discretion": 5,
            "force": 5,
            "agilite": 5,
            "magie": 5,
            "energie": 20,
            "vie": 20,
            "inventaire": [],
            "equipement": {"Amulette": None, "Armure": None, "Arme": None},
            "effets_attaque": {},
            "bonus_esquive": 0,
            "sorts": {},
            "resistances": {},
            "faiblesses": {}
        }

        # on applique les valeurs des races
        for attribut in self.game.races[self.perso.race].keys():
            if attribut in valeurs.keys():
                if type(valeurs[attribut]) == int:
                    valeurs[attribut] += self.game.races[self.perso.race][attribut]
                elif type(valeurs[attribut]) == dict:
                    for k, v in self.game.races[self.perso.race][attribut].items():
                        if not (k in valeurs[attribut].keys()):
                            valeurs[attribut][k] = v
                        elif type(v) == int:
                            valeurs[attribut][k] += v
                elif type(valeurs[attribut]) == list:
                    for v in self.game.races[self.perso.race][attribut]:
                        valeurs[attribut].append(v)

        # on applique les valeurs des classes
        for attribut in self.game.classes[self.perso.classe].keys():
            if attribut in valeurs.keys():
                if type(valeurs[attribut]) == int:
                    valeurs[attribut] += self.game.classes[self.perso.classe][attribut]
                elif type(valeurs[attribut]) == dict:
                    for k, v in self.game.classes[self.perso.classe][attribut].items():
                        if not (k in valeurs[attribut].keys()):
                            valeurs[attribut][k] = v
                        elif type(v) == int:
                            valeurs[attribut][k] += v
                elif type(valeurs[attribut]) == list:
                    for v in self.game.classes[self.perso.classe][attribut]:
                        valeurs[attribut].append(v)

        # on donne les valeurs
        self.perso.argent = valeurs["argent"]
        self.perso.charme = valeurs["charme"]
        self.perso.discretion = valeurs["discretion"]
        self.perso.force = valeurs["force"]
        self.perso.agilite = valeurs["agilite"]
        self.perso.magie = valeurs["magie"]
        self.perso.energie_totale = valeurs["energie"]
        self.perso.energie = self.perso.energie_totale
        self.perso.vie_totale = valeurs["vie"]
        self.perso.vie = self.perso.vie_totale
        self.perso.inventaire = valeurs["inventaire"]
        self.perso.equipement = valeurs["equipement"]
        self.perso.effets_attaque = valeurs["effets_attaque"]
        self.perso.bonus_esquive = valeurs["bonus_esquive"]
        self.perso.sorts = valeurs["sorts"]
        self.perso.resistances = valeurs["resistances"]
        self.perso.faiblesses = valeurs["faiblesses"]
