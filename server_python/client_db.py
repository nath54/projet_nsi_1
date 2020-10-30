# CECI EST LE CLIENT QUI SE CONNECTE À MARIADB

# Imports :

# Méthode 1 : mariadb
try:
    import mariadb
except Exception as e:
    # Méthode 2 : mysql
    try:
        import mysql.connector as mariadb
    except Exception as e:
        # Rien n'est installé
        raise UserWarning("Il faut installer la librairie mariadb ou mysql !")


import sys
import os
import json
import io


def jload(path_to_file):
    f = io.open(path_to_file, "r", encoding="utf-8")
    txt = f.read()
    f.close()
    return json.loads(txt)


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

    def __init__(self, game):
        """Initialise les caractéristiques de la base de données.

        Author: Nathan

        """
        # Faudra se mettre d'accord sur ça
        # Là c'est juste pour faire des tests
        self.user = "pyuser"
        self.password = "pypassword"
        self.host = "localhost"
        self.port = 3307
        self.database = "projet_nsi_1"
        self.game = game
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
        """Teste si la table comptes existe.

        Returns:
            bool: False = Ce n'est pas le premier lancement du serveur
                  True = C'est la première fois qu'on lance le serveur

        Author: Nathan

        """
        self.cursor.execute("SHOW TABLES LIKE 'comptes';")
        # On regarde si l'output contient des éléments
        output = [elt for elt in self.cursor]
        # S'il n'y en a pas, c'est la premiere fois que l'on lance le serveur
        return len(output) == 0

    def init_database(self):
        """Permet de créer toutes les tables au premier lancement.

        TODO: Ajouter les autres tables

        Author : Nathan, Hugo

        """
        query = ("""CREATE TABLE IF NOT EXISTS comptes
                    (id INT PRIMARY KEY AUTO_INCREMENT, pseudo TEXT,
                    email TEXT, password TEXT, perso_id INT);""")
        self.cursor.execute(query)
        self.connection.commit()

        query = ("""CREATE TABLE IF NOT EXISTS persos
                    (id INT PRIMARY KEY AUTO_INCREMENT, nom TEXT, classe TEXT,
                    race TEXT, niveau INT, force_ INT, intelligence INT,
                    charme INT, discretion INT, experience_totale INT,
                    experience INT, vie_totale INT, vie INT,
                    energie_totale INT, energie INT, equipement TEXT,
                    quetes TEXT, lieu INT);""")
        print(query)
        self.cursor.execute(query)
        self.connection.commit()

        query = ("""CREATE TABLE IF NOT EXISTS objets
                    (id INT PRIMARY KEY AUTO_INCREMENT, nom TEXT,
                    description_ TEXT, type_ TEXT, effet_utilise TEXT);""")
        self.cursor.execute(query)
        self.connection.commit()

        query = ("""CREATE TABLE IF NOT EXISTS pnjs
                    (id INT PRIMARY KEY AUTO_INCREMENT, nom TEXT,
                    description_ TEXT, race TEXT, dialogue TEXT);""")
        self.cursor.execute(query)
        self.connection.commit()

        query = ("""CREATE TABLE IF NOT EXISTS ennemis
                    (id INT PRIMARY KEY AUTO_INCREMENT, type_ TEXT, nom TEXT,
                    race TEXT, description_ TEXT
                    vie_min INT, vie_max INT, attaque_min INT,
                    attaque_max INT, attaque_effets: TEXT);""")
        self.cursor.execute(query)
        self.connection.commit()

        query = ("""CREATE TABLE IF NOT EXISTS lieux
                    (id INT PRIMARY KEY AUTO_INCREMENT, nom TEXT,
                    description_ TEXT, ennemis TEXT, pnjs TEXT, objets TEXT,
                    lieux TEXT);""")

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
        self.cursor.execute("""INSERT INTO comptes (pseudo, email, password)
                 VALUES
                 (%s,%s,%s)""", (pseudo, email, password))
        self.connection.commit()
        # on récupère ensuite l'id
        self.cursor.execute("SELECT id FROM comptes WHERE pseudo=%s",
                            (pseudo,))
        lc = [e for e in self.cursor]
        if len(lc) == 1:
            id_ = lc[0][0]
        else:
            raise UserWarning("Probleme with comptes, il n'y a pas q'un elt")
        return True, id_

    def test_compte_inscrit(self, pseudo, email):
        """Fonction qui teste si on peut inscrire un compte
        renvoie False s'il n'y a pas d'erreurs
        renvoie un string contenant un message d'erreur s'il y a une erreur

        Author : Hugo, Nathan
        """
        self.cursor.execute("SELECT pseudo, email FROM comptes")
        c = self.cursor
        for pseudo_, email_ in c:
            if pseudo == pseudo_:
                return "Le pseudo est déjà utilisé"
            elif email == email_:
                return "L'email est déjà utilisé"
        return False

    def test_connection(self, pseudo, password):
        """Fonction qui teste la connection d'un compte,
        renvoie False s'il n'y a pas d'erreurs
        renvoie un string contenant un message d'erreur s'il y a une erreur

        Author : Nathan
        """
        self.cursor.execute("SELECT password, id FROM comptes WHERE pseudo=%s",
                            (pseudo,))
        c = self.cursor
        lc = [e for e in c]
        if len(lc) == 0:
            return f"Il n'y a pas de compte avec le pseudo '{pseudo}'", None
        elif len(lc) > 1:
            return ("probleme de comptes, veuillez contacter un administateur"
                    " au plus vite "
                    "(il y a plusieurs comptes avec le même pseudo)", None)
        else:
            password_ = lc[0][0]
            id_ = lc[0][1]
            if password == password_:
                return False, id_
            else:
                return "Le mot de passe est faux !", None

    def transfert_json_to_bdd(self):
        """ 
        A faire : transférer toutes les données des fichiers json vers la bdd

        Author : Nathan
        """

        # Les ennemis :
        pathd = "Data/ennemis/"
        for fich in os.listdir(pathd):
            d = jload(pathd+fich)
            self.cursor.execute("""INSERT INTO ennemis (id, type_, nom, race,
                                description_, vie_min, vie_max, attaque_min,
                                attaque_max, attaque_effets)
                                VALUES
                                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                                (
                                    d["id"], d["type"], d["nom"], d["race"],
                                    d["goblin"], d["description"],
                                    d["vie"][0], d["vie"][1],
                                    d["attaque"][0], d["attaque"][1],
                                    json.dumps(d["attaque_effets"])
                                ))

        # A faire les autres
        # (il y aura sans doutes la table à changer
        #  comme j'ai du changer pour ennemi)
        # TODO
        pass

    def set_perso(self, perso):
        """
        Fonction qui enregistre un perso dans la bdd

        Author :
        """
        # TODO
        pass

    def get_perso(self, pseudo):
        """
        Fonction qui récupère les données du personnage

        Author :
        """
        data_perso = {}
        # TODO
        return data_perso

    def get_obj_from_DB(self, id):
        """Renvoie l'objet demandé

        Args:
            id(int): ID de l'objet à chercher

        Returns:
            Objet/None: Objet d'id `id` ou None si pas trouvé

        Author: Hugo, Nathan

        """
        query = ("SELECT * FROM objets WHERE id=%s", (str(id),))
        self.cursor.execute(query)
        for id, nom, desc, type_, effet in self.cursor:
            obj = self.game.Objet()
            obj.nom = nom
            obj.description = desc
            obj.type = type_
            obj.effet = effet
            return obj
        return None
