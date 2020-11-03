
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

    Auteur : Nathan

    """
    f = io.open(path_to_file, "r", encoding="utf-8")
    txt = f.read()
    f.close()
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

    Auteur : Nathan

    """
    txt = txt.lower()
    for k in replacements.keys():
        txt = txt.replace(k, replacement[k])
    return txt


def is_texts_equal(text_1, text_2):
    """Compare d

    Auteur : Hugo

    """
    return traiter_txt(text_1) == traiter_txt(text_2)
