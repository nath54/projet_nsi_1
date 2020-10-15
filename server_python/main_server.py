# PROGRAMME PRINCIPAL DU SERVEUR

# TODO: Remplacer les ??? dans les docstrings

# Importations :
# librairie python
import socket
import _thread
import json
import sys
# nos librairies
import client_db
import game


# Classe du serveur
class Server:
    """Classe du serveur du jeu

    Attributes:
        host (str): Si vide, écoute toutes les cartes réseaux
                    Sinon, on met l'adresse IP que l'on veut
        port (int): On utilise un port inutilisé
        max_size (int): Taille maximale d'un message, envoyé ou reçu
        clients (dict): Clé -- Clients
                        Val -- `dict` de propriétés relatives au client
        server (socket): ???
    """
    def __init__(self):
        self.host = ""
        self.port = 9876
        self.max_size = 1024
        self.clients = {}
        self.server = None
        # TODO
        pass

    def start(self):
        """Lance le serveur

        Cette fonction permet de lancer le serveur en TCP/IP, acceptant
        jusqu'à 5 connexions simultanées.

        Author: ???

        """
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        print("Server started.")
        while 1:
            (client, info) = self.server.accept()
            _thread.start_new_thread(self.handle, (client, info))

    def handle(self, client, infos):
        """Gère l'interaction serveur-client

        Args:
            client (???): Référence au client avec qui gérer l'interaction
            infos (???): ???

        Author: ???

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
                self.on_close(client, infos)
                return

    def send_all_except_c(self, client, message):
        """Fonction qui envoie un message a tous les autres clients

        Args:
            client (???): Référence au client ayant envoyé le message
            message (str): Message à envoyer aux autres clients

        Author: ???

        """
        message = json.dumps(message)
        message = message.encode(encoding="utf-8")
        if sys.getsizeof(message) > self.max_size:
            return
        for autre_client in self.clients.keys():
            if client != autre_client:
                autre_client.send(message)

    def send(self, client, message):
        """Envoie un message a un client précis

        Args:
            client (???): Référence au client ayant envoyé le message
            message (str): Message à envoyer aux autres clients

        Author: ???

        """
        message = json.dumps(message)
        message = message.encode(encoding="utf-8")
        size = sys.getsizeof(message)
        if size > self.max_size:
            print(f"""ERREUR : Le message est trop long ! {str(size)} bytes/
                   {str(self.max_size)} bytes""")
            return
        else:
            client.send(message)

    def on_accept(self, client, i):
        """Réaction si une connexion entrante est acceptée

        Args:
            client (???): Référence au client qui s'est connecté
            i (???): ???

        Author: ???

        """
        self.clients[client] = {}          # On y mettra plus d'infos plus tard
        print("Connexion acceptée", client)

    def on_message(self, client, infos, message):
        """Réaction si un message est reçu

        Args:
            client (???): Référence au client ayant envoyé le message
            infos (???): ???
            message (str): Message tapé par l'utilisateur.

        Author: ???

        """
        message = message.decode(encoding="utf-8")
        if len(message) > 0:
            print("Reçu : ", message)
            if message[0] == "{":
                data = json.loads(message)
                self.commandes(data)

    def on_close(self, client, infos):
        """Réaction si une connexion se ferme

        Args:
            client (???): Référence au client ayant fermé son application
            infos (???): ???

        Author: ???

        """
        print("Connexion fermée", client)
        del(self.clients[client])

    def commandes(self, data):
        """???

        Args:
            data (dict): un dictionnaire contenant les éléments d'une commande
                exemple : {"com":"attaquer","attaquant":perso,"cible":ennemi}

        Author: ???

        """
        # TODO
        pass

    def main(self):
        """Met en route le serveur

        Author: ???

        """
        self.start()
        # TODO
        pass


# On lance le programme ici
if __name__ == "__main__":
    server = Server()
    server.main()
