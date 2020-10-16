class Lieu:
    """Classe de lieu
    
    Attributes:
        lieux(list<Lieu>): Lieux connectés à l'instance
        objets(list<Objet>): Liste d'objet dans le lieu
        ennemis(list<Ennemi>): Liste des ennemis dans la zone
        pnj(list<PNJ>): Liste des PNJ dans la zone
        joueur(list<Perso>): Liste des persos présents

    """
    def __init__(self):
        self.lieux