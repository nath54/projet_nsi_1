# PROGRAMME PRINCIPAL DU CLIENT DU JEU

# Importations :
import socket
import _thread
import json
import sys
import asyncio


#la liste des characteres autorisés pour les pseudos, les emails, ou bien les mot de passes
chars = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",
       "A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z",
       "1","2","3","4","5","6","7","8","9","0",
       "-","_","@","."]

#fonction qui teste les emails
def test_email(txt):
    t = txt.split("@")
    if len(t) != 2:
        print("ERREUR /!\\ L'email doit être composé de 2 parties séparées par un @ !")
        return True
    if len(t[1].split(".")) != 2:
        print("ERREUR /!\\ La partie de l'email située après @ doit être "
              "constituée de deux parties séparées par un point !")
        return True
    for c in txt:
        if not c in chars:
            print(f"ERREUR /!\\ Email, Caractère non autorisé : '{c}' !")
            return True
    return False

def test_pseudo(txt):
    if len(txt) < 4:
        print("ERREUR /!\\ Pseudo : Minimum 4 caractères !")
        return True
    if len(txt) > 12:
        print("ERREUR /!\\ Pseudo : Maximum 12 caractères !")
        return True
    for c in txt:
        if not c in chars:
            print(f"ERREUR /!\\ Pseudo, Caractère non autorisé : '{c}' !")
            return True
    return False

def test_password(txt):
    if len(txt) < 8:
        print("ERREUR /!\\ Mot de passe : Minimum 8 caractères !")
        return True
    if len(txt) > 32:
        print("ERREUR /!\\ Mot de passe : Maximum 32 caractères !")
        return True
    for c in txt:
        if not c in chars:
            print(f"ERREUR /!\\ Mot de passe, Caractère non autorisé : '{c}'")
            return True
    return False

#fonction qui teste si un texte est du format json
def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True


class Client:
    """Classe principale du client.

    Attributes:
        host(str): IP de la machine à laquelle se connecter.
        port(int): Port utilisé par le socket
        max_size(int): Taille maximale d'un message en bits
        client(socket): socket.socket

    """

    def __init__(self):
        """Caractéristiques du socket.

        Author: Nathan

        """
        self.host = input("Host ? (si vide sera localshost)\n : ")
        if self.host == "":
            self.host = "localhost"
        self.port = 9876
        self.max_size = 1024
        self.client = None

        self.encours = True
        self.attente = False
        self.etat = "None"

        i=input("Voulez vous que ce soit un client websocket ?")
        if i.lower() in ["o","oui","y","yes"]:
            self.ws=True
            from webserver import WebServer
            self.webserver = WebServer(self)
        else:
            self.ws=False

    def debut(self):
        """
        Fonction qui se lance au début pour savoir si tu veux t'inscrire ou te connecter

        Author : Nathan

        """
        print("Voulez vous :\n  1) Vous inscrire ?\n  2) Vous connecter ?")
        r = input(": ")
        while not r in ["1","2"]:
            r = input(": ")
        if r == "1":
            self.inscription()
        else:
            self.connexion()

    def attente_serv(self):
        """
        Fonction qui attends qu'un message a été recu (dans un autre thread)
        pour continuer dans le thread actuel

        Auteur : Nathan

        """
        self.attente = True
        while self.attente:
            pass

    def connexion(self):
        #pseudo
        pseudo = input("pseudo : ")
        while test_pseudo(pseudo):
            pseudo = input("pseudo : ")
        #password
        password = input("mot de passe : ")
        while test_password(password):
            password = input("mot de passe : ")
        self.send(json.dumps({"type": "connection","pseudo": pseudo,
                              "password": password}))
        print("En attente du serveur ... ")
        self.attente_serv()
        print("recu !")
        if self.etat == "connecté":
            print("Connecté")
            self.interface()
        else:
            self.debut()
        

    def inscription(self):
        #email
        email = input("email : ")
        while test_email(email):
            email = input("email : ")
        #pseudo
        pseudo = input("pseudo : ")
        while test_pseudo(pseudo):
            pseudo = input("pseudo : ")
        #password
        password = input("mot de passe : ")
        while test_password(password):
            password = input("mot de passe : ")
        password_confirm = input("mot de passe (confirmation) : ")
        if password_confirm != password:
            print("ERREUR /!\\ Les mots de passes sont différents !")
            self.debut()
        else:
            #on peut envoyer les infos
            self.send(json.dumps({"type": "inscription", "pseudo": pseudo,
                                  "password": password, "email": email}))
            print("En attente du serveur ... ")
            self.attente_serv()
            print("recu !")
            if self.etat == "connecté":
                print("Connecté")
                self.interface()
            else:
                self.debut()

    def send(self, message, important=False):
        """Permet d'envoyer un message.

        Args:
            message(str): Le message à envoyer au serveur

        Author: Nathan

        """
        message = message.encode(encoding="utf-8")
        size = sys.getsizeof(message)
        if size > self.max_size:
            if important:
                raise UserWarning(f"ERREUR : Le message est trop long ! {+str(size)} bytes/{str(self.max_size)} bytes")
            print(f"""ERREUR : Le message est trop long ! {+str(size)} bytes/
                    {str(self.max_size)} bytes""")
        else:
            self.client.send(message)

    def start(self):
        """Permet de démarrer la connexion au serveur.

        Connexion avec le protocole TCP/IP, utilisation d'un thread pour la
        fonction `handle()` afin de ne pas encombrer le thread principal.

        Author: Nathan

        """
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
        _thread.start_new_thread(self.handle, ())

    def handle(self):
        """Permet de gérer les messages reçus.

        Author: Nathan

        """
        self.on_connect()
        while True:
            #try:
                msg = self.client.recv(self.max_size)
                msg = msg.decode(encoding="utf-8")
                print("recu : "+json.loads(msg))
                if len(msg) == 0:
                    raise UserWarning("message vide")
                if not self.ws:
                    self.on_message(msg)
                else:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete( self.webserver.on_message(msg) )
                """except Exception as e:
                print(e)
                self.on_close()
                return"""

    def on_connect(self):
        """Réaction si la connexion est acceptée."""
        # TODO
        pass

    def on_message(self, mess):
        """Réaction si un message est reçu.

        Args:
            mess(str): Le message reçu

        Author: Nathan

        """
        if is_json(mess):
            self.attente = False
            data=json.loads(mess)
            while type(data)==str:
                if is_json(data):
                    data=json.loads(data)
                else:
                    return
            if data["type"] == "connection successed":
                print("Connection acceptée")
                self.etat = "connecté"
                
            elif data["type"] == "inscription successed":
                print("Inscription acceptée")
                self.etat = "connecté"
                
            elif data["type"] == "connection failed":
                print("Connection refusée\nerreur : "+data["value"])
                
            elif data["type"] == "inscription failed":
                print("Inscription refusée\nerreur : "+data["value"])

            elif data["type"] == "creation perso":
                data_perso = self.creation_perso()
                self.send(json.dumps(data_perso))

    def on_close(self):
        """Réaction en cas de fermeture/problème.

        Author: Nathan

        """
        print("connection fermée")
        exit()

    def creation_perso(self):
        data_perso = { "nom":None, "race":None, "class":None , "sexe":None }
        #TODO : Faire que l'utilisateur peut créer son perso
        #Attenion ! Il faut faire un systeme sécurisé 
        #(il faut bien vérifier les réponses de l'utilisateur, et lui redemander si ca ne va pas)

        lst_classes = ["guerrier","archer","mage blanc","mage noir","mage guerrier","assassin","voleur","paladin","barbare","tank"] #il faut que ca s'adapte à la taille de la liste car elle va changer
        lst_race = ["humain","homme-dragon","elfe","elfe noir","orc","nain","demi-elfe","fée"] #pareil, ca va changer

        return data_perso

    def interface(self):
        """Permet à l'utilisateur d'écrire et d'envoyer des messages.

        Author: Nathan

        """
        while self.encours:
            txt = input("")
            t = txt.split(" ")
            if len(t) >= 1:
                c = t[0]
                a = " ".join(t[1:])
                dict_ = {"type": "commande", "commande": c, "arguments": a}
                self.send(json.dumps(dict_))

    def main(self):
        """Fonction principale du client.

        Author: Nathan

        """
        self.start()

        if not self.ws:
            self.debut()
        else:
            self.webserver.main()

# Le programme est lancé ici
if __name__ == "__main__":
    client = Client()
    client.main()
