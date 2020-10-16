class Lieu:
    """Classe de lieu

    Attributes:
        nom_lieu(str): Le nom du lieu
        lieux(list<Lieu>): Lieux connectés à l'instance
        objets(list<Objet>): Liste d'objet dans le lieu
        ennemis(list<Ennemi>): Liste des ennemis dans la zone
        pnj(list<PNJ>): Liste des PNJ dans la zone
        joueurs(list<Perso>): Liste des persos présents

    """
    def __init__(self, nom_lieu, lieux=[], objets=[], ennemis=[], pnj=[], 
                 joueurs=[]):
        """Permet de créer un nouveau lieu

        Attributes:
            nom_lieu(str): Le nom du lieu
            lieux(list<Lieu>): Lieux connectés à l'instance
            objets(list<Objet>): Liste d'objet dans le lieu
            ennemis(list<Ennemi>): Liste des ennemis dans la zone
            pnj(list<PNJ>): Liste des PNJ dans la zone
            joueurs(list<Perso>): Liste des persos présents

        """
        self.nom_lieu = nom_lieu
        self.lieux = lieux
        self.objets = objets
        self.ennemis = ennemis
        self.pnj = pnj
        self.joueurs = joueurs

    def __repr__(self):
        """Permet de dresser une description du lieu où l'on se trouve

        Pourra être utile quand un joueur utilisera la commande "voir"

        Author: Hugo

        """
        res = f"Vous vous trouvez dans {self.nom_lieu}." + "\n"
        if len(self.objets) != 0: 
            res += "Voici les objets présents dans cette zone :\n"
            for objet in self.objets:
                res += f"- {objet.nom}" + "\n"
        if len(self.pnj) != 0:
            res += "Personnages présents dans la zone :\n"
            for pnj in self.pnj:
                res += f"- {pnj.nom}" + "\n"
        if len(self.ennemis) != 0:
            res += "Ennemis dans la zone :\n"
            for ennemi in self.ennemis:
                res += f"- {ennemi.nom}" + "\n"
        if len(self.lieux) != 0:
            res += "Vous pouvez aller :\n"
            for lieu in self.lieux:
                res += f"- {lieu.nom_lieu}" + "\n"
        else:
            res += "Vous êtes bloqué ici !"
        return res
