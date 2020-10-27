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
    """Classe d'un Lieu

    Attributes:
        nom(str) : Le nom du lieu
        description(str) : La description du lieu
        ennemis(set) : Liste des Ennemis qui sont sur le lieu
        pnjs(set) : Liste des pnjs qui sont sur le lieu
        persos(set) : Liste des persos qui sont sur le lieu
        objets(set) : Liste des objets qui sont sur le lieu
        lieux_accessibles(list<int, str>) : Liste des lieux accessibles
        map_ (Map) : l'instance de la map pour y acceder plus facilement

    """
    def __init__(self):
        self.nom = "Lieu"
        self.description = "Un lieu"
        self.ennemis = set()
        self.pnjs = set()
        self.persos = set()
        self.objets = set()
        self.lieux_accessibles = list()
        self.map_ = None

        pass
        # TODO

    def __repr__(self):
        """Permet d'afficher

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
            txt_objets = ("\n" + random.choice(p_objs) + " :\n    -" +
                          '\n\t- '.join([objet.nom for objet in self.objets]))
        if len(self.pnjs) >= 1:
            txt_pnjs = ("\n" + random.choice(p_pnjs) + " :\n    -" +
                        '\n\t- '.join([pnj.nom for pnj in self.pnjs]))
        if len(self.ennemis) >= 1:
            txt_ennemis = ("\n" + random.choice(p_ennemis) + " :\n    -" +
                           '\n\t- '.join([enn.nom for enn in self.ennemis]))
        if len(self.persos) >= 1:
            txt_persos = ("\n" + random.choice(p_persos) + " :\n    -" +
                          '\n\t- '.join([perso.nom for perso in self.persos]))
        if len(self.lieux_accessibles) >= 1:
            txt_lieux = ("\n" + random.choice(p_lieux)+" :\n    -" +
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
