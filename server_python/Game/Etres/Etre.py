class Etre:
    """Classe abstraite qui servira de base pour tous les personnages

    Attributes:
        nom(str): Nom de l'instance
        lieu(Lieu): Instance du lieu dans lequel l'Etre se trouve

    """
    def __init__(self, name, lieu):
        self.nom = name
        self.lieu = lieu
