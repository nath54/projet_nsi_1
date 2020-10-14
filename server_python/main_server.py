#PROGRAMME PRINCIPAL DU SERVEUR

#Importations :
#librairie python
import socket
import _thread
import json
import sys
#nos librairies
import client_db
import game

#
class Server:
    def __init__(self):
        #infos socket
        self.host = "" # si on ne met rien, écoute sur toutes les cartes réseaux.
        # Sinon, on met une adresse IP ou alias correspondant à ce qu'on veut.
        self.port = 9876 # On doit utiliser un port qui n'est pas déjà utilisé.
        self.max_size=1024 #taille maximale d'un message recu ou envoyé
        self.clients={} #dictionnaire ayant pour clé les clients et en valeur un dictionnaire de propriétés relatives au client
        self.server=None
        #
        #TODO
        pass

    def start(self):
        # On prépare le serveur
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # C'est un serveur TCP/IP
        self.server.bind((self.host, self.port))
        # On lui associe une adresse et un port
        self.server.listen(5)
        #
        print("server started")
        # Le serveur est prèt à recevoir des connections entrantes
        while 1: # On lance une boucle infinie pour recevoir toutes les connections
            (client,info) = self.server.accept()
            _thread.start_new_thread(self.handle,(client,info))
            # On lance le handler en tant que thread pour ne pas bloquer cette boucle infinie.

    def handle(self,client,infos):
        self.on_accept(client,infos)
        print()
        while True:
            msg = client.recv(self.max_size)
            self.on_message(client,infos,msg)
            try:
                msg = client.recv(self.max_size)
                self.on_message(client,infos,msg)
            except Exception as e:
                print(e)
                self.on_close(client,infos)
                return

    #fonction qui envoie un message a tous les autres clients
    def send_all_except_c(self,client,mes):
        mes=json.dumps(mes)
        mes=mes.encode(encoding="utf-8")
        if sys.getsizeof(mes)>self.max_size:
            return
        for autre_client in self.clients.keys():
            if client!=autre_client:
                autre_client.send(mes)

    #fonction qui envoie un message a un client précis
    def send(self,client, mes):
        mes=json.dumps(mes)
        mes=mes.encode(encoding="utf-8")
        size=sys.getsizeof(mes)
        if size>self.max_size:
            print("ERROR : Le message est trop long ! "+str(size)+" bytes/"+str(self.max_size)+" bytes")
            return
        else:
            client.send(mes)

    def on_accept(self,client,i): # Lorsqu'une connection entrante est acceptée
        self.clients[client]={} #on y mettra plus d'infos plus tard
        print("connection acceptée",client)

    def on_message(self,client,infos,mes): # Lorsqu'une connection envoie un message
        mes=mes.decode(encoding="utf-8")
        if len(mes)>0:
            print("recu : ",mes)
            if mes[0]=="{":
                data=json.loads(mes)
                self.commandes(data)

    def on_close(self,client,infos): # Lorsqu'une connection se ferme
        print("connection fermée",client)
        del(self.clients[client])

    def commandes(self,data):
        #TODO
        pass

    def main(self):
        # Met en route le serveur.
        self.start()
        #TODO
        pass

#on lance le programme ici
if __name__=="__main__":
    server=Server()
    server.main()
