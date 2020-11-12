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

# region FONCTIONS DE TESTS
    def test_version(self, version):
        """Vérifie si la version de la BDD est inférieure à celle du serveur.

        Auteur: Nathan

        """
        self.cursor.execute("SHOW TABLES LIKE 'version_';")
        results = [elt for elt in self.cursor]
        if len(results) == 0:
            return True
        else:
            self.cursor.execute("SELECT version_ FROM version_;")
            results = [elt for elt in self.cursor]
            if len(results) == 0:
                return True
            else:
                version_bdd = results[0][0]
                if version_bdd < version:
                    return True
                else:
                    return False

    def is_first_time(self):
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
# endregion

# region CREATE TABLES :
    def create_table_comptes(self):
        """Crée la table comptes dans la BDD.

        Auteur: Nathan

        """
        query = ("""CREATE TABLE IF NOT EXISTS comptes
                    (id INT PRIMARY KEY AUTO_INCREMENT, pseudo TEXT,
                    email TEXT, password TEXT, perso_id INT);""")
        self.cursor.execute(query)
        self.connection.commit()

    def create_table_persos(self):
        """Crée la table perso dans la BDD.

        Auteur: Nathan

        """
        query = ("""CREATE TABLE IF NOT EXISTS persos
                    (id INT PRIMARY KEY AUTO_INCREMENT,
                    nom TEXT, genre TEXT, race TEXT, classe TEXT,
                    argent int, experience TEXT, inventaire TEXT,
                    lieu INT, quetes TEXT, equipement TEXT,
                    vie INT, vie_totale INT, energie INT, energie_totale INT,
                    charme INT, discretion INT, force_ INT, agilite INT,
                    magie INT, effets_attaque TEXT, bonus_esquive INT,
                    sorts TEXT, resistances TEXT, faiblesses TEXT);""")
        self.cursor.execute(query)
        self.connection.commit()

    def create_table_objets(self):
        """Crée la table objets dans la BDD.

        Auteur: Nathan

        """
        query = ("""CREATE TABLE IF NOT EXISTS objets
                    (id INT PRIMARY KEY, nom TEXT,
                    description_ TEXT, type_ TEXT, effets TEXT,
                    contenu TEXT, verrouille BOOLEAN, ouvert BOOLEAN);""")
        self.cursor.execute(query)
        self.connection.commit()

    def create_table_pnjs(self):
        """Crée la table pnjs dans la BDD.

        Auteur: Nathan

        """
        query = ("""CREATE TABLE IF NOT EXISTS pnjs
                    (id INT PRIMARY KEY, nom TEXT,
                    description_ TEXT, race TEXT, dialogue TEXT);""")
        self.cursor.execute(query)
        self.connection.commit()

    def create_table_ennemis(self):
        """Crée la table ennemis dans la BDD.

        Auteur: Nathan

        """
        query = ("""CREATE TABLE IF NOT EXISTS ennemis
                    (id INT PRIMARY KEY, type_ TEXT, nom TEXT, race TEXT,
                     description_ TEXT, vie_min INT, vie_max INT, attaque TEXT,
                     attaque_effets TEXT, agressivite INT, loot TEXT);""")
        self.cursor.execute(query)
        self.connection.commit()

    def create_table_lieux(self):
        """Crée la table lieux dans la BDD.

        Auteur: Nathan

        """
        query = ("""CREATE TABLE IF NOT EXISTS lieux
                    (id INT PRIMARY KEY, nom TEXT, appellations TEXT,
                    description_ TEXT, ennemis TEXT, pnjs TEXT, objets TEXT,
                    lieux TEXT);""")
        # ennemis, pnjs, objets, lieux contiennent des listes parsées par JSON
        self.cursor.execute(query)
        self.connection.commit()

    def create_table_quete(self):
        """Crée la table `quete` dans la DB.

        Auteur: Hugo

        """
        query = ("""CREATE TABLE IF NOT EXISTS quete
                    (id INT PRIMARY KEY, nom TEXT, description TEXT,
                     id_recompenses TEXT, conditions TEXT);""")
        self.cursor.execute(query)
        self.connection.commit()

    def create_table_genre(self):
        """Crée la table genre dans la BDD.

        Auteur: Nathan

        """
        query = ("""CREATE TABLE IF NOT EXISTS genres
                    (genre TEXT);""")
        self.cursor.execute(query)
        self.connection.commit()
        genre_base = ["homme", "femme", "agenre", "androgyne", "bigender",
                      "non-binaire"]
        for genre in genre_base:
            self.cursor.execute("INSERT INTO genres (genre) VALUES (%s)",
                                (genre, ))
            self.connection.commit()

    def create_table_version(self):
        """Crée la table version dans la BDD.

        Auteur: Nathan

        """
        query = ("""CREATE TABLE IF NOT EXISTS version_
                    (version_ int);""")
        self.cursor.execute(query)
        self.connection.commit()
        self.cursor.execute("INSERT INTO version_ (version_) VALUES (%s)",
                            (0, ))
        self.connection.commit()
# endregion

# region UPDATE
    def update(self, force=False):
        """Réinitialise les tables de mauvais format ou qui n'existent pas.

        Auteur: Nathan

        """
        # Comptes
        if force or self.get_schema("comptes") != {'id': 'int',
                                                   'pseudo': 'text',
                                                   'email': 'text',
                                                   'password': 'text',
                                                   'perso_id': 'int'}:
            self.cursor.execute("DROP TABLE comptes")
            self.connection.commit()
            self.create_table_comptes()
            print("La table comptes a été mise à jour !")
        # Persos
        if force or self.get_schema("persos") != {"id": "int", "nom": "text",
                                                  "genre": "text",
                                                  "race": "text",
                                                  "classe": "text",
                                                  "argent": "int",
                                                  "experience": "text",
                                                  "inventaire": "text",
                                                  "lieu": "int",
                                                  "quetes": "text",
                                                  "equipement": "text",
                                                  "vie": "int",
                                                  "vie_totale": "int",
                                                  "energie": "int",
                                                  "energie_totale": "int",
                                                  "charme": "int",
                                                  "discretion": "int",
                                                  "force_": "int",
                                                  "agilite": "int",
                                                  "magie": "int",
                                                  "effets_attaque": "text",
                                                  "bonus_esquive": "int",
                                                  "sorts": "text",
                                                  "resistances": "text",
                                                  "faiblesses": "text"}:
            self.cursor.execute("DROP TABLE IF EXISTS persos")
            self.connection.commit()
            self.create_table_persos()
            print("La table persos a été mise à jour !")
        # Ennemis
        if force or self.get_schema("ennemis") != {"id": "int",
                                                   "type_": "text",
                                                   "nom": "text",
                                                   "race": "text",
                                                   "description_": "text",
                                                   "vie_min": "int",
                                                   "vie_max": "int",
                                                   "attaque": "text",
                                                   "attaque_effets": "text",
                                                   "agressivite": "int",
                                                   "loot": "text"}:
            self.cursor.execute("DROP TABLE IF EXISTS ennemis")
            self.connection.commit()
            self.create_table_ennemis()
            print("La table ennemis a été mise à jour !")
        # Objets
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
        # Lieux
        if force or self.get_schema("lieux") != {"id": "int", "nom": "text",
                                                 "appellations": "text",
                                                 "description_": "text",
                                                 "ennemis": "text",
                                                 "pnjs": "text",
                                                 "objets": "text",
                                                 "lieux": "text"}:
            self.cursor.execute("DROP TABLE IF EXISTS lieux")
            self.connection.commit()
            self.create_table_lieux()
            print("La table lieux a été mise à jour !")
        # PNJ
        if force or self.get_schema("pnjs") != {"id": "int", "nom": "text",
                                                "description_": "text",
                                                "race": "text",
                                                "dialogue": "text"}:
            self.cursor.execute("DROP TABLE IF EXISTS pnjs")
            self.connection.commit()
            self.create_table_pnjs()
            print("La table pnjs a été mise à jour !")
        # Quete
        if force or self.get_schema("quete") != {"id": "int",
                                                 "nom": "text",
                                                 "description": "text",
                                                 "id_recompenses": "text",
                                                 "conditions": "text"}:
            self.cursor.execute("DROP TABLE IF EXISTS quete")
            self.connection.commit()
            self.create_table_quete()
            print("La table quete a été mise à jour !")
        # Genres
        if force or self.get_schema("genres") != {"genre": "text"}:
            self.cursor.execute("DROP TABLE IF EXISTS genres")
            self.connection.commit()
            self.create_table_genre()
        # version
        if force or self.get_schema("version_") != {"version_": "int"}:
            self.cursor.execute("DROP TABLE IF EXISTS version_")
            self.connection.commit()
            self.create_table_version()

    def init_database(self):
        """Permet de créer toutes les tables au premier lancement.

        Auteur: Nathan, Hugo

        """
        self.create_table_comptes()
        self.create_table_persos()
        self.create_table_objets()
        self.create_table_pnjs()
        self.create_table_ennemis()
        self.create_table_lieux()
        self.create_table_quete()
        self.create_table_genre()
        self.create_table_version()

# endregion

# region INSERT au premier lancement du serveur
    def transfert_json_to_bdd(self, version=None):
        """Transfére toutes les données des fichiers json vers la BDD.

        Etat : TODO Commencé, à finir
        Auteur: Nathan, Hugo

        """
        print("Transfert des donnnées json vers la BDD...")
        # region Ennemis :
        self.cursor.execute("TRUNCATE TABLE `ennemis`")
        self.connection.commit()
        pathd = "Data/ennemis/"
        # ks : key = key of json lieu , value[0] = name of column of db ennemis
        # value[1] = si json.dumps ou pas, value[2] = si list index ou pas

        ks = {"id": ["id", False], "type_": ["type", False],
              "nom": ["nom", False], "race": ["race", False],
              "description_": ["description", False],
              "vie_min": ["vie", False, 0], "vie_max": ["vie", False, 1],
              "attaque": ["attaque", True],
              "attaque_effets": ["attaque_effets", True],
              "agressivite": ["agressivite", False]}
        for fich in os.listdir(pathd):
            if not fich.endswith(".json"):
                continue
            d = jload(pathd + fich)
            values_query = []
            values_query_args = []
            for key in ks.keys():
                if ks[key][0] in d.keys():
                    values_query.append(key)
                    val = d[ks[key][0]]
                    if len(ks[key]) == 3:
                        val = val[ks[key][2]]
                    if ks[key][1]:
                        val = json.dumps(val)
                    values_query_args.append(val)
            txt_values_query = ", ".join(values_query)
            txt_query = ", ".join(["%s" for _ in values_query])
            # on crée la query :
            query = f"""INSERT INTO ennemis ({txt_values_query})
                       VALUES ({txt_query})"""
            self.cursor.execute(query, tuple(values_query_args))
            self.connection.commit()
        # endregion
        # region Objets :
        self.cursor.execute("TRUNCATE TABLE `objets`")
        self.connection.commit()
        pathd = "Data/objets/"
        # ks : key = key of json lieu , value[0] = name of column of db lieux
        # value[1] = si json.dumps ou pas, value[2] = si list index ou pas
        ks = {"id": ["id", False], "nom": ["nom", False],
              "description_": ["description", False],
              "type_": ["type", False], "effets": ["effets", True],
              "contenu": ["contenu", True],
              "verrouille": ["verrouille", False], "ouvert": ["ouvert", False]}
        #
        for fich in os.listdir(pathd):
            if not fich.endswith(".json"):
                continue
            d = jload(pathd + fich)
            d["contenu"] = "" if "contenu" not in d.keys() else d["contenu"]
            ver = "verrouille"
            d[ver] = d[ver] if ver in d.keys() else False
            d["ouvert"] = False if "ouvert" not in d.keys() else d["ouvert"]
            #
            values_query = []
            values_query_args = []
            for key in ks.keys():
                if ks[key][0] in d.keys():
                    values_query.append(key)
                    val = d[ks[key][0]]
                    if len(ks[key]) == 3:
                        val = val[ks[key][2]]
                    if ks[key][1]:
                        val = json.dumps(val)
                    values_query_args.append(val)
            txt_values_query = ", ".join(values_query)
            txt_query = ", ".join(["%s" for _ in values_query])
            # on crée la query :
            query = f"""INSERT INTO objets ({txt_values_query})
                       VALUES ({txt_query})"""
            self.cursor.execute(query, tuple(values_query_args))
            self.connection.commit()
        # endregion
        # region Lieu :
        self.cursor.execute("TRUNCATE TABLE `lieux`")
        self.connection.commit()
        pathd = "Data/map/"
        # ks : key = key of json lieu , value = name of column of db lieux
        ks = {"id": ["id", False], "nom": ["nom", False],
              "appellations": ["appellations", True],
              "description_": ["description", False],
              "ennemis": ["ennemis", True], "pnjs": ["pnjs", True],
              "objets": ["objets", True], "lieux": ["lieux", True]}
        #
        for fich in os.listdir(pathd):
            if not fich.endswith(".json"):
                continue
            d = jload(pathd + fich)
            #
            values_query = []
            values_query_args = []
            for key in ks.keys():
                if ks[key][0] in d.keys():
                    values_query.append(key)
                    val = d[ks[key][0]]
                    if len(ks[key]) == 3:
                        val = val[ks[key][2]]
                    if ks[key][1]:
                        val = json.dumps(val)
                    values_query_args.append(val)
            txt_values_query = ", ".join(values_query)
            txt_query = ", ".join(["%s" for _ in values_query])
            # on crée la query :
            query = f"""INSERT INTO lieux ({txt_values_query})
                       VALUES ({txt_query})"""
            self.cursor.execute(query, tuple(values_query_args))
            self.connection.commit()
        # endregion
        # region PNJs :
        self.cursor.execute("TRUNCATE TABLE pnjs")
        self.connection.commit()
        pathd = "Data/pnjs/"
        # ks : key = key of json lieu , value[0] = name of column of db lieux
        # value[1] = si json.dumps ou pas, value[2] = si list index ou pas
        ks = {"id": ["id", False], "nom": ["nom", False],
              "description_": ["description", False],
              "race": ["race", False], "dialogue": ["dialogues", True]}
        for fich in os.listdir(pathd):
            if not fich.endswith(".json"):
                continue
            d = jload(pathd + fich)
            values_query = []
            values_query_args = []
            for key in ks.keys():
                if ks[key][0] in d.keys():
                    values_query.append(key)
                    val = d[ks[key][0]]
                    if len(ks[key]) == 3:
                        val = val[ks[key][2]]
                    if ks[key][1]:
                        val = json.dumps(val)
                    values_query_args.append(val)
            txt_values_query = ", ".join(values_query)
            txt_query = ", ".join(["%s" for _ in values_query])
            # on crée la query :
            query = f"""INSERT INTO pnjs ({txt_values_query})
                       VALUES ({txt_query})"""
            self.cursor.execute(query, tuple(values_query_args))
            self.connection.commit()
        # endregion
        # region Quêtes :
        self.cursor.execute("TRUNCATE TABLE quete")
        self.connection.commit()
        pathd = "Data/quetes/"
        # ks : key = key of json lieu , value[0] = name of column of db lieux
        # value[1] = si json.dumps ou pas, value[2] = si list index ou pas
        ks = {"id": ["id", False], "nom": ["nom", False],
              "description": ["description", False],
              "id_recompenses": ["id_recompenses", True],
              "conditions": ["conditions", True]}
        for fich in os.listdir(pathd):
            if not fich.endswith(".json"):
                continue
            d = jload(pathd + fich)
            values_query = []
            values_query_args = []
            for key in ks.keys():
                if ks[key][0] in d.keys():
                    values_query.append(key)
                    val = d[ks[key][0]]
                    if len(ks[key]) == 3:
                        val = val[ks[key][2]]
                    if ks[key][1]:
                        val = json.dumps(val)
                    values_query_args.append(val)
            txt_values_query = ", ".join(values_query)
            txt_query = ", ".join(["%s" for _ in values_query])
            # on crée la query :
            query = f"""INSERT INTO quete ({txt_values_query})
                       VALUES ({txt_query})"""
            self.cursor.execute(query, tuple(values_query_args))
            self.connection.commit()
        # endregion

        # region version
        if version is not None:
            query = "UPDATE version_ SET version_=%s"
            self.cursor.execute(query, (version,))
            self.connection.commit()
        # endregion

        # TODO
        pass
# endregion

# region INSCRIPTION / CONNEXION
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
            raise UserWarning("Probleme with comptes, il n'y a pas qu'un elt")
        return True, id_

    def test_compte_inscrit(self, pseudo, email):
        """Teste si on peut inscrire un compte.

        renvoie False s'il n'y a pas d'erreurs
        renvoie un string contenant un message d'erreur s'il y a une erreur

        Auteur: Hugo, Nathan
        """
        self.cursor.execute("SELECT pseudo, email FROM comptes")
        c = self.cursor
        for pseudo_, email_ in c:
            if pseudo == pseudo_:
                return "Le pseudo est déjà utilisé"
            elif email == email_:
                return "L'email est déjà utilisé"
        return False

    def test_connexion(self, pseudo, password):
        """Teste la connexion d'un compte.

        Args:
            pseudo(str): Pseudo à tester
            password(str): Mot de passe à tester.

        Returns:
            bool/str: False --> Pas d'erreur
                      str --> Message d'erreur

        Auteur: Nathan

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

# endregion

# region FONCTIONS DE TYPES SET / NEW
    def set_perso(self, player):
        """Enregistre un perso dans la BDD.

        Args:
            player(Player): Joueur à enregistrer.

        Auteur: Nathan

        """
        id_ = player.id_
        # on va regarder si le player a déjà un perso
        self.cursor.execute("SELECT perso_id FROM comptes WHERE id=%s;", (id_,))
        results = [elt for elt in self.cursor]
        print("Results", str(results))
        perso_id = results[0][0] if len(results) >= 1 else None
        perso = player.perso
        inventaire = [[obj[0].index, obj[1]] for obj in perso.inventaire]
        # on va mettre toutes les quetes, finies ou non dans un dict
        quetes = {}
        for k, v in perso.quetes.items():
            quetes[k] = {"etat": v}
        for qt in perso.quetes_en_attente:
            quetes[qt.index] = {"etat": "en attente", "compteur": qt.compteur}
        if perso.quete_actuelle is not None:
            quetes[perso.quete_actuelle.index] = {"etat": "actuelle", "compteur": perso.quete_actuelle.compteur}
        #
        if perso_id is None:
            # si non on va lui en créer un
            #
            self.cursor.execute("""INSERT INTO persos
                                   (nom, genre, race, classe, argent,
                                    experience, inventaire, lieu, quetes,
                                    equipement, vie, vie_totale, energie,
                                    energie_totale, charme, discretion,
                                    force_, agilite, magie, effets_attaque,
                                    bonus_esquive, sorts, resistances,
                                    faiblesses)
                                   VALUES
                                   (%s, %s, %s, %s, %s,  %s, %s, %s, %s, %s,
                                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                    %s, %s, %s, %s);""",
                                (perso.nom, perso.genre, perso.race,
                                 perso.classe, perso.argent,
                                 json.dumps(perso.experience),
                                 json.dumps([[obj.index, qt] for obj, qt in perso.inventaire]),
                                 perso.lieu, json.dumps(quetes),
                                 json.dumps(perso.equipement), perso.vie,
                                 perso.vie_totale, perso.energie,
                                 perso.energie_totale, perso.charme,
                                 perso.discretion, perso.force, perso.agilite,
                                 perso.magie, json.dumps(perso.effets_attaque),
                                 perso.bonus_esquive, json.dumps(perso.sorts),
                                 json.dumps(perso.resistances),
                                 json.dumps(perso.faiblesses)))
            self.connection.commit()
            self.cursor.execute("SELECT id FROM persos WHERE nom = %s AND race = %s AND classe = %s AND genre = %s ORDER BY id DESC;", (perso.nom, perso.race, perso.classe, perso.genre))
            perso_id = [elt[0] for elt in self.cursor][0]
            self.cursor.execute("""UPDATE comptes SET perso_id = %s
                                   WHERE comptes.id = %s;
                                """, (perso_id, player.id_))
            self.connection.commit()
        else:
            # sinon on va juste modifier les valeurs
            self.cursor.execute("""UPDATE persos
                                   SET nom = %s, genre = %s, race = %s,
                                       classe = %s, argent = %s,
                                       experience = %s, inventaire = %s,
                                       lieu = %s, quetes = %s, equipement = %s,
                                       vie = %s, vie_totale = %s, energie = %s,
                                       energie_totale = %s, charme = %s,
                                       discretion = %s, force_ = %s,
                                       agilite = %s, magie = %s,
                                       effets_attaque = %s, bonus_esquive = %s,
                                       sorts = %s, resistances = %s,
                                       faiblesses = %s
                                   WHERE id=%s;""",
                                (perso.nom, perso.genre,
                                 perso.race, perso.classe, perso.argent,
                                 json.dumps(perso.experience),
                                 json.dumps(inventaire),
                                 perso.lieu, json.dumps(quetes),
                                 json.dumps(perso.equipement), perso.vie,
                                 perso.vie_totale, perso.energie,
                                 perso.energie_totale, perso.charme,
                                 perso.discretion, perso.force,
                                 perso.agilite, perso.magie,
                                 json.dumps(perso.effets_attaque),
                                 perso.bonus_esquive,
                                 json.dumps(perso.sorts),
                                 json.dumps(perso.resistances),
                                 json.dumps(perso.faiblesses), perso_id))
            self.connection.commit()

    def save_map(self, map_):
        """Permet de sauvegarder la carte.

        Args:
            map_(Map): Instance de la carte

        Auteur: Hugo

        """
        for lieu in map_.lieux.values():
            self.save_lieu(lieu)

    def save_lieu(self, lieu):
        """Permet de sauvegarder un lieu.

        Args:
            lieu(Lieu): Lieu à sauvegarder

        Auteur: Hugo, Nathan

        """
        query = """UPDATE lieux
                   SET ennemis = %s,
                       objets = %s,
                       pnjs = %s,
                       lieux = %s
                    WHERE id = %s;
                """
        ens = {}
        for en in lieu.ennemis:
            if en.index in ens.keys():
                ens[en.index] += 1
            else:
                ens[en.index] = 1

        objs = {}
        for ob in lieu.objets:
            if ob.index in objs.keys():
                objs[ob.index] += 1
            else:
                objs[ob.index] = 1
        self.cursor.execute(query,
                            (
                                json.dumps([el[0] if el[1] == 1 else list(el) for el in ens.items()]),
                                json.dumps([el[0] if el[1] == 1 else list(el) for el in objs.items()]),
                                json.dumps([pn.index for pn in lieu.pnjs]),
                                json.dumps(lieu.lieux_accessibles),
                                lieu.index
                            ))

    def new_genre(self, genre):
        self.cursor.execute("INSERT INTO genres (genre) VALUES (%s)", (genre,))
        self.connection.commit()

# endregion

# region GETTERS
    def get_schema(self, table_name):
        """Récupère la structure d'une table.

        Récupère la structure d'une table demandée sous forme de dictionnaire :
        dict<str: T>, T étant le type de la colonne (int, text, ...)

        Returns:
            dict: Table existe --> Renvoie son schéma
                  Table n'existe pas --> Renvoie un dict vide
        """
        self.cursor.execute("select * from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME=%s;", (table_name,))
        results = [elt for elt in self.cursor]
        schema = {}
        for elt in results:
            schema[elt[3]] = elt[7]
        return schema

    def get_perso(self, id_):
        """Récupère les données du personnage.

        Args:
            id_(int): ID du compte

        Auteur: Nathan

        """
        query = """SELECT nom, genre, race, classe, argent,  experience,
                    inventaire, lieu, quetes, equipement,
                    vie, vie_totale, energie, energie_totale,
                    charme, discretion, force_, agilite, magie,
                    effets_attaque, bonus_esquive, sorts,
                    resistances, faiblesses FROM persos INNER JOIN comptes ON
                    comptes.perso_id = persos.id WHERE comptes.id=%s"""
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
            "argent": d[4],
            "experience": json.loads(d[5]),
            "inventaire": json.loads(d[6]),
            "lieu": d[7],
            "quetes": json.loads(d[8]),
            "equipement": json.loads(d[9]),
            "vie": d[10],
            "vie_totale": d[11],
            "energie": d[12],
            "energie_totale": d[13],
            "charme": d[14],
            "discretion": d[15],
            "force_": d[16],
            "agilite": d[17],
            "magie": d[18],
            "effets_attaque": json.loads(d[19]),
            "bonus_esquive": d[20],
            "sorts": json.loads(d[21]),
            "resistances": json.loads(d[22]),
            "faiblesses": json.loads(d[23])
        }
        return data_perso

    def get_genres(self):
        self.cursor.execute("SELECT genre FROM genres;")
        results = [elt[0] for elt in self.cursor]
        return results

    def get_lieux(self):
        """Récupère les ID des lieux

        Auteur: Nathan

        """
        query = "SELECT id FROM lieux;"
        self.cursor.execute(query)
        lieux = [elt[0] for elt in self.cursor]
        return lieux

    def get_data_obj_DB(self, id_):
        """Renvoie l'objet demandé.

        Args:
            id_(int): ID de l'objet à chercher

        Returns:
            Objet/None: Objet d'id `id_` ou None si pas trouvé

        Auteur: Hugo, Nathan

        """
        self.cursor.execute("""SELECT nom, description_, type_, effets,
                                      contenu, verrouille, ouvert
                                FROM objets WHERE id=%s""", (id_,))
        for nom, desc, type_, effets, cont, verrouille, ouvert in self.cursor:
            datas = {"id": id_, "nom": "objet quelconque",
                     "description": "Une objet, je crois",
                     "type": "objet", "effets": {}, "contenu": [],
                     "verrouille": False, "ouvert": False}
            datas["nom"] = nom
            datas["description"] = desc
            datas["type"] = type_
            if effets is not None:
                datas["effets"] = json.loads(effets)
            datas["contenu"] = cont
            datas["verrouille"] = verrouille
            datas["ouvert"] = ouvert
            return datas
        return None

    def get_data_Lieu_DB(self, id_):
        """Renvoie les caractéristiques d'un lieu :

        Args:
            id_(int): Identifiant du Lieu

        Auteur: Nathan

        """
        query = "SELECT nom, appellations, description_, ennemis, pnjs, objets, lieux, appellations FROM lieux WHERE id = %s;"
        self.cursor.execute(query, (id_,))
        results = [elt for elt in self.cursor]
        for nom, appellations, desc, ennemis, pnjs, obj, lieux, appellations in results:
            datas = {"id": id_, "nom": "Lieu", "appellations": [],
                     "description": "Un lieu dans lequel vous êtes.",
                     "ennemis": [], "pnjs": [], "obj": [], "lieux": []}
            datas["nom"] = nom
            datas["appellations"] = json.loads(appellations)
            datas["description"] = desc
            datas["ennemis"] = json.loads(ennemis)
            datas["pnjs"] = json.loads(pnjs)
            datas["obj"] = json.loads(obj)
            datas["lieux"] = json.loads(lieux)
            return datas
        return None

    def get_data_Pnj_DB(self, id_):
        """Renvoie les caractéristiques d'un ennemi

        Args:
            id_(int): Identifiant du PNJ

        Auteur: Nathan

        """
        query = """SELECT nom, description_, race, dialogue FROM pnjs
                   WHERE id=%s;"""
        self.cursor.execute(query, (id_,))
        for nom, desc, race, dialogues in self.cursor:
            datas = {"nom": "Un pnj",
                     "description": "Un pnj. Waaa, quelle information pertinente !",
                     "race": "humain", "dialogues": None}
            datas["id"] = id_
            datas["nom"] = nom
            datas["desc"] = desc
            datas["race"] = race
            if dialogues is not None:
                datas["dialogues"] = json.loads(dialogues)
            return datas
        return None

    def get_data_Ennemi_DB(self, id_):
        """Renvoie les caractéristiques d'un ennemi

        Args:
            id_(int): L'identifiant de l'ennemi

        Auteur: Nathan, Hugo

        """
        query = """SELECT type_, nom, race, description_, vie_min, vie_max,
                          attaque, attaque_effets, agressivite, loot
                    FROM ennemis
                    WHERE id=%s"""
        self.cursor.execute(query, (id_,))
        results = [elt for elt in self.cursor]
        datas = {
            "id": 0,
            "type": "ennemi",
            "nom": "Ennemi Méchant",
            "description": "Ennemi qui va t'attaquer parce qu'il est méchant et que les méchants ils attaquent les gentils...",
            "vie": [0, 1],
            "attaque": {
                "corps à corps": None,
                "magique": None,
                "distance": None
            },
            "attaque_effets": {},
            "agressivite": 0
        }
        for type_, nom, race, description_, vie_min, vie_max, attaque, attaque_effets, agressivite, loot in results:
            datas["id"] = id_
            datas["type"] = type_
            datas["nom"] = nom
            datas["description"] = description_
            datas["vie"] = [vie_min, vie_max]
            datas["agressivite"] = agressivite
            if attaque is not None:
                datas["attaque"] = json.loads(attaque)
            if attaque_effets is not None:
                datas["attaque_effets"] = json.loads(attaque_effets)
            if loot is not None:
                datas["loot"] = json.loads(loot)
            return datas
        return None

    def get_data_quetes_DB(self, id_):
        """Renvoie les caractéristiques d'un ennemi

        Args:
            id_(int): L'identifiant de la quête

        Auteur: Hugo

        """
        # CREATE TABLE IF NOT EXISTS quete (id INT PRIMARY KEY, nom TEXT, description TEXT, recompenses TEXT, conditions TEXT)
        query = """SELECT nom, description, id_recompenses, conditions
                   FROM quete
                   WHERE id=%s"""
        self.cursor.execute(query, (id_,))
        datas = {
            "nom": "Quete",
            "description": "Une quete",
            "id_recompenses": [],
            "conditions": []
        }
        for nom, desc, recompense, cond in self.cursor:
            datas["nom"] = nom
            datas["description"] = desc
            datas["id_recompenses"] = json.loads(recompense)
            datas["conditions"] = json.loads(cond)
            return datas
        raise UserWarning(f"Aucune quete n'a été trouvée avec l'id {id_}")
# endregion

    def perso_death(self, id_):
        """Fonction qui supprime un perso mort

        Auteur: Hugo, Nathan
        """
        # on récupere l'id du perso
        query = """SELECT persos.id FROM persos
                   INNER JOIN comptes
                   ON comptes.perso_id = persos.id WHERE comptes.id=%s;"""
        self.cursor.execute(query, (id_,))
        id_perso = None
        results = [elt for elt in self.cursor]
        if len(results) >= 1:
            id_perso = results[0][0]
        # on supprime le perso
        query = """DELETE FROM persos WHERE id=%s;"""
        self.cursor.execute(query, (id_perso,))
        self.connection.commit()
        # on enleve l'id du perso dans le compte
        query = """UPDATE comptes
                   SET perso_id = null
                   WHERE id = %s;"""
        self.cursor.execute(query, (id_,))
        self.connection.commit()

