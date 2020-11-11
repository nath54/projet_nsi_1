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
        self.quetes = []
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
        self.type_ = "perso"
        self.quete_actuelle = None
        self.quetes_en_attente = []

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
            res += "\t - "
            if item[1] > 1:
                res += f"{item[1]} {item[0].nom} ({item[0].type})" + "\n"
            else:
                res += f"{item[0].nom} ({item[0].type})" + "\n"
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

        Auteur: Hugo, Nathan

        """
        txt_exp_1 = "    - " + "\n    - ".join([(str(key) + " : " + " / ".join([str(e) for e in self.experience[key]])) for key in self.experience])
        txt_exp = "points d'expériences du perso : \n" + txt_exp_1

        cac = self.get_attaque("corps à corps")
        mag = self.get_attaque("magique")
        dist = self.get_attaque("distance")
        txt_att_cac = "Rien" if cac is None else cac
        txt_att_dist = "Rien" if dist is None else dist
        txt_att_mag = "Rien" if mag is None else mag

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

Actuellement, votre attaque est :
    - corps à corps : {txt_att_cac}
    - distance : {txt_att_dist}
    - juste magique : {txt_att_mag}
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
                    break
                else:
                    obj[1] -= 1

    def add_to_invent(self, obj):
        """Ajoute un objet à l'inventaire

        Auteur: Hugo

        """
        # TODO: obj = Objet(id_obj) qui créé l'objet depuis la DB
        exist = False
        for i in self.inventaire:
            if i[0].nom == obj.nom:
                exist = True
                i[1] += 1
                break
        if not exist:
            self.inventaire.append([obj, 1])

    def desequiper(self, nom_obj, traiter_txt, id_obj=None):
        """Déséquipe un objet du personnage

        Auteur: Hugo, Nathan

        """
        for type_, obj in self.equip.items():
            if obj is None:
                continue
            if obj.index == id_obj or traiter_txt(obj.nom) == traiter_txt(nom_obj):
                self.equip[type_] = None
                self.add_to_invent(obj.index)
                # on enleve les effets de l'objet
                for k_effet, v_effet in obj.effets.items():
                    if k_effet == "attaque":
                        if "attaque" not in self.effets.keys():
                            continue
                        for k_a, v_a in v_effet.items():
                            if v_a is not None:
                                if type(v_a) in [int, float]:
                                    v_a = [v_a, v_a]
                                if self.effets["attaque"][k_a] is None:
                                    self.effets["attaque"][k_a] = [0, 0]
                                self.effets["attaque"][k_a] = self.sous_lsts(self.effets["attaque"][k_a], v_a)
                    # TODO
                    pass
                return False
        return f"Vous n'aviez pas de {nom_obj} sur vous..."

    def equiper(self, nom_obj, traiter_txt, id_obj=None):
        """Équipe un objet à un personnage

        Auteur: Hugo, Nathan

        """
        for obj, qt in self.inventaire:
            if obj.index == id_obj or traiter_txt(obj.nom) == traiter_txt(nom_obj):
                if obj.type in ["Amulette", "Arme", "Armure"]:
                    if self.equipement[obj.type] is None:
                        self.inventaire.remove([obj, qt])
                        self.equip[obj.type] = obj
                        # on ajouet les effets de l'objet
                        for k_effet, v_effet in obj.effets.items():
                            if k_effet == "attaque":
                                if "attaque" not in self.effets.keys():
                                    self.effets["attaque"] = {"corps à corps": None, "magique": None, "distance": None}
                                for k_a, v_a in v_effet.items():
                                    if v_a is not None:
                                        if type(v_a) in [int, float]:
                                            v_a = [v_a, v_a]
                                        if self.effets["attaque"][k_a] is None:
                                            self.effets["attaque"][k_a] = v_a
                                        else:
                                            self.effets["attaque"][k_a] = self.sum_lsts(self.effets["attaque"][k_a], v_a)
                            # TODO
                            pass
                            print(self.effets)
                        return False
                    else:
                        return f"Il y a déjà un(e) {obj.type} équipé"
                else:
                    return f"L'objet selectionné n'est pas équipable, il est de type {obj.type}"
        return "Objet non trouvé dans l'inventaire"

    def on_death(self):
        """Fonction qui est appelée à la mort du personnage

        Auteur: Hugo
        """
        client = None
        clients = self.game.server.clients
        for cliente, datac in clients.items():  # TODO: SOCKET
            if datac["player"].perso == self:
                client = cliente
        if client is not None:
            self.game.server.send(client, {"type": "message", "message": "Vous êtes mort... Je sais, c'est dur. Heureusement, pour vous aider à vous en remettre, on a décidé d'être sympa avec vous, vous ne souffrirez plus ! Votre âme est désormais... Supprimée. Ne me remerciez, c'est la fin, pas de souffrance éternelle ! Bon du coup si vous voulez continuer votre aventure, va falloir envisager de refaire un autre héros, parce que sinon le monde court à sa perte. Enfin *ce* monde a pas vraiment de fin en soit."}, True)
            id_ = self.client["player"].id_
            self.game.client_db.perso_death(id_)

    def test_dialogue(self):
        """Fonction qui teste si un dialogue est dispo avec une quete, ou un objet dans l'inventaire

        Auteur: Nathan
        """
        d = self.dialogue_en_cours
        if d is not None:
            if type(d) == dict:
                return
            elif type(d) == list and len(d) > 0:
                for dl in d:
                    if type(dl) == list:
                        if dl[0] is None:
                            self.dialogue_en_cours = dl[1]
                        elif type(dl[0]) == list:
                            if dl[0][0] == "quete":
                                if self.quete_actuelle is not None and self.quete_actuelle.index == dl[0][1]:
                                    self.dialogue_en_cours = dl[1]
                                    return
                            elif dl[0][0] == "obj":
                                for ob, _ in self.inventaire:
                                    if ob.index == dl[0][1]:
                                        self.dialogue_en_cours = dl[1]
                                        return
            else:
                self.dialogue_en_cours = None

    def quete_finie(self, id_quete):
        """Fonction qui fini la quete d'un perso

        Auteur: Nathan
        """
        if self.quete_actuelle.index != id_quete:
            raise UserWarning("Probleme quete finie, id différent !")
        self.quetes.append(self.quete_actuelle)
