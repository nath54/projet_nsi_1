from Game.Etres.Combattant import Combattant
from Game.Objets.Objet import Objet


class Perso(Combattant):
    """Classe de base pour les personnages.

    Attributes:
        classe(??? Enum/Constante/str): Classe du personnage
        force(int): Niveau de force du personnage (pour utiliser certaines
                    armes, il faut de la force, sinon risque d'échec critique)
        intel(int): (Intelligence) Permettra de recevoir des astuces/lire des
                    livres pour utiliser des sorts, etc...
        charme(int): Permet de prendre l'avantage dans les discussions, d'avoir
                     des prix réduits dans les boutiques...
        discr(int): (Discrétion) Augmente les chances de vol d'objet et
                    d'infiltration discrète
        monnaie(int): L'argent du personnage
        equip(dict): Équipement du personnage
        invent(list<[Objet, int]>): Inventaire du personnage :
                                    `int` est la quantité d'`Objet détenue`

    """

    def __init__(self, nom="", lieu=None):
        """Instancie le personnage.

        Author: Hugo

        TODO: Changer stats de base ?

        """
<<<<<<< Updated upstream
        Combattant.__init__(self, nom, lieu)
        self.equip = {"Amulette": None, "Casque": None, "Armure": None,
                      "Bottes": None, "Arme": None}
=======
        Combattant.__init__(self, nom, lieu)
        self.equip = {"Amulette": None, "Armure": None, "Arme": None}
>>>>>>> Stashed changes
        self.inventaire = []
        self.monnaie = 0
        self.classe = ""  # TODO
        self.charme = 0
        self.force = 0
        self.intel = 0
        self.discr = 0

    # region Format
    def format_invent(self):
        """Renvoie le contenu de l'inventaire.

        Returns:
            str: Contenu de l'inventaire (présentable)

        Author: Hugo

        """
        res = "Voici le contenu de votre inventaire :\n"
        for item[0] in self.inventaire:
            res += "\t" + f"- {item.name} ({item.type})" + "\n"
        return res

    def format_equip(self):
        """Formate l'équipement du personnage.

        Returns:
            str: Équipement du personnage (présentable)

        Author: Hugo

        """
        res = "Voici votre équipement :\n"
        for type_, equip in self.equip:
            nom = "Rien" if equip is None else equip.nom
            res += "\t" + f"- {type_} : {nom}"
        return res

    def format_stats(self):
        """Formate les stats du personnage.

        Returns:
            str: Stats du personnage (présentable)

        Author: Hugo

        """
        res = f"""Voici vos statistiques :
            - Force : {self.force}
            - Intelligence : {self.intel}
            - Charme : {self.charme}
            - Discrétion : {self.discr}
            - Vie : {self.vie}/{self.vie_totale}
            - Énergie : {self.energie}/{self.energie_totale}
            - Argent : {self.monnaie}"""
        return res
    # endregion

    def search_invent(self, nom_obj, id_obj=None):
        """Renvoie l'objet s'il est dans l'inventaire, sinon ne renvoie rien.

        Args:
            nom_obj(str): Nom de l'objet à trouver

        Author: Hugo

        """
        if id_obj is None:
            for objet, _ in self.inventaire:
                if objet.nom == nom_obj:
                    return objet
        else:
            for objet, _ in self.inventaire:
                if objet.id == id_obj:
                    return objet

    def consomme_item(self, objet):
        """Utilise un objet.

        Supprime un exemplaire d'un objet de l'inventaire et applique son effet

        Args:
            objet(Objet): L'Objet à consommer

        Author: Hugo

        """
        for obj in self.inventaire:
            if obj[0] == objet:
                exec(obj[0].effet)
                if obj[1] == 1:
                    self.inventaire = [i for i in self.inventaire if i != obj]
                else:
                    obj[1] -= 1

    def soigne_PV(self, nombre):
        """Soigne la vie du personnage.

        Args:
            nombre(int): Quantité de vie à récupérer

        Author: Hugo

        """
        self.vie += nombre
        if self.vie > self.vie_totale:
            self.vie = self.vie_totale

    def soigne_EN(self, nombre):
        """Soigne l'énergie du personnage.

        Args:
            nombre(int): Quantité d'énergie à récupérer

        Author: Hugo

        """
        self.energie += nombre
        if self.energie > self.energie_totale:
            self.energie = self.energie_totale

    def desequiper(self, nom_obj, id_obj=None):
        for key, val in self.equip:
            if val.index == id_obj or val.nom == nom_obj:
                self.equip[key] = None
                self.add_to_invent(val.index)
                return True
        return False

    def add_to_invent(self, id_obj):
        # TODO: obj = Objet(id_obj) qui créé l'objet depuis la DB
        self.inventaire.append(obj)

    def equiper(self, nom_obj, id_obj=None):
        for i in range(len(self.inventaire)):
            t_obj = self.inventaire[i]
            if t_obj.index == id_obj or t_obj.nom == nom_obj:
                if t_obj.type in ["Amulette", "Arme", "Armure"]:
                    del self.inventaire[i]
                    self.equip[t_obj.type] = t_obj
                    return True
        return False