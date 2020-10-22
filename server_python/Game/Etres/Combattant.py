from Game.Etres.Etre import Etre


class Combattant(Etre):
    """Classe abstraite dont dérivera les personnages pouvant se battre

    Attributes:
        vie_totale(int): Vie maximale
        vie(int): Vie restante
        energie_totale(int): Énergie maximale
        energie(int): Énergie restante
        effets(dict): Effets appliqués sur l'instance du combattant

    """
    def __init__(self, name="", lieu=None):
        super.__init__(name, lieu)
        self.vie_totale=0
        self.vie=self.vie_totale
        self.energie_totale=0
        self.enegie=self.energie_totale
        self.effets={}

    def full_vie(self):
        self.vie=self.vie_totale

    def full_energie(self):
        self.enegie=self.energie_totale

    
        
        
