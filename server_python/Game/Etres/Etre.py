class Etre:
    """Classe abstraite qui servira de base pour tous les personnages

    Attributes:
        nom(str): Nom de l'instance
        lieu(Lieu): Instance du lieu dans lequel l'Etre se trouve
        description(str): Description de l'Etre
        race(str): Race de l'instance de l'Etre

    """
    def __init__(self,
                 nom="Quelqu'un",
                 lieu=None,
                 description="Quelqu'un de tout a fait normal,"
                             "comme on en trouve partout",
                 race="humain"):
        self.nom = nom
        self.lieu = lieu
        self.description = description
        self.race = race
