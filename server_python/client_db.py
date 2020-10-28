# CECI EST LE CLIENT QUI SE CONNECTE À MARIADB

# Imports :

# Méthode 1 : mariadb
try:
    import mariadb
except:
    # Méthode 2 : mysql
    try:
        import mysql.connector as mariadb
    except:
        # Rien n'est installé
        print("Merci d'installer la librairie mariadb ou mysql pour Python !")

import sys


class Client_mariadb:
    """Classe du client MariaDB.

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
        """Initialise les caractéristiques de la base de données.

        Author: ???

        """
        # Faudra se mettre d'accord sur ça
        # Là c'est juste pour faire des tests
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
        """Ferme la connexion."""
        self.connection.close()

    def test_first_time(self):
        """Teste si la table accounts existe.

        Returns:
            bool: False = Ce n'est pas le premier lancement du serveur
                  True = C'est la première fois qu'on lance le serveur

        Author: Nathan

        """
        self.cursor.execute("SHOW TABLES LIKE 'accounts';")
        # On regarde si l'output contient des éléments
        output = [elt for elt in self.cursor]
        # S'il n'y en a pas, c'est la premiere fois que l'on lance le serveur
        return len(output) == 0

    def init_database(self):
        """Permet de créer toutes les tables au premier lancement.

        TODO: Ajouter les autres tables

        Author : Nathan, Hugo

        """
        query = ("CREATE TABLE IF NOT EXISTS accounts "
                 "(id INT PRIMARY KEY AUTO_INCREMENT,"
                 "pseudo TEXT, email TEXT, password TEXT, perso_id INT);")
        self.cursor.execute(query)
        self.connection.commit()

        query = ("CREATE TABLE IF NOT EXISTS persos "
                 "(id INT PRIMARY KEY AUTO_INCREMENT, nom TEXT, classe TEXT,"
                 "race TEXT, niveau INT, force INT, intelligence INT, "
                 "charme INT, discretion INT, experience_totale INT, "
                 "experience INT, vie_totale INT, vie INT, energie_totale INT,"
                 "energie INT, equipement TEXT, quetes TEXT, lieu INT);")
        self.cursor.execute(query)
        self.connection.commit()

        query = ("CREATE TABLE IF NOT EXISTS objets "
                 "(id INT PRIMARY KEY AUTO_INCREMENT, nom TEXT, "
                 "description TEXT, type_ TEXT, effet_utilise TEXT);")
        self.cursor.execute(query)
        self.connection.commit()

        query = ("CREATE TABLE IF NOT EXISTS pnj "
                 "(id INT PRIMARY KEY AUTO_INCREMENT, nom TEXT, "
                 "description TEXT, race TEXT, dialogue TEXT);")
        self.cursor.execute(query)
        self.connection.commit()

        query = ("CREATE TABLE IF NOT EXISTS ennemi "
                 "(id INT PRIMARY KEY AUTO_INCREMENT, nom TEXT, "
                 "description TEXT, vie_max INT);")
        self.cursor.execute(query)
        self.connection.commit()

        query = ("CREATE TABLE IF NOT EXISTS lieux "
                 "(id INT PRIMARY KEY AUTO_INCREMENT, nom TEXT, "
                 "description TEXT, ennemis TEXT, pnjs TEXT, objets TEXT, "
                 "lieux TEXT);")
        # ennemis, pnjs, objets et lieux contiennent les ID des éléments, avec
        # "/" comme séparateur entre chaque ID
        self.cursor.execute(query)
        self.connection.commit()

    def inscription(self, pseudo, email, password):
        """Permet de créer un compte.

        Args:
            pseudo(str): Pseudo du compte à créer
            email(str): E-mail associé au nouveau compte
            password(str): Mot de passe du compte

        Returns:
            bool: False = L'inscription n'a pas pu être complétée
                  True = Inscription réussie

        Author: Hugo

        """
        c = self.cursor.execute("SELECT pseudo, email, password FROM accounts")
        for pseudo_, email_, _ in c:
            if pseudo == pseudo_ or email == email_:
                # TODO: Faire que l'inscription gère le return False
                return False
        query = ("INSERT INTO accounts (pseudo, email, password) VALUES " +
                 "(%s,%s,%s)", pseudo, email, password)
        self.cursor.execute(query)
        self.connection.commit()
        return True
