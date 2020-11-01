
import json
import io
import os


def jload(path_to_file):
    """
    Fonction qui charge ouvre un fichier et qui le charge en json.

    Auteur : Nathan
    """
    f = io.open(path_to_file, "r", encoding="utf-8")
    txt = f.read()
    f.close()
    return json.loads(txt)


# fonction qui teste si un texte est du format json
def is_json(myjson):
    """Fonction qui teste si un string est de format json."""
    try:
        json.loads(myjson)
    except ValueError:
        return False
    return True
