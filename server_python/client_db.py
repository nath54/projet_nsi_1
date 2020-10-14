#CECI EST LE CLIENT QUI SE CONNECTE A MARIADB

#Imports : 
import mariadb

#Classe du client mariadb
class Client_mariadb:
    def __init__(self):
        self.user="user"
        self.password="password"
        self.host="localhost"
        self.port=3307
        self.database="database"
        try:
            self.connection = mariadb.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database

            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        #
        self.tablename="tablename"
        self.cursor = self.connection.cursor()
        #TODO
        pass

    def close(self):
        self.connection.close()


