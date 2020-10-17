import server_python.Personnages.Combattant
from server_python.Personnages.Objet import Enum_Objet


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
        invent(list<Objet>): Inventaire du personnage

    """
    def __init__(self, nom, lieu):
        """???

        Author: ???

        """
        super.__init__(nom, lieu)

    def print_inventaire(self):
        """Permet d'afficher le contenu de l'inventaire

        Author: Hugo

        """
        print("Voici le contenu de votre inventaire :\n")
        for item in self.invent:
            print(f"- {item.name} ({item.type})" + "\n")
