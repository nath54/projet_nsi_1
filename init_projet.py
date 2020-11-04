"""CECI EST UN PETIT SCRIPT D'INITIALISATION."""

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

import pip
import sys

def install(package):
    """Fonction qui va installer une librairie python avec pip

    Author: Internet
    """
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])

def demande_install(package):
    """Fonction qui va demander pour installer une librairie python avec pip

    Author: Nathan
    """
    return input(f"Le package {package} n'est pas installé, voulez vous l'installer ?\n : ").lower() in ["y","yes","ui","oui","o"]

def main():
    """Fonction qui va initialiser la bdd pour le projet.
    
    Author : Nathan
    """
    user = input("pseudo mariadb root : ")
    password = input("password root : ")
    host = "localhost"
    p = input("port : ")
    port = 3307 if p == "" else p
    database = "projet_nsi_1"
    try:
        connection = mariadb.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database)
        print("connecté a la database")
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    cursor = connection.cursor()
    # TODO : A finir, a completer
    cursor.execute('CREATE USER IF NOT EXISTS pyuser@localhost IDENTIFIED BY "pypassword";')
    connection.commit()
    cursor.execute('CREATE DATABASE IF NOT EXISTS projet_nsi_1;')
    connection.commit()
    cursor.execute('USE projet_nsi_1;')
    connection.commit()
    cursor.execute('GRANT ALL PRIVILEGES ON * TO pyuser@localhost;')
    connection.commit()
    # install python modules
    libs = ["sockets", "websockets"]
    for l in libs: 
        if not l in sys.modules and demande_install(l):
            install(l)

if __name__ == "__main__":
    main()
