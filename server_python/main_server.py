# PROGRAMME PRINCIPAL DU SERVEUR

# TODO: Remplacer les ??? dans les docstrings

# region Importations :
# librairie python
import socket
import _thread
import json
import sys
import time

# nos librairies
from Game.Game import Game
from Game.Etres.Perso import Perso
from Game.Map.Lieux.Lieu import Lieu
from Game.Objets.Objet import Objet
from client_db import Client_mariadb
from Player import Player
from cheat_code import *
from libs import *
# endregion


class Server:
    """Classe du serveur du jeu.

    Attributes:
        host(str): Si vide, écoute toutes les cartes réseaux
                    Sinon, on met l'adresse IP que l'on veut
        port(int): On utilise un port inutilisé
        max_size(int): Taille maximale d'un message reçu
        clients(dict): Clé -- socket.socket
                        Val -- `dict` de propriétés relatives au client
        server(socket): ???
        version(int) : version du jeu (pour comparer avec la version de la BDD)

    """

    def __init__(self):
        """Initialise le serveur de jeu.

        Auteur : Nathan

        """
        self.host = ""
        self.port = 9876
        self.max_size = 2048
        self.clients = {}
        self.server = None
        self.game = Game(jload)
        self.game.server = self
        self.client_db = Client_mariadb(self.game)
        self.game.client_db = self.client_db
        self.version = 1
        # faudrait peut etre trouver un meilleur nom que ca quand meme
        self.nom_du_jeu = "Py RPG MasterClass Option text multijoueur"
        # données des commandes
        self.commandes_dat = {
            "aide": {"com": ["aide", "help", "commandes"],
                     "help": """Affiche ce message d'aide, et des messages d'aides plus précis pour les commandes mises en arguments (ex : aide aller)""",
                     "fini": True},
            "voir": {"com": ["voir"],
                     "help": """Affiche les infos du lieu""",
                     "fini": True},
            "inventaire": {"com": ["inventaire"],
                           "help": """Affiche l'inventaire""",
                           "fini": True},
            "equipement": {"com": ["equipement"],
                           "help": """Affiche l'équipement""",
                           "fini": True},
            "stats": {"com": ["stats", "statistiques"],
                      "help": """Affiche les stats du perso""",
                      "fini": True},
            "joueurs": {"com": ["joueurs", "players"],
                        "help": "Affiche la liste des joueurs qui sont connectés",
                        "fini": True},
            "quete": {"com": ["quete", "devoir", "travail"],
                      "help": "Affiche la quête actuelle a faire",
                      "fini": True},
            "quetes finies": {"com": ["quete_finies", "a_faire"],
                              "help": "Affiche les quêtes que vous avez terminées",
                              "fini": True},
            "quetes en attentes": {"com": ["quetes_en_attente"],
                                   "help": "Affiche les quêtes que vous avez en attente",
                                   "fini": True},
            "faire quete": {"com": ["faire_quete"],
                            "help": "Si vous n'avez pas déjà de quête actuelle, met la quête demandée en quête actuelle",
                            "fini": False},
            "save": {"com": ["save", "sauvegarder", "save_game"],
                     "help": "Sauvegarde la map et l'état des joueurs",
                     "fini": True},
            "quit": {"com": ["quit", "exit", "close"],
                     "help": """Quitte le jeu""",
                     "fini": True},
            "attendre": {"com": ["attendre"],
                         "help": """Attends un tour""",
                         "fini": True},
            "desequiper": {"com": ["desequiper"],
                           "help": """Déséquipe un objet, vous devrez préciser le nom complet de l'objet (ex: 'desequiper epee_de_bois')""",
                           "fini": True},
            "equiper": {"com": ["equiper"],
                        "help": """Équipe un objet, vous devrez préciser le nom complet de l'objet (ex: 'equiper epee_de_bois')""",
                        "fini": True},
            "examiner": {"com": ["examiner"],
                         "help": """Affiche la description d'un objet, vous devrez préciser le nom complet de l'objet""",
                         "fini": True},
            "prendre": {"com": ["prendre", "ramasser"],
                        "help": """Prend l'objet et le rajoute dans l'inventaire, vous devrez préciser le nom complet de l'objet (ex : 'prendre epee_de_bois')""",
                        "fini": True},
            "jeter": {"com": ["jeter", "lacher"],
                      "help": """Enlève l'objet de l'inventaire, vous devrez préciser le nom complet de l'objet (ex : 'lacher epee_de_bois')""",
                      "fini": True},
            "ouvrir": {"com": ["ouvrir"],
                       "help": """Ouvre un objet qui s'ouvre""",
                       "fini": True},
            "fermer": {"com": ["fermer"],
                       "help": """Ferme un objet qui se ferme""",
                       "fini": True},
            "aller": {"com": ["aller", "bouger"],
                      "help": """Déplace le personnage dans un autre lieu, vous pouvez faire 'aller [nord/sud/est/ouest]' quand c'est possible, mais sinon, vous pouvez aussi utiliser la commande de cette facon : 'aller place', 'aller foret' ...""",
                      "fini": True},
            "entrer": {"com": ["entrer", "rentrer"],
                       "help": """Le personnage rentre dans un lieu (exemple : 'entrer maison'), si vous ne pouvez entrer que vers un seul lieu, vous pouvez utiliser 'entrer' tout seul, sans arguments, dans le cas contraire, il faudra préciser le lieu vers lequel vous voulez entrer.""",
                       "fini": True},
            "sortir": {"com": ["sortir", "quitter"],
                       "help": """Le personnage sort d'un lieu (exemple : 'entrer maison'), si vous ne pouvez sortir que vers un seul lieu, vous pouvez utiliser 'sortir' tout seul, sans arguments, dans le cas contraire, il faudra préciser le lieu vers lequel vous voulez sortir.""",
                       "fini": True},
            "parler": {"com": ["parler", "discuter"],
                       "help": """Parle avec un PNJ, vous devrez mettre le nom complet du PNJ (ex : 'parler vieux_paysan')""",
                       "fini": True},
            "message": {"com": ["message"],
                        "help": """Envoie un message dans le chat du jeu, ce message sera lisible par tous les joueurs""",
                        "fini": True},
            "attaquer": {"com": ["attaquer", "taper", "tabasser", "frapper"],
                         "help": """Attaque un ennemi, vous devrez mettre le nom de l'ennemi complet (exemple : 'taper petit_fantome' ou 'taper goblin-1') """,
                         "fini": True},
            "sort": {"com": ["sortilege", "sort", "magie"],
                     "help": """Lance un sortilège""",
                     "fini": False},
            "utiliser": {"com": ["utiliser"],
                         "help": """Utilise un objet (potentiellement sur un autre objet)""",
                         "fini": False},
            "mettre": {"com": ["mettre", "ranger"],
                       "help": """Met un objet dans un objet de type conteneur""",
                       "fini": False},
        }
        directions = ["ouest", "est", "nord", "sud", "nord-ouest",
                      "nord-est", "sud-ouest", "sud-est"]
        self.directions = [traiter_txt(d) for d in directions]
        self.nb_actions = 0
        self.nb_actions_save = 8

    def start(self):
        """Lance le serveur.

        Cette fonction permet de lancer le serveur en TCP/IP, acceptant
        jusqu'à 5 connexions simultanées.
        On va aussi lancer le jeu ici, bdd, Game, ...

        Auteur : Nathan

        """

        # On recupere la version du jeu (pour la comparer a celle de la db)
        f = open("version", "r")
        self.version = int(f.read())
        f.close()

        # Teste si c'est la bdd est initialisée, si non, on l'initialise
        if self.client_db.is_first_time():
            print("premier lancement")
            self.client_db.init_database()

        # On va aussi essayer de mettre à jour la bdd
        self.client_db.update()

        # On va vérifier les différentes versions des données de la bdd
        if self.client_db.test_version(self.version):  # or True:
            self.client_db.transfert_json_to_bdd(self.version)

        # TODO: Faudra aussi lancer les différents éléments du jeu
        # On lance le jeu ici
        self.game.start()

        # Lance le serveur socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)

        print("Server started.")
        while 1:
            (client, info) = self.server.accept()
            _thread.start_new_thread(self.handle, (client, info))

    def handle(self, client, infos):
        """Gère l'interaction serveur-client.

        Args:
            client(socket.socket): Référence au client avec qui gérer
                                   l'interaction
            infos(tuple<???, ???>): Couple d'informations : IP et ???

        Auteur : Nathan

        """
        self.on_accept(client, infos)
        while True:
            try:
                msg = client.recv(self.max_size)
                self.on_message(client, infos, msg)
            except Exception as e:
                print(e)
                self.on_close(client)
                return

    def send_all_except_c(self, client, message):
        """Envoie un message a tous les autres clients.

        Args:
            client(socket.socket): Référence au client auquel il ne faut pas
                                   envoyer de message
            message(str): Message à envoyer

        Auteur : Nathan

        """
        if sys.getsizeof(message) > self.max_size:
            return
        for autre_client in self.clients.keys():
            if client != autre_client:
                self.send(autre_client, message)

    def send_all(self, message):
        """Envoie un message à tous les clients.

        Args:
            message (str): Message à envoyer aux clients

        Auteur : Nathan

        """
        for cc in self.clients.keys():
            self.send(cc, message)

    def send(self, client, message, print_=False, important=False):
        """Envoie un message à un client précis.

        Args:
            client(socket.socket): Référence au client ayant envoyé le message
            message(str): Message à envoyer aux autres clients
            print_(bool): False --> N'affiche rien lorsqu'utilisé
                           True --> Affiche le message envoyé
            important(bool): False --> Un message d'erreur peut être envoyé
                              True --> Un UserWarning peut être envoyé

        Auteur : Nathan

        """
        if print_:
            print(message)
        message = json.dumps(message)
        if self.clients[client]["player"] is not None:
            p = self.clients[client]["player"].perso
            if p is not None:
                message.replace("@nom_perso", p.nom)
        message = message.encode(encoding="utf-8")
        size = sys.getsizeof(message)
        if size > self.max_size:
            if important:
                raise UserWarning(f"ERREUR : Le message est trop long !"
                                  "{str(size)}/{str(self.max_size)} bytes")
            print(f"""ERREUR : Le message est trop long ! {str(size)} bytes/
                   {str(self.max_size)} bytes""")
            return
        else:
            client.send(message)

    def send_message(self, client, message, important=False):
        """Envoie un message à un client

        Args:
            message(str): Message à envoyer (pas sous la forme dict)

        Auteur : ???

        """
        self.send(client, {"type": "message", "value": message}, important)

    def on_accept(self, client, i):
        """Réaction si une connexion entrante est acceptée.

        Args:
            client(socket.socket): Référence au client qui s'est connecté
            i(tuple<???, ???>): couple d'informations : IP et ???

        Auteur : Nathan

        """
        self.clients[client] = {"player": None}
        # On y mettra plus d'infos plus tard
        print("Connexion acceptée", client)
        print(type(client), i)

    def on_message(self, client, infos, message):
        """Réaction si un message est reçu.

        Args:
            client(socket.socket): Référence au client ayant envoyé le message
            infos(tuple<???, ???>): couple d'informations : IP et ???
            message (str): Message tapé par l'utilisateur.

        Auteur : Nathan

        """
        message = message.decode(encoding="utf-8")
        if len(message) <= 0:
            return
        db = self.client_db
        print(f"{self.clients[client]} : {message}")
        if is_json(message):
            pas_connecte = False
            perso_cree = True
            data = json.loads(message)
            cl = self.clients[client]
            if "player" not in cl.keys() or cl["player"] is None:
                pas_connecte = True
            elif cl["player"].perso is None:
                perso_cree = False
            if data["type"] == "cheat_code":
                if not pas_connecte and perso_cree:
                    cheat_code(self, client, data["commande"])
                elif pas_connecte:
                    dict_ = {"type": "not connected",
                             "value": "Veuillez vous connecter pour jouer"}
                    self.send(client, dict_, True)
                elif not perso_cree:
                    dict_ = {"type": "genres", "genres": json.dumps(db.get_genres())}
                    self.send(client, dict_, True)
                    time.sleep(0.1)
                    self.send(client, {"type": "creation perso"}, True)
            elif data["type"] == "commande":
                if not pas_connecte and perso_cree:
                    self.commandes(client, data)
                elif pas_connecte:
                    dict_ = {"type": "not connected",
                             "value": "Veuillez vous connecter pour jouer"}
                    self.send(client, dict_, True)
                elif not perso_cree:
                    dict_ = {"type": "genres", "genres": json.dumps(db.get_genres())}
                    self.send(client, dict_, True)
                    time.sleep(0.1)
                    self.send(client, {"type": "creation perso"}, True)
            elif data["type"] == "inscription":
                pseudo = data["pseudo"]
                email = data["email"]
                password = data["password"]
                erreur = db.test_compte_inscrit(pseudo, email)
                if erreur:
                    dict_ = {"type": "inscription failed", "value": erreur}
                    self.send(client, dict_, True)
                else:
                    reussi, id_ = db.inscription(pseudo, email, password)
                    if reussi:
                        self.clients[client]["player"] = Player(pseudo, self.game, id_)
                        self.send(client, {"type": "inscription successed"}, True)
                        time.sleep(0.1)
                        dict_ = {"type": "genres", "genres": json.dumps(db.get_genres())}
                        self.send(client, dict_, True)
                        time.sleep(0.1)
                        self.send(client, {"type": "creation perso"}, True)
                        # il faudra sans doute envoyer d'autres infos, comme une clé de connexion par exemple
                    else:
                        raise UserWarning("ERREUR : La BDD a échoué")
            elif data["type"] == "connection":
                pseudo = data["pseudo"]
                password = data["password"]
                erreur, id_ = self.client_db.test_connexion(pseudo, password)
                if erreur:
                    self.send(client, {"type": "connection failed", "value": erreur}, True)
                else:
                    self.clients[client]["player"] = Player(pseudo, self.game, id_)
                    # il faut aussi gerer le client qui est mort, et qui du coup, n'a plus de perso
                    data_perso = self.client_db.get_perso(id_)
                    if data_perso is not None:
                        self.send(client, {"type": "connection successed"}, True)
                        self.clients[client]["player"].load_perso(data_perso)
                        # il faudra sans doute envoyer d'autres infos, comme une clé de connexion par exemple
                        self.bienvenue(client)
                    else:
                        self.send(client, {"type": "connection successed but creation perso"}, True)
                        time.sleep(0.1)
                        dict_ = {"type": "genres", "genres": json.dumps(db.get_genres())}
                        self.send(client, dict_, True)
                        time.sleep(0.1)
                        self.send(client, {"type": "creation perso"}, True)
            elif data["type"] == "perso_cree":
                if data["genre"] == "autre" and data["genre"] not in db.get_genres():
                    db.new_genre(data["genre"])
                self.clients[client]["player"].creation(data)
                db.set_perso(self.clients[client]["player"])
                self.bienvenue(client)
            else:
                # TODO
                pass

    def on_close(self, client):
        """Réaction si une connexion se ferme.

        Args:
            client(socket): Référence au client ayant fermé son application

        Auteur : Nathan

        """
        # si le client n'a pas déjà été supprimé
        if client in self.clients.keys():
            self.save_client(client)
            print("Connexion fermée", client)
            self.send(client, {"type": "close"})
            client.close()  # a tester
            del(self.clients[client])

    def save_client(self, client):
        """Sauvegarde un personnage

        Args:
            client(socket.socket): Socket associé au perso

        Auteur : ???

        """
        # TODO
        player = self.clients[client]["player"]
        if player is not None and player.perso is not None:
            self.client_db.set_perso(player)
        # self.client_db.save_player(player)

    def save_all(self):
        """Sauvegarde tous les clients et la map

        Auteur : ???

        """
        # on sauvegarde tous les clients
        for client in self.clients.keys():
            self.save_client(client)
        # on sauvegarde la map
        self.client_db.save_map(self.game.map_)
        print("Jeu sauvegardé !")

    def format_dialog(self, perso):
        """Met en forme le dialogue

        Args:
            perso(Perso): Référence au perso en dialogue

        Auteur : ???

        """
        dial = perso.dialogue_en_cours
        if dial is None or type(dial) == list:
            return "Fin du dialogue"
        tint = ""
        if perso.interlocuteur is not None:
            tint = f"\n{perso.interlocuteur.nom} : "
        txt = tint + list(dial.keys())[0] + "\n"
        #
        rd = dial[list(dial.keys())[0]]
        if type(rd) == dict:
            x = 1
            for rep in rd.keys():
                txt += f"\n\t({x}) {rep}"
                x += 1
        else:
            pass
            # perso.dialogue_en_cours = None
        return txt

    def fin_dialogue(self, client, perso, nom_perso):
        """Gère la fin d'un dialogue avec un PNJ

        Args:
            client(socket.socket): Référence au client
            perso(Perso): Personnage qui a fini de parler.
            nom_perso(str): Nom du perso en question.

        Auteur : Nathan

        """
        texte_fait = ""
        if type(perso.dialogue_en_cours) == list:
            t = "Fin du dialogue"
            # TODO : faire que les effets en fin de dialogue s'appliquent
            for effet in perso.dialogue_en_cours:
                if type(effet) != dict or len(effet.items()) != 1:
                    continue
                e, v = list(effet.items())[0]
                # quete : le pnj donne une quete au perso
                if e == "quete":
                    # on met la quete actuelle en attente s'il y en a une
                    if perso.quete_actuelle is not None:
                        perso.quetes_en_attente.append(perso.quete_actuelle)
                    perso.quete_actuelle = self.game.Quete(self.game, v)
                    time.sleep(0.1)
                    self.send_message(client, f"{perso.interlocuteur.nom} vous a donné une nouvelle quete a faire : {perso.quete_actuelle.nom}", True)
                # objet : le pnj donne un objet au perso
                elif e == "objet":
                    bon = False
                    nom_obj = ""
                    for obj, qt in perso.inventaire:
                        if obj.index == v:
                            qt += 1
                            nom_obj = obj.nom
                            bon = True
                            break
                    if not bon:
                        obj = self.game.Objet(v, self.game)
                        nom_obj = obj.nom
                        perso.inventaire.append([obj, 1])
                    time.sleep(0.1)
                    self.send_message(client, f"{perso.interlocuteur.nom} vous a donné {nom_obj}", True)
                # quete finie : le perso a fini une quete
                elif e == "quete finie":
                    time.sleep(0.1)
                    self.send_message(client, f"Vous avez finie la quete {perso.quete_actuelle.nom}", True)
                    perso.quete_finie(v)
                elif e == "prendre objet":
                    # prendre objet : le pnj prend un objet de l'inventaire du perso
                    for obj in perso.inventaire:
                        if obj[0].index == v:
                            time.sleep(0.1)
                            self.send_message(client, f"{perso.interlocuteur.nom} vous a pris un/une {obj[0].nom}", True)
                            if obj[1] == 1:
                                perso.inventaire = [i for i in perso.inventaire if i != obj]
                            else:
                                obj[1] -= 1
                            break
            pass
            if perso.interlocuteur is not None:
                texte_fait = f"{nom_perso} a fini de parler avec {perso.interlocuteur.nom}. Ce dernier paraît soulagé d'avoir fini cette discussion, qui avait l'air terriblement ennuyante."
            else:
                texte_fait = f"{nom_perso} a fini de parler avec un Pnj. Ce dernier paraît soulagé d'avoir fini cette discussion, qui avait l'air terriblement ennuyante."
            perso.interlocuteur = None
            perso.dialogue_en_cours = None
        if perso.dialogue_en_cours is None:
            perso.dialogue_en_cours = None
            self.send_message(client, "Fin du dialogue", True)
            if perso.interlocuteur is not None:
                texte_fait = f"{nom_perso} a fini de parler avec {perso.interlocuteur.nom}. Ce dernier paraît soulagé d'avoir fini cette discussion, qui avait l'air terriblement ennuyante."
            else:
                texte_fait = f"{nom_perso} a fini de parler avec un Pnj. Ce dernier paraît soulagé d'avoir fini cette discussion, qui avait l'air terriblement ennuyante."
            perso.interlocuteur = None
        return texte_fait

    def input_client(self, client, message):
        """Attends une réponse du client

        Args:
            client(socket.socket): Référence au client
            message(str): Message à envoyer pour guider l'input du client

        Auteur: Nathan

        """
        nc = self.clients[client]["player"].pseudo
        print(f"En attente d'une réponse du player {nc}")
        self.send_message(client, message)
        mess = client.recv(self.max_size)
        print(f"Réponse recue : {mess}")
        return mess

    def input_bonne_reponse(self, client, message, brs):
        """Attend une réponse du client dans la liste des réponses possibles.

        Args:
            client(socket.socket): Référence au client
            message(str): Message à envoyer pour guider l'input du client
            brs(list<str>): Liste des réponses possibles

        Auteur: Nathan

        """
        assert len(brs) >= 1, "Il doit y avoir au moins une réponse possible"
        br = False
        erreur = ""
        while not br:
            rep = self.input_client(client, message)
            if is_json(rep):
                jr = json.loads(rep)
                cm = jr.get("commande", "")
                if jr.get("type", "") == "commande":
                    if traiter_txt(cm) in brs:
                        return cm
                        br = True
                    else:
                        erreur = "Vous voulez répondre autre chose ? Comme si vous avez la liberté d'expression ici ..."
                else:
                    erreur = "Il y a eu une erreur lors de la reception du message !"
            else:
                erreur = "Erreur lors de la reception du message !"
            self.send_message(client, erreur)
        raise UserWarning("Probleme avec input client !")

    # region Commandes
    def commandes(self, client, data):
        """Éxecute les commandes entrée par l'utilisateur.

        Args:
            client(socket): Personne qui a entré la commande
            data(dict<str: str>): un dictionnaire contenant les éléments d'une
                                  commande.
                                  exemple : {"command": "attaquer",
                                             "arguments": "ennemi"}

        Auteur : Nathan, Hugo

        """
        # region initialisation - traitement données
        data_len = len(data.keys())
        action = data["commande"]
        arguments = data["arguments"]
        args = data["arguments"].split(" ")
        # on enleve les arguments vides :
        while "" in args:
            args.remove("")
        perso = self.clients[client]["player"].perso
        # on affiche ces infos pour le debuggage
        print("data_len : ", data_len)
        print("len args : ", len(args))

        texte_fait = ""
        nom_perso = self.clients[client]["player"].perso.nom
        tour_p = 0
        # endregion

        self.nb_actions += 1
        if self.nb_actions >= self.nb_actions_save:
            self.nb_actions = 0
            self.save_all()
            self.send_all({"type": "message", "value": "game saved"})

        # TODO : Il faudra appeler une fonction qui va executer les effets que
        # le personnage a pour commencer son tour

        # On définit l'objet ciblé avec lequel l'utilisateur voudra (peut-être) agir
        # region definition obj_cible
        obj_cible = None
        if len(args) >= 1:
            for obj in perso.game.map_.lieux[perso.lieu].objets:
                if are_texts_equals(obj.nom, args[0]) or traiter_txt(" ".join(args)).startswith(traiter_txt(obj.nom)):
                    obj_cible = obj
                    break
        # endregion
        # region definition obj_cible_inv
        obj_cible_inv = None
        if len(args) >= 1:
            for obj, _ in perso.inventaire:
                if are_texts_equals(obj.nom, args[0]) or traiter_txt(" ".join(args)).startswith(traiter_txt(obj.nom)):
                    obj_cible_inv = obj
                    break
        # endregion
        # region definition ennemi_cible
        ennemi_cible = None
        if len(args) >= 1:
            for en in self.game.map_.lieux[perso.lieu].ennemis:
                if are_texts_equals(args[0], en.nom) or traiter_txt(" ".join(args)).startswith(traiter_txt(en.nom)):
                    ennemi_cible = en
        # endregion
        # region definition pnj_cible
        pnj_cible = None
        if len(args) >= 1:
            for pn in self.game.map_.lieux[perso.lieu].pnjs:
                if are_texts_equals(args[0], pn.nom) or traiter_txt(" ".join(args)).startswith(traiter_txt(pn.nom)):
                    pnj_cible = pn
        # endregion

        # Les premieres commandes sont des commandes à 0 ou plus arguments
        # commande aide : affiche le message d'aide
        if is_one_of(action, self.commandes_dat["aide"]["com"]):
            txt_help = "N'essayez pas d'inventer de nouvelles commandes, il y en a déjà assez comme ca !"
            if len(args) == 0:
                txt_help = "COMMANDES DISPONIBLES :"
                for key in self.commandes_dat.keys():
                    t = "'" + "', '".join(self.commandes_dat[key]["com"]) + "'"
                    tt = self.commandes_dat[key]["help"]
                    ttt = "Fonctionne" if self.commandes_dat[key]["fini"] else "Ne fonctionne pas encore"
                    txt_help += f"\n\t- {t} [{ttt}]"
                txt_help += "\n\nVous pouvez obtenir plus d'infos sur une commande précise en tapant 'aide [nom de la commande]'"
            else:
                for vl in self.commandes_dat.values():
                    coms, t_aide = vl["com"], vl["help"]
                    if is_one_of(arguments, coms):
                        ttt = "Cette commande fonctionne" if vl["fini"] else "Cette commande ne fonctionne pas encore"
                        txt_help = "Commande : " + arguments + "\n" + t_aide + "\n" + ttt
            self.send_message(client, txt_help, True)
        # commande voir ; affiche les infos du lieu
        elif is_one_of(action, ["voir"]):
            self.send_message(client, self.game.map_.lieux[perso.lieu].aff(perso), True)
        # commande joueurs ; affiche les joueurs connectés
        elif is_one_of(action, ["joueurs"]):
            txt_j = ""
            if len(self.clients.values()) == 1:
                txt_j = "Il n'y a pas d'autres joueurs connectés, vous êtes la seule personne a arpenter ce dangereux monde, ramenez des amis ! ;)"
            elif len(self.clients.values()) >= 2:
                txt_j = "Joueurs connectés :"
                for cl in self.clients.keys():
                    if cl != client:
                        pcl = self.clients[cl]["player"].perso
                        txt_j += f"\n\t- {pcl.nom}"
                        if pcl.lieu == perso.lieu:
                            txt_j += " [Même lieu que vous]"
                        else:
                            txt_j += f" [{self.game.map_.lieux[pcl.lieu].nom}]"
            else:
                txt_j = "Erreur, apparement, il semblerait qu'il n'y ait aucun clients connectés au serveur alors que vous l'êtes..."
            self.send_message(client, txt_j, True)
        # commande inventaire : affiche l'inventaire
        elif is_one_of(action, self.commandes_dat["inventaire"]["com"]):
            self.send_message(client, perso.format_invent(), True)
        # commande equipement : affiche l'equipement
        elif is_one_of(action, self.commandes_dat["equipement"]["com"]):
            self.send_message(client, perso.format_equip(), True)
        # commande stats : affiche des stats
        elif is_one_of(action, self.commandes_dat["stats"]["com"]):
            if len(args) == 0:
                print("stats :", perso.format_stats())
                self.send_message(client, perso.format_stats(), True)
            else:
                pass  # TODO: Afficher stats d'un autre Etre (bof)
        # commande quete : affiche la quete actuelle
        elif is_one_of(action, self.commandes_dat["quete"]["com"]):
            if perso.quete_actuelle is None:
                self.send_message(client, "Vous n'avez visiblement rien a faire, il serait temps de trouver du travail, chômeur !")
            else:
                self.send_message(client, f"Quete : {perso.quete_actuelle.nom} :\n{perso.quete_actuelle.description}")
        # commande quetes finies : affiche les quetes qui ont été finies
        elif is_one_of(action, self.commandes_dat["quetes finies"]["com"]):
            qt_fins = []
            for qt_id, etat in perso.quetes:
                if etat == "finie":
                    qt_fins.append(qt_id)
            if len(perso.quetes.keys()) >= 1:
                txt_qt = "Quetes finies :"
                for qt_id in qt_fins:
                    qt_nom = self.client_db.get_data_quetes_DB(qt_id)["nom"]
                    txt_qt += f"\n\t- {qt_nom}"
                self.send_message(client, txt_qt)
            else:
                self.send_message(client, "Je ne sais pas si c'est par flemme ou par manque de compétence, mais vous n'avez rien fait !")
        # commande quetes en attentes : affiche les quetes qui sont en attentes
        elif is_one_of(action, self.commandes_dat["quetes en attentes"]["com"]):
            if len(perso.quetes_en_attente) >= 1:
                txt_qt = "Quetes en attentes :"
                for qt_id in perso.quetes_en_attente:
                    qt_nom = self.client_db.get_data_quetes_DB(qt_id)["nom"]
                    txt_qt += f"\n\t- {qt_nom}"
                self.send_message(client, txt_qt)
            else:
                self.send_message(client, "Tel un maître de l'organisation, vous avez géré vos efforts, et vous n'avez donc aucun retard dans vos travaux à faire.")
        # TODO : faire que les quetes finies et les quete en attentes soient dans le meme dictionnaire : perso.quetes
        # commande save : le client sauvegarde le jeu
        elif is_one_of(action, self.commandes_dat["save"]["com"]):
            self.save_all()
            mes = {"type": "message", "value": "Partie sauvegardée !"}
            self.send_all(mes)
        # commande quit : le client quitte le jeu
        elif is_one_of(action, self.commandes_dat["quit"]["com"]):
            self.on_close(client)
        # commande attendre : le perso du joueur attend un tour
        elif is_one_of(action, self.commandes_dat["attendre"]["com"]):  # Bof
            self.send_message(client, "Votre flemme vous submerge pendant quelques instants, et vous ne faites rien pendant un tour... Les développeurs de ce jeu submergés eux aussi par la flemme vous remercient d'ailleurs.")
            texte_fait = f"{nom_perso}, submergé par la flemme, ne fait rien pendant un tour."
            tour_p += 1
        # les prochaines commandes ont au moins un argument
        elif data_len <= 1:
            self.send_message(client, "Commande inconnue", True)

        # Ce qui suit sont des commandes avec au moins 1 argument
        # commande desequiper
        elif is_one_of(action, self.commandes_dat["desequiper"]["com"]):
            erreur = perso.desequiper(arguments, traiter_txt)
            if not erreur:
                mess = f"Vous avez retiré {arguments} !"
                texte_fait = f"{nom_perso} a déséquipé {arguments}"
                tour_p += 0.5
            else:
                mess = erreur
            self.send_message(client, mess, True)
        # commande equiper
        elif is_one_of(action, self.commandes_dat["equiper"]["com"]):
            erreur = perso.equiper(arguments, traiter_txt)
            if not erreur:
                mess = f"Vous avez équipé {arguments}"
                texte_fait = f"{nom_perso} a équipé {arguments}"
                tour_p += 0.5
            else:
                mess = erreur
            self.send_message(client, mess, True)
        # commande examiner
        elif is_one_of(action, self.commandes_dat["examiner"]["com"]):
            if obj_cible is None and ennemi_cible is None and obj_cible_inv is None and pnj_cible is None:
                self.send_message(client, "Si je ne vois pas ce que je doit examiner, dois-je essayer d'en imaginer une description foireuse ?", True)
            elif obj_cible:
                self.send_message(client, f"{obj_cible.__repr__()}", True)
            elif obj_cible_inv:
                self.send_message(client, f"{obj_cible_inv.__repr__()}", True)
            elif ennemi_cible:
                self.send_message(client, f"{ennemi_cible.__repr__()}", True)
            elif pnj_cible:
                self.send_message(client, f"{pnj_cible.__str__()}", True)
        # commande prendre
        elif is_one_of(action, self.commandes_dat["prendre"]["com"]):
            if obj_cible is None:
                mess = "Honnêtement, j'adore le concept. Mais l'objet existe pas. Ou il est pas là. Au choix !"
                self.send_message(client, mess, True)
                return
            if obj_cible.type not in ["décor", "contenant"]:
                perso.add_to_invent(obj_cible)
                self.game.map_.lieux[perso.lieu].objets.remove(obj_cible)
                self.send_message(client, f"Vous avez pris le/la {obj_cible.nom}.")
                texte_fait = f"{nom_perso} a pris {obj_cible.nom}"
                tour_p += 0.5
            else:
                self.send_message(client, "Euh .... Vous essayez quand même de prendre quelque chose qui ne peut pas se prendre quand même là ! Je pense que vous devriez aller dans un hopital psychiatrique, parce que ce sera quoi le prochain stade ? Vous essayerez de prendre d'autre êtres vivants ?")
        # commande jeter
        elif is_one_of(action, self.commandes_dat["jeter"]["com"]):
            mess = "Impossible de jeter cet objet, avez-vous au moins vérifié que vous le possédez ?"
            mess += "\nAussi, essayez  d'écrire le nom de l'objet avec des _ à la place des espaces"
            mess += "\nexemple : lacher epee_en_bois"
            arg = args[0]
            qt = args[1] if len(args) > 1 else 1
            if type(qt) != int:
                try:
                    qt = int(qt)
                except Exception:
                    self.send_message(client, "Probleme de syntaxe, vous devez preciser le nom complet de l'objet en remplacant les espaces par des '_', exemple : 'lacher epee_de_bois'")
                    return

            for obj, obj_qt in perso.inventaire:
                if traiter_txt(obj.nom) == traiter_txt(arg):
                    if obj_qt < qt:
                        mess = f"Vous ne pouvez jeter autant de {obj.nom} que ça !"
                    else:
                        tour_p += 0.5
                        # on rajoute les objets au lieu
                        for i in range(qt):
                            new_obj = Objet(obj.index, self.game)
                            perso.game.map_.lieux[perso.lieu].objets.append(new_obj)
                        # on enleve l'objet de l'inventaire
                        if obj_qt == qt:
                            del perso.inventaire[i]
                            if qt == 1:
                                mess = f"Vous avez jeté votre {obj.nom} !"
                                texte_fait = f"{nom_perso} a jeté un/une {obj.nom}"
                            else:
                                mess = f"Vous avez jeté tous vos {obj.nom} !"
                                texte_fait = f"{nom_perso} a jeté tous ses {obj.nom}"
                        else:
                            perso.inventaire[i][1] -= qt
                            mess = f"Vous avez jeté {qt} de vos {obj.nom} !"
                            texte_fait = f"{nom_perso} a jeté {qt} {obj.nom}"

            self.send_message(client, mess)
        # commande ouvrir
        elif is_one_of(action, self.commandes_dat["ouvrir"]["com"]):
            if obj_cible.type == "contenant":
                if obj_cible.ouvert:
                    mess = "Cet objet est déjà ouvert..."
                else:
                    obj_cible.ouvert = True
                    mess = f"Vous ouvrez ce superbe {obj_cible.nom}\n{obj_cible.format_contenu()}"
                    texte_fait = f"{nom_perso} a ouvert {obj_cible.nom}"
                    tour_p += 0.5
            else:
                mess = "Comment ouvrir un objet qui ne possède pas d'ouverture..."
            self.send_message(client, mess, True)
        # commande fermer
        elif is_one_of(action, self.commandes_dat["fermer"]["com"]):
            if obj_cible.type == "contenant":
                if obj_cible.ouvert:
                    obj_cible.ouvert = False
                    mess = f"Vous avez refermé le {obj_cible.nom}."
                    texte_fait = f"{nom_perso} a fermé {obj_cible.nom}"
                    tour_p += 0.5
                else:
                    mess = f"Vous avez refermé le/la {obj_cible.nom}, qui était déjà fermé... Quel exploit !"
            else:
                mess = "Fermer un objet qui ne se ferme pas... Original."
            self.send_message(client, mess, True)
        # commande entrer
        elif is_one_of(action, self.commandes_dat["entrer"]["com"]):
            lieu_actuel = self.game.map_.lieux[perso.lieu]
            idls = []
            if len(args) == 0:
                for id_lieu, action in lieu_actuel.lieux_accessibles:
                    if action == "entrer":
                        idls.append(id_lieu)
            else:
                for id_lieu, action in lieu_actuel.lieux_accessibles:
                    if action == "entrer":
                        idls.append(id_lieu)
                        eq_ap = False
                        lieu = self.game.map_.lieux[id_lieu]
                        for lap in lieu.appellations:
                            if are_texts_equals(lap, args[0]) or are_texts_equals(lap, " ".join(args)):
                                eq_ap = True
                                break
                        if are_texts_equals(lieu.nom, args[0]) or eq_ap:
                            idls.append(id_lieu)
            if len(idls) == 0:
                self.send_message(client, "Vous ne pouvez entrer nulle part !")
            elif len(idls) > 1:
                self.send_message(client, "Vous pouvez entrer dans plusieurs lieux !")
            else:
                lieu = self.game.map_.lieux[idls[0]]
                perso.lieu = idls[0]
                self.send_message(client, f"Vous allez dans {lieu.nom}\n{lieu.aff(perso)}")
                texte_fait = f"{nom_perso} est entré dans le lieu {lieu.nom}"
        # commande sortir
        elif is_one_of(action, self.commandes_dat["sortir"]["com"]):
            lieu_actuel = self.game.map_.lieux[perso.lieu]
            idls = []
            if len(args) == 0:
                for id_lieu, action in lieu_actuel.lieux_accessibles:
                    if action == "sortir":
                        idls.append(id_lieu)
            else:
                for id_lieu, action in lieu_actuel.lieux_accessibles:
                    if action == "sortir":
                        idls.append(id_lieu)
                        eq_ap = False
                        for lap in lieu.appellations:
                            print(lap)
                            if are_texts_equals(lap, args[0]) or are_texts_equals(lap, " ".join(args)):
                                eq_ap = True
                                break
                        if are_texts_equals(lieu.nom, args[0]) or eq_ap:
                            idls.append(id_lieu)
            if len(idls) == 0:
                self.send_message(client, "Vous ne pouvez sortir de nulle part !")
            elif len(idls) > 1:
                self.send_message(client, "Vous pouvez sortir de plusieurs lieux !")
            else:
                lieu = self.game.map_.lieux[idls[0]]
                perso.lieu = idls[0]
                self.send_message(client, f"Vous sortez de {lieu.nom}\n{lieu.aff(perso)}")
                texte_fait = f"{nom_perso} est sortit du lieu {lieu.nom}"
        # commande aller
        elif is_one_of(action, self.commandes_dat["aller"]["com"]):
            lieu_actuel = self.game.map_.lieux[perso.lieu]
            is_valid = False
            if traiter_txt(args[0]) in self.directions:
                for id_lieu, action in lieu_actuel.lieux_accessibles:
                    if action == args[0]:
                        lieu = self.game.map_.lieux[id_lieu]
                        texte_fait = f"{nom_perso} est allé à {lieu.nom}"
                        self.send_message(client, f"Vous vous déplacez vers {lieu.nom}.\n{lieu.aff(perso)}", True)
                        perso.lieu = id_lieu
                        is_valid = True
            else:
                for id_lieu, _ in lieu_actuel.lieux_accessibles:
                    lieu = self.game.map_.lieux[id_lieu]
                    eq_ap = False
                    for lap in lieu.appellations:
                        if are_texts_equals(lap, args[0]) or are_texts_equals(lap, " ".join(args)):
                            eq_ap = True
                            break
                    if are_texts_equals(lieu.nom, args[0]) or eq_ap:
                        perso.lieu = id_lieu
                        texte_fait = f"{nom_perso} est allé à {lieu.nom}"
                        self.send_message(client, f"Vous vous déplacez vers {lieu.nom}.\n{lieu.aff(perso)}", True)
                        is_valid = True
                        break
            if not is_valid:
                self.send_message(client, "Le lieu que vous voulez visiter n'est pas disponible. En effet, il semble qu'il n'existe que dans votre tête. Quel dommage, il avait l'air magnifique !", True)
            pass
        # commande parler
        elif is_one_of(action, self.commandes_dat["parler"]["com"]):
            if pnj_cible is not None:
                if type(pnj_cible.dialogue) in [dict, list]:
                    perso.dialogue_en_cours = pnj_cible.dialogue
                    perso.interlocuteur = pnj_cible
                    perso.test_dialogue()
                    if perso.dialogue_en_cours is None or type(perso.dialogue_en_cours) == list:
                        texte_fait = self.fin_dialogue(client, perso, nom_perso)
                    self.send_message(client, f"Vous parlez avec {pnj_cible.nom}\n{self.format_dialog(perso)}", True)
                    perso.dialogue_en_cours = perso.dialogue_en_cours[list(perso.dialogue_en_cours.keys())[0]]
                    texte_fait = f"{nom_perso} a commencé à parler avec {pnj_cible.nom}"
                    time.sleep(0.1)
                    while perso.dialogue_en_cours is not None:
                        #
                        ii = self.input_bonne_reponse(client, "Que répondez vous ?", [str(v) for v in range(1, 3)])
                        idd = int(ii) - 1
                        dial = perso.dialogue_en_cours
                        if idd >= len(dial.keys()):
                            self.send_message(client, "Vous voulez répondre autre chose ? Comme si vous avez la liberté d'expression ici ...", True)
                            return
                        perso.dialogue_en_cours = dial[list(dial.keys())[idd]]
                        #
                        if type(perso.dialogue_en_cours) == dict:
                            perso.test_dialogue()
                            if perso.dialogue_en_cours is None or type(perso.dialogue_en_cours) == list:
                                texte_fait = self.fin_dialogue(client, perso, nom_perso)
                            if type(perso.dialogue_en_cours) == dict:
                                self.send_message(client, self.format_dialog(perso), True)
                                perso.dialogue_en_cours = perso.dialogue_en_cours[list(perso.dialogue_en_cours.keys())[0]]
                                perso.test_dialogue()
                        if perso.dialogue_en_cours is None or type(perso.dialogue_en_cours) == list:
                            texte_fait = self.fin_dialogue(client, perso, nom_perso)
                else:
                    self.send_message(client, "Votre interlocuteur n'a visiblement pas l'air d'avoir envie de parler, peut-être que vous êtes en train de l'embêter, ou bien il est muet, c'est aussi une possibilité ! ", True)
                    texte_fait = f"{nom_perso} a voulu parler avec {pnj_cible.nom}, mais ce dernier n'a pas très envie de discuter avec {nom_perso}"
            else:
                self.send_message(client, "vous voulez parler à un fantôme ? Oups, j'oubliais que les fantômes existent dans ce monde, pas comme votre interlocuteur ...", True)
                return
        # commande message
        elif is_one_of(action, self.commandes_dat["message"]["com"]):
            self.send_all_except_c(client, json.dumps({"type": "message", "value": self.clients[client]["player"].pseudo + " : " + " ".join(args)}))
        # commande attaquer
        elif is_one_of(action, self.commandes_dat["attaquer"]["com"]):
            if ennemi_cible is not None:
                patt_cac = perso.get_attaque("corps à corps")
                patt_dist = perso.get_attaque("distance")
                if patt_cac is None and patt_dist is None:
                    mes = "Vous ne pouvez pas attaquer, vous êtes aussi nul au corps à corps qu'à distance ..."
                    self.send_message(client, mes)
                else:
                    if patt_cac is not None and patt_dist is not None:
                        erreur = ""
                        message = f"{erreur}\n\nComment voulez vous attaquer ?\n  - (1) : au corps à corps (dégats : {patt_cac})\n  - (2) : à distance (dégats : {patt_dist})"
                        ii = self.input_bonne_reponse(client, message, [str(v) for v in range(1, 3)])
                        tp_att = ["corps à corps", "distance"][int(ii)]
                    else:
                        tp_att = "corps à corps" if patt_dist is None else "distance"
                    msg_result = perso.attaque_cible(ennemi_cible, tp_att)
                    self.send_message(client, msg_result)
                    texte_fait = f"{nom_perso} a attaqué {ennemi_cible.nom} :\n{msg_result}"
                    tour_p += 1
            else:
                mes = "Je ne trouve pas cet ennemi, pour compenser, voulez vous que je me frappe moi-même ?"
                self.send_message(client, mes)
        # commande sort
        elif is_one_of(action, self.commandes_dat["sort"]["com"]):
            pass
        # commande utiliser
        elif is_one_of(action, self.commandes_dat["utiliser"]["com"]):
            pass  # Utiliser un objet sur un autre

        elif data_len <= 2:
            self.send(client, "Commande inconnue", True)
            pass  # Action avec plus de 2 paramètres au-delà

        # Ce qui suit sont des commandes avec au moins 2 argument ou plus
        # commande mettre
        elif is_one_of(action, self.commandes_dat["mettre"]["com"]):
            pass
        # Il n'y a plus de commandes apres ca
        else:
            self.send_message(client, "J'ai pas compris ce que vous vouliez, pouvez vous répetez plus clairement, et si vous connaissez pas les commandes, vous pouvez taper 'aide' pour voir la liste des commandes disponibles.")

        self.game.map_.lieux[perso.lieu].tour += tour_p

        # Tour des ennemis
        # tous les ennemis de tous les lieux font leur tour
        for lieu in self.game.map_.lieux.values():
            while lieu.tour >= 1:
                lieu.tour -= 1
                for en in lieu.ennemis:
                    en.tour(lieu.index)
        # affichage de l'action du joueur au autres
        if texte_fait != "":
            self.send_all_except_c(client, json.dumps({"type": "message", "value": texte_fait}))

    # endregion

    def bienvenue(self, client):
        """Envoie un message de bienvenue au client

        Args:
            client(socket.socket): Référence au client se connectant.

        Auteur : ???

        """
        p = self.clients[client]["player"].perso
        mess = {"type": "message", "value": f"Bienvenue !\nVous aller jouer au jeu {self.nom_du_jeu} et nous espérons que vous vous amuserez !\n\nVous êtes {p.nom}\nVie : {p.vie}/{p.vie_totale}\n\n{self.game.map_.lieux[p.lieu].aff(p)}"}
        mess = json.dumps(mess)
        self.send(client, mess)
        mess = {"type": "message", "value": f"{p.nom} a rejoint la partie, il est dans le lieu : {self.game.map_.lieux[p.lieu].nom}"}
        mess = json.dumps(mess)
        self.send_all_except_c(client, mess)

    def main(self):
        """Met en route le serveur.

        Auteur : Nathan

        """
        self.start()
        # TODO
        pass


# On lance le programme ici
if __name__ == "__main__":
    server = Server()
    server.main()
