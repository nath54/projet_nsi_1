
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
        self.nom = "Nom"
        self.description = "Description"

        self.ennemis = set()
        self.pnjs = set()
        self.persos = set()
        self.objets = set()
        self.lieux_accessibles = dict()

        pass
        # TODO

    def affiche(self):
        """Permet d'afficher

        Fonction appelée par le serveur qui affiche le lieu lors de l'arrivée
        dans celui-ci lors d'un evenement important, ou à la demande du joueur.

        Author: Nathan

        TODO: À améliorer/revoir
        """

        txt_objets = '\n\t- '.join([objet.nom for objet in self.objets])
        txt_pnjs = '\n\t- '.join([pnj.nom for pnj in self.pnjs])
        txt_ennemis = '\n\t- '.join([ennemi.nom for ennemi in self.ennemis])
        txt_persos = '\n\t- '.join([perso.nom for perso in self.persos])
        txt_lieux = '\n\t- '.join([action + " : " +
                                  self.lieux_accessibles[action].nom
                                  for action in self.lieu])

        txt = f"""
Vous êtes dans {self.nom}
{self.description}

Des objets sont présents dans ce lieu :
    -{txt_objets}

Vous pouvez voir quelques personnages dans le coin :
    -{txt_pnjs}

Vous pouvez voir des ennemis à votre portée :
    -{txt_ennemis}

Vous pouvez aussi aller à :
    -{txt_lieux}

        """
        return txt
