import server_python.Personnages.Etre


class Combattant(Etre):
    """Classe abstraite dont dérivera les personnages pouvant se battre
    
    Attributes:
        vie_totale(int): Vie maximale
        vie(int): Vie restante
        mana_total(int): Mana maximal
        mana(int): Mana restant
        effets(list): Effets appliqué sur l'instance du combattant
    
    """
