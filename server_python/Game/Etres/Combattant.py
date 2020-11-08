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
            "corps à corps":None,
            "distance":None,
            "magique":None
        }
        self.esquive = 0

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

    def get_attaque(self, type_att="corps à corps"):
        print(f"\n\nGET_attaque : {self.effets}\n\n")
        att = self.attaque[type_att]
        if att == None:
            att = [0,0]
        if self.attaque["magique"] != None and type_att != "magique":
            att = self.sum_lsts(att, self.attaque["magique"])
        # on applique les effets
        for k_effet, v_effet in self.effets.items():
            if k_effet == "attaque":
                for tpatt in list(set(["magique", type_att])):
                    if v_effet[tpatt] != None:
                        if type(v_effet[tpatt]) in [int, float]:
                            att = self.sum_lst_nb(att, v_effet[tpatt])
                        elif type(v_effet[tpatt]) == list:
                            att = self.sum_lsts(att, v_effet[tpatt])
        #
        if att == [0, 0]:
            att = None
        return att

    def attaque_cible(self, cible, type_att="corps à corps"):
        r = random.randint(0, 100)
        attaque = self.get_attaque(type_att)
        msg = "Il ne s'est rien passé"
        if attaque == None:
            msg = f"{self.nom} ne peut pas attaquer"
        elif r > cible.esquive:
            # l'attaque est réussie
            degats = random.randint(attaque[0], attaque[1])
            cible.vie -= degats
            if cible.vie < 0:
                cible.vie = 0
            msg = f"{cible.nom} a subit {degats} dégats, il a maintenant {cible.vie} pv."
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
                msg += "\nL'ennemi est mort."
        else:
            msg = f"{cible.nom} a esquivé l'attaque"
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
