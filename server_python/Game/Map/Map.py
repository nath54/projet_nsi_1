import io,json,os
from Lieux.Lieu import Lieu

class Map:
    """Classe qui gérera la map du jeu"""
    def __init__(self):
        self.lieus=[]
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
        lieu=Lieu()
        dk=datalieu.keys()
        if "nom" in dk: lieu.nom=datalieu["nom"]
        if "description" in dk: lieu.description=datalieu["description"]
        
        #
        self.lieus.append(lieu)

if __name__=="__main__":
    map=Map()
    map.load_from_json()
