
import json
import io
import os

replacements = {"é": "e", "è": "e", "ê": "e",
                "ë": "e", "â": "a", "ä": "a",
                "à": "a", "á": "a", "ç": "c",
                "ù": "u", "ú": "u", "û": "u",
                "ü": "u", "î": "i", "ï": "i",
                "í": "i", "ö": "o", "ô": "o",
                "ó": "o", "ñ": "n", " ": "",
                "\t": "", "\r": "", "\n": "",
                "!": "", ",": "", "?": "",
                ";": "", ".": "", ": ": "",
                "/": "", "§": "", "%": "",
                "*": "", "-": "", "_": "",
                "'": "", '"': "", "(": "", ")": "",
                "&": "", "#": "", "{": "", "[": "", "|": "",
                "`": "", "\\": "", "^": "", "@": "", "]": "",
                "}": "", "=": "", "+": "", "°": "", "€": "",
                "£": "", "µ": "", "’": ""}


def jload(path_to_file):
    """Charge ouvre un fichier et qui le charge en json.

    Auteur: Nathan

    """
    f = io.open(path_to_file, "r", encoding="utf-8")
    txt = f.read()
    f.close()
    if len(txt) == 0:
        return {}
    return json.loads(txt)


def is_json(myjson):
    """Teste si un string est de format json."""
    try:
        json.loads(myjson)
    except ValueError:
        return False
    return True


def traiter_txt(txt):
    """Traite un texte afin de pouvoir le comparer avec un input utilisateur.

    Auteur: Nathan

    """
    txt = txt.lower()
    for k in replacements.keys():
        txt = txt.replace(k, replacements[k])
    return txt


def are_texts_equals(text_1, text_2):
    """Compare d

    Auteur: Hugo

    """
    return traiter_txt(text_1) == traiter_txt(text_2)


def is_one_of(text, liste):
    """Teste si l'élément text traité est dans la liste des éléments traités

    Auteur: Nathan

    """
    t = traiter_txt(text)
    for elt in liste:
        if t == traiter_txt(elt):
            return True
    return False
