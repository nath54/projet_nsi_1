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
        self.user = "user"
        self.password = "password"
        self.host = "localhost"
        self.port = 3307
        self.database = "database"
        try:
            self.connection = mariadb.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database)
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        self.tablename = "tablename"
        self.cursor = self.connection.cursor()
        # TODO
        pass

    def close(self):
        self.connection.close()
    
    def inscription(self,pseudo,email,password):
        pass