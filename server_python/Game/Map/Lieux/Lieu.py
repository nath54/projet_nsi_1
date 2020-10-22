
class Lieu:
    """Classe d'un Lieu

    Attributes:
        nom(string) : Le nom du lieu
        description(string) : La description du lieu
        ennemis(set) : Liste des Ennemis qui sont sur le lieu
        pnjs(set) : Liste des pnjs qui sont sur le lieu
        persos(set) : Liste des persos qui sont sur le lieu
        objets(set) : Liste des objets qui sont sur le lieu
        lieux_accessibles(set) : Dictionnaire sous la forme {action : lieu} des
                                 lieux qui sont accessibles depuis ce lieu avec
                                 l'action à faire pour pouvoir y accéder

    """
    def __init__(self):
        self.nom = "Lieu"
        self.description = "Un lieu"
        self.ennemis = set()
        self.pnjs = set()
        self.persos = set()
        self.objets = set()
        self.lieux_accessibles = dict()

        pass
        # TODO

    def __repr__(self):
        """Permet d'afficher

        Fonction appelée par le serveur qui affiche le lieu lors de l'arrivée
        dans celui-ci lors d'un evenement important, ou à la demande du joueur.

        Author: Nathan

        TODO: À améliorer/revoir
        """

        txt_objets,txt_pnjs,txt_ennemis,txt_persos,txt_lieux="","","","",""

        if len(self.objets)>=1: txt_objets = "\nDes objets sont présents dans ce lieu :\n    -"+'\n\t- '.join([objet.nom for objet in self.objets])
        if len(self.pnjs)>=1: txt_pnjs = "\nVous pouvez voir quelques personnages dans le coin : :\n    -"+'\n\t- '.join([pnj.nom for pnj in self.pnjs])
        if len(self.ennemis)>=1: txt_ennemis = "\nVous pouvez voir des ennemis à votre portée :\n    -"+'\n\t- '.join([ennemi.nom for ennemi in self.ennemis])
        if len(self.persos)>=1: txt_persos = "\nDes objets sont présents dans ce lieu :\n    -"+'\n\t- '.join([perso.nom for perso in self.persos])
        if len(self.lieux_accessibles)>=1: txt_lieux = "\nVous pouvez aussi aller à :\n    -"+'\n\t- '.join([action+" : "+self.lieux_accessibles[action].nom for action in self.lieu])

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
