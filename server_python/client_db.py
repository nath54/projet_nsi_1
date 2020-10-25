# CECI EST LE CLIENT QUI SE CONNECTE A MARIADB

# Imports :

#methode 1 : mariadb
try:
    import mariadb
except:
    #methode 2 : mysql
    try:
        import mysql.connector as mariadb
    except:
        #rien n'est installé
        print("Il faut que vous installiez la librairie mariadb ou la librairie mysql pour python !")

import sys

class Client_mariadb:
    """Classe du client MariaDB

    Attributes:
        user(str): Utilisateur de la base
        password(str): Mot de passe du profil
        host(str): Adresse de l'hôte de la base
        port(int): Port utilisé par MariaDB
        database(str): Nom de la base de données
        connection(???): Référence à la connexion entre le programme et MariaDB
        tablename(str): Nom de la table utilisée
        cursor(cursor): Curseur de la base de donnée `database`

    """
    def __init__(self):
        """Initialise les caractéristiques de la base de données

        Author: ???

        """
        # faudra se mettre d'accord sur ca
        # la c'est juste pour faire des tests
        self.user = "pyuser"
        self.password = "pypassword"
        self.host = "localhost"
        self.port = 3307
        self.database = "projet_nsi_1"
        try:
            self.connection = mariadb.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database)
            print("connecté a la database")
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        self.tablename = "tablename"
        self.cursor = self.connection.cursor()
        # TODO
        pass

    def close(self):
        """Ferme la connexion"""
        self.connection.close()

    def test_first_time(self):
        """
        fonction qui va tester si la table accounts est créée
        pour savoir si c'est le premier lancement du serveur

        Auteur : Nathan
        """
        self.cursor.execute("SHOW TABLES LIKE 'accounts'; ")
        # On regarde si l'output contient des éléments
        output = [elt for elt in self.cursor]
        # S'il n'y en a pas, c'est la premiere fois que l'on lance le serveur
        return len(output) == 0

    def init_database(self):
        """Permet de créer toutes les tables au premier lancement

        TODO: Ajouter les autres autres tables

        Author : Nathan

        """
        query = ("CREATE TABLE accounts (id INT PRIMARY KEY AUTO_INCREMENT," +
                 "pseudo TEXT, email TEXT, password TEXT, perso_id INT);")
        self.cursor.execute(query)
        self.connection.commit()

    def inscription(self, pseudo, email, password):
        """Permet de créer un compte

        Args:
            pseudo(str): Pseudo du compte à créer TODO: Pas de double
            email(str): E-mail associé au nouveau compte TODO: Pas de double
            password(str): Mot de passe du compte

        Author: ???

        """
        pass
