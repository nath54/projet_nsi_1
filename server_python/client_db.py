"""CECI EST LE CLIENT QUI SE CONNECTE À MARIADB."""

# Imports :

# Méthode 1 : mariadb
try:
    import mariadb  # ignore unresolved-import error
except Exception as e:
    # Méthode 2 : mysql
    try:
        import mysql.connector as mariadb  # ignore unresolved-import error
    except Exception as e:
        # Rien n'est installé
        raise UserWarning("Il faut installer la librairie mariadb ou mysql !")


import sys
import os
import json
import io
from libs import *


class Client_mariadb:
    """
    Classe du client MariaDB.

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

        Auteur: Nathan

        """
        # Faudra se mettre d'accord sur ça
        # Là c'est juste pour faire des tests
        self.user = "pyuser"
        self.password = "pypassword"
        self.host = "localhost"
        self.port = 3307
        self.database = "projet_nsi_1"
        self.game = game
        self.game.client_db = self
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

    def test_version(self, version):
        """Fonction qui vérifie si la version de la base de donnée est inférieure à celle du serveur.

        Auteur: Nathan
        """
        self.cursor.execute("SHOW TABLES LIKE 'version';")
        results = [elt for elt in self.cursor]
        if len(results) == 0:
            return True
        else:
            self.cursor.execute("SELECT version FROM version;")
            results = [elt for elt in self.cursor]
            if len(results) == 0:
                return True
            else:
                version_bdd = results[0][0]
                if version_bdd < version:
                    return True
                else:
                    return False

    def test_first_time(self):
        """Teste si la table comptes existe.

        Returns:
            bool: False = Ce n'est pas le premier lancement du serveur
                  True = C'est la première fois qu'on lance le serveur

        Auteur: Nathan

        """
        self.cursor.execute("SHOW TABLES LIKE 'comptes';")
        # On regarde si l'output contient des éléments
        output = [elt for elt in self.cursor]
        # S'il n'y en a pas, c'est la premiere fois que l'on lance le serveur
        return len(output) == 0

    def get_schema(self, table_name):
        """Fonction qui récupère la structure de la table demandée sous forme de dictionnaire : .
          {nom de la colonne : type de la colonne (int, text, ...)}

        renvoie un dictionnaire vide si la table n'existe pas
        """
        self.cursor.execute("select * from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME=%s;", (table_name,))
        results = [elt for elt in self.cursor]
        schema = {}
        for elt in results:
            schema[elt[3]] = elt[7]
        return schema

    def create_table_comptes(self):
        """Fonction qui crée la table comptes dans la bdd."""
        query = ("""CREATE TABLE IF NOT EXISTS comptes
                    (id INT PRIMARY KEY AUTO_INCREMENT, pseudo TEXT,
                    email TEXT, password TEXT, perso_id INT);""")
        self.cursor.execute(query)
        self.connection.commit()

    def create_table_persos(self):
        """Fonction qui crée la table perso dans la bdd."""

        query = ("""CREATE TABLE IF NOT EXISTS persos
                    (id INT PRIMARY KEY AUTO_INCREMENT,
                    nom TEXT, genre TEXT, race TEXT, classe TEXT, experience TEXT,
                    inventaire TEXT, lieu INT, quetes TEXT, equipement TEXT,
                    vie INT, vie_totale INT, energie INT, energie_totale INT,
                    charme INT, discretion INT, force_ INT, agilite INT, magie INT,
                    effets_attaque TEXT, bonus_esquive INT, sorts TEXT,
                    resistances TEXT, faiblesses TEXT);""")
        self.cursor.execute(query)
        self.connection.commit()

    def create_table_objets(self):
        """Fonction qui crée la table perso dans la bdd."""
        query = ("""CREATE TABLE IF NOT EXISTS objets
                    (id INT PRIMARY KEY, nom TEXT,
                    description_ TEXT, type_ TEXT, effets TEXT,
                    contenu TEXT, verrouille BOOLEAN, ouvert BOOLEAN);""")
        self.cursor.execute(query)
        self.connection.commit()

    def create_table_pnjs(self):
        """Fonction qui crée la table perso dans la bdd."""
        query = ("""CREATE TABLE IF NOT EXISTS pnjs
                    (id INT PRIMARY KEY, nom TEXT,
                    description_ TEXT, race TEXT, dialogue TEXT);""")
        self.cursor.execute(query)
        self.connection.commit()

    def create_table_ennemis(self):
        """Fonction qui crée la table perso dans la bdd."""
        query = ("""CREATE TABLE IF NOT EXISTS ennemis
                    (id INT PRIMARY KEY, type_ TEXT, nom TEXT,
                    race TEXT, description_ TEXT,
                    vie_min INT, vie_max INT, attaque_min INT,
                    attaque_max INT, attaque_effets TEXT);""")
        self.cursor.execute(query)
        self.connection.commit()

    def create_table_lieux(self):
        """Fonction qui crée la table perso dans la bdd."""
        query = ("""CREATE TABLE IF NOT EXISTS lieux
                    (id INT PRIMARY KEY, nom TEXT,
                    description_ TEXT, ennemis TEXT, pnjs TEXT, objets TEXT,
                    lieux TEXT);""")
        # ennemis, pnjs, objets et lieux contiennent des listes parsées par JSON
        self.cursor.execute(query)
        self.connection.commit()

    def create_table_genre(self):
        """Fonction qui crée la table genre dans la bdd."""
        query = ("""CREATE TABLE IF NOT EXISTS genres
                    (genre TEXT);""")
        self.cursor.execute(query)
        self.connection.commit()
        for genre in ["homme", "femme", "agenre", "androgyne", "bigender", "non-binaire"]:
            self.cursor.execute("INSERT INTO genres (genre) VALUES (%s)", (genre, ))
            self.connection.commit()

    def update(self, force=False):
        """Fonction qui supprime et qui recrée les tables qui ne sont pas dans le bon format ou qui n'existent pas.

        Auteur : Nathan
        """
        # comptes
        if force or self.get_schema("comptes") != {'id': 'int', 'pseudo': 'text',
                                                   'email': 'text', 'password': 'text',
                                                   'perso_id': 'int'}:
            self.cursor.execute("DROP TABLE comptes")
            self.connection.commit()
            self.create_table_comptes()
            print("La table comptes a été mise à jour !")
        # persos
        if force or self.get_schema("persos") != {"id": "int", "nom": "text", "genre": "text",
                                                  "race": "text", "classe": "text", "experience": "text",
                                                  "inventaire": "text", "lieu": "int", "quetes": "text",
                                                  "equipement": "text", "vie": "int", "vie_totale": "int",
                                                  "energie": "int", "energie_totale": "int", "charme": "int",
                                                  "discretion": "int", "force_": "int", "agilite": "int",
                                                  "magie": "int", "effets_attaque": "text", "bonus_esquive": "int",
                                                  "sorts": "text", "resistances": "text", "faiblesses": "text"}:
            self.cursor.execute("DROP TABLE IF EXISTS persos")
            self.connection.commit()
            self.create_table_persos()
            print("La table persos a été mise à jour !")
        # ennemis
        if force or self.get_schema("ennemis") != {"id": "int", "type_": "text", "nom": "text",
                                                   "race": "text", "description_": "text", "vie_min": "int",
                                                   "vie_max": "int", "attaque_min": "int", "attaque_max": "int",
                                                   "attaque_effets": "text"}:
            self.cursor.execute("DROP TABLE IF EXISTS ennemis")
            self.connection.commit()
            self.create_table_ennemis()
            print("La table ennemis a été mise à jour !")
        # objets
        if force or self.get_schema("objets") != {'id': 'int',
                                                  'nom': 'text',
                                                  'description_': 'text',
                                                  'type_': 'text',
                                                  'effets': 'text',
                                                  'contenu': 'text',
                                                  'verrouille': 'tinyint',
                                                  'ouvert': 'tinyint'}:
            self.cursor.execute("DROP TABLE IF EXISTS objets")
            self.connection.commit()
            self.create_table_objets()
            print("La table objets a été mise à jour !")
        # lieux
        if force or self.get_schema("lieux") != {"id": "int", "nom": "text",
                                                 "description_": "text",
                                                 "ennemis": "text",
                                                 "pnjs": "text",
                                                 "objets": "text",
                                                 "lieux": "text"}:
            self.cursor.execute("DROP TABLE IF EXISTS lieux")
            self.connection.commit()
            self.create_table_lieux()
            print("La table lieux a été mise à jour !")
        # pnjs
        if force or self.get_schema("pnjs") != {"id": "int", "nom": "text",
                                                "description_": "text",
                                                "race": "text",
                                                "dialogue": "text"}:
            self.cursor.execute("DROP TABLE IF EXISTS pnjs")
            self.connection.commit()
            self.create_table_pnjs()
            print("La table pnjs a été mise à jour !")
        if force or self.get_schema("genres") != {"genre": "text"}:
            self.cursor.execute("DROP TABLE IF EXISTS genres")
            self.connection.commit()
            self.create_table_genre()

    def init_database(self):
        """Permet de créer toutes les tables au premier lancement.

        TODO: Ajouter les autres tables

        Auteur : Nathan, Hugo

        """
        self.create_table_comptes()
        self.create_table_persos()
        self.create_table_objets()
        self.create_table_pnjs()
        self.create_table_ennemis()
        self.create_table_lieux()
        self.create_table_genre()

    def inscription(self, pseudo, email, password):
        """Permet de créer un compte.

        Args:
            pseudo(str): Pseudo du compte à créer
            email(str): E-mail associé au nouveau compte
            password(str): Mot de passe du compte

        Returns:
            bool: False = L'inscription n'a pas pu être complétée
                  True = Inscription réussie

        Auteur: Hugo

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
        """Fonction qui teste si on peut inscrire un compte.

        renvoie False s'il n'y a pas d'erreurs
        renvoie un string contenant un message d'erreur s'il y a une erreur

        Auteur : Hugo, Nathan
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
        """Fonction qui teste la connection d'un compte.

        renvoie False s'il n'y a pas d'erreurs
        renvoie un string contenant un message d'erreur s'il y a une erreur

        Auteur : Nathan
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
        """Transfére toutes les données des fichiers json vers la BDD.

        Etat : TODO Commencé, à continuer
        Auteur : Nathan, Hugo
        """
        # region Ennemis :
        self.cursor.execute("TRUNCATE TABLE `ennemis`")
        self.connection.commit()
        pathd = "Data/ennemis/"
        for fich in os.listdir(pathd):
            if not fich.endswith(".json"):
                continue
            d = jload(pathd + fich)
            self.cursor.execute("""INSERT INTO ennemis (id, type_, nom, race,
                                description_, vie_min, vie_max, attaque_min,
                                attaque_max, attaque_effets)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                                (
                                    d["id"], d["type"], d["nom"],
                                    d["race"], d["description"],
                                    d["vie"][0], d["vie"][1],
                                    d["attaque"][0], d["attaque"][1],
                                    json.dumps(d["attaque_effets"])
                                ))
            self.connection.commit()
        # endregion
        # region Objets :
        self.cursor.execute("TRUNCATE TABLE `objets`")
        self.connection.commit()
        pathd = "Data/objets/"
        for fich in os.listdir(pathd):
            if not fich.endswith(".json"):
                continue
            d = jload(pathd + fich)
            d["contenu"] = "" if "contenu" not in d.keys() else d["contenu"]
            d["verrouille"] = False if "verrouille" not in d.keys() else d["verrouille"]
            d["ouvert"] = False if "ouvert" not in d.keys() else d["ouvert"]
            self.cursor.execute("""INSERT INTO objets (id, nom, description_, type_, effets, contenu, verrouille, ouvert)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                                (
                                    d["id"], d["nom"], d["description"], d["type"],
                                    json.dumps(d["effets"]), json.dumps(d["contenu"]), d["verrouille"], d["ouvert"]
                                ))
            self.connection.commit()
        # endregion
        # region Lieu :
        self.cursor.execute("TRUNCATE TABLE `lieux`")
        self.connection.commit()
        pathd = "Data/map/"
        for fich in os.listdir(pathd):
            if not fich.endswith(".json"):
                continue
            d = jload(pathd + fich)
            query = """INSERT INTO lieux (id, nom, description_, ennemis, pnjs,
                        objets, lieux) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            self.cursor.execute(query, (d["id"], d["nom"], d["description"], json.dumps(d["ennemis"]),
                                        json.dumps(d["pnjs"]), json.dumps(d["objets"]), json.dumps(d["lieux"])))
            self.connection.commit()
        # endregion
        # region PNJs :
        self.cursor.execute("TRUNCATE TABLE `pnjs`")
        self.connection.commit()
        pathd = "Data/pnjs/"
        for fich in os.listdir(pathd):
            if not fich.endswith(".json"):
                continue
            d = jload(pathd + fich)
            query = """INSERT INTO pnjs (id, nom, description_, race,
                        dialogue) VALUES (%s, %s, %s, %s, %s);"""
            self.cursor.execute(query, (d["id"], d["nom"], d["description"], d["race"], json.dumps(d["dialogues"])))
            self.connection.commit()
        # endregion
        # A faire les autres
        # (il y aura sans doutes la table à changer comme j'ai du changer pour ennemi)
        # TODO
        pass

    def set_perso(self, player):
        """Fonction qui enregistre un perso dans la bdd.

        Auteur : Nathan
        """
        id_ = player.id_
        # on va regarder si le player a déjà un perso
        self.cursor.execute("SELECT perso_id FROM comptes WHERE id=%s;", (id_,))
        results = [elt for elt in self.cursor]
        if results == []:
            raise UserWarning("erreur !")
        perso_id = results[0][0]
        perso = player.perso
        if perso_id is None:
            # si non on va lui en créer un
            self.cursor.execute("""INSERT INTO persos
                                   (nom,
                                    genre,
                                    race,
                                    classe,
                                    experience,
                                    inventaire,
                                    lieu,
                                    quetes,
                                    equipement,
                                    vie,
                                    vie_totale,
                                    energie,
                                    energie_totale,
                                    charme,
                                    discretion,
                                    force_,
                                    agilite,
                                    magie,
                                    effets_attaque,
                                    bonus_esquive,
                                    sorts,
                                    resistances,
                                    faiblesses)
                                   VALUES
                                   (%s, %s, %s, %s, %s,
                                    %s, %s, %s, %s, %s,
                                    %s, %s, %s, %s, %s,
                                    %s, %s, %s, %s, %s,
                                    %s, %s, %s);""",
                                (perso.nom,
                                 perso.genre,
                                 perso.race,
                                 perso.classe,
                                 json.dumps(perso.experience),
                                 json.dumps(perso.inventaire),
                                 perso.lieu,
                                 json.dumps(perso.quetes),
                                 json.dumps(perso.equipement),
                                 perso.vie,
                                 perso.vie_totale,
                                 perso.energie,
                                 perso.energie_totale,
                                 perso.charme,
                                 perso.discretion,
                                 perso.force,
                                 perso.agilite,
                                 perso.magie,
                                 json.dumps(perso.effets_attaque),
                                 perso.bonus_esquive,
                                 json.dumps(perso.sorts),
                                 json.dumps(perso.resistances),
                                 json.dumps(perso.faiblesses)))
            self.connection.commit()
            #
            self.cursor.execute("SELECT id FROM persos WHERE nom = %s AND race = %s AND classe = %s AND genre = %s ORDER BY id DESC;", (perso.nom, perso.race, perso.classe, perso.genre))
            perso_id = [elt[0] for elt in self.cursor][0]
            #
            self.cursor.execute("""UPDATE comptes
                                   SET perso_id = %s
                                   WHERE comptes.id = %s;
                                """, (perso_id, player.id_))
            self.connection.commit()
        else:
            # sinon on va juste modifier les valeurs
            self.cursor.execute("""UPDATE persos
                                   SET nom = %s,
                                       genre = %s,
                                       race = %s,
                                       classe = %s,
                                       experience = %s,
                                       inventaire = %s,
                                       lieu = %s,
                                       quetes = %s,
                                       equipement = %s,
                                       vie = %s,
                                       vie_totale = %s,
                                       energie = %s,
                                       energie_totale = %s,
                                       charme = %s,
                                       discretion = %s,
                                       force_ = %s,
                                       agilite = %s,
                                       magie = %s,
                                       effets_attaque = %s,
                                       bonus_esquive = %s,
                                       sorts = %s,
                                       resistances = %s,
                                       faiblesses = %s
                                    WHERE id=%s;""",
                                (perso.nom,
                                    perso.genre,
                                    perso.race,
                                    perso.classe,
                                    json.dumps(perso.experience),
                                    json.dumps(perso.inventaire),
                                    perso.lieu,
                                    json.dumps(perso.quetes),
                                    json.dumps(perso.equipement),
                                    perso.vie,
                                    perso.vie_totale,
                                    perso.energie,
                                    perso.energie_totale,
                                    perso.charme,
                                    perso.discretion,
                                    perso.force,
                                    perso.agilite,
                                    perso.magie,
                                    json.dumps(perso.effets_attaque),
                                    perso.bonus_esquive,
                                    json.dumps(perso.sorts),
                                    json.dumps(perso.resistances),
                                    json.dumps(perso.faiblesses),
                                    perso_id))
            self.connection.commit()

        self.connection.commit()
        # TODO
        pass

    def get_perso(self, id_):
        """Fonction qui récupère les données du personnage.
        Cette fonction prend en argument l'id du compte

        Auteur : Nathan
        """
        query = """SELECT nom, genre, race, classe, experience,
                    inventaire, lieu, quetes, equipement,
                    vie, vie_totale, energie, energie_totale,
                    charme, discretion, force_, agilite, magie,
                    effets_attaque, bonus_esquive, sorts,
                    resistances, faiblesses FROM persos INNER JOIN comptes ON comptes.perso_id = persos.id WHERE comptes.id=%s"""
        self.cursor.execute(query, (id_,))
        results = [elt for elt in self.cursor]
        if len(results) == 0:
            raise UserWarning(f"Il n'y a pas de perso avec l'id {id_}")
        #
        d = results[0]
        data_perso = {
            "nom": d[0],
            "genre": d[1],
            "race": d[2],
            "classe": d[3],
            "experience": d[4],
            "inventaire": d[5],
            "lieu": d[6],
            "quetes": d[7],
            "equipement": d[8],
            "vie": d[9],
            "vie_totale": d[10],
            "energie": d[11],
            "energie_totale": d[12],
            "charme": d[13],
            "discretion": d[14],
            "force_": d[15],
            "agilite": d[16],
            "magie": d[17],
            "effets_attaque": d[18],
            "bonus_esquive": d[19],
            "sorts": d[20],
            "resistances": d[21],
            "faiblesses": d[22]
        }
        return data_perso

    def get_data_obj_DB(self, id_):
        """Renvoie l'objet demandé.

        Args:
            id_(int): ID de l'objet à chercher

        Returns:
            Objet/None: Objet d'id `id_` ou None si pas trouvé

        Auteur: Hugo, Nathan

        """
        self.cursor.execute("SELECT nom, description_, type_, effets, contenu, verrouille, ouvert FROM objets WHERE id=%s", (id_,))
        for nom, desc, type_, effets, contenu, verrouille, ouvert in self.cursor:
            # print(id_, nom, desc, type_, effets, contenu, verrouille, ouvert)
            return (nom, desc, type_, effets, contenu, verrouille, ouvert)
        return None

    def get_genres(self):
        self.cursor.execute("SELECT genre FROM genres;")
        results = [elt[0] for elt in self.cursor]
        return results

    def new_genre(self, genre):
        self.cursor.execute("INSERT INTO genres (genre) VALUES (%s)", (genre,))
        self.connection.commit()

    def get_data_Lieu_DB(self, id_):
        query = "SELECT nom, description_, ennemis, pnjs, objets, lieux FROM lieux WHERE id = %s;"
        self.cursor.execute(query, (id_,))
        results = [elt for elt in self.cursor]
        for nom, desc, ennemis, pnjs, obj, lieux in results:
            datas = {}
            datas["nom"] = nom
            datas["description"] = desc
            datas["ennemis"] = ennemis
            datas["pnjs"] = pnjs
            list_obj = json.loads(obj)
            datas["obj"] = list_obj
            list_lieux = json.loads(lieux)
            datas["lieux"] = list_lieux
            return datas
