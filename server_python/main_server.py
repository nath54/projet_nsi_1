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
        host (str): Si vide, écoute toutes les cartes réseaux
                    Sinon, on met l'adresse IP que l'on veut
        port (int): On utilise un port inutilisé
        max_size (int): Taille maximale d'un message reçu
        clients (dict): Clé -- socket.socket
                        Val -- `dict` de propriétés relatives au client
        server (socket): ???

        version(int) : version du jeu (pour la comparer avec la version de la bdd)
    """

    def __init__(self):
        """Initialise le serveur de jeu."""
        self.host = ""
        self.port = 9876
        self.max_size = 2048
        self.clients = {}
        self.server = None
        self.game = Game(jload)
        self.client_db = Client_mariadb(self.game)
        self.game.client_db = self.client_db
        self.version = 1
        self.nom_du_jeu = "Py RPG MasterClass Option text multijoueur"
        #
        self.commandes_dat = {
            "aide": {"com": ["aide", "help", "commandes"],
                     "help": """Affiche ce message d'aide""",
                     "fini": False},
            "voir": {"com": ["voir"],
                     "help": """Affiche les infos du lieu""",
                     "fini": True},
            "inventaire": {"com": ["inventaire"],
                           "help": """Affiche l'inventaire""",
                           "fini": True},
            "equipement": {"com": ["equipement"],
                           "help": """Affiche l'equipement""",
                           "fini": True},
            "stats": {"com": ["stats", "statistiques"],
                      "help": """Affiche les stats du perso""",
                      "fini": True},
            "quit": {"com": ["quit", "quitter", "exit"],
                     "help": """Quitte le jeu""",
                     "fini": False},
            "attendre": {"com": ["attendre"],
                         "help": """Attends un tour""",
                         "fini": False},
            "desequiper": {"com": ["desequiper"],
                           "help": """Desequipe un objet""",
                           "fini": False},
            "equiper": {"com": ["equiper"],
                        "help": """Equipe un objet""",
                        "fini": False},
            "examiner": {"com": ["examiner"],
                         "help": """Affiche la description d'un objet""",
                         "fini": True},
            "prendre": {"com": ["prendre", "ramasser"],
                        "help": """Prend l'objet et le rajoute dans l'inventaire""",
                        "fini": True},
            "jeter": {"com": ["jeter", "lacher"],
                      "help": """Enleve l'objet de l'inventaire""",
                      "fini": True},
            "ouvrir": {"com": ["ouvrir"],
                       "help": """Ouvre un objet qui s'ouvre""",
                       "fini": False},
            "fermer": {"com": ["fermer"],
                       "help": """Ferme un objet qui se ferme""",
                       "fini": False},
            "aller": {"com": ["aller", "bouger"],
                      "help": """Déplace le personnage dans un autre lieu""",
                      "fini": True},
            "parler": {"com": ["parler", "discuter"],
                       "help": """Parle avec un pnj""",
                       "fini": False},
            "message": {"com": ["message"],
                        "help": """Envoie un message dans le chat du jeu""",
                        "fini": False},
            "attaquer": {"com": ["attaquer", "taper", "tabasser"],
                         "help": """Attaque un ennemi""",
                         "fini": False},
            "sort": {"com": ["sortilege", "sort", "magie"],
                     "help": """Lance un sortilege""",
                     "fini": False},
            "utiliser": {"com": ["utiliser"],
                         "help": """Utilise un objet (potentiellement sur un autre objet)""",
                         "fini": False},
            "mettre": {"com": ["mettre", "ranger"],
                       "help": """Met un objet dans un objet de type conteneur""",
                       "fini": False},
        }

    def start(self):
        """Lance le serveur.

        Cette fonction permet de lancer le serveur en TCP/IP, acceptant
        jusqu'à 5 connexions simultanées.
        On va aussi lancer le jeu ici, bdd, Game, ...

        Auteur: Nathan

        """

        # On recupere la version du jeu (pour la comparer a celle de la db)
        f = open("version", "r")
        self.version = int(f.read())
        f.close()

        # Teste si c'est la bdd est initialisée, si non, on l'initialise
        if self.client_db.test_first_time():
            print("premier lancement")
            self.client_db.init_database()

        # On va aussi essayer de mettre à jour la bdd
        self.client_db.update()

        # On va vérifier les différentes versions des données de la bdd
        if True or self.client_db.test_version(self.version):
            self.client_db.transfert_json_to_bdd()

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
            client (socket.socket): Référence au client avec
                                    qui gérer l'interaction
            infos (couple): couple d'informations : ip, ???

        Auteur: Nathan

        """
        self.on_accept(client, infos)
        while True:
            # try:
            msg = client.recv(self.max_size)
            self.on_message(client, infos, msg)
            # except Exception as e:
            #     print(e)
            #     self.on_close(client)
            #     return

    def send_all_except_c(self, client, message):
        """Envoie un message a tous les autres clients.

        Args:
            client (socket.socket): Référence au client ayant envoyé le message
            message (str): Message à envoyer aux autres clients

        Auteur: Nathan

        """
        message = json.dumps(message)
        message = message.encode(encoding="utf-8")
        if sys.getsizeof(message) > self.max_size:
            return
        for autre_client in self.clients.keys():
            if client != autre_client:
                autre_client.send(message)

    def send(self, client, message, print_=False, important=False):
        """Envoie un message a un client précis.

        Args:
            client (socket.socket): Référence au client ayant envoyé le message
            message (str): Message à envoyer aux autres clients

        Auteur: Nathan

        """
        if print_:
            print(message)
        message = json.dumps(message)
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

    def on_accept(self, client, i):
        """Réaction si une connexion entrante est acceptée.

        Args:
            client (socket.socket) Référence au client qui s'est connecté
            i (couple): couple d'informations : ip, ???

        Auteur: Nathan

        """
        self.clients[client] = {"player": None}
        # On y mettra plus d'infos plus tard
        print("Connexion acceptée", client)
        print(type(client), i)

    def on_message(self, client, infos, message):
        """Réaction si un message est reçu.

        Args:
            client (socket.socket): Référence au client ayant envoyé le message
            infos (couple): couple d'informations : ip, ???
            message (str): Message tapé par l'utilisateur.

        Auteur: Nathan

        """
        message = message.decode(encoding="utf-8")
        if len(message) <= 0:
            return
        db = self.client_db
        print(f"{self.clients[client]} : {message}")
        if is_json(message):
            data = json.loads(message)
            if data["type"] == "cheat_code":
                cheat_code(self, client, data["commande"])
            if data["type"] == "commande":
                cl = self.clients[client]
                if (not ("player" in cl.keys())) or (cl["player"] is None):
                    dict_ = {"type": "not connected",
                             "value": "Veuillez vous connecter pour jouer"}
                    self.send(client, json.dumps(dict_))
                else:
                    self.commandes(client, data)
            elif data["type"] == "inscription":
                pseudo = data["pseudo"]
                email = data["email"]
                password = data["password"]
                erreur = db.test_compte_inscrit(pseudo, email)
                if erreur:
                    dict_ = {"type": "inscription failed", "value": erreur}
                    self.send(client, json.dumps(dict_))
                else:
                    reussi, id_ = db.inscription(pseudo, email, password)
                    if reussi:
                        self.clients[client]["player"] = Player(pseudo, self.game, id_)
                        self.send(client, json.dumps({"type": "inscription successed"}))
                        time.sleep(0.1)
                        dict_ = {"type": "genres", "genres": json.dumps(db.get_genres())}
                        self.send(client, json.dumps(dict_))
                        time.sleep(0.1)
                        self.send(client, json.dumps({"type": "creation perso"}))
                        # il faudra sans doute envoyer d'autres infos, comme une clé de connexion par exemple
                    else:
                        raise UserWarning("ERREUR : La BDD a échoué")
            elif data["type"] == "connection":
                pseudo = data["pseudo"]
                password = data["password"]
                erreur, id_ = self.client_db.test_connexion(pseudo, password)
                if erreur:
                    self.send(client, json.dumps({"type": "connection failed", "value": erreur}))
                else:
                    self.send(client, json.dumps({"type": "connection successed"}))
                    self.clients[client]["player"] = Player(pseudo, self.game, id_)
                    data_perso = self.client_db.get_perso(id_)
                    self.clients[client]["player"].load_perso(data_perso)
                    # il faudra sans doute envoyer d'autres infos, comme une clé de connexion par exemple
                    self.bienvenue(client)
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

        Auteur: Nathan

        """
        print("Connexion fermée", client)
        self.send(client, json.dumps({"type": "connection fermée"}))
        del(self.clients[client])

    def save(self, client):
        pass

    # region Commandes
    def commandes(self, client, data):
        """Éxecute les commandes entrée par l'utilisateur.

        Args:
            client(socket): Personne qui a entré la commande
            data(dict): un dictionnaire contenant les éléments d'une commande
                exemple : {"command": "attaquer", "arguments": "ennemi"}

        Auteur: Nathan, Hugo

        """
        data_len = len(data.keys())
        action = data["commande"]
        args = data["arguments"].split(" ")
        perso = self.clients[client]["player"].perso
        print("data_len : ", data_len)
        print("len args : ", len(args))

        # Les premieres commandes sont des commandes à 0 ou plus arguments
        if is_one_of(action, self.commandes_dat["aide"]["com"]):
            txt_help = "COMMANDES :"
            for key in self.commandes_dat.keys():
                t = "'" + "', '".join(self.commandes_dat[key]["com"]) + "'"
                tt = self.commandes_dat[key]["help"]
                ttt = "Fonctionne" if self.commandes_dat[key]["fini"] else "Ne fonctionne pas"
                txt_help += f"\n\t- {t} : {tt} [{ttt}]"
            self.send(client, {"type": "message", "value": txt_help}, True)
        if is_one_of(action, ["voir"]):
            self.send(client, {"type": "message", "value": self.game.map_.lieux[perso.lieu].aff()}, True)
        elif is_one_of(action, self.commandes_dat["inventaire"]["com"]):
            if len(args) == 0 or args[0] == "":
                self.send(client, {"type": "message", "value": perso.format_invent()}, True)
            else:
                self.invent_multi_args(client, data)
        elif is_one_of(action, self.commandes_dat["equipement"]["com"]):
            self.send(client, {"type": "message", "value": perso.format_equip()}, True)
        elif is_one_of(action, self.commandes_dat["stats"]["com"]):
            if len(args) == 0:
                print("stats :", perso.format_stats())
                self.send(client, {"type": "message", "value": perso.format_stats()}, True)
            else:
                pass  # TODO: Afficher stats d'un autre Etre (bof)
        elif is_one_of(action, self.commandes_dat["quit"]["com"]):
            self.on_close(client)
        elif is_one_of(action, self.commandes_dat["attendre"]["com"]):  # Bof
            pass
        elif data_len <= 1:
            self.send(client, {"type": "message", "value": "Commande inconnue"}, True)

        # Ce qui suit sont des commandes avec au moins 1 argument
        elif is_one_of(action, self.commandes_dat["desequiper"]["com"]):
            b = perso.desequiper(args[0])
            if b:
                mess = f"Vous avez retiré {args[0]} !"
            else:
                mess = f"Vous n'aviez pas de {args[0]} sur vous..."
            self.send(client, {"type": "message", "value": mess}, True)
        elif is_one_of(action, self.commandes_dat["equiper"]["com"]):
            b = perso.equiper(args[0])
            if b:
                mess = f"Vous avez équipé {args[0]}"
            else:
                mess = f"Vous ne possédez pas '{args[0]}'"
            self.send(client, {"type": "message", "value": mess}, True)
        # On définit l'objet ciblé avec lequel l'utilisateur voudra (peut-être) agir
        obj_cible = None
        if len(args) >= 1:
            for obj in perso.game.map_.lieux[perso.lieu].objets:
                if are_texts_equals(obj.nom, args[0]) or traiter_txt(" ".join(args)).startswith(traiter_txt(obj.nom)):
                    obj_cible = obj
                    break

        if is_one_of(action, self.commandes_dat["examiner"]["com"]):
            if obj_cible is None:
                self.send(client, {"type": "message", "value": "Si je ne vois pas l'objet, dois-je essayer d'en imaginer une description foireuse ?"}, True)
            else:
                self.send(client, {"type": "message", "value": f"{obj_cible.__repr__()}"}, True)
        elif is_one_of(action, self.commandes_dat["prendre"]["com"]):
            if obj_cible is None:
                mess = "Honnêtement, j'adore le concept. Mais l'objet existe pas. Ou il est pas là. Au choix !"
                self.send(client, {"type": "message", "value": mess}, True)
                return
            if obj_cible.type not in ["décor", "contenant"]:
                perso.add_to_invent(obj.index)
                self.game.map_.lieux[perso.lieu].objets.remove(obj_cible)
                self.send(client, {"type": "message", "value": f"Vous avez pris le/la {obj.nom}."})
        elif is_one_of(action, self.commandes_dat["jeter"]["com"]):
            arg = args[0]
            qt = args[1] if len(args) > 1 else 1
            if type(qt) != int:
                try:
                    qt = int(qt)
                except Exception:
                    # TODO : renvoyer une erreur au client
                    return

            for i in range(len(perso.inventaire)):
                obj = perso.inventaire[i]
                if obj[0].nom == arg:
                    if obj[1] < qt:
                        self.send(client, json.dumps({"type": "message", "value": f"Vous ne pouvez jeter autant de {obj[0].nom} que ça !"}), True)
                    else:
                        for i in range(qt):
                            new_obj = Objet(obj[0].index, self.game)
                            perso.game.map_.lieux[perso.lieu].objets.append(new_obj)
                        if obj[1] == qt:
                            del perso.inventaire[i]
                        else:
                            perso.inventaire[i][1] -= qt
        elif is_one_of(action, self.commandes_dat["ouvrir"]["com"]):
            if obj_cible.type == "contenant":
                if obj_cible.ouvert:
                    mess = "Cet objet est déjà ouvert..."
                else:
                    mess = f"Vous ouvrez ce superbe {obj_cible.nom}\n{obj_cible.format_contenu()}"
            else:
                mess = "Comment ouvrir un objet qui ne possède pas d'ouverture..."
            self.send(client, {"type": "message", "value": mess}, True)
        elif is_one_of(action, self.commandes_dat["fermer"]["com"]):
            if obj_cible.type == "contenant":
                if obj_cible.ouvert:
                    mess = f"Vous avez refermé le {obj_cible.nom}."
                else:
                    mess = f"Vous avez refermé le/la {obj_cible.nom}, qui était déjà fermé... Quel exploit !"
            else:
                mess = "Fermer un objet qui ne se ferme pas... Original."
            self.send(client, {"type": "message", "value": mess}, True)
        elif is_one_of(action, self.commandes_dat["aller"]["com"]):
            lieu = self.game.map_.lieux[perso.lieu]
            is_valid = False
            if args[0] in ["ouest", "est", "nord", "sud", "nord-ouest",
                           "nord-est", "sud-ouest", "sud-est"]:
                for id_lieu, action in lieu.lieux_accessibles:
                    if action == args[0]:
                        perso.lieu = id_lieu
                        is_valid = True
            else:
                for id_lieu, _ in lieu.lieux_accessibles:
                    lieu = self.game.map_.lieux[id_lieu]
                    eq_ap = False
                    for lap in lieu.appellations:
                        print(lap)
                        if are_texts_equals(lap, args[0]) or are_texts_equals(lap, " ".join(args)):
                            eq_ap = True
                            break
                    if are_texts_equals(lieu.nom, args[0]) or eq_ap:
                        perso.lieu = id_lieu
                        self.send(client, {"type": "message", "value": f"Vous vous déplacez vers {lieu.nom}.\n{lieu.aff()}"}, True)
                        is_valid = True
                        break
            if not is_valid:
                self.send(client, {"type": "message", "value": "Le lieu que vous voulez visiter n'est pas disponible. En effet, il semble qu'il n'existe que dans votre tête. Quel dommage, il avait l'air magnifique !"}, True)
            pass
        elif is_one_of(action, self.commandes_dat["parler"]["com"]):
            pass
        elif is_one_of(action, self.commandes_dat["message"]["com"]):
            pass
        elif is_one_of(action, self.commandes_dat["attaquer"]["com"]):
            ennemi_cible = None
            if len(args) >= 1:
                for en in self.game.map_.lieux[perso.lieu]:
                    if are_texts_equals(args[0], en.nom) or traiter_txt(" ".join(args)).startswith(traiter_txt(en.nom)):
                        ennemi_cible = en
            if ennemi_cible is not None:
                msg_result = perso.attaque_cible(ennemi_cible)
                self.send(client, {"type": "message", "value": msg_result})
        elif is_one_of(action, self.commandes_dat["sort"]["com"]):
            pass
        elif data_len <= 2:
            self.send(client, "Commande inconnue", True)
            pass  # Action avec plus de 2 paramètres au-delà

        # Ce qui suit sont des commandes avec au moins 2 argument ou plus
        elif is_one_of(action, self.commandes_dat["utiliser"]["com"]):
            pass  # Utiliser un objet sur un autre
        elif is_one_of(action, self.commandes_dat["mettre"]["com"]):
            pass

        # TODO
        pass

    def invent_multi_args(self, perso, data):
        """Si la commande entrée est 'inventaire ...'.

        Gère le cas où la commande entrée est 'inventaire voir ...' ou
        'inventaire utiliser ...'

        Args:
            perso(Perso): Personnage demandant l'action
            data(dict): Dict contenant les informations de la commande

        Auteur: Hugo

        """
        compl = data.get("arg_1", "")
        nom_obj = data.get("arg_2", "")
        if compl in ["voir", "examiner"]:
            objet = perso.search_invent(nom_obj)
            if objet is not None:
                self.send(client, objet, True)
            else:
                self.send(client, "Désolé, vous ne possédez pas cet objet.", True)
        elif compl == "utiliser":
            objet = perso.search_invent(nom_obj)
            if objet is not None:
                perso.consomme_item(objet)
                self.send(client, f"{nom_obj} a été consommé !", True)
            else:
                self.send(client, "Désolé, vous ne possédez pas cet objet.", True)
    # endregion

    def bienvenue(self, client):
        p = self.clients[client]["player"].perso
        mess = {"type": "message", "value": f"Bienvenue !\nVous aller jouer au jeu {self.nom_du_jeu} et nous esperons que vous vous amuserez !\n\nVous êtes {p.nom}\nVie : {p.vie}/{p.vie_totale}\n\n{self.game.map_.lieux[p.lieu]}"}
        mess = json.dumps(mess)
        self.send(client, mess)

    def main(self):
        """Met en route le serveur.

        Auteur: Nathan

        """
        self.start()
        # TODO
        pass


# On lance le programme ici
if __name__ == "__main__":
    server = Server()
    server.main()
