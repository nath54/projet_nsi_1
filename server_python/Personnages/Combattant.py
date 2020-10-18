from Personnages.Etre import Etre


class Combattant(Etre):
    """Classe abstraite dont dérivera les personnages pouvant se battre

    Attributes:
        vie_totale(int): Vie maximale
        vie(int): Vie restante
        energie_totale(int): Énergie maximale
        energie(int): Énergie restante
        effets(list): Effets appliqués sur l'instance du combattant

    """
    def __init__(self, name, lieu):
        super.__init__(name, lieu)
