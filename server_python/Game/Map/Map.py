import io,json,os

class Map:
    """Classe qui gérera la map du jeu"""
    def __init__(self):
        # TODO
        pass

    def load_from_json(self):
        """

        """
        emplacement="Data/map/"
        for fichier in os.listdir(emplacement):
            f=io.open(emplacement+fichier,"r",encoding="utf-8")
            data=json.loads(f.read())
            print(data)
            f.close()

    def create_lieu(self,datalieu):
        #TODO
        pass

if __name__=="__main__":
    map=Map()
    map.load_from_json()
