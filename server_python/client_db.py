# CECI EST LE CLIENT QUI SE CONNECTE A MARIADB

# Imports :
import mariadb
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
        # on va regarder si l'output contient des elements
        output = [elt for elt in self.cursor]
        # s'il n'y en a pas, on va dire que c'est la premiere fois que l'on lance le serveur
        return len(output)==0

    def init_database(self):
        """
        fonction qui va créer toutes les tables que l'on aura besoin
        lors du premier lancement du serveur

        pour l'instant, il n'y a que accounts, mais faudra rajouter les autres

        Auteur : Nathan
        """
        self.cursor.execute("CREATE TABLE accounts (id INT PRIMARY KEY AUTO_INCREMENT, pseudo TEXT, email TEXT, password TEXT, perso_id INT);")
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
