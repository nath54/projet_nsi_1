from Game.Etres.Combattant import Combattant
from Game.Objets.Objet import Objet


class Perso(Combattant):
    """Classe de base pour les personnages.

    Attributes:
        lieu(int): Identifiant du lieu dans lequel se trouve le personnage
        classe(??? Enum/Constante/str): Classe du personnage
        force(int): Niveau de force du personnage (pour utiliser certaines
                    armes, il faut de la force, sinon risque d'échec critique)
        intel(int): (Intelligence) Permettra de recevoir des astuces/lire des
                    livres pour utiliser des sorts, etc...
        charme(int): Permet de prendre l'avantage dans les discussions, d'avoir
                     des prix réduits dans les boutiques...
        discr(int): (Discrétion) Augmente les chances de vol d'objet et
                    d'infiltration discrète
        argent(int): L'argent du personnage
        equip(dict): Équipement du personnage
        invent(list<[Objet, int]>): Inventaire du personnage :
                                    `int` est la quantité d'`Objet` détenue
        quetes(dict<{int: Quete}>): Journal de quête du personnage
                                    `int` est l'ID de la quête
        histo_lieu(set<int>): Registre des ID des lieux déjà visités durant
                              cette session.

    """

    def __init__(self, game):
        """Instancie le personnage.

        Auteur: Hugo, Nathan

        """
        Combattant.__init__(self, game)
        self.lieu = None
        self.equip = {"Artéfact": None, "Armure": None, "Arme": None}
        self.inventaire = []
        self.argent = 0
        self.classe = ""  # TODO
        self.race = ""
        self.charme = 0
        self.force = 0
        self.magie = 0
        self.discretion = 0
        self.histo_lieu = set()  # TODO: Marquer le lieu dans lequel le perso apparaît
        self.dialogue_en_cours = None
        self.interlocuteur = None

    # region Format
    def format_invent(self):
        """Renvoie le contenu de l'inventaire.

        Returns:
            str: Contenu de l'inventaire (présentable)

        Auteur: Hugo

        """
        if len(self.inventaire) == 0:
            return "Aïe, on dirait que la crise est passée par là."
        res = "Voici le contenu de votre inventaire :\n"
        for item in self.inventaire:
            res += "\t" + f"- {item[0].nom} ({item[0].type})" + "\n"
        return res

    def format_equip(self):
        """Formate l'équipement du personnage.

        Returns:
            str: Équipement du personnage (présentable)

        Auteur: Hugo

        """
        res = "Voici votre équipement :\n"
        for type_, equip in self.equip.items():
            nom = "Rien" if equip is None else equip.nom
            res += "\n\t" + f"- {type_} : {nom}"
        return res

    def format_stats(self):
        """Formate les stats du personnage.

        Returns:
            str: Stats du personnage (présentable)

        Auteur: Hugo

        """
        txt_exp_1 = "    - " + "\n    - ".join([(str(key) + " : " + " / ".join([str(e) for e in self.experience[key]])) for key in self.experience])
        txt_exp = "points d'expériences du perso : \n" + txt_exp_1

        # region txt stats
        res = f"""STATS :
nom : {self.nom}
genre : {self.genre}
race : {self.race}
classe : {self.classe}

{txt_exp}
lieu : {self.game.map_.lieux[self.lieu].nom}
argent : {self.argent} pieces d'or

vie : {self.vie} / {self.vie_totale}
energie : {self.energie} / {self.energie_totale}

stats :
    - charme : {self.charme}
    - discretion : {self.discretion}
    - force : {self.force}
    - agilite : {self.agilite}
    - magie : {self.magie}
    - bonus d'esquive : {self.bonus_esquive}

résistances :  {self.resistances}
faiblesses : {self.faiblesses}
"""
        # endregion
        return res
    # endregion

    def search_invent(self, nom_obj, id_obj=None):
        """Renvoie l'objet s'il est dans l'inventaire, sinon ne renvoie rien.

        Args:
            nom_obj(str): Nom de l'objet à trouver
            id_obj(int): ID de l'objet à trouver

        Auteur: Hugo

        """
        if id_obj is None:
            for objet, _ in self.inventaire:
                if objet.nom == nom_obj or objet.id == id_obj:
                    return objet

    def consomme_item(self, objet):
        """Utilise un objet.

        Supprime un exemplaire d'un objet de l'inventaire et applique son effet

        Args:
            objet(Objet): L'Objet à consommer

        Auteur: Hugo

        """
        for obj in self.inventaire:
            if obj[0] == objet:
                # TODO
                if obj[1] == 1:
                    self.inventaire = [i for i in self.inventaire if i != obj]
                else:
                    obj[1] -= 1

    def desequiper(self, nom_obj, id_obj=None):
        """Déséquipe un objet du personnage

        Auteur: Hugo

        """
        for key, val in self.equip:
            if val.index == id_obj or val.nom == nom_obj:
                self.equip[key] = None
                self.add_to_invent(val.index)
                return True
        return False

    def add_to_invent(self, id_obj):
        """Ajoute un objet à l'inventaire

        Auteur: Hugo

        """
        # TODO: obj = Objet(id_obj) qui créé l'objet depuis la DB
        obj = Objet(id_obj, self.game)
        exist = False
        for i in self.inventaire:
            if i[0].nom == obj.nom:
                exist = True
                i[1] += 1
                break
        if not exist:
            self.inventaire.append([obj, 1])

    def equiper(self, nom_obj, id_obj=None):
        """Équipe un objet à un personnage

        Auteur: Hugo

        """
        for i in range(len(self.inventaire)):
            t_obj = self.inventaire[i]
            if t_obj.index == id_obj or t_obj.nom == nom_obj:
                if t_obj.type in ["Amulette", "Arme", "Armure"]:
                    del self.inventaire[i]
                    self.equip[t_obj.type] = t_obj
                    return True
        return False
