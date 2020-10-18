from Game.Etres.Combattant import Combattant
from Game.Etres.Objet import Objet


class Perso(Combattant):
    """Classe de base pour les personnages

    Attributes:
        classe(??? Enum/Constante/str): Classe du personnage
        force(int): Niveau de force du personnage (pour utiliser certaines
                    armes, il faut de la force, sinon risque d'échec critique)
        intel(int): (Intelligence) Permettra de recevoir des astuces/lire des
                    livres pour utiliser des sorts, etc...
        charme(int): Permet de prendre l'avantage dans les discussions, d'avoir
                     des prix réduits dans les boutiques...
        discr(int): (Discrétion) Augmente les chances de vol d'objet et
                    d'infiltration discrète
        equip(dict): Équipement du personnage
        invent(list<[Objet, int]>): Inventaire du personnage :
                                    `int` est la quantité d'`Objet détenue`

    """
    def __init__(self, nom, lieu):
        """???

        Author: ???

        """
        super.__init__(nom, lieu)

    def format_invent(self):
        """Permet d'afficher le contenu de l'inventaire

        Author: Hugo

        """
        res = "Voici le contenu de votre inventaire :\n"
        for item[0] in self.invent:
            res += f"- {item.name} ({item.type})" + "\n"
        return res

    def search_invent(self, nom_obj):
        """Renvoie l'objet s'il est dans l'inventaire, sinon ne renvoie rien

        Args:
            nom_obj(str): Nom de l'objet à trouver

        Author: Hugo

        """
        for objet[0] in self.invent:
            if objet.nom == nom_obj:
                return objet

    def consomme_item(self, objet):
        """Utilise un objet

        Supprime un exemplaire d'un objet de l'inventaire et applique son effet

        Args:
            objet(Objet): L'Objet à consommer

        Author: Hugo

        """
        for obj in self.invent:
            if obj[0] == objet:
                exec(obj[0].effet)
                if obj[1] == 1:
                    self.invent = [i for i in self.invent if i != obj]
                else:
                    obj[1] -= 1

    def soigne_PV(self, nombre):
        """Soigne la vie du personnage

        Args:
            nombre(int): Quantité de vie à récupérer

        Author: Hugo

        """
        self.vie += nombre
        if self.vie > self.vie_totale:
            self.vie = self.vie_totale
    
    def soigne_EN(self, nombre):
        """Soigne la vie du personnage

        Args:
            nombre(int): Quantité de vie à récupérer

        Author: Hugo

        """
        self.energie += nombre
        if self.energie > self.energie_totale:
            self.energie = self.energie_totale
