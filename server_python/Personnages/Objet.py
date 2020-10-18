
class Objet:
    """Classe définissant les objets

    Attributes:
        nom(str): Nom de l'objet
        description(str): Description de l'objet (Lore/renseignement)
        type(str): Type de l'objet (Consommable, Équipement, Objet-Clé)

    """
    def __init__(self, nom, description, type_):
        """Créer un objet

        Args:
            nom(str): Le nom de l'objet
            description(str): Description de l'objet
            type_(str): Le type de l'objet

        Author: Hugo

        """
        self.nom = nom
        self.description = description
        self.type = type_

    def __repr__(self):
        """Permet d'afficher une description de l'objet

        Author: Hugo

        """
        n = "\n"
        return f"{2 * n}{self.nom} ({self.type}){n}{self.description}{2 * n}"


if __name__ == "__main__":
    new = Objet("Épée du mercenaire",
                "Épée portée par le célèbre guerrier nuage",
                "Arme")
    print(new)
