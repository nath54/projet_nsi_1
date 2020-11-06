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
        self.attaque = (0, 1)
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

    def attaque_cible(self, cible):
        r = random.randint(0, 100)
        msg = "Il ne s'est rien passé"
        if r > cible.esquive:
            # l'attaque est réussie
            degats = random.randint(self.attaque[0], self.attaque[1])
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
            if cible.type_ == "ennemis":
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
