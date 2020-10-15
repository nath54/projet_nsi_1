# PROGRAMME PRINCIPAL DU CLIENT DU JEU

# Importations :
import socket
import _thread
import json
import sys


class Client:
    """Classe principale du client

    Attributes:
        host(str): IP de la machine à laquelle se connecter.
        port(int): Port utilisé par le socket
        max_size(int): Taille maximale d'un message en bits
        client(socket): ???

    """
    def __init__(self):
        """Caractéristiques du socket

        Author: ???

        """
        self.host = "localhost"
        self.port = 9876
        self.max_size = 1024
        self.client = None
        # TODO
        pass

    def send(self, message):
        """Permet d'envoyer un message

        Args:
            message(str): Le message à envoyer au serveur

        Author: ???

        """
        message = message.encode(encoding="utf-8")
        size = sys.getsizeof(message)
        if size > self.max_size:
            print(f"""ERREUR : Le message est trop long ! {+str(size)} bytes/
                    {str(self.max_size)} bytes""")
        else:
            self.client.send(message)

    def start(self):
        """Permet de démarrer la connexion au serveur

        Connexion avec le protocole TCP/IP, utilisation d'un thread pour la
        fonction `handle()` afin de ne pas encombrer le thread principal.

        Author: ???

        """
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
        _thread.start_new_thread(self.handle, (self.client,))

    def handle(self):
        """Permet de gérer les messages reçus

        Author: ???

        """
        self.on_connect()
        while True:
            try:
                msg = self.client.recv(self.max_size)
                if len(msg) == 0:
                    raise UserWarning("message vide")
                self.on_message(msg)
            except Exception as e:
                print(e)
                self.on_close()
                return

    def on_connect(self):
        """Réaction si la connexion est acceptée"""
        # TODO
        pass

    def on_message(self, mess):
        """Réaction si un message est reçu

        Args:
            mess(str): Le message reçu (encodé en base 'utf-8')

        Author: ???

        """
        # TODO
        pass

    def on_close(self):
        """Réaction en cas de fermeture/problème

        Author: ???

        """
        # TODO
        pass

    def main(self):
        """Fonction principale du client

        Author: ???

        """
        self.start()
        # TODO
        pass


# Le programme est lancé ici
if __name__ == "__main__":
    client = Client()
    client.main()
