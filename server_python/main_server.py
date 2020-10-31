# PROGRAMME PRINCIPAL DU SERVEUR

# TODO: Remplacer les ??? dans les docstrings

# region Importations :
# librairie python
import socket
import _thread
import json
import sys

# nos librairies
from client_db import Client_mariadb
from Game.Game import Game
from Game.Etres.Perso import Perso
from Player import Player
# endregion


# fonction qui teste si un texte est du format json
def is_json(myjson):
    """Fonction qui teste si un string est de format json."""
    try:
        json.loads(myjson)
    except ValueError:
        return False
    return True


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
    """

    def __init__(self):
        """Initialise le serveur de jeu."""
        self.host = ""
        self.port = 9876
        self.max_size = 1024
        self.clients = {}
        self.server = None
        self.game = Game()
        self.client_db = Client_mariadb(self.game)
        # TODO
        pass

    def start(self):
        """Lance le serveur.

        Cette fonction permet de lancer le serveur en TCP/IP, acceptant
        jusqu'à 5 connexions simultanées.
        On va aussi lancer le jeu ici, bdd, Game, ...

        Author: Nathan

        """
        # Teste si c'est la bdd est initialisée, si non, on l'initialise
        if self.client_db.test_first_time():
            print("premier lancement")
            self.client_db.init_database()

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

        Author: Nathan

        """
        self.on_accept(client, infos)
        while True:
            msg = client.recv(self.max_size)
            self.on_message(client, infos, msg)
            try:
                msg = client.recv(self.max_size)
                self.on_message(client, infos, msg)
            except Exception as e:
                print(e)
                self.on_close(client)
                return

    def send_all_except_c(self, client, message):
        """Fonction qui envoie un message a tous les autres clients.

        Args:
            client (socket.socket): Référence au client ayant envoyé le message
            message (str): Message à envoyer aux autres clients

        Author: Nathan

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

        Author: Nathan

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

        Author: Nathan

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

        Author: Nathan

        """
        message = message.decode(encoding="utf-8")
        if len(message) > 0:
            print(f"{self.clients[client]} : {message}")
            if is_json(message):
                data = json.loads(message)
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
                    erreur = self.client_db.test_compte_inscrit(pseudo, email)
                    if erreur:
                        self.send(client, json.dumps({"type": "inscription failed", "value": erreur}))
                    else:
                        reussi, id_ = self.client_db.inscription(pseudo, email, password)
                        if reussi:
                            self.clients[client]["player"] = Player(pseudo, self.game, id_)
                            self.send(client, json.dumps({"type": "inscription successed"}))
                            self.send(client, json.dumps({"type": "creation perso"}))
                            # il faudra sans doute envoyer d'autres infos, comme une clé de connection par exemple
                        else:
                            raise UserWarning("ERREUR : La bdd a échoué ")
                elif data["type"] == "connection":
                    pseudo = data["pseudo"]
                    password = data["password"]
                    erreur, id_ = self.client_db.test_connection(pseudo, password)
                    if erreur:
                        self.send(client, json.dumps({"type": "connection failed", "value": erreur}))
                    else:
                        self.send(client, json.dumps({"type": "connection successed"}))
                        data_perso = self.client_db.get_perso(pseudo)
                        self.clients[client]["player"] = Player(pseudo, self.game, id_)
                        self.clients[client]["player"].load_perso(data_perso)
                        # il faudra sans doute envoyer d'autres infos, comme une clé de connection par exemple
                elif data["type"] == "perso_cree":
                    self.clients[client]["player"].create_perso(data)
                    self.client_db.set_perso(self.clients[client]["player"].perso)
                else:
                    # TODO
                    pass

    def on_close(self, client):
        """Réaction si une connexion se ferme.

        Args:
            client (socket.socket): Référence au client ayant fermé son application

        Author: Nathan

        """
        print("Connexion fermée", client)
        del(self.clients[client])

    # region Commandes
    def commandes(self, client, data):
        """Éxecute les commandes entrée par l'utilisateur.

        Args:
            client(socket.socket): Personne qui a entré la commande
            data(dict): un dictionnaire contenant les éléments d'une commande
                exemple : {"command": "attaquer", "arg_1": ennemi}

        Author: Nathan, Hugo

        """
        data_len = len(data.keys())
        action = data["commande"]
        perso = self.clients[client]["player"].perso

        # Les premieres commandes sont des commandes à 0 ou plus arguments
        if action == "voir":
            self.send(client, perso.lieu, True)
        elif action == "inventaire":
            if data_len == 1:
                self.send(client, perso.format_invent(), True)
            else:
                self.invent_multi_args(client, data)
        elif action == "equipement":
            self.send(client, perso.format_equip(), True)
        elif action == "stats":
            if data_len == 1:
                self.send(client, perso.format_stats(), True)
            else:
                pass  # TODO: Afficher stats d'un autre Etre (bof)
        elif action == "quit":
            self.on_close(client)
        elif action == "attendre":  # Bof
            pass
        #
        elif data_len <= 1:
            self.send(client, "Commande inconnue", True)

        # Ce qui suit sont des commandes avec au moins 1 argument
        elif action == "desequiper":
            b = perso.desequiper(data["arg_1"])
            if b:
                mess = f"Vous avez retiré {data['arg_1']} !"
            else:
                mess = f"Vous n'aviez pas de {data['arg_1']} sur vous..."
            self.send(client, mess, True)
        elif action == "equiper":
            b = perso.equiper(data["arg_1"])
            if b:
                mess = f"Vous avez équipé {data['arg_1']}"
            else:
                mess = f"Vous ne possédez pas '{data['arg_1']}'"
            self.send(client, mess, True)
        elif action == "examiner":
            pass
        elif action == "fouiller":
            pass
        elif action == "prendre":
            pass
        elif action == "jeter":
            pass
        elif action == "utiliser":
            if data_len == 2:
                pass  # Utiliser un objet
            elif data_len == 3:
                pass  # Utiliser un objet sur un autre
        elif action == "consommer":
            pass
        elif action == "ouvrir":
            pass
        elif action == "fermer":
            pass
        elif action == "aller":
            pass
        elif action == "parler":
            pass
        elif action == "message":
            pass
        elif action == "attaquer":
            pass
        #
        elif data_len <= 2:
            self.send(client, "Commande inconnue", True)
            pass  # Action avec plus de 2 paramètres au-delà

        # Ce qui suit sont des commandes avec au moin 1 argument
        elif action == "mettre":
            pass
        elif action == "sortilege":
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

        Author: Hugo

        """
        compl = data.get("arg_1", "")
        nom_obj = data.get("arg_2", "")
        if compl in ["voir", "examiner"]:
            objet = perso.search_invent(nom_obj)
            if objet is not None:
                print(objet)
                # TODO: send_to_perso(perso)
            else:
                print("Désolé, vous ne possédez pas cet objet.")
                # TODO: send_to_perso(perso)
        elif compl == "utiliser":
            objet = perso.search_invent(nom_obj)
            if objet is not None:
                perso.consomme_item(objet)
                print(f"{nom_obj} a été consommé !")
                # TODO: send_to_perso(perso)
            else:
                print("Désolé, vous ne possédez pas cet objet.")
                # TODO: send_to_perso(perso)
    # endregion

    def main(self):
        """Met en route le serveur.

        Author: Nathan

        """
        self.start()
        # TODO
        pass


# On lance le programme ici
if __name__ == "__main__":
    server = Server()
    server.main()
