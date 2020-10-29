from Game.Etres.Etre import Etre

import random


class Combattant(Etre):
    """Classe abstraite dont dérivera les personnages pouvant se battre.

    Attributes:
        vie_totale(int): Vie maximale
        vie(int): Vie restante
        energie_totale(int): Énergie maximale
        energie(int): Énergie restante
        effets_attaque(dict): Effets que l'attaquant peu infliger {effet: pourcentage à chaque attaque}
        effets(dict): Effets appliqués sur l'instance du combattant {effet: temps restant}
        attaque(couple): attaque min et attaque max du combattant
        esquive(int): % de chance d'esquiver une attaque

    """

    def __init__(self):
        """Instancie le Combattant.

        Args:

        Author: Nathan, Hugo

        """
        super.__init__(name, lieu)
        self.vie_totale = 0
        self.full_vie()
        self.energie_totale = 0
        self.full_energie()
        self.effets_attaque = {}
        self.effets = {}
        self.attaque = (0,1)
        self.esquive=0

    def full_vie(self):
        """Rend toute sa santé au personnage.

        Author: Nathan

        """
        self.vie = self.vie_totale

    def full_energie(self):
        """Rend toute son énergie au personnage.

        Author: Nathan

        """
        self.energie = self.energie_totale

    def attaque_cible(self, cible):
        r = random.randint(0, 100)
        if r > cible.esquive:
            # l'attaque est réussie
            degats = random.randint(self.attaque[0],self.attaque[1])
            cible.vie -= degats
            for effet in self.effets_attaque.keys():
                r = random.randint(0, 100)
                if r <= self.effets_attaque[effet]:
                    #l'effet est infligé à l'adversaire
                    temps_restant = 0 # ! A changer ! il faudra récupérer le temps d'un effet
                    cible.effets[effet] = temps_restant
            cible.test_mort()

    def test_mort(self):
        if self.vie<=0:
            #TODO : informer le moteur du jeu que le combattant est mort et qu'il faut le supprimer du coup
            pass

