class Player:
    """Classe du joueur.

    Attributes:
        pseudo(str): Pseudo du compte
        password(str): Mot de passe du compte
        perso(Perso): Référence au personnage du compte

    """

    def __init__(self):
        """Initie le compte du joueur."""
        self.pseudo = ""
        self.password = ""
        self.perso = None
