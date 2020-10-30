class Etre:
    """Classe abstraite qui servira de base pour tous les personnages.

    Attributes:
        nom(str): Nom de l'instance
        lieu(Lieu): Instance du lieu dans lequel l'Etre se trouve
        description(str): Description de l'Etre
        race(str): Race de l'instance de l'Etre

    """

    def __init__(self,game):
        """Instancie un Être."""
        self.nom = ""
        self.lieu = None
        self.description = ""
        self.race = ""
        self.game = game
