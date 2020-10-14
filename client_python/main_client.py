#PROGRAMME PRINCIPAL DU CLIENT DU JEU

#importations :
import socket
import _thread
import json
import sys

#classe principale du client
class Client:
    def __init__(self):
        #infos pour le socket
        self.host = "localhost"  #ip de la machine, localhost pour travailler en local
        self.port = 9876 #port utilisé par le socket
        self.max_size=2048 #taille maximale en bytes qu'un message peut avoir
        self.client=None
        #
        #TODO
        pass

    #fonction pour envoyer le message 
    def send(self, mes):
        mes=mes.encode(encoding="utf-8") #on encode le message
        size=sys.getsizeof(mes) #on regarde sa taille
        if size>self.max_size: #si la taille du message dépasse la taille maximale autorisée, on n'envoie pas le message
            print("ERROR : Le message est trop long ! "+str(s)+" bytes/"+str(self.max_size)+" bytes")
        else:
            self.client.send(mes)

     # ne pas toucher start et handle, sauf si vous savez ce que vous faites
    def start(self):
        # On prépare le client
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # On utilisera protocole TCP/IP
        self.client.connect((self.host,self.port))
        # Le client est connecté. Il est prèt à envoyer et recevoir des messages.
        _thread.start_new_thread(self.handle,(self.client,))
        # On lance le handler en tant que thread pour ne pas bloquer le reste du programme.
    
    #fonction qui gere les messages recus
    def handle(self):
        self.on_connect(self.client)
        while True:
            try:
                msg = self.client.recv(self.max_size)
                if len(msg)==0: raise UserWarning("message vide")
                self.on_message(msg)
            except:
                print(sys.exc_info()[0])
                self.on_close()
                return

    def on_connect(self): # Lorsque la connection est acceptée
        #TODO
        pass
    
    def on_message(self,mess): # Lorsqu'un message est reçu
        #TODO
        pass

    def on_close(self): # Lorsque la connection se ferme ou un problème a été rencontré
        #TODO
        pass

    #fonction principale du client
    def main(self):
        # Met en route le client
        client = self.start()
        # Ici on peut mettre du code après start ...
        #
        #TODO
        pass


#le programme est lancé ici
if __name__=="__main__":
    client=Client()
    client.main()
