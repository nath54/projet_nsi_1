from Game.Etres.Etre import Etre


class Combattant(Etre):
    """Classe abstraite dont dérivera les personnages pouvant se battre.

    Attributes:
        vie_totale(int): Vie maximale
        vie(int): Vie restante
        energie_totale(int): Énergie maximale
        energie(int): Énergie restante
        effets(dict): Effets appliqués sur l'instance du combattant

    """

    def __init__(self, name="Quelqu'un", lieu=None):
        """Instancie le Combattant.

        Args:
            name(str): Nom à attribuer au Combattant.
            lieu(Lieu): Lieu dans lequel il se trouve.

        Author: Nathan, Hugo

        """
        super.__init__(name, lieu)
        self.vie_totale = 0
        self.full_vie()
        self.energie_totale = 0
        self.full_energie()
        self.effets = {}

    def full_vie(self):
        """Rend toute sa santé au personnage.

        Author: Nathan

        """
        self.vie = self.vie_totale

    def full_energie(self):
        """Rend toute son énergie au personnage.

        Author: Nathan

        """
        self.energie = self.energie_totale
