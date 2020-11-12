import random

p_objs = [
    "Il y a des objets ici"
]

p_pnjs = [
    "Vous pouvez parler avec",
    "Des pnjs sont dans le coin"
]

p_ennemis = [
    "Des ennemis sont a votre porté",
    "Vous pouvez frapper",
    "Attention, vous pouvez vous faire attaquer par"
]

p_persos = [
    "D'autres joueurs sont dans la même zone que vous",
    "Vous avez des amis ici"
]

p_lieux = [
    "Vous pouvez aller à"
]


class Lieu:
    """Classe d'un Lieu.

    Attributes:
        nom(str) : Le nom du lieu
        description(str) : La description du lieu
        ennemis(list<Ennemis>) : Liste des Ennemis qui sont sur le lieu
        pnjs(list<Pnj>) : Liste des pnjs qui sont sur le lieu
        persos(list<Perso>) : Liste des persos qui sont sur le lieu
        objets(list<Objet>) : Liste des objets qui sont sur le lieu
        lieux_accessibles(list<int, str>) : Liste des lieux accessibles
        map_ (Map) : l'instance de la map pour y acceder plus facilement
        appellation(list<str>): Liste des noms qu'on peut entrer pour aller à
                                un endroit

    """

    def __init__(self, game, id_):
        """Permet d'initialiser les caractéristiques d'un lieu."""
        self.game = game
        datas = game.client_db.get_data_Lieu_DB(id_)
        if datas is None:
            raise IndexError(f"L'index {id_} n'est pas reconnu")
        self.nom = datas.get("nom", "Lieu")
        self.appellations = datas.get("appellations", [])
        self.description = datas.get("description", "")
        self.ennemis = []
        for id_ennemi in datas.get("ennemis", []):
            if type(id_ennemi) == int:
                self.ennemis.append(self.game.Ennemi(id_ennemi, self.game))
            elif type(id_ennemi) == list:
                for x in range(id_ennemi[1]):
                    self.ennemis.append(self.game.Ennemi(id_ennemi[0],
                                                         self.game, nb=x))
        self.pnjs = []
        pnnjs = datas.get("pnjs", [])
        for id_pnj in pnnjs:
            if type(id_pnj) != int:
                continue
            self.pnjs.append(self.game.Pnj(id_pnj, self.game))
        self.persos = []
        self.objets = []
        for id_obj in datas.get("obj", []):
            self.objets.append(self.game.Objet(id_obj, self.game))
        self.lieux_accessibles = datas.get("lieux", [])
        self.map_ = game.map_
        self.index = id_
        self.tour = 0

    def aff(self, perso_=None):
        """Permet d'afficher la description d'un lieu.

        Fonction appelée par le serveur qui affiche le lieu lors de l'arrivée
        dans celui-ci lors d'un evenement important, ou à la demande du joueur.

        Auteur: Nathan

        TODO: À améliorer/revoir

        """
        txt_objets = ""
        txt_pnjs = ""
        txt_ennemis = ""
        txt_persos = ""
        txt_lieux = ""

        lieux_accessibles = []
        for ls_lieu in self.lieux_accessibles:
            print(ls_lieu)
            bon = True
            if len(ls_lieu) >= 3:
                if perso_ is None:
                    bon = False
                else:
                    for c in ls_lieu[2]:
                        if type(c) != list:
                            continue
                        if c[0] == "quete":
                            if perso_.quete_actuelle is None or perso.quete_actuelle.index != c[1]:
                                bon = False
                                break
                        if c[0] == "objet":
                            bon = False
                            for obj, qt in perso.inventaire:
                                if obj.index == c[1]:
                                    bon = True
                                    break

        self.persos = self.game.get_all_persos_lieu(self.index)
        if len(self.objets) >= 1:
            txt_objets = "\n\n" + random.choice(p_objs) + " :\n\t- " + "\n\t- ".join([objet.nom for objet in self.objets])
        if len(self.pnjs) >= 1:
            txt_pnjs = "\n\n" + random.choice(p_pnjs) + " :\n\t- " + '\n\t- '.join([pnj.nom for pnj in self.pnjs])
        if len(self.ennemis) >= 1:
            txt_ennemis = "\n\n" + random.choice(p_ennemis) + " :\n\t- " + '\n\t- '.join([enn.nom for enn in self.ennemis])
        prs = [perso.nom for perso in self.persos if perso != perso_]
        if len(prs) >= 1:
            txt_persos = "\n\n" + random.choice(p_persos) + " :\n\t- " + '\n\t- '.join(prs)
        if len(lieux_accessibles) >= 1:
            txt_lieux = "\n\n" + random.choice(p_lieux) + " :\n\t- " + "\n\t- ".join([self.map_.lieux[lieu[0]].nom + " [" + lieu[1] + "]"
                                                                                      for lieu in lieux_accessibles])

        return f"""
Vous êtes dans {self.nom}
{self.description}{txt_objets}{txt_pnjs}{txt_ennemis}{txt_lieux}{txt_persos}
"""

    def __repr__(self):
        return self.aff()

    def suppr_ennemi(self, enn):
        print("enleve\n", len(self.ennemis))
        self.ennemis.remove(enn)
        print(len(self.ennemis))
