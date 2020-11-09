from Game.Etres.Etre import Etre

import random


class Combattant(Etre):
    """Classe abstraite dont dérivera les personnages pouvant se battre.

    Attributes:
        vie_totale(int): Vie maximale
        vie(int): Vie restante
        energie_totale(int): Énergie maximale
        energie(int): Énergie restante
        effets_attaque(dict): Effets que l'attaquant peu infliger
                              {effet: pourcentage à chaque attaque}
        effets(dict): Effets appliqués sur l'instance du combattant
                      {effet: temps restant}
        attaque(couple): attaque min et attaque max du combattant
        esquive(int): % de chance d'esquiver une attaque
    """

    def __init__(self, game):
        """Instancie le Combattant.

        Args:

        Auteur: Nathan, Hugo

        """
        Etre.__init__(self, game)
        self.vie_totale = 0
        self.full_vie()
        self.energie_totale = 0
        self.full_energie()
        self.effets_attaque = {}
        self.effets = {}
        self.attaque = {
            "corps à corps": None,
            "distance": None,
            "magique": None
        }
        self.esquive = 0
        self.type_ = "combattant"

    def full_vie(self):
        """Rend toute sa santé au personnage.

        Auteur: Nathan

        """
        self.vie = self.vie_totale

    def full_energie(self):
        """Rend toute son énergie au personnage.

        Auteur: Nathan

        """
        self.energie = self.energie_totale

    def soigne_PV(self, nombre):
        """Soigne la vie du personnage.

        Args:
            nombre(int): Quantité de vie à récupérer

        Auteur: Hugo

        """
        self.vie += nombre
        if self.vie > self.vie_totale:
            self.vie = self.vie_totale

    def soigne_EN(self, nombre):
        """Soigne l'énergie du personnage.

        Args:
            nombre(int): Quantité d'énergie à récupérer

        Auteur: Hugo

        """
        self.energie += nombre
        if self.energie > self.energie_totale:
            self.energie = self.energie_totale

    def debut_tour(self):
        """Applique au personnage les effets qu'il a

        Auteur: TODO

        """
        pass

    def sum_lsts(self, la, lb):
        """Fonction qui permet la somme de deux listes de nombres de mêmes tailles

        Auteur: Nathan
        """
        assert len(la) == len(lb), "Les deux listes n'ont pas la même taille !"
        assert all([type(elt) in [int, float] for elt in la + lb]), "Ce ne sont pas des listes de nombres"
        return [la[x] + lb[x] for x in range(len(la))]

    def sous_lsts(self, la, lb):
        """Fonction qui permet la soustraction de deux listes de nombres de mêmes tailles

        Auteur: Nathan
        """
        assert len(la) == len(lb), "Les deux listes n'ont pas la même taille !"
        assert all([type(elt) in [int, float] for elt in la + lb]), "Ce ne sont pas des listes de nombres"
        return [la[x] - lb[x] for x in range(len(la))]

    def sum_lst_nb(self, la, n):
        """Fonction qui permet la somme de tous les éléments d'une liste de nombres par un nombre

        Auteur: Nathan
        """
        assert type(n) in [int, float], "Le nombre donné n'est pas un nombre"
        assert all([type(a) in [int, float] for a in la]), "Ce ne sont pas des listes de nombres"
        return [a + n for a in la]

    def moy_lst(self, lst):
        """Fonction qui renvoie la moyenne d'une liste de nombres

        Auteur: Nathan
        """
        assert type(lst) == list and all([type(n) in [int, float] for n in lst]), "Ce n'est pas une liste de nombre !"
        return sum(lst) / len(lst)

    def get_attaque(self, type_att="corps à corps"):
        att = self.attaque[type_att]
        if att is None:
            att = [0, 0]
        if self.attaque["magique"] is not None and type_att != "magique":
            att = self.sum_lsts(att, self.attaque["magique"])
        # on applique les effets
        for k_effet, v_effet in self.effets.items():
            if k_effet == "attaque":
                for tpatt in list(set(["magique", type_att])):
                    if v_effet[tpatt] is not None:
                        if type(v_effet[tpatt]) in [int, float]:
                            att = self.sum_lst_nb(att, v_effet[tpatt])
                        elif type(v_effet[tpatt]) == list:
                            att = self.sum_lsts(att, v_effet[tpatt])
        # l'attaque ne peut pas etre négative, et le premier numero doit être inférieur au second
        if att[0] < 0:
            att[0] = 0
        if att[1] < 0:
            att[1] = 0
        if att[0] > att[1]:
            att[0] = att[1]
        if att == [0, 0]:
            att = None
        return att

    def get_defense(self, tp_def="corps à corps"):
        deff = [0, 0]
        lst_def = list(set(["magique", tp_def]))
        # on applique les effets
        for k_effet, v_effet in self.effets.items():
            if k_effet in ["defense", "défense"]:
                for tpdef in lst_def:
                    if v_effet[tpdef] is not None:
                        if type(v_effet[tpdef]) in [int, float]:
                            deff = self.sum_lst_nb(deff, v_effet[tpdef])
                        elif type(v_effet[tpdef]) == list:
                            deff = self.sum_lsts(deff, v_effet[tpdef])
        # la défense ne peut pas etre négative, et le premier numero doit être inférieur au second
        if deff[0] < 0:
            deff[0] = 0
        if deff[1] < 0:
            deff[1] = 0
        if deff[0] > deff[1]:
            deff[0] = deff[1]
        if deff == [0, 0]:
            deff = None
        return deff

    def attaque_cible(self, cible, type_att="corps à corps"):
        r = random.randint(0, 100)
        attaque = self.get_attaque(type_att)
        msg = "Il ne s'est rien passé"
        if attaque is None:
            msg = f"{self.nom} ne peut pas attaquer"
        elif r > cible.esquive:
            msg = f"{self.nom} attaque {cible.nom}"
            # l'attaque est réussie
            degats = random.randint(attaque[0], attaque[1])
            cible.vie -= degats
            if cible.vie < 0:
                cible.vie = 0
            msg += f"\n{cible.nom} a subit {degats} dégats, il a maintenant {cible.vie} pv."
            for effet in self.effets_attaque.keys():
                r = random.randint(0, 100)
                if r <= self.effets_attaque[effet]:
                    # l'effet est infligé à l'adversaire
                    msg += f"\n{cible.nom} a subit l'effet {effet} !"
                    temps_restant = 0
                    # ! A changer ! il faudra récupérer le temps d'un effet
                    cible.effets[effet] = temps_restant
            if cible.type_ in ["ennemis", "ennemi"]:
                enleve = self.test_mort_cible(cible)
            else:
                enleve = self.test_mort()
            if enleve:
                msg += f"\n{cible.nom} est mort."
            # si l'ennemi se fait toucher, l'ennemi va etre ultra agressif
            if cible.type_ in ["ennemis", "ennemi"]:
                cible.agressivite = 100
        else:
            msg = f"{cible.nom} a esquivé l'attaque"
            # on va augmenter l'agressivité de l'ennemi
            if cible.type_ in ["ennemis", "ennemi"]:
                cible.agressivite += 10
                if cible.agressivite > 100:
                    cible.agressivite = 100
        return msg

    def test_mort(self):
        if self.vie <= 0:
            self.game.map_.lieux[self.lieu].suppr_ennemi(self)
            return True
        return False

    def test_mort_cible(self, cible):
        if cible.vie <= 0:
            self.game.map_.lieux[self.lieu].suppr_ennemi(cible)
            return True
        return False
