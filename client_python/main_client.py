"""PROGRAMME PRINCIPAL DU CLIENT DU JEU."""

# Importations :
import socket
import _thread
import json
import sys
import asyncio


# la liste des characteres autorisés pour les pseudos, les emails,
# ou bien les mots de passes
chars = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k",
         "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
         "w", "x", "y", "z",
         "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
         "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
         "W", "X", "Y", "Z",
         "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
         "-", "_", "@", "."]


def test_email(txt):
    """Vérifie qu'un mail a le bon format.

    Auteur: Nathan
    """
    t = txt.split("@")
    if len(t) != 2:
        print("ERREUR /!\\ : "
              "L'email doit être composé de 2 parties séparées par un @ !")
        return True
    if len(t[1].split(".")) != 2:
        print("ERREUR /!\\ La partie de l'email située après @ doit être "
              "constituée de deux parties séparées par un point !")
        return True
    for c in txt:
        if not (c in chars):
            print(f"ERREUR /!\\ Email, Caractère non autorisé : '{c}' !")
            return True
    return False


def test_pseudo(txt):
    """Vérifie qu'un pseudo a le bon format.

    Auteur : Nathan
    """
    if len(txt) < 4:
        print("ERREUR /!\\ Pseudo : Minimum 4 caractères !")
        return True
    if len(txt) > 12:
        print("ERREUR /!\\ Pseudo : Maximum 12 caractères !")
        return True
    for c in txt:
        if not (c in chars):
            print(f"ERREUR /!\\ Pseudo, Caractère non autorisé : '{c}' !")
            return True
    return False


def test_password(txt):
    """Vérifie qu'un mot de passe a le bon format.

    Auteur: Nathan
    """
    if len(txt) < 8:
        print("ERREUR /!\\ Mot de passe : Minimum 8 caractères !")
        return True
    if len(txt) > 32:
        print("ERREUR /!\\ Mot de passe : Maximum 32 caractères !")
        return True
    for c in txt:
        if not (c in chars):
            print(f"ERREUR /!\\ Mot de passe, Caractère non autorisé : '{c}'")
            return True
    return False


def is_json(myjson):
    """Teste si un str est en format json.

    Auteur: Nathan
    """
    try:
        json.loads(myjson)
    except ValueError:
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

        Auteur: Nathan

        """
        self.host = input("Host ? (si vide sera localshost)\n : ")
        if self.host == "":
            self.host = "localhost"
        self.port = 9876
        self.max_size = 2048
        self.client = None

        self.encours = True
        self.attente = False
        self.etat = "None"

        i = input("Voulez vous que ce soit un client websocket ?\n(par défaut = non)\n : ")
        if i.lower() in ["o", "oui", "y", "yes"]:
            self.ws = True
            from webserver import WebServer
            self.webserver = WebServer(self)
        else:
            self.ws = False

        self.genres = ["homme", "femme", "agenre", "androgyne", "bigender",
                       "non-binaire", "autre"]
        self.debug = False

    def debut(self):
        """Demande si l'on veut s'inscrire ou se connecter.

        Auteur: Nathan

        """
        print("Voulez vous :\n  1) Vous inscrire ?\n  2) Vous connecter ?")
        r = input(": ")
        while not (r in ["1", "2"]):
            r = input(": ")
        if r == "1":
            self.inscription()
        else:
            self.connexion()

    def attente_serv(self):
        """Attends la réception d'un message.

        Quand le message a été reçu, on peut continuer le thread actuel

        Auteur: Nathan

        """
        self.attente = True
        print("\nEn attente du serveur ...\n")
        while self.attente:
            pass

    def connexion(self):
        """Demande les informations pour se connecter.

        Auteur: Nathan
        """
        print("\nConnection :\n")
        # pseudo
        pseudo = input("pseudo : ")
        while test_pseudo(pseudo):
            pseudo = input("pseudo : ")
        # password
        password = input("mot de passe : ")
        while test_password(password):
            password = input("mot de passe : ")
        self.send(json.dumps({"type": "connection", "pseudo": pseudo,
                              "password": password}))
        self.attente_serv()
        # print("recu !")
        if self.etat == "connecté":
            # print("Connecté")
            self.interface()
        else:
            self.debut()

    def inscription(self):
        """Demande les informations pour s'inscrire.

        Auteur: Nathan
        """
        print("\nInscription :\n")
        # email
        email = input("email : ")
        while test_email(email):
            email = input("email : ")
        # pseudo
        pseudo = input("pseudo : ")
        while test_pseudo(pseudo):
            pseudo = input("pseudo : ")
        # password
        password = input("mot de passe : ")
        while test_password(password):
            password = input("mot de passe : ")
        password_confirm = input("mot de passe (confirmation) : ")
        if password_confirm != password:
            print("ERREUR /!\\ Les mots de passes sont différents !")
            self.debut()
        else:
            # on peut envoyer les infos
            self.send(json.dumps({"type": "inscription", "pseudo": pseudo,
                                  "password": password, "email": email}))
            print("En attente du serveur ... ")
            self.attente_serv()
            # print("recu !")
            if self.etat == "connecté":
                self.attente_serv()
                if self.etat == "creation_perso":
                    data_perso = self.creation_perso()
                    self.send(json.dumps(data_perso))
                    self.interface()
                else:
                    print("erreur inconnue ...")
                    self.debut()
            else:
                self.debut()

    def send(self, message, important=False):
        """Permet d'envoyer un message.

        Args:
            message(str): Le message à envoyer au serveur

        Auteur: Nathan

        """
        message = message.encode(encoding="utf-8")
        size = sys.getsizeof(message)
        if size > self.max_size:
            if important:
                raise UserWarning(f"ERREUR : Le message est trop long ! "
                                  "{str(size)} / {str(self.max_size)} bytes")
            print(f"""ERREUR : Le message est trop long ! {str(size)} bytes/
                    {str(self.max_size)} bytes""")
        else:
            self.client.send(message)

    def start(self):
        """Permet de démarrer la connexion au serveur.

        Connexion avec le protocole TCP/IP, utilisation d'un thread pour la
        fonction `handle()` afin de ne pas encombrer le thread principal.

        Auteur: Nathan

        """
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
        _thread.start_new_thread(self.handle, ())

    def handle(self):
        """Permet de gérer les messages reçus.

        Auteur: Nathan

        """
        self.on_connect()
        while True:
            try:
                msg = self.client.recv(self.max_size)
                msg = msg.decode(encoding="utf-8")
                if self.debug:
                    print("recu : ", msg)
                # print("recu : ", json.loads(msg))
                if len(msg) == 0:
                    raise UserWarning("message vide")
                if not self.ws:
                    self.on_message(msg)
                else:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(self.webserver.on_message(msg))
            except Exception as e:
                print(e)
                self.on_close()
                return

    def on_connect(self):
        """Réaction si la connexion est acceptée."""
        # TODO
        pass

    def on_message(self, mess):
        """Réaction si un message est reçu.

        Args:
            mess(str): Le message reçu

        Auteur: Nathan

        """
        if is_json(mess):
            data = json.loads(mess)
            while type(data) == str:
                if is_json(data):
                    data = json.loads(data)
                else:
                    return
            if type(data) != dict:
                return
            # print("on_message : ", data)
            if data["type"] == "connection successed":
                print("Connection acceptée")
                self.etat = "connecté"
                self.attente = False

            elif data["type"] == "inscription successed":
                print("Inscription acceptée")
                self.etat = "connecté"
                self.attente = False

            elif data["type"] == "connection failed":
                print("Connection refusée\nerreur : " + data["value"])
                self.attente = False

            elif data["type"] == "inscription failed":
                print("Inscription refusée\nerreur : " + data["value"])
                self.attente = False

            elif data["type"] == "creation perso":
                # print("creation perso")
                self.etat = "creation_perso"
                self.attente = False

            elif data["type"] == "genres":
                self.genres = json.loads(data["genres"])

            elif data["type"] == "close":
                self.on_close()

            elif data["type"] == "message":
                print("\n" + str(data["value"]) + "\n")

    def on_close(self):
        """Réaction en cas de fermeture/problème.

        Auteur: Nathan

        """
        self.encours = False
        print("connection fermée")
        input("appuyer pour fermer le client du jeu...")
        exit()

    def test_nom(self, nom):
        """Teste si un nom est dans le bon format

        Auteur: Léa

        """
        if len(nom) < 2:
            return "Le nom doit avoir au minimum 2 lettres !"
        elif len(nom) > 20:
            return "Le nom doit avoir au maximum 20 lettres !"

    def creation_perso(self):
        """Demande les informations pour créer un personnage.

        Auteur: Léa
        """
        data_perso = {"type": "perso_cree", "nom": None, "race": None,
                      "classe": None, "genre": None}

        lst_classes = {
            "guerrier": "Un guerrier sait se battre au corps à corps, il est fort et il porte facilement tout type d'armure",
            "archer": "Un archer sait se battre à distance, et est plutôt agile",
            "prêtre": "Un prêtre excelle dans les sorts de soutiens, mais n'est pas très bon en attaque",
            "mage noir": "Un mage noir excelle dans la sorcellerie maudite, il peut invoquer des créatures ou controler des cadavres",
            "mage guerrier": "Un mage guerrier est équilibré dans les combats aux corps à corps et la maitrise des sorts de combats",
            "assassin": "Un assassin est habile et précis, il rate peu et esquive beaucoup, mais n'est pas très fort physiquement",
            "voleur": "Un voleur est habile et esquive beaucoup, il peut voler des pnjs et des ennemis",
            "paladin": "Un paladin est un guerrier qui connait des sorts de soutiens, il peut à la fois se battre et soigner ses alliés",
            "barbare": "Un barbare est un guerrier qui a vécu loin de la société civilisé, il se bat avec son instinct animal, et peut même devenir un berseker",
            "tank": "Un tank est un guerrier spécialisé dans la défense, il défend ses alliés et encaisse les gros dégats à leurs place, mais en contrepartie il ne fait pas beaucoup de dégats en attaque"
        }

        lst_races = {
            "humain": "Les humains sont la race la plus présente sur la planete, ils sont équilibrés",
            "drakonien": "Les drakoniens sont des créatures mi-homme mi-dragon, ils ont une peau solide, et ont des facilités pour lancer des sorts de feu. Ils ont une apparence humaine en tant normal (même s'ils ont un bien meilleur physique que les humains ordinaires), mais ont une forme plus draconienne lors des combats",
            "elfe": "Les elfes sont les habitants de la forêt, ils ressemblent aux humains, mais ont des oreilles pointues, une peau plus verte pâle, et ont une bien meilleure longévité que les humains, ils ont des faiblesses contre le feu, mais sont plutôt habiles",
            "elfe noir": "Les elfes noirs sont des elfes qui sont tombés du côté obscur, ils ont une connaissance des sortileges maudits, n'ont pas de faiblesses contre le feu comme les autres elfes, mais contre des sortileges bénits",
            "demi-elfe": "Les demi-elfes sont des enfants d'homme et d'elfe",
            "orc": "Les orcs ne sont pas très intelligents et habiles, mais ils sont forts et résistants",
            "nain": "Les nains sont forts et résistants, peu habiles, mais ont des grands avantages dans les grottes et les montagnes",
            "fée": "Les fées sont des créatures magiques plutôt faibles physiquement, mais qui ont de gros bonus dans la magie"
        }

        # pareil, ca va changer
        lst_genres = self.genres
        # c'est pour faire plaisir à tout le monde

        print("Création du personnage : \n")
        # nom
        print("Quel est le nom de votre personnage ?\n")
        nom = input("nom : ")
        erreur = self.test_nom(nom)
        while erreur:
            print("ERREUR /!\\ : " + erreur)
            nom = input("nom : ")
        data_perso["nom"] = nom

        # On affiche les races
        print("\n\nRaces Disponibles : \n")
        for n, d in lst_races.items():
            print(f"  - {n} : {d}\n")
        # race
        print("\nQuel est la race de votre personnage ?\n")
        race = input("race : ")
        while race not in lst_races.keys():
            print("ERREUR /!\\ : La race n'est pas dans la liste !")
            race = input("race : ")
        data_perso["race"] = race

        # On affiche les races
        print("\n\nClasses Disponibles : ")
        for n, d in lst_classes.items():
            print(f"  - {n} : {d}\n")
        # classe
        print("\nQuel est la classe de votre personnage ?\n")
        classe = input("classe : ")
        while classe not in lst_classes.keys():
            print("ERREUR /!\\ : La classe n'est pas dans la liste !")
            classe = input("classe : ")
        data_perso["classe"] = classe

        # On affiche les genres :
        print("\nGenres : ")
        for g in lst_genres + ["autre"]:
            print(f"  - {g}")
        # genre
        print("Quel est le genre de votre personnage ?")
        genre = input("genre : ")
        data_perso["genre"] = genre
        return data_perso

    def interface(self):
        """Permet à l'utilisateur d'écrire et d'envoyer des messages.

        Auteur: Nathan

        """
        while self.encours:
            txt = input("")
            # si le jeu a été quitté pendant l'input
            if not self.encours:
                return
            t = txt.split(" ")
            if len(t) >= 1:
                if txt.startswith("/cheat "):
                    a = " ".join(t[1:])
                    dict_ = {"type": "cheat_code", "commande": a}
                    self.send(json.dumps(dict_))
                else:
                    c = t[0]
                    a = " ".join(t[1:])
                    dict_ = {"type": "commande", "commande": c, "arguments": a}
                    self.send(json.dumps(dict_))

    def main(self):
        """Fonction principale du client.

        Auteur: Nathan

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
