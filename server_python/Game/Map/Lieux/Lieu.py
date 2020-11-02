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
        datas = game.client_db.get_data_Lieu_DB(id_)
        if datas is None:
            raise IndexError(f"L'index {id_} n'est pas reconnu")
        self.nom = datas.get("nom", "Lieu")
        self.description = datas.get("description", "")
        self.ennemis = []
        for id_ennemi in datas.get("ennemis", []):
            self.ennemis.append(self.game.Ennemi(self.game, id_ennemi))
        self.pnjs = []
        for id_pnj in datas.get("pnjs", []):
            self.pnjs.append(self.game.Pnj(game, id_pnj))
        self.persos = []
        self.objets = []
        for id_obj in datas.get("obj", []):
            self.objets.append(self.game.Objet(game, id_obj))
        self.lieux_accessibles = []
        self.map_ = game.map_

        pass
        # TODO

    def aff(self):
        """Permet d'afficher la description d'un lieu.

        Fonction appelée par le serveur qui affiche le lieu lors de l'arrivée
        dans celui-ci lors d'un evenement important, ou à la demande du joueur.

        Author: Nathan

        TODO: À améliorer/revoir

        """
        txt_objets = ""
        txt_pnjs = ""
        txt_ennemis = ""
        txt_persos = ""
        txt_lieux = ""

        if len(self.objets) >= 1:
            txt_objets = ("\n" + random.choice(p_objs) + " :\n    -"
                          '\n\t- '.join([objet.nom for objet in self.objets]))
        if len(self.pnjs) >= 1:
            txt_pnjs = ("\n" + random.choice(p_pnjs) + " :\n    -"
                        '\n\t- '.join([pnj.nom for pnj in self.pnjs]))
        if len(self.ennemis) >= 1:
            txt_ennemis = ("\n" + random.choice(p_ennemis) + " :\n    -"
                           '\n\t- '.join([enn.nom for enn in self.ennemis]))
        if len(self.persos) >= 1:
            txt_persos = ("\n" + random.choice(p_persos) + " :\n    -"
                          '\n\t- '.join([perso.nom for perso in self.persos]))
        if len(self.lieux_accessibles) >= 1:
            txt_lieux = ("\n" + random.choice(p_lieux) + " :\n    -"
                         '\n\t- '.join([self.map_.lieux[lieu[0]].nom
                                        for lieu in self.lieux_accessibles]))

        txt = f"""
Vous êtes dans {self.nom}
{self.description}
{txt_objets}
{txt_pnjs}
{txt_ennemis}
{txt_lieux}
{txt_persos}
        """
        return txt

    def __repr__(self):
        return self.aff()
